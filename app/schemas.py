from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    role: str
    content: str


class MessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    input_tokens: int
    output_tokens: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationSummary(BaseModel):
    title: str
    summary: str
    action_items: list[str]