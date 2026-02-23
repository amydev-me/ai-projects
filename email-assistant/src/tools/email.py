from langchain_core.tools import tool
from src.mock_data import INBOX


@tool
def draft_email(to: str, subject: str, body: str) -> str:
    """Draft an email before sending."""
    return f"DRAFT\nTo: {to}\nSubject: {subject}\n\n{body}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to the recipient."""
    for email in INBOX:
        if email["from"] == to:
            email["replied"] = True
    return f"Email sent to {to} with subject '{subject}'."