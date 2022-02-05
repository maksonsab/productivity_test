from os import environ


SQLALCHEMY_DATABASE_URL = environ.get('PRODUCTIVITY_DB')

'''Это должно быть секретом!!!!!!'''
PASSWORD_SATL = 'some_salt'
JWT_SECRET = '6Dn81RMH8UcoFdW_x-VETe5XmfasP_rO'

