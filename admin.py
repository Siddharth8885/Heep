from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Task
router = APIRouter(prefix="/admin", tags=["admin"])
@router.get("/users")
def users(session: Session = Depends(get_session)):
    return [u.dict() for u in session.exec(select(User)).all()]
@router.get("/tasks")
def tasks(session: Session = Depends(get_session)):
    return [t.dict() for t in session.exec(select(Task)).all()]
@router.post("/tasks/{task_id}/dispute")
def mark_dispute(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id); 
    if not task: return {"ok": False, "error":"not found"}
    task.status = "disputed"; session.commit(); return {"ok": True}
