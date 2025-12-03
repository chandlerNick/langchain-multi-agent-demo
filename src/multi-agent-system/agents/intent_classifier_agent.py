# Classifies email intent: Spam, Bug Ticket, Normal, or Human Review
from typing import Literal
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from agentstructure.state import EmailClassification, EmailAgentState
import re

llm = ChatOpenAI(  # NOTE: This wont work until I set up the gpt-oss model in the kubernetes deployment
    model="openai/gpt-oss-120b",
    api_key="dummy",
    base_url="http://localhost:8000/v1"
)


def classify_intent(state: EmailAgentState) -> Command[Literal["human_review", "draft_response", "spam"]]:
    """Classify as spam, machine_processable, or human_review and route accordingly.

    Uses LLM when available; falls back to simple heuristics.
    """

    structured_llm = llm.with_structured_output(EmailClassification)

    classification_prompt = f"""
    Analyze this customer email and classify it:

    Email: {state['email_content']}
    From: {state['sender_email']}

    Provide classification including intent, urgency, topic, and summary.
    Intent must be one of: spam, machine_processable, human_review.
    """

    try:
        classification = structured_llm.invoke(classification_prompt)
    except Exception:
        content = (state.get("email_content") or "").lower()
        spam_patterns = [
            r"unsubscribe", r"lottery", r"free money", r"winner", r"viagra",
            r"click here", r"limited time", r"guaranteed"
        ]
        is_spam = any(re.search(p, content) for p in spam_patterns)
        classification = {
            "intent": "spam" if is_spam else "machine_processable",
            "urgency": "low" if is_spam else "medium",
            "topic": "spam" if is_spam else "general",
            "summary": "Heuristic classification due to LLM unavailability",
        }

    # Normalize intent from LLM output to expected buckets
    intent = (classification.get("intent") or "").lower()
    urgency = (classification.get("urgency") or "").lower()

    if intent == "spam":
        goto = "spam"
    elif urgency == "critical":
        # Critical always for human review but still draft later in flow
        classification["intent"] = "human_review"
        goto = "draft_response"
    elif intent in {"billing", "complex", "human_review"}:
        classification["intent"] = "human_review"
        goto = "draft_response"
    else:
        classification["intent"] = "machine_processable"
        goto = "draft_response"

    return Command(
        update={"classification": classification},
        goto=goto,
    )
