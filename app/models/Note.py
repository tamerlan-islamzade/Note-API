from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy import String , DateTime , func , ForeignKey
from datetime import datetime

from app.models.base import Base

#Note Model
class Note(Base):
    __tablename__="notes"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    head:Mapped[str] = mapped_column(String(20) , nullable=False)
    content:Mapped[str]=mapped_column(String(100) , nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())

    #Foreign key to User - delete notes automatically when user deleted
    user_id:Mapped[int]= mapped_column(ForeignKey("user.id",ondelete="CASCADE"))

    #Many to One - each note belong to one user
    user:Mapped["User"]=relationship(back_populates="notes")

    def __repr__(self):
        return f"Notes(id={self.id!r},head={self.head!r},content={self.content!r},created_at={self.created_at!r})"
