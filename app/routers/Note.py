from fastapi import APIRouter ,Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.schema import Notes
from app.crud.CrudNote import CrudNote
from app.dependencies import get_current_user
from app.models.User import User

router=APIRouter(prefix="/notes",tags=["Notes"])

@router.get("/",response_model=list[Notes.NoteResponse])
async def getAll(db:AsyncSession=Depends(get_db)):
    #get all Notes from database
    return await CrudNote().getAll(db=db)

@router.get("/{note_id}",response_model=Notes.NoteResponse)
async def getById(note_id:int,db:AsyncSession=Depends(get_db)):
    #get single note by id from database
    note=await CrudNote().get_by_id(db=db,note_id=note_id)
    if not note:
        raise HTTPException(status_code=404,detail="Note not Found")
    
    return note

@router.post("/",response_model=Notes.NoteResponse)
async def createNote(note_data:Notes.NoteCreate,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    """
    create new note
    authetication token required that provides user id
    """
    try:
        return await CrudNote().createNote(db=db,note_data=note_data,user_id=current_user.id)
    except ValueError as v:
        raise HTTPException(status_code=400,detail=str(v))

@router.put("/{note_id}",response_model=Notes.NoteResponse)
async def editNote(note_id:int,note_data:Notes.NoteEdit,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    """
    edit note from given data
    authentication token required
    raise 403 if user.id not equal note.user_id
    """
    try:
        note=await CrudNote().editNote(note_id=note_id,note_data=note_data,db=db,user_id=current_user.id)
        if note is None:
            raise HTTPException(status_code=403,detail="Forbidden")
        
        return note
    except ValueError as v:
        raise HTTPException(status_code=400,detail=str(v))
    except RuntimeError as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete("/{note_id}")
async def deleteNote(note_id:int,db:AsyncSession=Depends(get_db),current_user:User=Depends(get_current_user)):
    """
    delete single Note
    authentication token required
    raise 403 if user.id not equal note.user_id
    """
    result=await CrudNote().delete(db=db,note_id=note_id,user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=403,detail="Forbidden")
    
    return {"status":"success","message":"successfuly deleted"}