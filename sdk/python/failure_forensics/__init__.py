"""Small, dependency-free Failure Forensics SDK prototype."""

from __future__ import annotations

import os
import time
import uuid
from collections.abc import Callable, Generator, Iterable
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from datetime import UTC, datetime
from functools import wraps
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
TracePayload = dict[str, Any]
Exporter = Callable[[TracePayload], None]


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


class InMemoryExporter:
    """Stub exporter used by examples and tests without a live API."""

    def __init__(self) -> None:
        self.traces: list[TracePayload] = []

    def __call__(self, trace: TracePayload) -> None:
        self.traces.append(deepcopy(trace))


class SpanContext:
    """Handle yielded by ``Forensics.span`` for outputs and data-flow links."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def trace_id(self) -> str:
        return str(self._data["trace_id"])

    @property
    def span_id(self) -> str:
        return str(self._data["span_id"])

    def set_output(self, output: Any) -> None:
        self._data["output"] = output


class Forensics:
    """Record traces, nested spans, and explicit ``inputs_from`` links."""

    def __init__(
        self,
        project: str,
        api_key: str | None = None,
        exporter: Exporter | None = None,
    ) -> None:
        self.project = project
        self.api_key = api_key or os.environ.get("FF_API_KEY")
        self.exporter = exporter or InMemoryExporter()
        unique = uuid.uuid4().hex
        self._current_trace: ContextVar[TracePayload | None] = ContextVar(
            f"ff_trace_{unique}", default=None
        )
        self._current_span: ContextVar[SpanContext | None] = ContextVar(
            f"ff_span_{unique}", default=None
        )

    def trace(
        self, name: str, *, pipeline_version: str | None = None
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorate one end-to-end operation and export its completed trace."""

        def decorator(function: Callable[P, R]) -> Callable[P, R]:
            @wraps(function)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                if self._current_trace.get() is not None:
                    raise RuntimeError("nested @trace calls are not supported")

                trace: TracePayload = {
                    "trace_id": uuid.uuid4().hex,
                    "project": self.project,
                    "name": name,
                    "pipeline_version": pipeline_version,
                    "started_at": _timestamp(),
                    "status": "ok",
                    "spans": [],
                    "links": [],
                }
                started = time.perf_counter()
                trace_token = self._current_trace.set(trace)
                span_token = self._current_span.set(None)
                try:
                    return function(*args, **kwargs)
                except Exception as error:
                    trace["status"] = "error"
                    trace["error"] = {
                        "type": type(error).__name__,
                        "message": str(error),
                    }
                    raise
                finally:
                    trace["ended_at"] = _timestamp()
                    trace["latency_ms"] = (time.perf_counter() - started) * 1000
                    self._current_span.reset(span_token)
                    self._current_trace.reset(trace_token)
                    self.exporter(trace)

            return wrapper

        return decorator

    @contextmanager
    def span(
        self,
        name: str,
        *,
        type: str = "custom",
        component: str | None = None,
        input: Any = None,
        inputs_from: Iterable[SpanContext] | None = None,
    ) -> Generator[SpanContext, None, None]:
        """Record one step and links from spans whose outputs it consumes."""
        trace = self._current_trace.get()
        if trace is None:
            raise RuntimeError("span() must be used inside an @trace function")

        parent = self._current_span.get()
        span_data: dict[str, Any] = {
            "trace_id": trace["trace_id"],
            "span_id": uuid.uuid4().hex[:16],
            "parent_span_id": parent.span_id if parent else None,
            "name": name,
            "type": type,
            "component_key": component,
            "input": input,
            "started_at": _timestamp(),
            "status": "ok",
        }
        active_span = SpanContext(span_data)
        for source in inputs_from or ():
            if not isinstance(source, SpanContext):
                raise TypeError("inputs_from entries must be SpanContext objects")
            if source.trace_id != active_span.trace_id:
                raise ValueError("inputs_from spans must belong to the current trace")
            trace["links"].append(
                {
                    "from_span_id": source.span_id,
                    "to_span_id": active_span.span_id,
                    "relation": "consumes_output_of",
                }
            )

        started = time.perf_counter()
        token = self._current_span.set(active_span)
        try:
            yield active_span
        except Exception as error:
            span_data["status"] = "error"
            span_data["error"] = {
                "type": error.__class__.__name__,
                "message": str(error),
            }
            raise
        finally:
            span_data["ended_at"] = _timestamp()
            span_data["latency_ms"] = (time.perf_counter() - started) * 1000
            trace["spans"].append(span_data)
            self._current_span.reset(token)


__all__ = ["Forensics", "InMemoryExporter", "SpanContext"]
