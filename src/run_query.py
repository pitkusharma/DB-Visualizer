from common import State, manage_state

@manage_state
def execute_query(state: State, db):
    """Execute SQL query."""
    try:
        query_result = db._execute(state["generated_query"])
        result = {'status': True, 'query_result': query_result}
    except Exception as e:
        result = {'status': False, 'reason': str(e)}
    return result
