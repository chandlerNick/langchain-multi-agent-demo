# Multi Agent System

This directory holds the agent build, it should be run in its own pod eventually.

It is intended to have a simple json input/output interface that allows it to be connected to various mail services.

To run (currently):
0. Ensure `uv` is properly configured for your machine.
1. In root of this git repo run `make deploy`, ensure the llm is up on port 8000 (terminal 1)
2. In `src/multi-agent-system` (this dir) run `uv run uvicorn main:fastapi_app --reload --port 4000` (terminal 2)
3. Test with something like `curl -X POST http://127.0.0.1:4000/invoke   -H "Content-Type: application/json"   -d '{"email_content": "Your invoice seems wrong, please fix it.", "sender_email": "customer@example.com", "email_id": "1"}'
`
4. Eventually, hook up to streamlit frontend & deploy said frontend.