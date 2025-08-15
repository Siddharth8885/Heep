from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task, User, Proof, Transaction, Wallet
from app.schemas import TaskCreate, TaskRead, AcceptTask, EarlyProofIn, FinalProofIn
from app.utils import haversine_km

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskRead)
def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    requester = session.get(User, payload.requester_id)
    if not requester: raise HTTPException(404, "Requester not found")
    task = Task(title=payload.title, description=payload.description, lat=payload.lat, lng=payload.lng, deadline=payload.deadline, budget=payload.budget, urgent=payload.urgent, requester_id=requester.id, escrow_status="funded", status="open")
    session.add(task); session.commit(); session.refresh(task)
    return task

@router.get("/available", response_model=List[TaskRead])
def available_tasks(lat: float, lng: float, radius_km: float = 25.0, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.status == "open")).all()
    return [t for t in tasks if haversine_km(lat, lng, t.lat, t.lng) <= radius_km]

@router.post("/{task_id}/accept", response_model=TaskRead)
def accept_task(task_id: int, payload: AcceptTask, session: Session = Depends(get_session)):
    task = session.get(Task, task_id); helper = session.get(User, payload.helper_id)
    if not task or not helper: raise HTTPException(404, "Task or helper not found")
    if task.status != "open": raise HTTPException(409, "Task not open")
    task.helper_id = helper.id; task.accepted_at = datetime.utcnow()
    task.early_proof_due_at = task.accepted_at + timedelta(minutes=payload.countdown_minutes); task.status = "accepted"
    session.add(task); session.commit(); session.refresh(task); return task

@router.post("/{task_id}/early-proof")
def submit_early_proof(task_id: int, payload: EarlyProofIn, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task: raise HTTPException(404, "Task not found")
    if task.status not in ("accepted","in_progress"): raise HTTPException(409, "Task not in acceptable state")
    if datetime.utcnow() > (task.early_proof_due_at or datetime.utcnow()):
        task.status = "reopened"; task.helper_id = None; session.commit(); raise HTTPException(410, "Early proof window expired; task reopened")
    proof = Proof(task_id=task.id, type="early", **payload.dict()); session.add(proof)
    task.status = "awaiting_requester_confirm"; session.commit(); return {"ok": True}

@router.post("/{task_id}/confirm-start")
def requester_confirm_start(task_id: int, approve: bool = True, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task: raise HTTPException(404, "Task not found")
    if task.status != "awaiting_requester_confirm": raise HTTPException(409, "Not awaiting confirmation")
    if approve:
        task.requester_start_confirmed = True; task.status = "in_progress"
    else:
        if task.helper_id:
            wallet = session.exec(select(Wallet).where(Wallet.user_id == task.helper_id)).first()
            if wallet:
                wallet.balance = max(0, wallet.balance - 100)
                session.add(Transaction(user_id=task.helper_id, task_id=task.id, amount=-100, type="penalty"))
        task.status = "reopened"; task.helper_id = None
    session.commit(); return {"ok": True, "status": task.status}

@router.post("/{task_id}/final-proof")
def submit_final_proof(task_id: int, payload: FinalProofIn, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task: raise HTTPException(404, "Task not found")
    proof = Proof(task_id=task.id, type="final", **payload.dict()); session.add(proof)
    task.final_proof_submitted_at = datetime.utcnow(); task.status = "completed"; session.commit(); return {"ok": True}

@router.post("/{task_id}/confirm-completion")
def requester_confirm_completion(task_id: int, approve: bool = True, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task: raise HTTPException(404, "Task not found")
    if not approve: task.status = "disputed"; session.commit(); return {"ok": True, "status": task.status}
    if task.helper_id:
        wallet = session.exec(select(Wallet).where(Wallet.user_id == task.helper_id)).first()
        if wallet:
            wallet.balance += task.budget
            session.add(Transaction(user_id=task.helper_id, task_id=task.id, amount=task.budget, type="escrow_release"))
    task.escrow_status = "released"; task.requester_completion_confirmed = True; session.commit(); return {"ok": True, "wallet_credit": task.budget}
