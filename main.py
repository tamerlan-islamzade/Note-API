from fastapi import FastAPI

from app.database.connection import engine
from app.models.base import Base
from app.routers.Note import router as Noterouter
from app.routers.Auth import router as Authrouter
from app.routers.User import router as Userrouter

app=FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(Noterouter)
app.include_router(Authrouter)
app.include_router(Userrouter)