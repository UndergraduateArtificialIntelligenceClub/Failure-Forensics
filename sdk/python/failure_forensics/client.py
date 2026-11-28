"""SDK client for starting spans, decorating traced functions, and recording spans into the buffer."""


import functools
from typing import Any, Callable, Optional
import uuid

from failure_forensics.context import get_current_parent_id
from failure_forensics.models import Span, SpanType
from failure_forensics.span import SpanContextManager


class Forensics:
    """High-level client that manages defaults, creates spans, and buffers validated Span models."""

    def __init__(
        self,
        project: str,
        api_key: str,
        endpoint: Optional[str] = None,
        default_attributes: Optional[dict[str, Any]] = None,
    ) -> None:
        self.project = project
        self.api_key = api_key
        self.endpoint = endpoint
        self.default_attributes: dict[str, Any] = (
            dict(default_attributes) if default_attributes else {}
        )
        self.buffer: list[Span] = []
        self._active_trace_id: Optional[str] = None
        self._trace_depth: int = 0

    def span(
        self,
        name: str,
        span_type: SpanType | str = SpanType.CUSTOM,
        *,
        trace_id: Optional[str] = None,
        inputs_from: Optional[list[Any]] = None,
        component_key: Optional[str] = None,
        attributes: Optional[dict[str, Any]] = None,
        model_provider: Optional[str] = None,
        model_name: Optional[str] = None,
        prompt_version: Optional[str] = None,
        component_version: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        estimated_cost_usd: Optional[float] = None,
        input_ref: Optional[str] = None,
        output_ref: Optional[str] = None,
        prompt_ref: Optional[str] = None,
        raw_response_ref: Optional[str] = None,
    ) -> SpanContextManager:
        merged_attributes = dict(self.default_attributes)
        if attributes:
            merged_attributes.update(attributes)

        resolved_trace_id = trace_id or self._active_trace_id

        cm = SpanContextManager(
            name=name,
            span_type=span_type,
            inputs_from=inputs_from,
            trace_id=resolved_trace_id,
            client=self,
            component_key=component_key,
            attributes=merged_attributes,
            prompt_ref=prompt_ref,
            raw_response_ref=raw_response_ref,
        )
        cm.set_genai_metadata(
            system=model_provider,
            model=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=estimated_cost_usd,
            prompt_version=prompt_version,
            component_version=component_version,
            input_ref=input_ref,
            output_ref=output_ref,
        )
        return cm

    def trace(
        self,
        name: Optional[str] = None,
        span_type: SpanType | str = SpanType.AGENT,
        *,
        component_key: Optional[str] = None,
        attributes: Optional[dict[str, Any]] = None,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                span_name = name or func.__name__
                started_new_trace = (
                    self._trace_depth == 0
                    and self._active_trace_id is None
                    and get_current_parent_id() is None
                )
                if started_new_trace:
                    trace_id = uuid.uuid4().hex
                    self._active_trace_id = trace_id
                else:
                    trace_id = self._active_trace_id

                self._trace_depth += 1
                try:
                    with self.span(
                        span_name,
                        span_type=span_type,
                        trace_id=trace_id,
                        component_key=component_key,
                        attributes=attributes,
                    ):
                        return func(*args, **kwargs)
                finally:
                    self._trace_depth -= 1
                    if started_new_trace:
                        self._active_trace_id = None

            return wrapper

        return decorator

    def _record_span(self, span_cm: SpanContextManager) -> None:
        self.buffer.append(span_cm.to_model())
