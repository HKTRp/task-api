import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    text: str


class Task(TaskCreate):
    id: int
    completed_at: datetime.date | None
    completed: bool
