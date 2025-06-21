from langchain.sql_database import SQLDatabase
from urllib.parse import quote_plus
from sqlalchemy import inspect


def connect_to_database(db_type, username, password, host, port, db_name):
    """
    Connects to a database using LangChain's SQLDatabase.from_uri.

    Args:
        db_type (str): Type of the database ('postgresql', 'mysql', or 'mssql').
        username (str): Database username.
        password (str): Database password.
        host (str): Database host (typically 'localhost').
        port (int): Database port number.
        db_name (str): Name of the database.

    Returns:
        SQLDatabase instance connected to the specified database.
    """
    db_type = db_type.lower()

    if db_type == "postgresql":
        uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"

    elif db_type == "mysql":
        uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"

    elif db_type == "mssql":
        uri = f"mssql+pyodbc://{username}:{quote_plus(password)}@{host},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"

    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return SQLDatabase.from_uri(uri)


def get_compact_schema_summary(sql_db):
    inspector = inspect(sql_db._engine)
    summary_lines = []

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_defs = [
            f"{col['name']} ({col['type']})" for col in columns
        ]
        summary = f"Table: {table_name} → " + ", ".join(column_defs)
        summary_lines.append(summary)

    return "\n".join(summary_lines)

# db = connect_to_database("mysql", "root", "root", "localhost", 3306, "sakila")
# db