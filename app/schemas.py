from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskSet(TaskBase):
    pass


class TaskSchema(TaskBase):
    id: int
    completed: bool = False