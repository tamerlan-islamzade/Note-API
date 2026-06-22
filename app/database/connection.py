from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession , async_sessionmaker
from app.core.config import settings


engine=create_async_engine(settings.database_url,echo=True)

#expre_on_commit=False keep objects usable after commit without re-qurying
async_session=async_sessionmaker(engine,expire_on_commit=False , class_=AsyncSession)

async def get_db():
    #Fast-api dependecy that provides a database session
    async with async_session() as session:
        yield session
