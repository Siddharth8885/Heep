from typing import Optional
from datetime import datetime
from pydantic import BaseModel
class UserCreate(BaseModel):
  phone: str; name: Optional[str] = None; role: str = "helper"
class UserRead(BaseModel):
  id: int; phone: str; name: Optional[str]; role: str; trust_score: float
  class Config: from_attributes = True
class TaskCreate(BaseModel):
  title: str; description: str; lat: float; lng: float; deadline: datetime; budget: int; urgent: bool = False; requester_id: int
class TaskRead(BaseModel):
  id: int; title: str; description: str; lat: float; lng: float; deadline: datetime; budget: int; urgent: bool; status: str; requester_id: int; helper_id: Optional[int]
  class Config: from_attributes = True
class AcceptTask(BaseModel):
  helper_id: int; countdown_minutes: int = 15
class EarlyProofIn(BaseModel):
  photo_url: Optional[str] = None; video_url: Optional[str] = None; document_url: Optional[str] = None; gps_lat: Optional[float] = None; gps_lng: Optional[float] = None
class FinalProofIn(EarlyProofIn): pass
class RatingIn(BaseModel):
  task_id: int; helper_id: int; requester_id: int; timeliness: int; quality: int; communication: int; reliability: int; comment: Optional[str] = None
class ChatIn(BaseModel):
  task_id: int; sender_id: int; message: str
