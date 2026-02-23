import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("email_assistant")

# ── Environment ────────────────────────────────────────────────────────────────
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ── Shared singletons ──────────────────────────────────────────────────────────
def get_llm(model: str = OPENAI_MODEL) -> ChatOpenAI:
    """Return a ChatOpenAI instance. Pass a different model name to override."""
    return ChatOpenAI(model=model)