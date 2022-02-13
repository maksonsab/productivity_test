import datetime

from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, Date, ARRAY, and_, delete
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.orm.session import Session


from app.db import Base, get_session



class User(Base):
    """Таблица с пользователями"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    pwd = Column(String)


    votes = relationship("Vote", back_populates="creator") #для быстрого получения всех голосований пользователя


    def __init__(self, login, fn, ln, pwd):
        self.login = login
        self.first_name = fn
        self.last_name = ln
        self.pwd = pwd



    def get_user(session: Session = next(get_session()), login:str = None, id:int = None):
        if login:
            user = session.query(User).filter(User.login == login).one_or_none()
            return user
        if id:
            user = session.query(User).get(id)
            return user

class Vote(Base):
    """Хранятся голосования"""
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creation_date = Column(Date)
    edit_date = Column(Date)
    visible = Column(Boolean, default=True)
    description = Column(String)
    closed = Column(Boolean, default=False)
    anon = Column(Boolean, default= True)
    revote = Column(Boolean, default=True)

    creator = relationship("User", back_populates="votes")
    questions = relationship("VoteQuestion", back_populates="vote")
    answers = relationship("VoteAnswer", back_populates="votes")


    def __init__(self, title, creator_id, description, anon, revote):
        self.title = title
        self.creator_id = creator_id
        self.creation_date = datetime.datetime.now()
        self.description = description
        self.anon = anon
        self.revote = revote

    def update(self, title, description, anon, revote, closed, visible, session: Session = next(get_session())):
        self.title = title
        self.description = description
        self.anon = anon
        self.revote = revote
        self.edit_date = datetime.datetime.now()
        self.closed = closed
        self.visible = visible
        session.commit()
    
    def delete(self, session: Session = next(get_session())):
        VoteAnswer.delete(self.id)
        VoteQuestion.delete(self.id)
        session.delete(self)
        session.commit()


    def get_results(self):
        length = len(self.answers)
        list_ans = list(range(len(self.questions[0].answers)))
        result = dict()
        for ans in list_ans:
            result[ans] = [0,]
        try:
            for answer in self.answers: 
                if answer.answer not in list_ans:
                    raise ValueError
                result[answer.answer][0] += 1            
        except Exception as e:
            print(e)
        print(result)
        for key in result:
            value = result.get(key)
            percent = value[0] / (length * 0.01)
            value.append(round(percent,2))
            result[key] = value        
        
        return result
        

    @staticmethod
    def get_them_all(session: Session = next(get_session())):
        return session.query(Vote).all()


    @staticmethod
    def get_vote(id, session: Session = next(get_session())):
        return session.query(Vote).filter(Vote.id == id).first()

    @staticmethod
    def get_all_from_user(user_id, session: Session = next(get_session()), ):
        return session.query(Vote).filter(Vote.creator_id == user_id).all()
    
    @staticmethod
    def is_user_vote(user_id: int, vote_id: int) -> bool:
        '''Голосовал ли пользователь'''
        vote = Vote.get_vote(vote_id)
        pass



class VoteQuestion(Base):
    """Хранятся вопросы для голосования"""
    __tablename__ = 'votes_questions'
    id = Column(Integer, primary_key=True)
    vote_id = Column(Integer, ForeignKey("votes.id"))
    text = Column(String)
    answers = Column(ARRAY(String))

    all_answered = relationship("VoteAnswer", back_populates="question")
    vote = relationship("Vote", back_populates="questions")


    def __init__(self, vote_id, text, answers) -> None:
        self.vote_id = vote_id
        self.text = text
        self.answers = answers

    def update(self, text, answers, session: Session = next(get_session())) -> None:
        self.text = text
        self.answers = answers
        session.commit()

    @staticmethod
    def delete(vote_id, session: Session = next(get_session())):
        session.execute(delete(VoteQuestion).where(VoteQuestion.vote_id == vote_id))



class VoteAnswer(Base):
    """Хранятся ответы на голосования"""
    __tablename__ = 'vote_answers'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(),ForeignKey('users.id'), nullable=True)
    vote_id = Column(Integer(), ForeignKey('votes.id'), nullable=False)
    question_id = Column(Integer(), ForeignKey('votes_questions.id'))
    answer = Column(Integer(), nullable=False)

    question = relationship("VoteQuestion", back_populates="all_answered")
    votes = relationship("Vote", back_populates='answers')

    def __init__(self, user_id, vote_id, question_id, answer):
        self.user_id = user_id
        self.vote_id = vote_id
        self.question_id = question_id
        self.answer = answer
    
    @staticmethod
    def delete(vote_id, session: Session = next(get_session())):
        session.execute(delete(VoteAnswer).where(VoteAnswer.vote_id == vote_id))
        
