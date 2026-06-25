from typing import Optional

'''
Validators for UserCreate
fields are required, never None
'''
def validate_username_required(cls,username:str)->str:
    #validator for username
    if len(username)<5 or len(username)>12:
        raise ValueError("Username must be between 5 and 12 characters")
    return username

def validate_password_required(cls,password:str)->str:
    #validator for password
    if len(password)<5 or len(password)>12:
        raise ValueError("Password must be between 5 and 12 characters")
    return password

'''
Validators for UserEdit
fields are Optianal, can be None
'''
def validate_username(cls,username:Optional[str])->Optional[str]:
    #validator for username
    if username and (len(username)<5 or len(username)>12):
        raise ValueError("Username must be between 5 and 12 characters")
    return username

def validate_password(cls,password:Optional[str])->Optional[str]:
    #validator for password
    if password and (len(password)<5 or len(password)>12):
        raise ValueError("Password must be 5 and 12 characters")
    return password
    
