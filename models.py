import datetime

from os import lseek
from types import ClassMethodDescriptorType
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, Date
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import Date


from db import Base, session

class User(Base):
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

    def get_user(login = None, id = None):
        if login:
            return session.query(User).filter(User.login == login).one()
        if id:
            return session.query(User).get(id)

class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="surveys")
    creation_date = Column(Date)
    visible = Column(Boolean, default=True)
    description = Column(String)
    servey_type = Column(Integer)

    questions = relationship("Question", back_populates="survey")


    def __init__(self, title, creator_id, description, stype):
        self.title = title
        self.creator_id = creator_id
        self.creation_date = datetime.datetime.now()
        self.visible = 1
        self.description = description
        self.servey_type = stype

   
    def get_them_all():
        return session.query(Survey).all()


    @staticmethod
    def get_suv(id):
        suv = session.query(Survey).filter(Survey.id == id)
        return suv
    @staticmethod
    def get_all_from_user(user_id):
        surveys = session.query(Survey).filter(Survey.creator_id == user_id).all()
        return surveys


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    text = Column(String)
    answer = Column(String)

    survey = relationship("Survey", back_populates="questions")


    def __init__(self, survei_id, text, answer) -> None:
        self.survey_id = survei_id
        self.text = text
        self.answer = answer



