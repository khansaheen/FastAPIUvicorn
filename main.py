#In this Python tutorial you will learn about FastAPI, a Web framework for developing RESTful APIs in Python. FastAPI is based on Pydantic and type hints to validate, serialize, and deserialize data, and automatically auto-generate OpenAPI documents. It fully supports asynchronous programming and can run with Uvicorn and Gunicorn

from models import User, Gender, Role, UserUpdateRequest
from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID, uuid4
from enum import Enum


app = FastAPI()

db: List[User] = [
    User(
        id = uuid4(),
        first_name = "Shruti",
        last_name = "Sinha",
        gender = Gender.female,
        roles = [Role.student, Role.user]
    ),
    User(
        id = uuid4(),
        first_name = "Dimple",
        last_name = "Jain",
        gender = Gender.female,
        roles = [Role.student]
    )
]

@app.get("/")
async def root():
    return {"Hello" : "mu"}

@app.get("/api/users")
async def fetch_users():
    return db;

@app.post("/api/users")
async def regeister_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(status_code=404, detail = f"user with id: {user_id} does not exists")
            
@app.put("/api/users/{user_id}")
async def update_user(user_update: UserUpdateRequest,user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(status_code=404, detail = f"user with id: {user_id} does not exists")