from langchain.agents import create_agent
from src.config import get_llm

_SYSTEM_PROMPT = """
You are a travel agent. Find the best flights to the wedding destination.

Selection criteria (in priority order):
  1. Price — economy class, lowest fare
  2. Duration — shortest travel time
  3. Date — choose the time of year most suitable for a wedding at this destination

Rules:
- Search for one ticket, one way.
- Do not ask follow-up questions.
- Make multiple searches if needed to compare options.
- Return a shortlist of at least 3 flight options with airline, price, duration, and departure time.
"""


def create_travel_agent(flight_tools: list):
    """
    Factory function.
    flight_tools must be resolved before calling this (they come from MCP).
    """
    return create_agent(
        model=get_llm(),
        tools=flight_tools,
        system_prompt=_SYSTEM_PROMPT,
    )