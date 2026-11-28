"""Step recorder to assign ID's, record timing and errors and build Span models."""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional
import uuid

from failure_forensics.context import get_current_parent_id, pop_span_id, push_span_id
from failure_forensics.models import (
    ErrorDetails,
    Span,
    SpanLink,
    SpanLinkRelation,
    SpanStatus,
    SpanType,
)


def _new_span_id() -> str:
    return uuid.uuid4().hex[:16]


def _new_trace_id() -> str:
    return uuid.uuid4().hex


def _extract_span_id(item: Any) -> Optional[str]:
    if isinstance(item, str):
        return item
    return getattr(item, "span_id", None)


class SpanContextManager:
    """Context manager recording a single operation within a trace."""

    def __init__(
        self,
        name: str,
        span_type: SpanType | str = SpanType.CUSTOM,
        inputs_from: Optional[List[Any]] = None,
        trace_id: Optional[str] = None,
        client: Optional[Any] = None,
        attributes: Optional[Dict[str, Any]] = None,
        component_key: Optional[str] = None,
        input_data: Any = None,
        input_ref: Optional[str] = None,
        output_ref: Optional[str] = None,
        prompt_ref: Optional[str] = None,
        raw_response_ref: Optional[str] = None,
        model_provider: Optional[str] = None,
        model_name: Optional[str] = None,
        prompt_version: Optional[str] = None,
        component_version: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        estimated_cost_usd: Optional[float] = None,
    ) -> None:
        self.span_id: str = _new_span_id()
        self.trace_id: str = trace_id if trace_id is not None else _new_trace_id()
        self.parent_span_id: Optional[str] = get_current_parent_id()
        self.name: str = name
        self.type: SpanType = SpanType(span_type)
        self.component_key: Optional[str] = component_key
        self.client: Optional[Any] = client

        self._start_mono: Optional[float] = None
        self._end_mono: Optional[float] = None
        self.started_at: Optional[datetime] = None
        self.ended_at: Optional[datetime] = None
        self.latency_ms: float = 0.0

        self.status: SpanStatus = SpanStatus.OK
        self.error: Optional[ErrorDetails] = None

        self.input: Any = input_data
        self.output: Any = None
        self.input_ref: Optional[str] = input_ref
        self.output_ref: Optional[str] = output_ref
        self.prompt_ref: Optional[str] = prompt_ref
        self.raw_response_ref: Optional[str] = raw_response_ref

        self.model_provider: Optional[str] = model_provider
        self.model_name: Optional[str] = model_name
        self.prompt_version: Optional[str] = prompt_version
        self.component_version: Optional[str] = component_version
        self.input_tokens: Optional[int] = input_tokens
        self.output_tokens: Optional[int] = output_tokens
        self.estimated_cost_usd: Optional[float] = estimated_cost_usd

        self.attributes: Dict[str, Any] = dict(attributes) if attributes else {}
        self.links: List[SpanLink] = []

        if inputs_from:
            for item in inputs_from:
                source_id = _extract_span_id(item)
                if source_id and source_id != self.span_id:
                    self.links.append(
                        SpanLink(
                            from_span_id=source_id,
                            to_span_id=self.span_id,
                            relation=SpanLinkRelation.CONSUMES_OUTPUT_OF,
                        )
                    )

    def set_genai_metadata(
        self,
        *,
        system: Optional[str] = None,
        model: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        cost_usd: Optional[float] = None,
        prompt_version: Optional[str] = None,
        component_version: Optional[str] = None,
        input_ref: Optional[str] = None,
        output_ref: Optional[str] = None,
    ) -> None:
        """Record GenAI and Failure Forensics metadata on both fields and attributes."""
        if system is not None:
            self.model_provider = system
            self.attributes["gen_ai.system"] = system
        if model is not None:
            self.model_name = model
            self.attributes["gen_ai.request.model"] = model
        if input_tokens is not None:
            self.input_tokens = input_tokens
            self.attributes["gen_ai.usage.input_tokens"] = input_tokens
        if output_tokens is not None:
            self.output_tokens = output_tokens
            self.attributes["gen_ai.usage.output_tokens"] = output_tokens
        if cost_usd is not None:
            self.estimated_cost_usd = cost_usd
            self.attributes["ff.cost.usd"] = cost_usd
        if prompt_version is not None:
            self.prompt_version = prompt_version
            self.attributes["ff.prompt.version"] = prompt_version
        if component_version is not None:
            self.component_version = component_version
            self.attributes["ff.component.version"] = component_version
        if input_ref is not None:
            self.input_ref = input_ref
            self.attributes["ff.payload.input_ref"] = input_ref
        if output_ref is not None:
            self.output_ref = output_ref
            self.attributes["ff.payload.output_ref"] = output_ref

    def set_output(self, output: Any) -> None:
        """Record the output produced by this span."""
        self.output = output

    def to_model(self) -> Span:
        """Convert recorded span state into a validated models.Span instance."""
        start_dt = self.started_at or datetime.now(timezone.utc)
        end_dt = self.ended_at or start_dt
        if end_dt < start_dt:
            end_dt = start_dt

        return Span(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            name=self.name,
            type=self.type,
            component_key=self.component_key,
            started_at=start_dt,
            ended_at=end_dt,
            latency_ms=max(0.0, self.latency_ms),
            status=self.status,
            input=self.input,
            output=self.output,
            input_ref=self.input_ref,
            output_ref=self.output_ref,
            prompt_ref=self.prompt_ref,
            raw_response_ref=self.raw_response_ref,
            model_provider=self.model_provider,
            model_name=self.model_name,
            prompt_version=self.prompt_version,
            component_version=self.component_version,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            estimated_cost_usd=self.estimated_cost_usd,
            error=self.error,
            attributes=self.attributes,
        )

    def __enter__(self) -> "SpanContextManager":
        self.started_at = datetime.now(timezone.utc)
        self._start_mono = time.perf_counter()
        push_span_id(self.span_id)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        self._end_mono = time.perf_counter()
        self.ended_at = datetime.now(timezone.utc)
        if self._start_mono is not None:
            self.latency_ms = max(0.0, (self._end_mono - self._start_mono) * 1000.0)

        if exc_type is not None:
            self.status = SpanStatus.ERROR
            error_type = exc_type.__name__
            error_message = str(exc_val) if exc_val is not None else error_type
            self.error = ErrorDetails(type=error_type, message=error_message)
            self.attributes["exception.type"] = error_type
            self.attributes["exception.message"] = error_message

        pop_span_id()

        if self.client is not None:
            self.client._record_span(self)

        return False
