import datetime

from fastapi import Depends
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, Date, ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.orm.session import Session


from db import Base, get_session


class User(Base):
    """Пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    pwd = Column(String)
    surveys = relationship("Survey", back_populates="creator")


    def __init__(self, login, fn, ln, pwd):
        self.login = login
        self.first_name = fn
        self.last_name = ln
        self.pwd = pwd

    @staticmethod
    def authorize(username:str, pwd:str):
        user = User.get_user(login=username)
        if user:
            if user.pwd == pwd:
                return user
        return False


    def get_user(session: Session = next(get_session()), login:str = None, id:int = None):
        if login:
            user = session.query(User).filter(User.login == login).one_or_none()
            return user
        if id:
            user = session.query(User).get(id)
            return user

class Survey(Base):
    """Хранятся опросы"""
    __tablename__ = 'surveys'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="surveys")
    creation_date = Column(Date)
    visible = Column(Boolean, default=True)
    description = Column(String)
    servey_type = Column(Integer) #1 голосование 2 - Опрос

    questions = relationship("Question", back_populates="survey")


    def __init__(self, title, creator_id, description, stype):
        self.title = title
        self.creator_id = creator_id
        self.creation_date = datetime.datetime.now()
        self.visible = 1
        self.description = description
        self.servey_type = stype

   
    def get_them_all(session: Session = next(get_session())):
        return session.query(Survey).all()


    @staticmethod
    def get_suv(id, session: Session = next(get_session())):
        suv = session.query(Survey).filter(Survey.id == id)
        return suv.first()

    @staticmethod
    def get_all_from_user(user_id, session: Session = next(get_session()), ):
        surveys = session.query(Survey).filter(Survey.creator_id == user_id).all()
        return surveys


class Question(Base):
    """Хранятся вопросы"""
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    text = Column(String)
    answer = Column(ARRAY(String))

    survey = relationship("Survey", back_populates="questions")


    def __init__(self, survei_id, text, answer) -> None:
        self.survey_id = survei_id
        self.text = text
        self.answer = answer


class Answer(Base):
    """Хранятся ответы на вопросы"""
    __tablename__ = 'answers'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(),ForeignKey('users.id'), nullable=True)
    survey_id = Column(Integer(), ForeignKey('surveys.id'), nullable=False)
    answers = Column(ARRAY(String))

