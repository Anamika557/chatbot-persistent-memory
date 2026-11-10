import streamlit as st

from app.database import SessionLocal
from app.models import ChatSession
from app.chat import (
    create_chat,
    get_chat_history,
    send_message,
    summarize_chat
)

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬"
)

st.title("AI Chatbot with Persistent Memory")

# System Prompt
system_prompt = st.sidebar.text_area(
    "Customize AI Behaviour",
    value="You are a helpful AI assistant. Answer clearly and simply."
)

db = SessionLocal()

try:
    st.sidebar.title("Chat History")

    if st.sidebar.button("➕ New Chat"):
        chat = create_chat(db)
        st.session_state.chat_id = chat.id
        st.rerun()

    sessions = (
        db.query(ChatSession)
        .order_by(ChatSession.created_at.desc())
        .all()
    )

    for chat in sessions:
        if st.sidebar.button(chat.title, key=f"chat_{chat.id}"):
            st.session_state.chat_id = chat.id
            st.rerun()

    # Select current chat
    if "chat_id" not in st.session_state:
        if sessions:
            st.session_state.chat_id = sessions[0].id
        else:
            chat = create_chat(db)
            st.session_state.chat_id = chat.id

    chat_id = st.session_state.chat_id

    # Display conversation
    history = get_chat_history(db, chat_id)

    for message in history:
        with st.chat_message(message.role):
            st.write(message.content)

    # Summarize Chat button
    if history:
        if st.button("Summarize Chat"):
            with st.spinner("Generating summary..."):
                try:
                    summary = summarize_chat(db, chat_id)

                    st.subheader("Conversation Summary")
                    st.write("**Title:**", summary.title)
                    st.write("**Summary:**", summary.summary)
                    st.write("**Action Items:**")

                    for item in summary.action_items:
                        st.write(f"- {item}")

                except Exception as e:
                    st.error(f"Summary failed: {e}")

    # User input
    prompt = st.chat_input("Type your message...")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            response_area = st.empty()
            full_response = ""

            for chunk in send_message(
                db,
                chat_id,
                prompt,
                system_prompt
            ):
                full_response += chunk
                response_area.markdown(full_response)

finally:
    db.close()