from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain.tools import ToolRuntime
from langgraph.types import Command


@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
    """Authenticate the user with email and password."""
    if email == runtime.context.email_address and password == runtime.context.password:
        return Command(
            update={
                "authenticated": True,
                "messages": [ToolMessage("Authentication successful.", tool_call_id=runtime.tool_call_id)],
            }
        )
    return Command(
        update={
            "authenticated": False,
            "messages": [ToolMessage("Authentication failed. Please try again.", tool_call_id=runtime.tool_call_id)],
        }
    )