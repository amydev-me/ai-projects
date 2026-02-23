import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from tavily import TavilyClient

load_dotenv()

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("wedding_planner")

# ── Environment ────────────────────────────────────────────────────────────────
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
DB_URI: str = os.getenv("DB_URI", "sqlite:///resources/Chinook.db")

# ── Shared singletons ──────────────────────────────────────────────────────────
def get_llm(model: str = OPENAI_MODEL) -> ChatOpenAI:
    """Return a ChatOpenAI instance. Pass a different model name to override."""
    return ChatOpenAI(model=model)


def get_db() -> SQLDatabase:
    return SQLDatabase.from_uri(DB_URI)


def get_tavily_client() -> TavilyClient:
    if not TAVILY_API_KEY:
        raise EnvironmentError("TAVILY_API_KEY is not set in your .env file.")
    return TavilyClient(api_key=TAVILY_API_KEY)