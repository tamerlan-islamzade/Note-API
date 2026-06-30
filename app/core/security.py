from passlib.context import CryptContext
from datetime import datetime , timezone , timedelta
import jwt

from app.schema.Auth  import TokenData
from app.core.config import settings

pwd_context=CryptContext(schemes=["bcrypt"])
def hash_password(password:str)->str:
    #Hash a plain-text password using bcrypt
    clean_password=str(password).strip()
    return pwd_context.hash(clean_password)


def verify_password(plain_password:str,hashed_password:str)->bool:
    #Verify a plain-text password against a bcrypt hash
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(token_data:TokenData):
    #generate a signed jwt access token from the given data
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    payload=token_data.model_dump(by_alias=True)
    payload.update({"exp":expire})
    encoded=jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return encoded
