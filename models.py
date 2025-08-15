from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str; name: Optional[str] = None; role: str = "helper"
    trust_score: float = 0.0; created_at: datetime = Field(default_factory=datetime.utcnow)
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str; description: str; lat: float; lng: float; deadline: datetime; budget: int; urgent: bool = False
    escrow_status: str = "funded"; status: str = "open"; created_at: datetime = Field(default_factory=datetime.utcnow)
    requester_id: int = Field(foreign_key="user.id"); helper_id: Optional[int] = Field(default=None, foreign_key="user.id")
    accepted_at: Optional[datetime] = None; early_proof_due_at: Optional[datetime] = None
    requester_start_confirmed: bool = False; final_proof_submitted_at: Optional[datetime] = None
    requester_completion_confirmed: bool = False
class Proof(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id"); type: str
    photo_url: Optional[str] = None; video_url: Optional[str] = None; document_url: Optional[str] = None
    gps_lat: Optional[float] = None; gps_lng: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
class Wallet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id"); balance: int = 0
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id"); task_id: Optional[int] = None
    amount: int; type: str; created_at: datetime = Field(default_factory=datetime.utcnow); meta: Optional[str] = None
class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id"); helper_id: int = Field(foreign_key="user.id")
    requester_id: int = Field(foreign_key="user.id")
    timeliness: int; quality: int; communication: int; reliability: int
    comment: Optional[str] = None; created_at: datetime = Field(default_factory=datetime.utcnow)
class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id"); sender_id: int = Field(foreign_key="user.id")
    message: str; created_at: datetime = Field(default_factory=datetime.utcnow)
