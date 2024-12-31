from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from typing import List, Dict
from app.models import Base
from app.schemas import TaskSet, TaskSchema
from app.database import get_session, engine
from app.crud import make_item, update_item, delete_item, get_item, get_items


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post('/todos/create_task', response_model=TaskSchema)
async def create_task(task: TaskSet, db: AsyncSession = Depends(get_session)) -> TaskSchema:
    task_created = await make_item(db, task)
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