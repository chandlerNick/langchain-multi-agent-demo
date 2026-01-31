# Agentic AI Email Automation System  
**Built with LangGraph**

This project implements an **agentic AI workflow** to automate email handling and responses using **LangGraph**.  
The system intelligently reads incoming emails, classifies their intent, drafts responses, and sends them - with optional human-in-loop review for critical messages.

It utilizes GPT-OSS-120B as the underlying LLM which we deploy on the BHT compute cluster's Nvidia A100 80GB GPUs.

## Further details

For a quick overview of the project (including photos of UI), look at Agentic_Email_Automation_Presentation.pdf

If you want to replicate the workflow (and have sufficient resources) examine the directories `src/multi-agent-system` and `src/streamlit_ui` as well as the `.env.example` and `Makefile`.

Note that the system primarily follows this [tutorial](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) with some modifications and plumbing / ops done to serve the LLM, create a front end, and wrap the agent in a service.
