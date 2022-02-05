from fastapi import FastAPI, Request, Cookie, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import routes

from app.modules import auth



app = FastAPI()
app.include_router(routes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

