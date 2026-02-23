from langchain_mcp_adapters.client import MultiServerMCPClient

# ── MCP server registry ────────────────────────────────────────────────────────
# Add or remove MCP servers here without touching any other file.
_MCP_SERVERS = {
    "kiwi-com-flight-search": {
        "transport": "http",
        "url": "https://mcp.kiwi.com/mcp",
    },
}


def create_mcp_client() -> MultiServerMCPClient:
    """Return a configured MultiServerMCPClient."""
    return MultiServerMCPClient(_MCP_SERVERS)