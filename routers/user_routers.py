from fastapi import APIRouter, HTTPException, Depends
from db.models.user_model import User
from db.schemas.user_schema import user_schema, users_schema
from db.db_connection import db_connection
from bson import ObjectId

router = APIRouter(prefix="/api",
                   tags=["Users"],
                   responses={404: {"message": "User not found"}})

def find_user(field: str, key):
    try:
        user = db_connection.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error": "User not found"}
    
def find_user_by_username(username: str):
    try:
        user = db_connection.users.find_one({"username": username})
        return User(**user_schema(user))
    except:
        raise HTTPException(status_code=404, detail={"Error": "User not found"})

@router.get("/users", status_code=200)
async def get_all_users():
    return users_schema(db_connection.users.find())

@router.get("/user/{id}", status_code=200)
async def find_one_user(id: str):
    try:
        return find_user("_id", ObjectId(id))
    except:
        raise HTTPException(status_code=404)

@router.post("/user", response_model=User, status_code=201)
async def create_user(user: User) -> User:

    if type(find_user_by_username(user.username)) == User:
        raise HTTPException(status_code=404, detail={"Error":"User already exists."})
    
    user_dict = dict(user)
    del user_dict["id"]
    

    id = db_connection.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_connection.users.find_one({"_id": id}))
    return User(**new_user)

@router.put("/user", response_model=User, status_code=201)
async def put_user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_connection.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=400, detail={"Error": "User not found"})
    else:
        return find_user("_id", ObjectId(user.id))
  
@router.delete("/user/{id}", status_code=200)
async def delete_user(id: str):
    try:
        user_name = find_user("_id", ObjectId(id)).username
        db_connection.users.find_one_and_delete({"_id": ObjectId(id)})
        return {"Ok": f"User deleted: {user_name}"}
    except:
        raise HTTPException(status_code=400, detail={"Error": "User not found"})