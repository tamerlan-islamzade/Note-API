from fastapi import APIRouter , Depends ,HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import User
from app.database.connection import get_db
from app.crud.CrudUser import CrudUser


router=APIRouter(prefix="/users",tags=["Users"])

@router.get("/",response_model=list[User.UserResponseAll])
async def getAllUsers(db:AsyncSession=Depends(get_db)):
    #get all users data
    return await CrudUser().getAll(db=db)

@router.get("/{user_id}",response_model=User.UserResponseById)
async def getUserById(user_id:int,db:AsyncSession=Depends(get_db)):
    #get single user by id
    user=await CrudUser().getById(db=db,user_id=user_id)
    if not user:
        raise HTTPException(status_code=404,detail="Not Found")