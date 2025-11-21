import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{os.getenv('POSTGRESQL_USERNAME','user')}:{os.getenv('POSTGRESQL_PASSWORD','password')}@{os.getenv('POSTGRESQL_SERVER','localhost')}:{os.getenv('POSTGRESQL_PORT','5432')}/{os.getenv('POSTGRESQL_DATABASE','mydb')}"
)

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

