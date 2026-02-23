from langchain_core.tools import tool
from src.config import get_db, logger

_db = get_db()


@tool
def query_playlist_db(query: str) -> str:
    """
    Execute a SQL query against the Chinook playlist database.
    Use this to find tracks, albums, artists, and pricing information.
    """
    try:
        results = _db.run(query)
        return str(results)
    except Exception as exc:
        logger.error("query_playlist_db failed: %s", exc)
        return f"Database query failed: {exc}"