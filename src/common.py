from typing_extensions import TypedDict
import pandas as pd
from functools import wraps
from typing import Callable


class State(TypedDict, total=False):
    status: bool
    user_request: str
    generated_query: str
    query_result: str
    answer: str
    query_result_df: pd.DataFrame
    graph_required: bool
    graph_code: str
    reason: str
    table_required: bool
    answer: str


def manage_state(func: Callable) -> Callable:
    """Handels state object updation, error handelling."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Fetch 'state' from either args[0] or kwargs['state']
        state = kwargs.get("state") or (args[0] if len(args) > 0 else None)

        # If state status is False we are not executing the function and just returning the existing state
        if state is None or not state.get("status", False):
            return state

        result = func(*args, **kwargs)

        # Updating the state
        for key, val in result.items():
            state[key] = result[key]

        return state

    return wrapper
