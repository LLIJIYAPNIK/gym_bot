from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    status = Column(String(255), nullable=False)


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, autoincrement=True)
    muscle = Column(String(255), nullable=False)
    muscle_type = Column(String(255), nullable=False)
    video_id = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)


class Program(Base):
    __tablename__ = "program"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    type_training = Column(String(255), nullable=False)
    file_id = Column(String(255), nullable=False)
    user = relationship("User", backref="program")


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    type_menu = Column(String(255), nullable=False)
    file_id = Column(String(255), nullable=False)
    user = relationship("User", backref="menu")


class Questionnaire(Base):
    __tablename__ = "questionnaire"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    type_questionnaire = Column(String(255), nullable=False)
    questionnaire_id = Column(Integer, nullable=False)
    user = relationship("User", backref="questionnaire")
