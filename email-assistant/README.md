# 📧 AI Email Assistant

A conversational email assistant built with **LangChain**, **LangGraph**, and **middleware patterns** from the LangChain course module 3.

> Part of the [AI Projects](../) collection — see also [Wedding Planner](../wedding-planner).

---

## Architecture

```
User Input
    |
    v
@wrap_model_call      <- swaps tools based on auth state
@dynamic_prompt       <- swaps system prompt based on auth state
    |
    v
Agent
  |- authenticate     <- only available when NOT authenticated
  |- check_inbox      <- only available when authenticated
  |- draft_email      <- only available when authenticated
  |- send_email       <- requires human approval before sending
    |
    v
HumanInTheLoopMiddleware  <- pauses before send_email for approval
```

---

## Middleware Patterns Demonstrated

| Pattern | File | Purpose |
|---|---|---|
| @wrap_model_call | middleware/wrap_model.py | Dynamically swap tools based on auth state |
| @dynamic_prompt | middleware/wrap_model.py | Dynamically swap system prompt based on auth state |
| HumanInTheLoopMiddleware | middleware/human_loop.py | Pause before send_email for human approval |

---

## Project Structure

```
email-assistant/
├── main.py                      # Entry point + HITL approval loop
├── pyproject.toml               # uv project config and dependencies
├── .env                         # API keys (not committed)
├── README.md
└── src/
    ├── state.py                 # AuthenticatedState + EmailContext
    ├── mock_data.py             # Mock inbox emails
    ├── agent.py                 # Wires everything together
    ├── tools/
    │   ├── auth.py              # authenticate tool
    │   ├── inbox.py             # check_inbox tool
    │   └── email.py             # draft_email, send_email tools
    └── middleware/
        ├── wrap_model.py        # dynamic_tool_call + dynamic_prompt_func
        └── human_loop.py        # HumanInTheLoopMiddleware config
```

---

## Prerequisites

- Python 3.12
- uv (https://docs.astral.sh/uv/)
- An OpenAI API key

---

## Getting Started

1. Clone the repo

```bash
git clone https://github.com/your-username/ai-projects.git
cd ai-projects/email-assistant
```

2. Install dependencies

```bash
uv sync
```

3. Set up environment variables

Create a .env file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5-mini
```

4. Run

```bash
uv run main.py
```

---

## Example Conversation

```
You: Can you check my inbox?
Assistant: Please provide your email and password to authenticate.

You: My email is user@example.com and password is password123
Assistant: Authentication successful! Here are your emails:

[unread] ID: 1 | From: admin@example.com
Subject: Welcome to our service
...

You: Reply to the delivery email and say thank you for the update
Assistant: I have drafted a reply. Here it is:
DRAFT
To: delivery@example.com
Subject: Re: Your order has been shipped
Thank you for the update!

Would you like me to send this?

You: yes

  About to send:
   To:      delivery@example.com
   Subject: Re: Your order has been shipped
   Body:    Thank you for the update!

Approve? (yes / no)
You: yes
Assistant: Email sent to delivery@example.com successfully!
```

---

## Key Design Decisions

**Dynamic tools via @wrap_model_call** — the agent only sees the authenticate tool when logged out, and inbox/email tools when logged in. This prevents the LLM from attempting to call tools it should not have access to.

**Dynamic prompt via @dynamic_prompt** — the system prompt switches between an unauthenticated and authenticated persona, keeping the agent focused on the right task at each stage.

**Human-in-the-loop before send_email** — sending an email is irreversible, so HumanInTheLoopMiddleware pauses execution and shows the draft to the user before proceeding. The user can approve or reject.

**context_schema vs state_schema** — EmailContext (credentials) is injected as external context at startup and never changes. AuthenticatedState tracks whether the user has logged in and is updated by the authenticate tool via Command.

---
