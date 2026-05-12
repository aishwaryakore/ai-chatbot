# AI Chatbot

A conversational AI chatbot built with **LangGraph**, **LangChain**, and **Streamlit**. It supports multi-turn conversations with persistent memory, real-time tool use (web search, stock prices, and a calculator), and a sidebar for navigating past chat sessions.

---

## Features

- **Multi-turn memory** — conversations are persisted to a local SQLite database via LangGraph's `SqliteSaver` checkpointer, so chat history survives across sessions.
- **Multiple chat threads** — start new conversations at any time and switch between past ones using the sidebar.
- **Tool use** — the LLM can invoke three tools on demand:
  - **Web search** (DuckDuckGo) — answers questions requiring up-to-date information.
  - **Stock price lookup** (Alpha Vantage API) — fetches the latest price for any ticker symbol.
  - **Calculator** — performs basic arithmetic (add, subtract, multiply, divide).
- **Streaming responses** — AI replies stream token-by-token in the UI; tool calls are shown in a collapsible status box while they run.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | OpenAI (via `langchain-openai`) |
| Agent framework | LangGraph (`StateGraph`) |
| Memory / persistence | SQLite (`langgraph-checkpoint-sqlite`) |
| Tools | LangChain Community (`DuckDuckGoSearchRun`), Alpha Vantage REST API |
| Frontend | Streamlit |

---

## Project Structure

```
ai-chatbot/
├── chatbot_frontend.py   # Streamlit UI — chat input, sidebar, streaming display
├── langgraph_backend.py  # LangGraph agent graph — LLM node, tool node, SQLite checkpointer
├── tools.py              # Tool definitions — web search, stock price, calculator
├── .gitignore
└── README.md
```

### File overview

**`langgraph_backend.py`** — Defines the agent as a `StateGraph` with two nodes: a `chat_node` that calls the OpenAI LLM (with tools bound), and a `tools` node that executes any requested tool. Conditional edges route back and forth between them until the LLM produces a final response. The compiled graph is checkpointed per `thread_id` in `chatbot.db`.

**`chatbot_frontend.py`** — Streamlit app that manages session state (current thread, message history), renders the chat UI, and streams responses from the backend. The sidebar lists all past threads (loaded from the checkpointer on startup) and lets the user reload any previous conversation.

**`tools.py`** — Exports a `TOOLS` list containing: a `DuckDuckGoSearchRun` search tool, a `calculator` tool for arithmetic, and a `get_stock_price` tool that queries the Alpha Vantage API.

---

## Setup

### Prerequisites

- Python 3.10+
- An OpenAI API key
- An Alpha Vantage API key (free tier available at [alphavantage.co](https://www.alphavantage.co/))

### Installation

```bash
git clone https://github.com/aishwaryakore/ai-chatbot.git
cd ai-chatbot
pip install streamlit langgraph langchain langchain-openai langchain-community langgraph-checkpoint-sqlite python-dotenv requests
```

### Environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> The Alpha Vantage API key is currently hardcoded in `tools.py`. Replace the `apikey` value in `get_stock_price` with your own key, or move it to `.env` for better security.

### Run the app

```bash
streamlit run chatbot_frontend.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Usage

- Type a message in the chat input at the bottom to start a conversation.
- Click **New Chat** in the sidebar to begin a fresh thread.
- Click any previous thread ID in the sidebar to reload that conversation.
- When the LLM uses a tool, a status indicator appears in the chat while the tool runs, then collapses when it finishes.

---

## Notes

- Conversation history is stored in `chatbot.db` (SQLite) in the project directory, which is excluded from version control via `.gitignore`.
- The agent uses a ReAct-style loop: the LLM may invoke multiple tools in sequence before delivering a final answer.