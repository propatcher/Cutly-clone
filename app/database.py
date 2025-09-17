from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.settings import settings

engine = create_async_engine(url=settings.DATABASE_URL)
async_session = async_sessionmaker(engine,expire_on_commit=False)

class Base(DeclarativeBase):
    pass