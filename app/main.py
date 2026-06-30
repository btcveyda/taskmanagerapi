from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="A simple REST API for managing daily tasks.",
)


class TaskBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="pending", pattern=r"^(pending|done)$")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, pattern=r"^(pending|done)$")


class Task(TaskBase):
    id: int


_tasks: dict[int, Task] = {}
_next_id = 1


def reset_store() -> None:
    global _tasks, _next_id
    _tasks = {}
    _next_id = 1


def _next_task_id() -> int:
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    task_id = _next_task_id()
    created_task = Task(id=task_id, **task.model_dump())
    _tasks[task_id] = created_task
    return created_task


@app.get("/tasks", response_model=List[Task])
def list_tasks(status: Optional[str] = Query(default=None, pattern=r"^(pending|done)$")) -> List[Task]:
    if status is None:
        return list(_tasks.values())
    return [task for task in _tasks.values() if task.status == status]


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_data = task.model_dump()
    update_data = task_update.model_dump(exclude_unset=True)
    updated_data.update(update_data)
    updated_task = Task(**updated_data)
    _tasks[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]
    return None
