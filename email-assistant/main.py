import asyncio
import os
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from src.agent import agent
from src.state import EmailContext

os.makedirs("logs", exist_ok=True)


async def main():
    context = EmailContext()
    config = {"configurable": {"thread_id": "1"}}

    print("📧 Email Assistant — type 'exit' to quit\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            context=context,
        )

        last_message = response["messages"][-1]

        # Handle HITL interrupt
        if response.get("__interrupt__"):
            interrupt = response["__interrupt__"][0]
            action = interrupt.value["action_requests"][0]

            print(f"\n About to send:")
            print(f"   To:      {action['args'].get('to', '')}")
            print(f"   Subject: {action['args'].get('subject', '')}")
            print(f"   Body:    {action['args'].get('body', '')}")
            print("\nApprove? (yes / no)")
            decision = input("You: ").strip().lower()

            resume = {"decisions": [{"type": "approve"}]} if decision in {"yes", "y"} else {"decisions": [{"type": "reject"}]}

            response = await agent.ainvoke(
                Command(resume=resume),
                config=config,
                context=context,
            )
            print("\nAssistant:", response["messages"][-1].content, "\n")
        else:
            print("\nAssistant:", last_message.content, "\n")


if __name__ == "__main__":
    asyncio.run(main())