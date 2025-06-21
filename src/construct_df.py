from common import State, manage_state
import pandas as pd
from typing import Dict


@manage_state
def construct_dataframe(state: State) -> Dict:
    """
    Constructs a pandas DataFrame from the query result.
    """
    data = state.get("query_result")
    if not isinstance(data, (list, tuple)) or not data:
        raise ValueError("Error processing request. reason: internal server error.")

    df = pd.DataFrame(data)
    return {'query_result_df': df}
