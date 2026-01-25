from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.config import settings

# Create a database engine using the POSTGRES_URL from settings
engine = create_async_engine(
    # Use the POSTGRES_URL method to get the database URL
    url=settings.POSTGRES_URL,
    # Enable echo for SQL query logging
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    
# Session to interact with the database
async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session

# Session Dependency Annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]