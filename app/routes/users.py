from fastapi import APIRouter, Request, Response, status
from fastapi.responses import HTMLResponse

from app.models import User
from app.templates import templates
from app.modules import auth


router = APIRouter(prefix='/users', tags=['users'])





@router.get("/{login}/", response_class=HTMLResponse)
def userinfo(request:Request, login:str):
    user = auth.get_user_session(request)
    if not user:
        return Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    resp = User.get_user(login=login)
    return templates.TemplateResponse('user.html', {'request': request, 'title':f'Пользователь:{resp.login}', 'data':resp, 'user': user})