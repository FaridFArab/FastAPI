from fastapi import FastAPI
import uvicorn
from todo.models import Todo, Todo_Pydantic, TodoIn_Pydantic
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


@app.get('/')
async def get_root():
    return {'Result': 'Value'}


@app.post('/todos', response_model=Todo_Pydantic)
async def create_todo(todo: TodoIn_Pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)


class Status(BaseModel):
    message: str


register_tortoise(
    app,
    db_url="postgres://postgres:10484617@localhost:5432/FastTodo",
    modules={'models': ["todo.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


def main():
    uvicorn.run(app, port=8000, host='localhost')


if __name__ == '__main__':
    main()
