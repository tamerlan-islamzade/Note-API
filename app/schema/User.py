from pydantic import BaseModel
from datetime import datetime
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
    model_config={
        'from_attributes':True
    }

class UserEdit(BaseModel):
    username:str | None=None
    password:str | None=None
    model_config={
        'from_attributes':True
    }
