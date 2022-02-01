from os import environ


from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


SQLALCHEMY_DATABASE_URL = environ.get('PRODUCTIVITY_DB')


engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = Session(engine)
Base = declarative_base()


def get_session()-> Session:
    try:
        session = db_session
        yield session
    finally:
        session.close()