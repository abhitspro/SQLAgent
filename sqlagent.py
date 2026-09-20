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

# Memory store
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import Redis message history module for Persistent Storage
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# for custom tools
from langchain_core.tools import tool


# 2. Build MySQL Connection String from Environment Variables
# Read credentials from .env to keep passwords and host details hidden
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "ecommerce_agent_db")

# Format: mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database_name>
ECOM_DB = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL is missing. Please check your .env file.")

@tool
def calculate_discount(price: float, discount_percentage: float) -> str:
    """Calculates the final price after applying a percentage discount.
    Use this tool when a user asks for discount calculations, promotional pricing, or sale quotes.
    """
    final_price = price * (1 - discount_percentage / 100)
    return f"Original: ${price:.2f}, Discounted ({discount_percentage}%): ${final_price:.2f}"

@tool
def send_email_alert(recipient_email: str, subject: str, message: str) -> str:
    """Sends an email notification to a specified address.
    Use this tool ONLY when explicitly requested to alert or notify someone via email.
    """
    # Place actual email dispatch logic here (e.g., via SendGrid or SMTP)
    return f"Alert email successfully dispatched to {recipient_email}."

# Collect custom tools into a list
custom_tools = [calculate_discount, send_email_alert]

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




    # # Custom system instructions forcing SELECT-only operations
    # CUSTOM_SYSTEM_PREFIX = """
    # You are an agent designed to interact with a SQL database.
    # Given an input question, create a syntactically correct MySQL query to run, then look at the results and return the answer.

    # CRITICAL SECURITY RULES:
    # 1. You are strictly allowed to run SELECT queries ONLY.
    # 2. NEVER execute DML or DDL statements (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT).
    # 3. If the user asks you to modify, update, delete, or alter any data or tables, politely refuse.
    # """

    #  for extra tools
    CUSTOM_SYSTEM_PREFIX = """
    You are an intelligent agent designed to interact with a MySQL database and execute helper tools.
    Given an input question, evaluate whether to run SQL database queries or execute custom tools.

    CRITICAL SECURITY RULES:
    1. You are strictly allowed to run SELECT queries ONLY.
    2. NEVER execute DML or DDL statements (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT).
    """




    # # 5. Create SQL Agent
    # agent_executor = create_sql_agent(
    #     llm=llm,
    #     db=db,
    #     agent_type="tool-calling",
    #     prefix= CUSTOM_SYSTEM_PREFIX,
    #     verbose=True 
    # )

    """When you pass agent_type="tool-calling", LangChain equips the LLM with a set of pre-built SQL tools:
        1. sql_db_list_tables: Lists all available tables in your database.
        2. sql_db_schema: Fetches table structures, column names, data types, and foreign key rules.
        3. sql_db_query: Runs a generated SQL statement and retrieves raw rows.
        4. sql_db_query_checker: Validates SQL syntax before execution to prevent syntax errors.
    """

    prompt = ChatPromptTemplate.from_messages([ # list of tuples
        ("system",CUSTOM_SYSTEM_PREFIX),
        MessagesPlaceholder(variable_name = "chat_history"),
        ('human',"{input}"),
        MessagesPlaceholder(variable_name = 'agent_scratchpad'),
        ])

    # 5. Create SQL Agent
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        prefix= CUSTOM_SYSTEM_PREFIX,
        extra_tools=custom_tools, # to integrate custom tool
        prompt = prompt,
        verbose=True 
    )

    """When you pass agent_type="tool-calling", LangChain equips the LLM with a set of pre-built SQL tools:
        1. sql_db_list_tables: Lists all available tables in your database.
        2. sql_db_schema: Fetches table structures, column names, data types, and foreign key rules.
        3. sql_db_query: Runs a generated SQL statement and retrieves raw rows.
        4. sql_db_query_checker: Validates SQL syntax before execution to prevent syntax errors.
    """


    # # In-memory dictionary to hold session histories
    # store = {} 
    
    # implementing Redis for Persistent storage instead of store {}
    # REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")



    # def get_session_history(session_id: str):
    #     if session_id not in store:
    #         store[session_id] = ChatMessageHistory()
    #     return store[session_id]

    # Replaces the old in-memory `store = {}` dictionary
    def get_redis_session_history(session_id: str):
        return RedisChatMessageHistory(
            session_id=session_id,
            url=REDIS_URL,
            ttl=86400  # Automatically cleans up inactive sessions after 24 hours (86,400 seconds)
        )



    # agent_with_history = RunnableWithMessageHistory(
    #     agent_executor, # what to run. Tells LangChain which agent workflow should be given memory capabilities.
    #     get_session_history, # to fetch history
    #     input_messages_key='input',    # what to store in history
    #     history_messages_key="chat_history", # where to check for history
    # )

    # Wrap your existing agent executor
    agent_with_history = RunnableWithMessageHistory(
        agent_executor,
        get_redis_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )



    # # 6. Run Test Query
    # query = "Who is our top spending customer?"
    # response = agent_executor.invoke({"input": query})
    # print("\n--- Output ---")
    # print(response["output"])   

    # # Test malicious query attempt
    # query = "Delete all cancelled orders from the orders table."
    # response = agent_executor.invoke({"input": query})

    # print("\n--- Output ---")
    # print(response["output"])
    ##################################

    # # Invoke agent with history
    # # Session 1: Initial Question
    # response1 = agent_with_history.invoke( # distionary of input variables
    #     {'input': "Who is our top spending customer?"},
    #     config={"configurable": {"session_id": "user_session_1"}}  # for get_session_history()
    # )
    # print("Q1 Answer:", response1["output"])

    # # Session 1: Follow-up Question (Agent remembers previous answer context)
    # response2 = agent_with_history.invoke(
    #     {"input": "What products did they order?"},
    #     config={"configurable": {"session_id": "user_session_1"}}
    # )
    # print("Q2 Answer:", response2["output"])

    # test redis
    # # 6. Test Call
    # response = agent_with_history.invoke(
    #     {"input": "Who is our top spending customer?"},
    #     config={"configurable": {"session_id": "user_session_101"}}
    # )
    # print("\nQ1 Answer:", response["output"])

    # # 6. Test Call
    # response = agent_with_history.invoke(
    #     {"input": "What products did they order?"},
    #     config={"configurable": {"session_id": "user_session_101"}}
    # )
    # print("\nQ2 Answer:", response["output"])

    # test custom tools
    # test case 01: Product ID 101 does not exist
    response = agent_with_history.invoke(
        {"input":"Find the price of product ID 101 from the database, and tell me what the cost would be with a 20% discount."},
        config={"configurable": {"session_id": "custom_tool_session"}}
    )

    print("\nResult:", response["output"])
    # Result: I ran a query to look up the price for product ID 101, but that product isn’t in the `products` table (the table only contains IDs 1, 2, and 3). Because the price can’t be retrieved, I can’t calculate a 20 % discount for it. If you have a different product ID or need help with another item, just let me know!
    #It correctly identified that Product ID 101 does not exist (and saw that valid IDs are 1, 2, and 3).

    # test case 02: Valid Product ID
    response = agent_with_history.invoke(
        {"input": "Find the price of product ID 1, and tell me what its cost would be with a 20% discount."},
        config={"configurable": {"session_id": "custom_tool_session"}}
    )

    print("\nFinal Output:", response["output"])
    #  Final Output: **Product ID 1**

    # - **Original price:** $199.99  
    # - **20 % discount:** $159.99 

    


except Exception as e:
    print(f"Error connecting or running agent: {e}")

