from pydantic import BaseModel , field_validator
from datetime import datetime

import app.schema.validators.user_validator as usr_val 
from app.schema.Notes import NoteResponse

class UserResponseAll(BaseModel):
    id:int
    username:str
    created_at:datetime

    model_config={
        'from_attributes':True
    }

class UserResponseById(BaseModel):
    id:int
    username:str
    created_at:datetime
    notes:list[NoteResponse]
    model_config={
        'from_attributes':True
    }

class UserCreate(BaseModel):
    username:str
    password:str

    #validators for username and password
    validate_username=field_validator("username")(classmethod(usr_val.validate_username_required))
    validate_password=field_validator("password")(classmethod(usr_val.validate_password_required))

    model_config={
        'from_attributes':True
    }

class UserEdit(BaseModel):
    username:str | None=None
    password:str | None=None

    #Validators for username and password
    validate_username=field_validator("username")(classmethod(usr_val.validate_username))
    validate_password=field_validator("password")(classmethod(usr_val.validate_password))

    model_config={
        'from_attributes':True
    }
