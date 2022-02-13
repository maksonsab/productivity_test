from os import environ


SQLALCHEMY_DATABASE_URL = environ.get('PRODUCTIVITY_DB')
JWT_SECRET = environ.get('JWT_SECRET')

