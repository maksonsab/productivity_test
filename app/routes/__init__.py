from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

import app.models
from app.modules import auth as authorize
from app.templates import templates
from . import (users, auth, votes)
router = APIRouter()

router.include_router(users.router)
router.include_router(votes.router)
router.include_router(auth.router)

@router.get('/', response_class=HTMLResponse)
def index(request:Request):
    resp = app.models.Vote.get_them_all()
    user_session = authorize.get_user_session(request)
    print(user_session)
    return templates.TemplateResponse('index.html', {'request':request, 'title':'Главная', 'data': resp, 'user': user_session })





