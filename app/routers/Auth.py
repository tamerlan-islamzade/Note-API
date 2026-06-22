from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.crud.CrudUser import CrudUser
from app.schema.User import UserResponseById, UserCreate
from app.schema.Auth import TokenData, Token
from app.dependencies import get_current_user
from app.core.security import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponseById, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user. Raises 400 if username is already taken."""
    try:
        return await CrudUser().createUser(user_data=user_data, db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.
    Raises 400 if username or password is incorrect.
    """
    user = await CrudUser().getUserByUsername(username=form_data.username, db=db)

    # Check user exists and password matches — same error for both to avoid user enumeration
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username or password incorrect")

    payload = TokenData.model_validate(user)
    access_token = create_access_token(token_data=payload)
    return {"access_token": access_token, "token_type": "bearer"}