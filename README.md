# 📧 Agentic AI Email Automation System  
**Built with LangGraph + LangChain**

This project implements an **agentic AI workflow** to automate email handling and responses using **LangGraph** and **LangChain**.  
The system intelligently reads incoming emails, classifies their intent, drafts responses, and sends them — with optional human-in-loop review for critical messages.

---

## 🚀 Features

✅ Automated email reading  
✅ Intent classification (Spam / Bug / Normal / Human-critical)  
✅ AI-generated draft reply  
✅ Human Review loop for flagged emails  
✅ Autonomous reply sending for safe messages  
✅ Modular agent nodes (easily extendable)  
✅ Future scope: Telegram bot integration for human-in-loop alerts & approvals  

---

## 🧠 System Flow

### High-Level Pipeline

1. **Start**
2. **Read incoming mail**
3. **Classify intent**
   - Spam 🗑️
   - Normal query 💬
   - Human-required review 🧍‍♂️
4. **Draft AI reply**
5. **Review (Auto or Human)**
6. **Send reply or terminate**
7. **End**

---

## 🧩 Agent Nodes

The system uses multiple AI "agents" (LangGraph nodes):

| Agent | Responsibility |
|-------|----------------|
| 📥 Mail Reader | Fetches new emails |
| 🧠 Intent Classifier | Categorizes email intent |
| ✍️ Reply Generator | Drafts intelligent responses |
| 🧍 Human Review Agent | Approves / modifies critical replies |
| 📤 Auto-Send Agent | Sends final email |

## 📦 Tech Stack

| Tool | Purpose |
|------|--------|
| **LangChain** | LLM orchestration |
| **LangGraph** | Agent workflow graph |
| **LLM (OpenAI / Local)** | NLP + Response generation |
| **Python** | Backend logic |
| **Email IMAP/SMTP** | Mail reading & sending |
| **(Upcoming)** Telegram Bot | Notification & approvals |

## Streamlit App 
- inbox shows emails with clickable bubbles to select.
- mail content displays the selected email.
- send reply simulates sending the reply

## 🛠️ Installation

```bash
git clone https://github.com/your-username/agentic-email-ai.git
uv sync


