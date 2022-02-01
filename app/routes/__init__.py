from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

import app.models
from app.templates import templates
from . import (users, survey)
router = APIRouter()

router.include_router(users.router)
router.include_router(survey.router)

@router.get('/', response_class=HTMLResponse)
def index(request:Request):
    resp = app.models.Survey.get_them_all()
    return templates.TemplateResponse('index.html', {'request':request, 'title':'Главная', 'data': resp })





