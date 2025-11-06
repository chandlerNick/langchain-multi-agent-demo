from langgraph.types import Command
from agentstructure.state import EmailAgentState
import logging

logger = logging.getLogger(__name__)

def spam(state: EmailAgentState) -> Command[None]:
    """
    Handle spam emails by logging them and terminating the workflow branch.
    """
    email_id = state.get("email_id", "unknown")
    sender = state.get("sender_email", "unknown")
    logger.info(f"[SPAM] Email {email_id} from {sender} flagged as spam. Content ignored.")
    
    # Optionally, you could store in state for recordkeeping:
    # state.setdefault("spam_emails", []).append(state["email_content"])

    # Terminate workflow branch
    return Command(goto="END")