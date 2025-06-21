from common import State, manage_state
from typing_extensions import Annotated, TypedDict


class AnswerOutput(TypedDict):
    status: Annotated[bool, "True if request processing was successful, otherwise False"]
    answer: Annotated[str, "Concise natural language summary; leave empty if not applicable"]
    graph_required: Annotated[bool, "True if graphical output is suitable"]
    graph_code: Annotated[str, "Matplotlib code using `query_result_df`; leave empty if not applicable"]
    table_required: Annotated[bool, "True if table output is suitable"]
    reason: Annotated[str, "Explain failure if status is false; otherwise leave empty"]

@manage_state
def generate_answer(state: State, llm) -> AnswerOutput:
    """
    Analyze user request, SQL query, and result sample to generate structured answer output.
    Uses the DataFrame variable name 'query_result_df' in prompt and expected output.
    """
    query_result_df = state['query_result_df']
    sample_rows = query_result_df.head(3).to_dict(orient="records")
    column_names = list(query_result_df.columns)

    prompt = (
        "You are a data analysis assistant. Analyze the following inputs:\n"
        "- A user question\n"
        "- A corresponding SQL query\n"
        "- A sample of the SQL query result (assume full data is in a pandas DataFrame named `query_result_df`)\n\n"
        "You must return a JSON object with the following structure:\n"
        "{\n"
        '  "status": true | false,\n'
        '  "answer": "concise natural language summary (only if status is true othersie leave it blank)",\n'
        '  "graph_required": true | false,\n'
        '  "graph_code": "matplotlib code using the query_result_df variable (only if graph_required is true othersie leave it blank)",\n'
        '  "table_required": true | false,\n'
        '  "reason": "explanation for failure (only if status is false othersie leave it blank)"\n'
        "}\n\n"
        "Rules:\n"
        "- Use the existing variable `query_result_df` in all graphing code.\n"
        "- Never include actual table data.\n"
        "- Avoid hardcoded values. Use column names and query_result_df operations.\n"
        "- Only return valid JSON. No explanations outside the JSON.\n"
        "- If the data includes rows and columns suitable for tabular display (like listings, joined information, or group summaries), set `table_required` to true.\n"
        "- If the user request explicitly or implicitly asks for a chart, visual representation, or uses terms like 'graph', 'plot', 'visualize', 'show trend', etc., set `graph_required` to true.\n"
        "- If unsure, prefer setting `table_required` to true and `graph_required` to false.\n\n"
        f"User Request: {state['user_request']}\n"
        f"SQL Query: {state['generated_query']}\n"
        f"Result Columns: {column_names}\n"
        f"Sample Rows: {sample_rows}\n"
    )

    structured_llm = llm.with_structured_output(AnswerOutput)
    result = structured_llm.invoke(prompt)
    return result
