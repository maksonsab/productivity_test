from os import environ


from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import SQLALCHEMY_DATABASE_URL



engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = Session(engine)
Base = declarative_base()


def get_session()-> Session:
    try:
        session = db_session
        yield session
    finally:
        session.close()


def init_db():
    print('Создаем новую базу данных!')
    Base.metadata.create_all(engine)