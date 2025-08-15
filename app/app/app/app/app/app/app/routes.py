from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from .database import get_session
from .models import Item

router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    with get_session() as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@router.get("/items/")
def read_items():
    with get_session() as session:
        items = session.exec(select(Item)).all()
        return items

@router.get("/items/{item_id}")
def read_item(item_id: int):
    with get_session() as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
