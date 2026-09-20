import os
from dotenv import load_dotenv

load_dotenv()
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq  # Changed import

# Import SQL database wrapper to interact with relational databases
from langchain_community.utilities import SQLDatabase

# Import toolkit containing database inspection & query execution tools,
# and the helper function to construct the SQL agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent


# 2. Build MySQL Connection String from Environment Variables
# Read credentials from .env to keep passwords and host details hidden
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "ecommerce_agent_db")

# Format: mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database_name>
ECOM_DB = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    # 3. Initialize SQLDatabase wrapper from LangChain
    db = SQLDatabase.from_uri(ECOM_DB)

    # Verify the agent can detect database tables
    print("Connected to Dialect:", db.dialect)
    print("Available Tables:", db.get_usable_table_names())

    # 4. Initialize Free Gemini Model
    # "gemini-2.5-flash-lite" is active, fast, and fully supports LangChain SQL tool-calling
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash-lite",
    #     google_api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
    #     temperature=0
    # )

    # Initialize Groq's Free Llama model (supports tool-calling)
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )




    # Custom system instructions forcing SELECT-only operations
    CUSTOM_SYSTEM_PREFIX = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct MySQL query to run, then look at the results and return the answer.

    CRITICAL SECURITY RULES:
    1. You are strictly allowed to run SELECT queries ONLY.
    2. NEVER execute DML or DDL statements (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT).
    3. If the user asks you to modify, update, delete, or alter any data or tables, politely refuse.
    """
    # 5. Create SQL Agent
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        prefix= CUSTOM_SYSTEM_PREFIX,
        verbose=True 
    )

    """When you pass agent_type="tool-calling", LangChain equips the LLM with a set of pre-built SQL tools:
        1. sql_db_list_tables: Lists all available tables in your database.
        2. sql_db_schema: Fetches table structures, column names, data types, and foreign key rules.
        3. sql_db_query: Runs a generated SQL statement and retrieves raw rows.
        4. sql_db_query_checker: Validates SQL syntax before execution to prevent syntax errors.
    """


    # 6. Run Test Query
    query = "Who is our top spending customer?"
    response = agent_executor.invoke({"input": query})
    print("\n--- Output ---")
    print(response["output"])   

    # Test malicious query attempt
    query = "Delete all cancelled orders from the orders table."
    response = agent_executor.invoke({"input": query})

    print("\n--- Output ---")
    print(response["output"])



except Exception as e:
    print(f"Error connecting or running agent: {e}")

