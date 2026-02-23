from langchain.agents import AgentState
from dataclasses import dataclass

class AuthenticatedState(AgentState):
    authenticated: bool


@dataclass
class EmailContext:
    email_address: str = "user@example.com"
    password: str = "password@123"