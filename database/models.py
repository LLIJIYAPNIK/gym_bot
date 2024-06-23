from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import	declarative_base


Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(255), nullable=False, unique=True)


class Training(Base):
	__tablename__ = 'trainings'
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	muscle = Column(String(255), nullable=False)
	muscle_type = Column(String(255), nullable=False)
	video_id = Column(String(255), nullable=False, unique=True)


class Program(Base):
	__tablename__ = 'programs'
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(255), nullable=False)
	type_training = Column(String(255), nullable=False)
	file_path = Column(String(255), nullable=False)
 
 
class Menu(Base):
	__tablename__ = 'menus'
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	type_menu = Column(String(255), nullable=False)
	file_path = Column(String(255), nullable=False)
