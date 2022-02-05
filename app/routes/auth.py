from crypt import methods
from types import MethodType
from fastapi import APIRouter, Request, Response, Form, responses, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse


from app.modules import auth
from app.templates import templates



router = APIRouter(tags=['auth'])


@router.get('/login', response_class=HTMLResponse)
def login(request:Request):
    return templates.TemplateResponse('login.html', {'request': request, 'title': 'Авторизация','session': auth.get_user_session(request)})

@router.post('/login')
def authorize(response:Response, login: str = Form(...), password: str = Form(...),):
    user = auth.auth_user(login, password)
    if user:
        print(f'user: {user}')
        response.set_cookie(key='session', value=user)
        return  response #RedirectResponse( ,url='/', status_code=status.HTTP_303_SEE_OTHER, )
    return RedirectResponse(url='/login', status_code = status.HTTP_303_SEE_OTHER)
     
