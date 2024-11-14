#.venv\Scripts\activate активация окружения
# uvicorn dz:app --reload запуск фаст апи
from fastapi import FastAPI, HTTPException, Path

from typing import Dict, Any, Tuple

app = FastAPI()

users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users", response_model=Dict[str, str])
async def get_users() -> Dict[str, str]:
    return users


@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int) -> str:
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    new_user_id = str(max(map(int, users.keys())) + 1) if users else '1'
    users[new_user_id] = f"Имя: {username}, возраст: {age}"
    return f"User  {new_user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str, username: str, age: int) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User  {user_id} has been updated"


@app.delete("/user/{user_id}")
async def delete_user(user_id: str) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    del users[user_id]
    return f"User  {user_id} has been deleted"
