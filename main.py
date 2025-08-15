from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import users, tasks, ratings, chat, admin
app = FastAPI(title="Heep API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(users.router); app.include_router(tasks.router); app.include_router(ratings.router); app.include_router(chat.router); app.include_router(admin.router)
@app.on_event("startup")
def on_startup(): init_db()
@app.get("/health")
def health(): return {"status": "ok"}
