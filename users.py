from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Wallet, Rating, Transaction
from app.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    user = User(phone=payload.phone, name=payload.name, role=payload.role)
    session.add(user); session.commit(); session.refresh(user)
    wallet = Wallet(user_id=user.id, balance=0); session.add(wallet); session.commit()
    return user

@router.get("/{user_id}/wallet")
def wallet(user_id: int, session: Session = Depends(get_session)):
    w = session.exec(select(Wallet).where(Wallet.user_id==user_id)).first()
    tx = session.exec(select(Transaction).where(Transaction.user_id==user_id).order_by(Transaction.created_at.desc())).all()
    return {"balance": w.balance if w else 0, "transactions": [t.dict() for t in tx]}

@router.get("/{user_id}/trust")
def trust(user_id: int, session: Session = Depends(get_session)):
    rs = session.exec(select(Rating).where(Rating.helper_id==user_id)).all()
    if not rs: return {"trust_score": 0.0}
    avg = sum((r.timeliness+r.quality+r.communication+r.reliability)/4 for r in rs)/len(rs)
    u = session.get(User, user_id); 
    if u: u.trust_score = round(avg, 2); session.add(u); session.commit()
    return {"trust_score": round(avg,2)}
