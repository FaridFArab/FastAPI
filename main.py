from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from todo.views import todos_router

app = FastAPI()

app.include_router(todos_router,)


@app.get('/')
async def get_root():
    return {'Result': 'Value'}


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
