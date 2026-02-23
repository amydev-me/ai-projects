import asyncio
from langchain_core.messages import HumanMessage

from src.mcp.client import create_mcp_client
from src.agents.travel_agent import create_travel_agent
from src.agents.coordinator import create_coordinator
from src.tools.agent_tools import make_flight_tool
from src.config import logger

CONFIG = {"configurable": {"thread_id": "1"}, "recursion_limit": 50}


async def main() -> None:
    # 1. Resolve async MCP tools
    mcp_client = create_mcp_client()
    flight_tools = await mcp_client.get_tools()

    # 2. Build agents that depend on those tools
    travel_agent = create_travel_agent(flight_tools)
    search_flights = make_flight_tool(travel_agent)

    # 3. Build the coordinator with everything wired up
    coordinator = create_coordinator(search_flights)

    print("Wedding Planner — type 'exit' to quit\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye! ")
            break

        try:
            response = await coordinator.ainvoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
            )
            print("\nCoordinator:", response["messages"][-1].content, "\n")
        except Exception as exc:
            logger.error("Coordinator error: %s", exc)
            print(f"\n[Error] Something went wrong: {exc}\n")


if __name__ == "__main__":
    asyncio.run(main())