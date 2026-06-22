from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError , SQLAlchemyError

from app.models.User import User
from app.schema.User import UserCreate , UserEdit
from app.core.security import hash_password


class CrudUser:
    #All database operations for User model
    async def getAll(cls,db:AsyncSession):
        #get All users
        query=select(User)
        result=await db.execute(query)
        users=result.scalars().all()
        return users
    async def getUserByUsername(cls,db:AsyncSession,username:str):
        #get single User by given username
        query=select(User).filter(User.username==username)
        result=await db.execute(query)
        user=result.scalar_one_or_none()
        return user
    async def getById(cls,user_id:int,db:AsyncSession):
        #get single User by given id
        query=select(User).filter(User.id==user_id)
        result=await db.execute(query)
        user=result.scalar_one_or_none()
        return user
    async def createUser(cls,user_data:UserCreate,db:AsyncSession):
        #create new User by given data
        try:
            user_dict=user_data.model_dump()
            user_dict["hashed_password"]=hash_password(password=user_dict.pop("password"))
            newUser=User(**user_dict)
            db.add(newUser)
            await db.commit()
            await db.refresh(newUser)
            return newUser
        #User doesnt save if username already exists
        except IntegrityError:
            await db.rollback()
            raise ValueError("this username already taken")
    
    async def updateUser(cls,user_data:UserEdit,user_id:int,db:AsyncSession):
        #update User datas by given data
        query=select(User).filter(User.id==user_id)
        result=await db.execute(query)
        user=result.scalar_one_or_none()
        if not user:
            return None
        
        update_user=user_data.model_dump(exclude_unset=True)
        #hash given password
        if "password" in update_user:
            update_user["hashed_password"]=hash_password(password=update_user.pop("password"))

        for key , val in update_user.items():
            setattr(user,key,val)
        try:
            await db.commit()
            await db.refresh(user)
            return user
        #new data doesnt save if username already exists
        except IntegrityError:
            await db.rollback()
            raise ValueError("this username has already taken")
        except SQLAlchemyError:
            await db.rollback()
            raise RuntimeError("ERROR")
    async def deleteUser(cls,user_id:int,db:AsyncSession):
        #delete user by given id
        user=await cls.getById(user_id=user_id,db=db)
        if not user:
            return False
        
        await db.delete(user)
        await db.commit()
        return True

