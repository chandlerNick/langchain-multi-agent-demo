# Reads and parses incoming emails
from langchain_core.messages import HumanMessage
from agentstructure.state import EmailAgentState

def read_email(state: EmailAgentState) -> dict:
    """Extract and parse email content"""
    # In production, this would connect to your email service
    return {
        "messages": [HumanMessage(content=f"Processing email: {state['email_content']}")]
    }
