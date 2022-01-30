from operator import mod
from pyexpat import model
from turtle import title
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn


import models



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    resp = models.Survey.get_them_all()
    return templates.TemplateResponse('index.html', {'request':request, 'title':'Все опросы', 'data': resp })

     

@app.get('/survey/{id}', response_class=HTMLResponse)
def survey(request: Request, id:int):
    resp = models.Survey.get_suv(id).first()
    return templates.TemplateResponse('survey.html', {'request': request, 'data' : resp, 'title': resp.title})

@app.get('/user/{login}', response_class=HTMLResponse)
def userinfo(request:Request, login:str):
    resp = models.User.get_user(login=login)
    return templates.TemplateResponse('user.html', {'request': request, 'title':f'Пользователь:{resp.login}', 'data':resp})




if __name__ == '__main__':
    uvicorn.run("server:app", port=8000, host='0.0.0.0', reload = True)