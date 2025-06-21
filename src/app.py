import streamlit as st
from handle_db import connect_to_database
from model import llm
from process_pipeline import pipeline
from common import State
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')

# Streamlit UI to collect database details
st.sidebar.header("Database Connection")
db_type = st.sidebar.selectbox("Database Type", ["postgresql", "mysql", "mssql"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')
host = st.sidebar.text_input("Host")
port = st.sidebar.number_input("Port", min_value=0)
db_name = st.sidebar.text_input("Database Name")

# Initialize db_conn in Streamlit's state to persist across runs
if "db_conn" not in st.session_state:
    st.session_state.db_conn = None

if st.sidebar.button("Connect to Database"):
    try:
        db = connect_to_database(db_type, username, password, host, port, db_name)
        st.success("Database connected successfully.")
        st.session_state.db_conn = db
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")

# Main section for question
st.title("Plain English Database Query & Visualization Tool")
request = st.text_input("Enter your question or query or graph visualization request in plain english:")

if st.button("Generate Result") and request:
    if st.session_state.db_conn is not None:
        state = State(status=True)
        state["user_request"] = request
        state = pipeline(state, llm, st.session_state.db_conn)

        if state['status']:
            answer = state['answer']
            query_result_df = state['query_result_df']
            st.write(answer)

            if state['graph_required']:
                try:
                    exec(state['graph_code'])
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Failed to execute graph code: {e}")

            if state['table_required']:
                st.table(query_result_df)
        else:
            st.error(f"Error processing request. {state['reason']}")
    else:
        st.error("Database is not connected.")
