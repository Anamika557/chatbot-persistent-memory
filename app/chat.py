from sqlalchemy.orm import Session

from app.models import ChatSession, Message
from app.llm import stream_response, generate_summary
from app.schemas import ConversationSummary


# Create a new chat
def create_chat(db: Session):
    chat = ChatSession(title="New Chat")

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


# Retrieve chat history
def get_chat_history(db: Session, session_id: int):
    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at)
        .all()
    )


# Send a message and generate AI response
def send_message(
    db: Session,
    session_id: int,
    user_message: str,
    system_prompt: str
):
    # Save user message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=user_message
    )

    db.add(user_msg)

    # Automatically update the chat title
    chat = db.query(ChatSession).filter(
        ChatSession.id == session_id
    ).first()

    if chat and chat.title == "New Chat":
        chat.title = (
            user_message[:40] + "..."
            if len(user_message) > 40
            else user_message
        )

    db.commit()

    # Retrieve conversation history
    history = get_chat_history(db, session_id)

    conversation = "\n".join(
        f"{msg.role}: {msg.content}"
        for msg in history
    )

    # Track token usage
    usage = {
        "input_tokens": 0,
        "output_tokens": 0
    }

    # Generate streaming response
    full_response = ""

    for chunk in stream_response(
        conversation,
        system_prompt,
        usage
    ):
        full_response += chunk
        yield chunk

    # Save AI response and token usage
    ai_msg = Message(
        session_id=session_id,
        role="assistant",
        content=full_response,
        input_tokens=usage["input_tokens"],
        output_tokens=usage["output_tokens"]
    )

    db.add(ai_msg)
    db.commit()


# Summarize conversation
def summarize_chat(db: Session, session_id: int):

    history = get_chat_history(db, session_id)

    if not history:
        raise ValueError("No messages available to summarize.")

    conversation = "\n".join(
        f"{msg.role}: {msg.content}"
        for msg in history
    )

    summary_json = generate_summary(conversation)

    # Validate JSON using Pydantic
    validated_summary = ConversationSummary.model_validate_json(
        summary_json
    )

    return validated_summary