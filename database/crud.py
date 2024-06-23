from sqlalchemy import select, and_, update, delete
from .models import Base, Training
from sqlalchemy.orm import sessionmaker


class DatabaseManager:
  def __init__(self, model: Base, session_maker: sessionmaker):
    self.model = model
    self.session_maker = session_maker
  
  async def get_by_id(self, id: int):
    async with self.session_maker() as session:
      result = await session.execute(select(self.model).where(self.model.id == id))
      return result.scalars().first()
    
  async def add(self, **kwargs):
    async with self.session_maker() as session:
      instance = self.model(**kwargs)
      session.add(instance)
      await session.commit()
      await session.refresh(instance)
      return instance
    
  async def get_by_condition(self, condition, quantity: bool = False, select_this = Training):
    async with self.session_maker() as session:
      result = await session.execute(select(select_this).where(condition))
      if not quantity:
        return result.scalars().first()
      return result.scalars().all()
    
  async def get_all(self, model):
      async with self.session_maker() as session:
          result = await session.execute(select(model))
          columns = result.keys()
          return result.fetchall()
    
  async def update(self, id: int, **kwargs):
    async with self.session_maker() as session:
      await session.execute(update(self.model).where(self.model.id == id).values(**kwargs))
      await session.commit()
      
  async def update_by_condition(self, condition, **kwargs):
    async with self.session_maker() as session:
      await session.execute(update(self.model).where(condition).values(**kwargs))
      await session.commit()
      
  async def delete(self, id: int):
    async with self.session_maker() as session:
      await session.execute(delete(self.model).where(self.model.id == id))
      await session.commit()
      
  async def delete_by_condition(self, condition):
    async with self.session_maker() as session:
      await session.execute(delete(self.model).where(condition))
      await session.commit()
