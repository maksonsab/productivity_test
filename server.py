import json


from fastapi import FastAPI, Request, Cookie, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn


import models



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token' : form_data.username + 'token'}


@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    resp = models.Survey.get_them_all()
    return templates.TemplateResponse('index.html', {'request':request, 'title':'Все опросы', 'data': resp })

     

@app.get('/survey/{id}', response_class=HTMLResponse)
def survey(request: Request, id:int):
    resp = models.Survey.get_suv(id)
    return templates.TemplateResponse('survey.html', {'request': request, 'data' : resp, 'title': resp.title})

@app.get('/user/{login}', response_class=HTMLResponse)
def userinfo(request:Request, login:str):
    resp = models.User.get_user(login=login)
    return templates.TemplateResponse('user.html', {'request': request, 'title':f'Пользователь:{resp.login}', 'data':resp})




@app.get('/create')
def create_survey(token: str = Depends(oauth2_scheme)):
    return {'token' : token}


if __name__ == '__main__':
    uvicorn.run("server:app", port=8000, host='0.0.0.0', reload = True)