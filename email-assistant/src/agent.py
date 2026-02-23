from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from src.middleware.wrap_model import dynamic_tool_call, dynamic_prompt_func
from src.middleware.human_loop import human_in_the_loop
from src.state import AuthenticatedState, EmailContext
from src.tools.auth import authenticate
from src.tools.inbox import check_inbox
from src.tools.email import draft_email, send_email
from src.config import get_llm

agent = create_agent(
    model=get_llm(),
    tools=[authenticate, check_inbox, draft_email, send_email],
    state_schema=AuthenticatedState,
    context_schema=EmailContext,
    checkpointer=InMemorySaver(),   
    middleware=[
        dynamic_tool_call,
        dynamic_prompt_func,
        human_in_the_loop,
    ],
)