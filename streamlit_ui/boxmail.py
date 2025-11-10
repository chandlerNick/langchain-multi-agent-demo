import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Mini Mailbox", layout="wide")

# --- Load emails ---
DB_PATH = Path(__file__).parent / "db_inbox/mail_inbox.json"
with open(DB_PATH, "r", encoding="utf-8") as f:
    MAILS = json.load(f)

# --- Session state initialization ---
if "selected_mail_index" not in st.session_state:
    st.session_state.selected_mail_index = None
if "show_reply" not in st.session_state:
    st.session_state.show_reply = False
if "reply_text" not in st.session_state:
    st.session_state.reply_text = ""

st.title("Mini Mailbox")
# --- Always create three columns ---
col_inbox, col_mail_read, col_mail_answer = st.columns([1, 2, 2])

# ------------------- INBOX COLUMN -------------------
with col_inbox:
    st.header("Inbox")
    max_display = 5
    for i, mail in enumerate(MAILS[:max_display]):
        cols = st.columns([0.1, 0.9])
        with cols[0]:
            if st.button("●", key=f"select_{i}"):
                st.session_state.selected_mail_index = i
                st.session_state.show_reply = False  # reset reply when selecting new mail
        with cols[1]:
            st.markdown(f"**{mail['from']}**  \n{mail['subject']}")
            st.markdown("---")

# ------------------- MAIL CONTENT COLUMN -------------------
with col_mail_read:
    st.header("Email content")
    
    idx = st.session_state.selected_mail_index
    if idx is not None:
        selected_mail = MAILS[idx]
        st.text_area("From", value=selected_mail["from"], height=30, disabled=True)
        st.text_area("To", value=selected_mail["to"], height=30, disabled=True)
        st.text_area("Subject", value=selected_mail["subject"], height=30, disabled=True)
        st.text_area("Body", value=selected_mail["body"], height=200, disabled=True)
        
        # Show "Answer" button only if reply column is not visible
        if not st.session_state.show_reply:
            if st.button("Answer"):
                st.session_state.show_reply = True
    else:
        st.info("Select a mail to see full content.")

# ------------------- REPLY COLUMN -------------------
with col_mail_answer:
    if st.session_state.show_reply and idx is not None:
        st.header("Write your answer")
        default_reply = f"Hi {selected_mail['from'].split('@')[0]},\n\n"
        st.session_state.reply_text = st.text_area(
            "Your reply",
            value=st.session_state.get("reply_text", default_reply),
            height=300
        )
        if st.button("Send reply"):
            st.success(f"Reply sent to {selected_mail['from']} (simulation).")
            st.session_state.reply_text = ""
            st.session_state.show_reply = False  # collapse reply column after sending
