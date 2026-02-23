from langchain.agents.middleware import HumanInTheLoopMiddleware

human_in_the_loop = HumanInTheLoopMiddleware(
    interrupt_on={
        "send_email": {
            "allowed_decisions": ["approve", "reject"],
        },
        "authenticate": False,
        "check_inbox":  False,
        "draft_email":  False,
    }
)