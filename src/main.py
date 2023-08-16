from fastapi import FastAPI
from tasks.router import router as tasks_router
from tasks import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tasks app")


app.include_router(tasks_router, prefix='/api/v1.0')
