import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from tasks import models, schemas

router = APIRouter(
    prefix='/tasks',
    tags=['Task']
)


def get_task_by_id(task_id: int, db: Session):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task with id %d not found" % task_id)
    return task


@router.get("/", response_model=list[schemas.Task])
async def get_tasks_list(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(models.Task).offset(offset).limit(limit).all()


@router.get("/{task_id}", response_model=schemas.Task)
async def get_task_info(task_id: int, db: Session = Depends(get_db)):
    return get_task_by_id(task_id, db)


@router.post("/", status_code=201, response_model=schemas.Task)
async def append_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title, text=task.text)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.patch("/{task_id}/complete")
async def mark_completed(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(task_id, db)
    if task.completed:
        raise HTTPException(409, "Task with id %d already completed" % task_id)
    task.completed = True
    task.completed_at = datetime.date.today()
    db.commit()
    db.refresh(task)
    return {'status': 200}


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(task_id, db)
    db.delete(task)
    db.commit()
    return {'status': 200}
