from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Task
from schemas import TaskSet
from fastapi import HTTPException, status


async def make_item(db: AsyncSession, item: TaskSet):
    task = Task(title=item.title, description=item.description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_items(db: AsyncSession):
    try:
        result = await db.execute(select(Task))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=e)


async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(Task).filter(Task.id == item_id))
    return result.scalar_one_or_none()


async def update_item(db: AsyncSession, item_id: int, item: TaskSet):
    try:
        result = await db.execute(select(Task).filter(Task.id == item_id))
        db_item = result.scalar_one_or_none()
        db_item.title = item.title
        db_item.description = item.description
        db_item.completed = item.completed
        await db.commit()
        await db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


async def delete_item(db: AsyncSession, item_id: int):
    try:
        result = await db.execute(select(Task).filter(Task.id == item_id))
        db_item = result.scalar_one_or_none()
        await db.delete(db_item)
        await db.commit()
        return db_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)