import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    text: str
    deadline: datetime.date | None


class Task(TaskCreate):
    id: int
    completed: bool
