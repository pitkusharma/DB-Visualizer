from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import Annotated
from typing_extensions import TypedDict
from common import State, manage_state
from handle_db import get_compact_schema_summary


system_message = """
Given an input question, generate a syntactically correct {dialect} SELECT query that can help retrieve the answer.

# Constraints and Expectations:

- You must generate only SELECT-type queries.  
  If the input asks for a non-SELECT operation (e.g., UPDATE, INSERT, DELETE, CREATE), or cannot be satisfied using data selection alone (e.g., training models, modifying schemas), set `status` to False and provide a clear explanation in `reason`. Do not return any query in such cases.

- If the question is about database metadata (e.g., listing tables, showing columns, describing schema), generate a SELECT query using standard catalog views such as `information_schema.tables` or `information_schema.columns` (if supported in {dialect}).

- If the input includes terms like "plot", "graph", "visualize", or "chart", assume the user wants to visualize the data — and generate the SELECT query required to retrieve that data. Do not reject these inputs.

- Never use `SELECT *`. Always select only the relevant columns based on the question.

- If the user requests “all”, “entire list”, “complete list”, or explicitly wants all records, DO NOT include a LIMIT clause.  
  In all other cases, limit the query to at most {top_k} records.

- Use only the columns and tables that are defined in the provided schema. Do not reference any names that are not listed.

- If the query is successfully generated and `status` is True:
  - Set `reason` to an empty string (`""`).
  - Do NOT explain anything or include additional comments.

Schema available:
{table_info}
"""

user_prompt = "Request: {input}"

query_prompt_template = ChatPromptTemplate(
    [("system", system_message), ("user", user_prompt)]
)

class QueryOutput(TypedDict):
    """Structure of the generated SQL query output."""

    status: Annotated[bool, "True if the query was successfully generated and is valid; False otherwise."]
    reason: Annotated[str, "Reason for failure while generating the query (if query generation is successful keep it as empty string.)."]
    generated_query: Annotated[str, "Syntactically valid SQL SELECT query."]

@manage_state
def write_query(state: State, llm, db):
    """Generate SQL query to fetch information."""

    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 15,
            "table_info": get_compact_schema_summary(db),
            "input": state["user_request"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return result
