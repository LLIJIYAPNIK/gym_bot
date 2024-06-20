from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)