# langchain-multi-agent-demo
We utilize LangChain detailing how it works and give an example multi-agent application.

## Core Idea
Build a multi agent system using LangGraph to fill out arbitrary forms given a bunch of information about the user.

UI Flow
1. Initial Prompt (Form link & User info)
2. Try to fill out form
3. If needed
   a. Ask for more info
4. Repeat 2-3 until done
