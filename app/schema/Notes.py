from pydantic import BaseModel , field_validator
from datetime import datetime

import app.schema.validators.note_validators as note_val

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

    #validators for head and content
    validate_head=field_validator("head")(classmethod(note_val.validate_head_required))
    validate_content=field_validator("content")(classmethod(note_val.validate_content_required))

    model_config={
        "from_attributes":True
    }


class NoteEdit(BaseModel):
    head:str | None=None
    content:str | None=None

    #validators for head and content
    validate_head=field_validator("head")(classmethod(note_val.validate_head))
    validate_content=field_validator("content")(classmethod(note_val.validate_content))

    model_config={
        "from_attributes":True
    }