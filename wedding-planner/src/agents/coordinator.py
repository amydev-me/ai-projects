from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from src.config import get_llm
from src.state import WeddingState
from src.tools.state_tools import update_state
from src.tools.agent_tools import search_venues, suggest_playlist

_SYSTEM_PROMPT = """
You are a wedding coordinator. Your job is to gather information from the couple
and delegate planning tasks to your specialist agents.

Information to collect (ask only for what is still missing):
  - Origin         — where the couple is travelling from
  - Destination    — where the wedding will take place
  - Guest count    — number of guests
  - Music genre    — preferred music style for the playlist
  - Wedding date   — preferred date or time of year

Workflow:
  1. Collect all five pieces of information through friendly conversation.
  2. Once all information is gathered, call update_state to persist it.
  3. Delegate to search_flights, search_venues, and suggest_playlist in parallel if possible.
  4. Synthesise the results into a final wedding plan for the couple.

Rules:
  - Never ask for information the user has already provided.
  - Be warm, professional, and concise.
"""


def create_coordinator(search_flights_tool):
    """
    Factory function.
    search_flights_tool is injected because it depends on async MCP tools
    that are resolved at runtime in main().
    """
    return create_agent(
        model=get_llm(),
        tools=[search_flights_tool, search_venues, suggest_playlist, update_state],
        checkpointer=InMemorySaver(),
        state_schema=WeddingState,
        system_prompt=_SYSTEM_PROMPT,
    )