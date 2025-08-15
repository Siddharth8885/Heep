from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Chat
from app.schemas import ChatIn
router = APIRouter(prefix="/chat", tags=["chat"])
@router.post("")
def send_message(payload: ChatIn, session: Session = Depends(get_session)):
    msg = Chat(**payload.dict()); session.add(msg); session.commit(); session.refresh(msg)
    return msg
@router.get("/{task_id}")
def list_messages(task_id: int, session: Session = Depends(get_session)):
    rows = session.exec(select(Chat).where(Chat.task_id==task_id).order_by(Chat.created_at.asc())).all()
    return [r.dict() for r in rows]
