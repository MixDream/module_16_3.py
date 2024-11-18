# .venv\Scripts\activate активация окружения
# uvicorn main:app --reload запуск фаст апи
from fastapi import FastAPI, HTTPException, Path
from typing import Dict
from pydantic import BaseModel, Field, conint, constr, field_validator

app = FastAPI()

users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}

class User(BaseModel):
    username: constr(min_length=1, max_length=50) = Field(..., description="Имя пользователя", examples=["UrbanUser "])
    age: conint(ge=0) = Field(..., description="Возраст пользователя", examples=[24])

    @field_validator('age')
    def age_must_be_positive(cls, value):
        if value < 0:
            raise ValueError("Возраст не может быть отрицательным")
        return value

@app.get("/users", response_model=Dict[str, str])
async def get_users() -> Dict[str, str]:
    return users

@app.post("/user")
async def create_user(user: User) -> str:
    new_user_id = str(max(map(int, users.keys())) + 1) if users else '1'
    users[new_user_id] = f"Имя: {user.username}, возраст: {user.age}"
    return f"User  {new_user_id} is registered"

@app.put("/user/{user_id}")
async def update_user(
    user: User,  
    user_id: int = Path(..., ge=1, le=100, description='Enter User ID', examples=[1])  
) -> str:
    user_id_str = str(user_id)
    if user_id_str not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    users[user_id_str] = f"Имя: {user.username}, возраст: {user.age}"
    return f"User  {user_id_str} has been updated"

@app.delete("/user/{user_id}")
async def delete_user(
    user_id: int = Path(..., ge=1, le=100, description='Enter User ID', examples=[1])  
) -> str:
    user_id_str = str(user_id)
    if user_id_str not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    del users[user_id_str]
    return f"User  {user_id_str} has been deleted"
