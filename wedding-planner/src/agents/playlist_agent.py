from langchain.agents import create_agent
from src.config import get_llm
from src.tools.database import query_playlist_db

_SYSTEM_PROMPT = """
You are a playlist specialist. Query the SQL database to curate the perfect wedding playlist for a given genre.

After building the playlist:
  - Calculate the total duration of all tracks.
  - Calculate the total cost (each track has an associated unit price).
  - Present the final playlist in a clear, readable format.

Rules:
- If a query fails, adjust it and try again — do not give up.
- Make multiple queries if needed to find the best tracks.
- Always return a non-empty playlist.
"""

playlist_agent = create_agent(
    model=get_llm(),
    tools=[query_playlist_db],
    system_prompt=_SYSTEM_PROMPT,
)