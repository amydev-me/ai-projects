from langchain_core.tools import tool
from src.config import get_tavily_client, logger

_client = get_tavily_client()


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information (venues, travel tips, etc.)."""
    try:
        results = _client.search(query)
        return str(results["results"])
    except Exception as exc:
        logger.error("web_search failed: %s", exc)
        return f"Search failed: {exc}"