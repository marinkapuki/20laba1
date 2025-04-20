from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Модель данных
class User(BaseModel):
    id: int
    name: str
    age: int

# Имитация базы данных
fake_db = {}

# Конечная точка для создания пользователя
@app.post("/users/", response_model=User)
async def create_user(user: User):
    if user.id in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_db[user.id] = user
    return user

# Конечная точка для получения пользователя
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = fake_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
