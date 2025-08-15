from fastapi import FastAPI
from .database import create_db_and_tables
from .models import Item
from sqlmodel import Session, select
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with Session(create_db_and_tables.engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(create_db_and_tables.engine) as session:
        items = session.exec(select(Item)).all()
        return items
