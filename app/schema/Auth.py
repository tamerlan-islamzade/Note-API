from pydantic import BaseModel , ConfigDict , Field , field_serializer
from pydantic.aliases import AliasChoices
from typing import Optional

class Token(BaseModel):
    #jwt token response returned after successful login
    access_token:str
    token_type:str
    model_config=ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    #Payload encodedinside the jwt token

    #acceppts "id" from User Model or sub from jwt payload as input , serializes as "sub"
    user_id:Optional[int]=Field(default=None,validation_alias=AliasChoices("id","sub"),serialization_alias="sub")
    model_config=ConfigDict(from_attributes=True)

    #jwt "sub" must be string - convert int user_id before encoding
    @field_serializer("user_id")
    def serialize_user_id(self,v):
        return str(v) if v is not None else None