from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    muscle = Column(String(255), nullable=False)
    muscle_type = Column(String(255), nullable=False)
    video_id = Column(String(255), nullable=False)


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    type_training = Column(String(255), nullable=False)
    file_id = Column(String(255), nullable=False)


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    type_menu = Column(String(255), nullable=False)
    file_id = Column(String(255), nullable=False)


class Questionnaire(Base):
    __tablename__ = "questionnaire"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    type_questionnaire = Column(String(255), nullable=False)
    questionnaire_id = Column(Integer, nullable=False)
