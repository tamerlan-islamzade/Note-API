from sqlalchemy.orm import Mapped , mapped_column , relationship
from sqlalchemy import String , DateTime , func
from datetime import datetime

from app.models.base import Base

class User(Base):
    __tablename__="user"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str]=mapped_column(String(12),unique=True,nullable=False)
    hashed_password:Mapped[str]
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())

    # One-to-many: one user can have many notes
    # lazy="selectin" automatically loads notes in a separate query when user is fetched
    notes:Mapped[list["Note"]]=relationship(back_populates="user",lazy="selectin")
    def __repr__(self):
        return f"user={self.id!r},username={self.username},created_at={self.created_at!r}"