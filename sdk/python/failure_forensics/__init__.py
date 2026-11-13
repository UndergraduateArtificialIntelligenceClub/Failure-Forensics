import os
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional

class Forensics:
    def __init__(self, project: str, api_key: Optional[str] = None, exporter: Optional[Callable] = None):
        self.project = project
        self.api_key = api_key or os.environ.get("FF_API_KEY", "test-key")
        self.exporter = exporter or (lambda trace_data: print("\n[STUB EXPORTER] Exported Trace Data:\n", trace_data))

    def trace(self, name: str):
        """Decorator to trace an end-to-end execution function."""
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                trace_id = f"tr-{int(time.time()*1000)}"
                spans = []
                self._current_trace = {
                    "trace_id": trace_id, 
                    "project": self.project, 
                    "name": name,
                    "spans": spans
                }
                
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    status = "healthy"
                except Exception as e:
                    status = "failed"
                    raise e
                finally:
                    duration = (time.time() - start_time) * 1000
                    self._current_trace["duration_ms"] = duration
                    self._current_trace["status"] = status
                    self.exporter(self._current_trace)
                
                return result
            return wrapper
        return decorator

    @contextmanager
    def span(
        self, 
        name: str, 
        type: str = "custom", 
        input: Optional[Dict[str, Any]] = None, 
        inputs_from: Optional[list] = None
    ):
        """Context manager for tracking individual steps with inputs_from lineage links."""
        span_data = {
            "name": name,
            "type": type,
            "input": input,
            "inputs_from": inputs_from or [],
            "started_at": time.time(),
            "status": "success"
        }
        
        class SpanContext:
            def __init__(self, data):
                self.data = data
            def set_output(self, output: dict):
                self.data["output"] = output

        active_span = SpanContext(span_data)
        
        try:
            yield active_span
        except Exception as e:
            span_data["status"] = "error"
            span_data["error_message"] = str(e)
            raise e
        finally:
            span_data["ended_at"] = time.time()
            span_data["latency_ms"] = (span_data["ended_at"] - span_data["started_at"]) * 1000
            
            if hasattr(self, "_current_trace"):
                self._current_trace["spans"].append(span_data)
