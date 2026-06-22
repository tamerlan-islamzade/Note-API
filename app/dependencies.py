import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException , status
from sqlalchemy.future import select

from app.core.config import settings
from app.database.connection import get_db
from app.models.User import User
from app.schema.Auth import TokenData

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:AsyncSession=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="this token is not valid",
        headers={"www-Authenticate":"Bearer"}   
    )
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        id=payload.get("sub")
        if id is None:
            raise credentials_exception
        payload["sub"]=int(id)
        token_data=TokenData(**payload)
        
    except TypeError:
        raise credentials_exception
    
    query=select(User).filter(User.id==token_data.user_id)
    result=await db.execute(query)
    user=result.scalar_one_or_none()
    return user
