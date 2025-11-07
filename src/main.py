# Entry point for the Agentic AI Email Automation system
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from agentstructure.workflow_graph import build_workflow

app = build_workflow()  # Add this if you want a checkpointer: checkpointer=MemorySaver()

# Create FastAPI app to expose endpoints (/invoke, /stream, /resume, /docs)
fastapi_app = FastAPI(title="LangGraph Email Agent")

class InvokeInput(BaseModel):
    email_content: str
    sender_email: str
    email_id: str

@fastapi_app.post("/invoke")
def invoke_graph(data: InvokeInput):
    """Run the entire LangGraph workflow once."""
    input_state = {
        "email_content": data.email_content,
        "sender_email": data.sender_email,
        "email_id": data.email_id,
    }
    result = app.invoke(input_state)
    return result

@fastapi_app.post("/stream")
def stream_graph(data: InvokeInput):
    """Stream node events as Server-Sent Events (for debugging)."""
    input_state = {
        "email_content": data.email_content,
        "sender_email": data.sender_email,
        "email_id": data.email_id,
    }
    events = []
    for event in app.stream(input_state):
        events.append(event)
    return {"events": events}


# If run directly, note that the uvicorn app should be used. We can put this in a module perhaps for deployment.
if __name__ == "__main__":
    print("Usage: uv run uvicorn main:fastapi_app --reload --port 4000")
