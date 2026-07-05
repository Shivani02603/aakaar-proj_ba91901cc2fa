"""Pydantic schemas — STAMPED from the build contract. Do not hand-edit;
these mirror database/models.py and frontend/src/types.ts exactly."""

from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    token: str


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    token: str
    expires_at: str
    created_at: str


class ChatHistoryCreate(BaseModel):
    session_id: str
    question: str
    answer: str
    source_chunk_ids: str


class ChatHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    session_id: str
    question: str
    answer: str
    source_chunk_ids: str
    asked_at: str
