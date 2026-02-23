"""
Agent-backed tools that the coordinator delegates to.

- search_venues and suggest_playlist are straightforward @tool definitions
  because their sub-agents have no async initialisation dependencies.

- make_flight_tool() is a factory because the travel agent requires
  flight_tools that come from an async MCP call; the factory lets us
  inject those tools after they are resolved in main().
"""

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.tools import ToolRuntime

from src.agents.venue_agent import venue_agent
from src.agents.playlist_agent import playlist_agent
from src.config import logger


# ── Venue tool ─────────────────────────────────────────────────────────────────

@tool
async def search_venues(runtime: ToolRuntime) -> str:
    """Delegate to the venue specialist to find the best wedding venues."""
    destination = runtime.state.get("destination", "")
    capacity = runtime.state.get("guest_count", "")

    if not destination:
        return "Destination is not set yet. Please provide a destination first."

    query = f"Find wedding venues in {destination} for {capacity} guests"
    logger.info("search_venues → query: %s", query)

    try:
        response = await venue_agent.ainvoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response["messages"][-1].content
    except Exception as exc:
        logger.error("search_venues failed: %s", exc)
        return f"Venue search failed: {exc}"


# ── Playlist tool ──────────────────────────────────────────────────────────────

@tool
async def suggest_playlist(runtime: ToolRuntime) -> str:
    """Delegate to the playlist specialist to curate a wedding playlist."""
    genre = runtime.state.get("genre", "")

    if not genre:
        return "Music genre is not set yet. Please provide a genre first."

    query = f"Find {genre} tracks for a wedding playlist"
    logger.info("suggest_playlist → query: %s", query)

    try:
        response = await playlist_agent.ainvoke(
            {"messages": [HumanMessage(content=query)]}
        )
        return response["messages"][-1].content
    except Exception as exc:
        logger.error("suggest_playlist failed: %s", exc)
        return f"Playlist curation failed: {exc}"


# ── Flight tool factory ────────────────────────────────────────────────────────

def make_flight_tool(travel_agent):
    """
    Factory that closes over a travel_agent instance (which depends on async
    MCP tools) and returns a @tool-decorated coroutine ready for the coordinator.
    """

    @tool
    async def search_flights(runtime: ToolRuntime) -> str:
        """Delegate to the travel specialist to find the best flight options."""
        origin = runtime.state.get("origin", "")
        destination = runtime.state.get("destination", "")
        date = runtime.state.get("date", "")

        if not origin or not destination:
            return "Origin and destination must both be set before searching flights."

        query = f"Find flights from {origin} to {destination} departing around {date}"
        logger.info("search_flights → query: %s", query)

        try:
            response = await travel_agent.ainvoke(
                {"messages": [HumanMessage(content=query)]},
                config={"recursion_limit": 15},
            )
            return response["messages"][-1].content
        except Exception as exc:
            logger.error("search_flights failed: %s", exc)
            return f"Flight search failed: {exc}"

    return search_flights