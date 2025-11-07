# Classifies email intent: Spam, Bug Ticket, Normal, or Human Review
from typing import Literal
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from agentstructure.state import EmailClassification, EmailAgentState

llm = ChatOpenAI(  # NOTE: This wont work until I set up the gpt-oss model in the kubernetes deployment
    model="openai/gpt-oss-120b",
    api_key="dummy",
    base_url="http://localhost:8000/v1"
)


def classify_intent(state: EmailAgentState) -> Command[Literal["human_review", "draft_response", "spam"]]:
    """Use LLM to classify email intent and urgency, then route accordingly"""

    # Create structured LLM that returns EmailClassification dict
    structured_llm = llm.with_structured_output(EmailClassification)

    # Format the prompt on-demand, not stored in state
    classification_prompt = f"""
    Analyze this customer email and classify it:

    Email: {state['email_content']}
    From: {state['sender_email']}

    Provide classification including intent, urgency, topic, and summary.
    """

    # Get structured response directly as dict
    classification = structured_llm.invoke(classification_prompt)

    # Determine next node based on classification
    if classification['intent'] == 'billing' or classification['urgency'] == 'critical':
        goto = "human_review"
    elif classification['intent'] == 'spam':
        goto = "spam"
    else:
        goto = "draft_response"

    # Store classification as a single dict in state
    return Command(
        update={"classification": classification},
        goto=goto
    )
