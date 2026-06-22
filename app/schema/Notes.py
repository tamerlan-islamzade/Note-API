from pydantic import BaseModel
from datetime import datetime

class NoteResponse(BaseModel):
    id:int
    head:str
    content:str
    user_id:int
    created_at:datetime
    model_config={
        "from_attributes":True
    }

class NoteCreate(BaseModel):
    head:str
    content:str
    model_config={
        "from_attributes":True
    }


class NoteEdit(BaseModel):
    head:str | None=None
    content:str | None=None
    model_config={
        "from_attributes":True
    }