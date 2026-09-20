# 🤖 Production SQL AI Agent with Persistent Memory & Custom Tools

An enterprise-ready AI Agent built with **LangChain**, **Groq (Llama 3.3 70B)**, **MySQL**, and **Upstash Redis**. The agent dynamically generates and executes secure read-only SQL queries while maintaining persistent conversation memory across sessions and leveraging custom Python tools.

---

## ✨ Features

- **🚀 Llama 3.3 70B via Groq**: High-speed, high-accuracy tool calling and query generation.
- **🛡️ Strict Read-Only Security**: System prompt guardrails enforce strictly `SELECT` statements, preventing any DDL/DML data modification (`INSERT`, `UPDATE`, `DELETE`, `DROP`).
- **💾 Cloud Persistent Memory**: Powered by `langchain-redis` and **Upstash Redis** to maintain session-aware history across server restarts with configurable TTL expiration.
- **🧰 Custom Tool Integration**: Extensible architecture via `extra_tools` allowing the agent to combine database execution with custom Python tools (e.g., business math, notifications).
- **📦 Clean Modular Dependencies**: Up-to-date with current `langchain` package standards.

---

## 🏗️ Architecture Flow

```text
User Input ──> RunnableWithMessageHistory (Upstash Redis)
                     │
                     ▼
          Llama-3.3-70B (Groq LLM)
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
  SQL Database Toolkit       Custom Tools
  (Read-Only MySQL)      (e.g., Discount Calc)
        └────────────┬────────────┘
                     │
                     ▼
               Final Response
```

---

## 🛠️ Prerequisites & Stack

- **Python**: 3.10+ (Recommended)
- **Database**: MySQL Server
- **Memory Store**: Upstash Redis (Serverless)
- **LLM Provider**: Groq API

---

## 🚀 Quick Start Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv

# On Windows PowerShell
.venv\Scripts\Activate.ps1

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration (`.env`)

Create a `.env` file in the project root with the following variables:

```env
# Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# MySQL Database Configuration
DB_USER=root
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecommerce_agent_db

# Upstash Redis Connection (TLS Protocol)
REDIS_URL=rediss://default:YOUR_PASSWORD@YOUR_ENDPOINT.upstash.io:6379
```

> **Note:** Ensure your Upstash connection string starts with `rediss://` (with SSL/TLS enabled).

---

## 📋 Requirements (`requirements.txt`)

```text
langchain>=0.2.0
langchain-groq
langchain-redis>=0.1.0
redis>=5.0.0
mysql-connector-python
SQLAlchemy
python-dotenv
```

---

## 🏃 Usage

Run the agent script:

```bash
python sqlagent.py
```

### Session Memory Example
```python
# First query stores state in Upstash under 'session_123'
response = agent_with_history.invoke(
    {"input": "Find the price of product ID 1 and calculate a 20% discount."},
    config={"configurable": {"session_id": "session_123"}}
)
print(response["output"])

# Follow-up query in the same session remembers context
response2 = agent_with_history.invoke(
    {"input": "Are there any other products in that same category?"},
    config={"configurable": {"session_id": "session_123"}}
)
print(response2["output"])
```

---

## 🛡️ Security Rules

1. **SELECT-Only Enforcement**: System prompt explicitly refuses any request to perform `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, or `CREATE`.
2. **Environment Protection**: Credentials are managed via `python-dotenv` and ignored in `.gitignore`.

---
