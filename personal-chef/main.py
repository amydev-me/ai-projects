# Standard library
import os

# Third-party libraries
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from tavily import TavilyClient

# =========================
# Configuration
# =========================
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    try:
        results = client.search(query)
        return str(results["results"])
    except Exception as e:
        return f"Search failed: {e}"


def main():
    system_prompt = """You are a personal chef. The user will give you a list of ingredients they have left over in their house. 
                            Using the web search tool, search the web for recipes that can be made with the ingredients they have.
                            Return recipe suggestion and eventually the recipe instructions to the user, if requested"""

    llm = ChatOpenAI(model=OPENAI_MODEL)

    agent = create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )

    print("Personal Chef Agent (type 'exit' to quit)\n")
    config = {"configurable": {"thread_id": "1"}}

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]}, config=config
        )

        print("\nChef:", response["messages"][-1].content, "\n")


if __name__ == "__main__":
    main()
