'''@app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token' : form_data.username + 'token'}


@app.get('/', response_class=HTMLResponse)

   

@app.get('/survey/{id}', response_class=HTMLResponse)
def survey(request: Request, id:int):
    resp = models.Survey.get_suv(id)
    return templates.TemplateResponse('survey.html', {'request': request, 'data' : resp, 'title': resp.title})





@app.get('/create')
def create_survey(token: str = Depends(oauth2_scheme)):
    return {'token' : token}


if __name__ == '__main__':
    uvicorn.run("server:app", port=8000, host='0.0.0.0', reload = True)

'''