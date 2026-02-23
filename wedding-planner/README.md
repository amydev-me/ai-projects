# 💍 AI Wedding Planner

A multi-agent AI application that plans your perfect wedding — flights, venues, and playlists — through a conversational interface.

Built with **LangGraph**, **LangChain**, and **MCP (Model Context Protocol)**.

> Part of the [AI Projects](../) collection — see also [Personal Chef](../personal-chef).

---

## Architecture

```
                        ┌─────────────────────┐
                        │     Coordinator      │
                        │   (LangGraph Agent)  │
                        └────────┬────────────┘
                                 │ delegates to
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                       ▼
 ┌────────────────┐   ┌──────────────────┐   ┌─────────────────┐
 │  Travel Agent  │   │   Venue Agent    │   │ Playlist Agent  │
 │  (MCP + Kiwi) │   │  (Tavily Search) │   │ (Chinook SQLDB) │
 └────────────────┘   └──────────────────┘   └─────────────────┘
```

The **Coordinator** gathers wedding details from the user through conversation, then delegates to three specialist agents in parallel:

- **Travel Agent** — finds the best economy flights via the Kiwi.com MCP server
- **Venue Agent** — searches for venues by location, capacity, price, and reviews
- **Playlist Agent** — queries the Chinook database to curate a genre-specific playlist with total duration and cost

---

## Project Structure

```
wedding-planner/
├── main.py                        # Entry point
├── pyproject.toml                 # uv project config & dependencies
├── .env                           # API keys (not committed)
├── README.md
└── src/
    ├── config.py                  # Env vars, LLM, DB, logging setup
    ├── state.py                   # WeddingState (LangGraph MessagesState)
    ├── tools/
    │   ├── web_search.py          # Tavily web search tool
    │   ├── database.py            # SQL query tool (Chinook DB)
    │   ├── state_tools.py         # update_state tool
    │   └── agent_tools.py         # Sub-agent tools + make_flight_tool factory
    ├── agents/
    │   ├── venue_agent.py         # Venue specialist
    │   ├── playlist_agent.py      # Playlist specialist
    │   ├── travel_agent.py        # Travel specialist (factory)
    │   └── coordinator.py         # Orchestrator (factory)
    └── mcp/
        └── client.py              # MCP server registry
```

---

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — fast Python package manager
- An OpenAI API key
- A Tavily API key ([free tier available](https://tavily.com))
- The Chinook SQLite database in `resources/Chinook.db`

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/your-username/ai-projects.git
cd ai-projects/wedding-planner
```

**2. Install dependencies**
```bash
uv sync
```

**3. Set up environment variables**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5-mini
TAVILY_API_KEY=your_tavily_api_key
DB_URI=sqlite:///resources/Chinook.db
```

**4. Run**
```bash
uv run main.py
```

**Adding a new dependency**
```bash
uv add <package-name>
```

---

## Example Conversation

```
💍 Wedding Planner — type 'exit' to quit

You: Hi! I want to plan my wedding.

Coordinator: Congratulations! I'd love to help you plan your perfect wedding.
Let's start with a few details. Where will you and your guests be travelling from?

You: We're based in Kuala Lumpur. The wedding will be in Bali, around 80 guests.
     We love jazz music and are thinking sometime in July.

Coordinator: Beautiful choice! I have everything I need. Let me coordinate
your flights, venues, and playlist now...
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | OpenAI GPT-5-mini |
| Web search | [Tavily](https://tavily.com) |
| Flight search | [Kiwi.com MCP](https://mcp.kiwi.com) |
| Database | SQLite (Chinook) via LangChain |
| MCP client | [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) |
| Package manager | [uv](https://docs.astral.sh/uv/) |

---

## Key Design Decisions

**Factory functions for agents** — `create_travel_agent()` and `create_coordinator()` are factories rather than module-level singletons. This is because the travel agent depends on MCP flight tools that are resolved asynchronously at startup, so they must be injected after `await mcp_client.get_tools()` completes.

**Shared state via `WeddingState`** — wedding details (origin, destination, guest count, genre, date) are stored in LangGraph's graph state and updated incrementally via the `update_state` tool, giving all agents access to the same context.

**Sub-agents as tools** — each specialist agent is wrapped in a `@tool` so the coordinator can call them declaratively, keeping orchestration logic in the LLM rather than hardcoded control flow.

---

## .gitignore

```
__pycache__/
*.pyc
.env
resources/
.venv/
```