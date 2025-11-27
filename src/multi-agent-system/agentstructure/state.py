# Manages shared state and memory between agents
from typing import TypedDict, Literal

# Define the structure for email classification
class EmailClassification(TypedDict):
    intent: Literal["question", "spam", "complex"]
    urgency: Literal["low", "medium", "high", "critical"]
    topic: str
    summary: str

class EmailAgentState(TypedDict):
    # Raw email data
    email_content: str
    sender_email: str
    email_id: str
    user_metadata: str

    # Classification result
    classification: EmailClassification | None

    # Generated content
    draft_response: str | None
    messages: list[str] | None
