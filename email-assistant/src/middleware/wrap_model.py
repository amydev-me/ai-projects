from typing import Callable
from langchain.agents.middleware import wrap_model_call, dynamic_prompt, ModelRequest, ModelResponse
from src.tools.auth import authenticate
from src.tools.inbox import check_inbox
from src.tools.email import draft_email, send_email


@wrap_model_call
async def dynamic_tool_call(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Swap available tools based on authentication state."""
    authenticated = request.state.get("authenticated")
    tools = [check_inbox, draft_email, send_email] if authenticated else [authenticate]
    request = request.override(tools=tools)
    return await handler(request)


@dynamic_prompt
def dynamic_prompt_func(request: ModelRequest) -> str:
    """Swap system prompt based on authentication state."""
    authenticated = request.state.get("authenticated")
    if authenticated:
        return "You are a helpful email assistant. You can check the inbox, draft replies, and send emails. Always draft before sending."
    return "You are a helpful email assistant. Ask the user for their email and password to authenticate."