from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.Note import Note
from app.schema import Notes

class CrudNote:
    #All database operations for Note model
    async def getAll(cls,db:AsyncSession):
        #Get all Notes
        query=select(Note)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_id(cls,db:AsyncSession,note_id):
        #Get single Note by given id
        query=select(Note).where(Note.id==note_id)
        result= await db.execute(query)
        return result.scalar_one_or_none()
    
    async def createNote(cls,db:AsyncSession,note_data:Notes.NoteCreate,user_id:int):
        #create new Note from given data
        newNote=Note(**note_data.model_dump(),user_id=user_id)
        db.add(newNote)
        await db.commit()
        await db.refresh(newNote)
        return newNote

    async def editNote(cls,db:AsyncSession,note_data:Notes.NoteEdit,note_id:int,user_id:int):
        #edit single Note by given data
        query=select(Note).filter(Note.id==note_id,Note.user_id==user_id)
        result=await db.execute(query)
        note=result.scalar_one_or_none()
        if not note:
            return None
        update_data=note_data.model_dump(exclude_unset=True)
        for key,val in update_data.items():
            setattr(note,key,val)
        
        try:
            await db.commit()
            await db.refresh(note)
            return note
        except SQLAlchemyError:
            await db.rollback()
            raise RuntimeError("Error")
    
    async def delete(cls,db:AsyncSession,note_id:int,user_id):
        #delete single Note by Note id and User id
        query=select(Note).filter(Note.id==note_id,Note.user_id==user_id)
        result=await db.execute(query)
        note=result.scalar_one_or_none()
        if not note:
            return False
        await db.delete(note)
        await db.commit()   
        return True   