# 🤖 LangChain SQL Agent with MySQL & Groq

An intelligent, context-aware Natural Language-to-SQL AI Agent built using **LangChain**, **Groq (Llama 3.3)**, and **MySQL**.

This application allows users to ask natural language questions about an e-commerce database (such as sales performance, top spending customers, product stock, and order statuses). The agent dynamically inspects database schemas, writes syntactically valid MySQL queries, executes them safely, and translates raw database results into clear human responses.

---

## 📌 Features

* **Natural Language to SQL Translation:** Converts human text queries into complex multi-table SQL queries (`JOIN`, `GROUP BY`, `SUM`, `ORDER BY`).
* **Tool Calling Capabilities:** Leverages native function calling (`agent_type="tool-calling"`) to inspect schemas and validate query syntax before execution.
* **Strict Read-Only Guardrails:** Instructed via custom system prompts to execute `SELECT` queries only—preventing destructive operations like `DELETE`, `UPDATE`, or `DROP`.
* **High Performance & Low Latency:** Powered by Groq's LPUs and Llama 3 models for ultra-fast response times.
* **Environment Security:** Keeps sensitive credentials (database keys, API keys) safe using `python-dotenv`.

---

## 🗄️ Database Architecture

The project connects to a standard relational E-Commerce database (`ecommerce_agent_db`) consisting of 5 interconnected tables:

* **`customers`**: Stores customer profiles, locations, and registration dates.
* **`categories`**: Product classifications (Electronics, Clothing, Books, etc.).
* **`products`**: Item names, category links, pricing, and available stock.
* **`orders`**: Tracking order dates, statuses (`Pending`, `Shipped`, `Delivered`, `Cancelled`), and total amounts.
* **`order_items`**: Line-item breakdown linking orders to specific products with quantities and unit prices.

---

## 🛠️ Prerequisites & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/sql-agent-langchain.git](https://github.com/your-username/sql-agent-langchain.git)
cd sql-agent-langchain
