from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.config import get_db
from database.models import ChatHistory, User
from backend.schemas import ChatHistoryCreate, ChatHistoryResponse
from backend.routers.auth import get_current_user

router = APIRouter(tags=["ChatHistory"])

@router.post("/chat_history", status_code=201, response_model=ChatHistoryResponse)
def create_chat_history(
    data: ChatHistoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_chat_history = ChatHistory(**data.model_dump(), user_id=user.id)
    db.add(new_chat_history)
    db.commit()
    db.refresh(new_chat_history)
    return new_chat_history

@router.get("/chat_history", response_model=List[ChatHistoryResponse])
def list_chat_histories(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    session_id: Optional[UUID] = Query(None),
):
    query = db.query(ChatHistory).filter(ChatHistory.user_id == user.id)
    if session_id:
        query = query.filter(ChatHistory.session_id == session_id)
    return query.all()

@router.get("/chat_history/{id}", response_model=ChatHistoryResponse)
def get_chat_history(
    id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chat_history = db.query(ChatHistory).filter(
        ChatHistory.id == id, ChatHistory.user_id == user.id
    ).first()
    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return chat_history

@router.put("/chat_history/{id}", response_model=ChatHistoryResponse)
def update_chat_history(
    id: UUID,
    data: ChatHistoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chat_history = db.query(ChatHistory).filter(
        ChatHistory.id == id, ChatHistory.user_id == user.id
    ).first()
    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    for key, value in data.model_dump().items():
        setattr(chat_history, key, value)
    db.commit()
    db.refresh(chat_history)
    return chat_history

@router.delete("/chat_history/{id}")
def delete_chat_history(
    id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chat_history = db.query(ChatHistory).filter(
        ChatHistory.id == id, ChatHistory.user_id == user.id
    ).first()
    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    db.delete(chat_history)
    db.commit()
    return {"status": "deleted"}