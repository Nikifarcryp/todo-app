from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, Response, status, Request
from typing import List, Dict
from models import Base
from schemas import TaskSet, TaskSchema
from database import get_session, engine
from crud import make_item, update_item, delete_item, get_item, get_items
from contextlib import asynccontextmanager


app = FastAPI()

ml_models = {}

async def run_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_models["run_databases"] = run_database
    yield
    ml_models.clear()


@app.post('/todos/create_task/', response_model=TaskSchema)
async def create_task(response: Response, task: TaskSet, db: AsyncSession = Depends(get_session)) -> TaskSchema:
    task_created = await make_item(db, task)
    response.status_code = status.HTTP_201_CREATED
    return task_created


@app.put('/todos/edit_task', response_model=TaskSchema)
async def edit_task(task: TaskSchema, task_id: int, db: AsyncSession = Depends(get_session)) -> TaskSchema:
    updated_task = await update_item(db, task_id, item=task)
    return updated_task


@app.get('/todos/get_tasks', response_model=List[TaskSchema])
async def get_tasks(db: AsyncSession = Depends(get_session)) -> [TaskSchema]:
    tasks = await get_items(db)
    return tasks


@app.get('/todos/get_task/{item_id}', response_model=TaskSchema)
async def get_task(item_id: int, db: AsyncSession = Depends(get_session)) -> TaskSchema:
    task = await get_item(db, item_id)
    return task


@app.delete('/todos/delete_task/{item_id}', response_model=TaskSchema)
async def delete_task(item_id: int, db: AsyncSession = Depends(get_session)) -> Dict:
    task = await delete_item(db, item_id)
    return {'Status': 'Deleted successfully', 'Deleted Task': task}