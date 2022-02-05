import time
from sqlalchemy.orm.session import Session
from fastapi import Request
#from fastapi.security import 

from jose import jwt
from passlib.hash import bcrypt

from app.models import User
from app.db import get_session
from .. config import JWT_SECRET


def get_user_session(request:Request):
    user_session = request.cookies.get('session')
    if user_session:
        return Authentication.verify_token(user_session) 
    return None

def get_user(token: str) -> User:  
    user_from_token = Authentication.verify_token(token)
    return user_from_token

def auth_user(login, password) -> str:
    '''Возвращает токен из пары логин/пароль'''
    try:
        user = User.get_user(login=login)
        if not user or not Authentication.check_password(password, user.pwd):
            return None
        return Authentication.generate_token(user)

    except:
        print('bad login or pass')
        return None 

def create_user(login: str, fn: str, ln: str, pwd: str, session: Session = next(get_session())) -> None:
    '''Создает пользователя'''
    secure_pwd = Authentication.hash_password(pwd)
    new_user = User(login, fn, ln, secure_pwd)
    session.add(new_user)
    session.commit()

class Authentication(object):


    @classmethod
    def check_password(cls, form_password: str, hash_password: str) -> bool:
        '''Сверяет пароль из формы авторизации и хэш пароля из базы данных'''
        return bcrypt.verify(form_password, hash_password)

    @classmethod
    def hash_password(cls, password: str)-> str:
        '''Возвращает хэш пароля'''
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls,token: str) -> User:
        '''Проверяется токен и возвращаяется юзер'''
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user = data.get('user')
            user_obj = User.get_user(id=user['id'])
            return user_obj
        except:
            pass
    
    @classmethod
    def generate_token(cls, user: User) -> str:
        '''Возвращает токен пользователя'''
        data = {
            'user': {
                'id' : user.id,
                'login' : user.login
                },
            'expiration' : time.time() + 3600
            }
        token = jwt.encode(data, JWT_SECRET, algorithm='HS256')
        return token

        

    
