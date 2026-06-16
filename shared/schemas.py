from pydantic import BaseModel
from typing import Optional, List


class TaskSchema(BaseModel):
    id: int
    title: str
    status: str = "pending"
    user_id: str = "default"


class MemorySchema(BaseModel):
    id: int
    content: str
    tags: str = ""
    user_id: str = "default"


class EventSchema(BaseModel):
    type: str
    payload: dict
    ts: str
