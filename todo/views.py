from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from todo.models import Todo, Todo_Pydantic, TodoIn_Pydantic

todos_router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@todos_router.post('/', response_model=Todo_Pydantic)
async def create_todo(todo: TodoIn_Pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)


@todos_router.put('/{todo_id}', response_model=Todo_Pydantic, responses={404:{'model': HTTPNotFoundError}})
async def update_todo(todo_id: int, todo: TodoIn_Pydantic):
    await Todo.filter(id=todo_id).update(**todo.dict(exclude={"id"}, exclude_unset=True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))


@todos_router.delete('/{todo_id}', response_model=Status, responses={404:{'model': HTTPNotFoundError}})
async def delete_todo(todo_id: int):
    delete_count = await Todo.filter(id=todo_id).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return Status(message=f"Deleted todo {todo_id}")


@todos_router.get('/', response_model=List[Todo_Pydantic])
async def get_todos():
    return await Todo_Pydantic.from_queryset(Todo.all())


@todos_router.get('/{todo_id}', response_model=Todo_Pydantic, responses={404:{'model': HTTPNotFoundError}})
async def get_todo(todo_id:int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))