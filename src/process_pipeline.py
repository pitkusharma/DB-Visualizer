from common import State
from generate_query import write_query
from run_query import execute_query
from process_result import generate_answer
from construct_df import construct_dataframe


def pipeline(state: State, llm, db) -> State:
    """Execute pipeline from generating query to retrieving desired answer."""

    # 1 Generate the SQL query
    state = write_query(state, llm, db)

    # 2 Execute the query and retrive the data from db
    state = execute_query(state, db)

    # 3 Construct the dataframe from data
    state = construct_dataframe(state)

    # 4 Generate the final answer
    state = generate_answer(state, llm)

    return state
