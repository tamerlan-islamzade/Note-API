from typing import Optional

'''
Validators for NoteCreate
fields are required, never None

'''
def validate_head_required(cls,head:str)->str:
    if len(head)<5 or len(head)>20:
        raise ValueError("Head must be between 5 and 20 characters")
    return head

def validate_content_required(cls,content:str)->str:
    if len(content)<10 or len(content)>100:
        raise ValueError("Content must be between 10 and 100 characters")
    return content

'''
Validators for NoteEdit
Fields are optional, can be None
'''

def validate_head(cls,head:Optional[str])->Optional[str]:
    if head and (len(head)<5 or len(head)>20):
        raise ValueError("Head must be between 5 and 20 characters")
    return head

def validate_content(cls,content:Optional[str])->Optional[str]:
    if content and (len(content)<10 or len(content)>100):
        raise ValueError("Content must be between 10 and 100 characters")
    return content