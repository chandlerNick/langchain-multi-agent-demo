📧 Agent Mail Interface (Streamlit)

This folder contains the Streamlit front-end for the LangGraph multi-agent system. It lets you simulate incoming emails, visualize agent reasoning (classification), and review or approve drafted responses.

🏗 Architecture

This UI acts as the client in a microservices setup:

- Frontend (this app): runs on port 8501 and sends JSON payloads to the agent.
- Backend (Agent): expected to be available at http://127.0.0.1:4000.
- LLM (cluster): typically connected via a tunnel on port 8000.

## Getting started

Prerequisites:

- Python 3.10+
- A package manager (e.g., `uv` if you use it here, or `pip`)

Important: the multi-agent backend must be running and reachable on port 4000 for this UI to function.

### Installation

From the project root, change to this directory and install required dependencies:

```powershell
cd streamlit_ui
# Example using the uv package manager if available
uv add streamlit pandas requests

# Alternatively (if you don't have `uv`) install via pip from the project requirements
pip install -r ../requirements.txt
```
### Backend preparation 
For LLM connection and backend configuration, see `src/multi-agent-system/README.md`.

### Run the app

To start the dashboard run:

```powershell
streamlit run boxmail_using_agent_structure.py
```

This will open your default browser at http://localhost:8501.

### 📖 Usage guide

Incoming Email section:

- Sender Email: simulate who sent the message (e.g. customer@example.com).
- Email Content: paste the email text you want the agent to process.
- Send to Agent: click the button to send the request to your FastAPI backend.

Review Response section:

- Classification: shows how the agent categorized the email (e.g. "Complaint", "Billing") and the confidence score.
- AI Advice: if the agent detects a critical issue, an alert or recommendation is shown.
- Draft Response: the proposed reply — you can edit this before performing the simulated "send".

🔧 Troubleshooting

❌ Connection Failed

Cause: the Streamlit app cannot reach the Agent API.

Fix: make sure the Agent backend is running:

```powershell
# from src/multi-agent-system
uv run uvicorn main:fastapi_app --reload --port 4000
```

Agent Error: 500 Internal Server Error

Cause: the Agent (port 4000) crashed, often because it cannot communicate with the LLM (port 8000).

Fix: ensure your Kubernetes tunnel or LLM connection is active from the project root:

```powershell
make deploy
# or check that a kubectl port-forward is running
```

JSONDecodeError

Cause: the Agent returned a non-JSON response (usually an HTML error page).

Fix: check the debug output in the Streamlit UI and the Agent process logs for details.