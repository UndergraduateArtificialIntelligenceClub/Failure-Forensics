""" stack manager to keep track of what step is running right now """

from contextvars import ContextVar
from typing import List, Optional

# Context variable holding the list of active span IDs for the current context
_active_span_stack: ContextVar[List[str]] = ContextVar("_active_span_stack", default=[])

def push_span_id(span_id: str) -> None:
    """Push a new active span ID onto the stack."""
    stack = list(_active_span_stack.get())
    stack.append(span_id)
    _active_span_stack.set(stack)

def pop_span_id() -> None:
    """Pop the current span ID off the stack."""
    stack = list(_active_span_stack.get())
    if stack:
        stack.pop()
        _active_span_stack.set(stack)

def get_current_parent_id() -> Optional[str]:
    """Get the active parent span ID (the top of the stack), if any."""
    stack = _active_span_stack.get()
    return stack[-1] if stack else None
