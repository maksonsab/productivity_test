from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templates import templates
from app.models import Survey

router = APIRouter(prefix='/survey', tags=['surveys'])


@router.get('/{id}', response_class=HTMLResponse)
def get_survey(id:int, request:Request):
    resp = Survey.get_suv(id)
    return templates.TemplateResponse('survey.html', {'request': request, 'data': resp, 'title': resp.title })