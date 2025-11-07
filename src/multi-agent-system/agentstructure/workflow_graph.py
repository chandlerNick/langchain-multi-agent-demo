# Defines LangGraph workflow for the full agent chain
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from agentstructure.state import EmailAgentState
from agents.read_mail_agent import read_email
from agents.intent_classifier_agent import classify_intent
from agents.draft_reply_agent import draft_response, send_reply
from agents.human_review_agent import human_review
from agents.spam_agent import spam

def build_workflow(checkpointer=None):
    # --- Define workflow ---
    workflow = StateGraph(EmailAgentState)
    workflow.add_node("read_email", read_email)
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("draft_response", draft_response)
    workflow.add_node("human_review", human_review)
    workflow.add_node("send_reply", send_reply)
    workflow.add_node("spam", spam)

    workflow.add_edge(START, "read_email")
    workflow.add_edge("read_email", "classify_intent")
    workflow.add_edge("classify_intent", "draft_response")
    workflow.add_edge("draft_response", "human_review")
    workflow.add_edge("human_review", "send_reply")
    workflow.add_edge("send_reply", END)

    # end at spam too
    workflow.add_edge("classify_intent", "spam")
    workflow.add_edge("spam", END)

    # --- Compile + serve ---
    app = workflow.compile(checkpointer=checkpointer)
    return app