from os import remove
from uuid import UUID,uuid4
import uuid
from fastapi import FastAPI,status,HTTPException
from typing import List
from models import Gender, User,Role,UserUpdateRequest


app = FastAPI()

db:List[User]=[
    User(
        id=UUID("3a70e112-f093-4845-960d-b66d1a1417c8"),
        first_name="jamil",
        last_name="Ahmed",
        gender=Gender.male,
        roles=[Role.student]
        ), 
     User(
        id=UUID("76218d8f-4b20-46d8-98df-6da6cac36dd1"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.student,Role.admin]
        )    
]

@app.get("/",status_code=status.HTTP_200_OK)
def root():
    return{
        "Hello":"Mundo" 
        }

@app.get("/api/v1/users")
def fetch_users():
    return db 

@app.post("/api/v1/users")
def new_user(user:User):
    db.append(user)
    return {"id":user.id}

@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id:UUID):
    for user in db:
        if user.id==user_id:
            db.remove(user)
            return {user_id:" user deleted"}
    raise HTTPException(
        status_code=404,
        detail=f'user whit id:{user_id} does not exists'
    )

@app.put("/api/v1/users/{user_id}")
def update_user(
    user_update:UserUpdateRequest, 
    user_id:UUID
    ):
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
            return {user_id:"has been updated"}
    raise HTTPException(
        status_code=404,
        detail=f'user whit id:{user_id} does not exists'

    )
