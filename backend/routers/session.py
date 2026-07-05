from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as DBSession
from typing import List, Optional
from uuid import UUID

from database.config import get_db
from database.models import Session, User
from backend.schemas import SessionCreate, SessionResponse
from backend.routers.auth import get_current_user

router = APIRouter(tags=["Session"])

@router.post("/sessions", status_code=201, response_model=SessionResponse)
def create_session(data: SessionCreate, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    new_session = Session(**data.model_dump(), user_id=user.id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/sessions", response_model=List[SessionResponse])
def list_sessions(
    db: DBSession = Depends(get_db),
    user: User = Depends(get_current_user),
    token: Optional[str] = Query(None)
):
    query = db.query(Session).filter(Session.user_id == user.id)
    if token:
        query = query.filter(Session.token == token)
    return query.all()

@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: UUID, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/sessions/{session_id}", response_model=SessionResponse)
def update_session(session_id: UUID, data: SessionCreate, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    for key, value in data.model_dump().items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: UUID, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(Session).filter(Session.id == session_id, Session.user_id == user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"status": "deleted"}