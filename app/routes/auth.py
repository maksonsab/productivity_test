from fastapi import APIRouter, Request, Response, Form, responses, status, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse


from app.modules import auth
from app.templates import templates



router = APIRouter(tags=['auth'])


@router.get('/login', response_class=HTMLResponse)
def login(request:Request):
    return templates.TemplateResponse('login.html', {'request': request, 'title': 'Авторизация','user': auth.get_user_session(request)})

@router.post('/login', response_class=RedirectResponse)
def authorize(request: Request, login: str = Form(...), password: str = Form(...), ):
    user = auth.auth_user(login, password,)
    if user:
        print(f'user: {user}')
        response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
        response.set_cookie(key='session', value=user, httponly=True, expires=36000)
        return response
    return RedirectResponse(url='/login', status_code = status.HTTP_303_SEE_OTHER)
     
@router.get('/registration', response_class=HTMLResponse)
def registration(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request, 'user' : None})

@router.post('/registration')
def register_user(request:Request, login: str = Form(...), f_n: str = Form(...), l_n: str = Form(...), password: str = Form(...)):
    message = auth.create_user(login, f_n, l_n, password)
    return JSONResponse(message)