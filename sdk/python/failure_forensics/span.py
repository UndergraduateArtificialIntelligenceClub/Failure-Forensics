import time
import uuid
from typing import Any, Dict, List, Optional
from failure_forensics.context import get_current_parent_id, pop_span_id, push_span_id


class SpanLink:
    def __init__(
        self,
        target_span_id: str,
        relation: str = "consumes_output_of",
    ):
        self.target_span_id = target_span_id
        self.relation = relation


class SpanContextManager:
    def __init__(
        self,
        name: str,
        span_type: str = "custom",
        inputs_from: Optional[List[Any]] = None,
        trace_id: Optional[str] = None,
        client: Optional[Any] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        self.span_id = str(uuid.uuid4())
        self.trace_id = trace_id
        self.parent_span_id = get_current_parent_id()
        self.name = name
        self.type = span_type
        self.client = client

        self.started_at: Optional[float] = None
        self.ended_at: Optional[float] = None
        self.status = "ok"
        self.otel_status = "OK"
        self.error_type: Optional[str] = None
        self.error_message: Optional[str] = None
        self.outputs: Optional[Dict[str, Any]] = None
        self.attributes: Dict[str, Any] = dict(attributes) if attributes else {}
        self.links: List[SpanLink] = []

        if inputs_from:
            for item in inputs_from:
                target_id = getattr(item, "span_id", str(item))
                self.links.append(
                    SpanLink(target_span_id=target_id, relation="consumes_output_of")
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
        if system is not None:
            self.attributes["gen_ai.system"] = system
        if model is not None:
            self.attributes["gen_ai.request.model"] = model
        if input_tokens is not None:
            self.attributes["gen_ai.usage.input_tokens"] = input_tokens
        if output_tokens is not None:
            self.attributes["gen_ai.usage.output_tokens"] = output_tokens
        if cost_usd is not None:
            self.attributes["ff.cost.usd"] = cost_usd
        if prompt_version is not None:
            self.attributes["ff.prompt.version"] = prompt_version
        if component_version is not None:
            self.attributes["ff.component.version"] = component_version
        if input_ref is not None:
            self.attributes["ff.payload.input_ref"] = input_ref
        if output_ref is not None:
            self.attributes["ff.payload.output_ref"] = output_ref

    def set_output(self, output: Dict[str, Any]) -> None:
        self.outputs = output

    def __enter__(self) -> "SpanContextManager":
        self.started_at = time.time()
        push_span_id(self.span_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.ended_at = time.time()

        if exc_type is not None:
            self.status = "error"
            self.otel_status = "ERROR"
            self.error_type = exc_type.__name__
            self.error_message = str(exc_val)
            self.attributes["exception.type"] = self.error_type
            self.attributes["exception.message"] = self.error_message

        pop_span_id()

        if self.client is not None:
            self.client._record_span(self)

        return False
