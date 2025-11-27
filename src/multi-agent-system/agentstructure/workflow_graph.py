# Defines LangGraph workflow for the full agent chain
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from agentstructure.state import EmailAgentState

# Import your agents
from agents.read_mail_agent import read_email
from agents.intent_classifier_agent import classify_intent
from agents.draft_reply_agent import draft_response, send_reply
from agents.human_review_agent import human_review
from agents.spam_agent import spam

def route_intent(state: EmailAgentState):
    """
    Conditional logic to determine the next node based on classification.
    """
    classification = state.get("classification")
    
    if not classification:
        return "draft_response" 

    intent = classification.get("intent")
    
    if intent == "spam":
        return "spam"
    else:
        return "draft_response"

def build_workflow(checkpointer=None):
    # --- Define workflow ---
    workflow = StateGraph(EmailAgentState)

    # Add Nodes
    workflow.add_node("read_email", read_email)
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("draft_response", draft_response)
    # The 'human_review' node stays, but it will act as an automated step 
    # (e.g., a second LLM check) rather than a pause for a real human.
    workflow.add_node("human_review", human_review)
    workflow.add_node("send_reply", send_reply)
    workflow.add_node("spam", spam)

    # --- Define Edges ---

    # 1. Start sequence
    workflow.add_edge(START, "read_email")
    workflow.add_edge("read_email", "classify_intent")

    # 2. Branching logic
    workflow.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "spam": "spam",
            "draft_response": "draft_response"
        }
    )

    # 3. Standard response flow (Fully Automated)
    workflow.add_edge("draft_response", "human_review")
    workflow.add_edge("human_review", "send_reply")
    workflow.add_edge("send_reply", END)

    # 4. Spam flow
    workflow.add_edge("spam", END)

    # --- Compile ---
    app = workflow.compile(checkpointer=checkpointer)
    
    return app