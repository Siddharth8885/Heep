from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Rating, User
from app.schemas import RatingIn
router = APIRouter(prefix="/ratings", tags=["ratings"])
@router.post("")
def create_rating(payload: RatingIn, session: Session = Depends(get_session)):
    r = Rating(**payload.dict()); session.add(r); session.commit()
    ratings = session.exec(select(Rating).where(Rating.helper_id==payload.helper_id)).all()
    if ratings:
        avg = sum((x.timeliness+x.quality+x.communication+x.reliability)/4 for x in ratings)/len(ratings)
        u = session.get(User, payload.helper_id)
        if u: u.trust_score = round(avg,2); session.add(u); session.commit()
    return {"ok": True}
