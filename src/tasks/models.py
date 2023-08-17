from sqlalchemy import Boolean, Column, Integer, String, Date
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), nullable=False, index=True)
    text = Column(String(1024), nullable=False)
    deadline = Column(Date, nullable=True, index=True)
    completed = Column(Boolean, default=False, nullable=False)
