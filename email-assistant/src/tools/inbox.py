from langchain_core.tools import tool
from src.mock_data import INBOX


@tool
def check_inbox() -> str:
    """Check the inbox, return all emails, and automatically mark them as read."""
    if not INBOX:
        return "No emails found."
    result = []
    for email in INBOX:
        email["read"] = True
        status = "replied" if email["replied"] else "unread"
        result.append(
            f"[{status}] ID: {email['id']} | From: {email['from']}\n"
            f"Subject: {email['subject']}\n"
            f"Body: {email['body']}\n"
        )
    return "\n---\n".join(result)