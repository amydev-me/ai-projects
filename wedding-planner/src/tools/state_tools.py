from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain.tools import ToolRuntime
from langgraph.types import Command

@tool
def update_state(
    origin: str,
    destination: str,
    guest_count: str,
    genre: str,
    date: str,
    runtime: ToolRuntime,
) -> Command:
    """
    Persist wedding details to the shared graph state.
    Only pass fields that have a value — empty strings are ignored.
    """
    update: dict = {
        "messages": [
            ToolMessage("State updated successfully.", tool_call_id=runtime.tool_call_id)
        ]
    }

    if origin:
        update["origin"] = origin
    if destination:
        update["destination"] = destination
    if guest_count:
        update["guest_count"] = guest_count
    if genre:
        update["genre"] = genre
    if date:
        update["date"] = date

    return Command(update=update)