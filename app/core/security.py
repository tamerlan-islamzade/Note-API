import bcrypt
from datetime import datetime , timezone , timedelta
import jwt

from app.schema.Auth  import TokenData
from app.core.config import settings

def hash_password(password:str)->str:
    #Hash a plain-text password using bcrypt
    bytes=password.encode("utf-8")

    salt=bcrypt.gensalt()
    hashed_bytes=bcrypt.hashpw(bytes,salt)
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password:str,hashed_password:str)->bool:
    #Verify a plain-text password against a bcrypt hash
    try:
        plain_bytes=plain_password.encode("utf-8")
        hashed_bytes=hashed_password.encode("utf-8")
        return bcrypt.checkpw(plain_bytes,hashed_bytes)
    except Exception:
        return False

def create_access_token(token_data:TokenData):
    #generate a signed jwt access token from the given data
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    payload=token_data.model_dump(by_alias=True)
    payload.update({"exp":expire})
    encoded=jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return encoded
