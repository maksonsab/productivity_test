from types import ClassMethodDescriptorType
from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, Date
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.sql.visitors import Visitable


from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    pwd = Column(String)
    surveys = relationship("Survey", back_populates="creator")





class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    questions = relationship("Question", back_populates="survey")
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="surveys")
    creation_date = Column(Date)
    visible = Column(Boolean, default=True)
    description = Column(String)
    servey_type = Column(Integer, max=2)




class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    text = Column(String)
    answer = Column(String)

    survey = relationship("Survey", back_populates="qusetions")




