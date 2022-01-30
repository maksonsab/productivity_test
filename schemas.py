from pydantic import BaseModel


class UserBase(BaseModel):
    login:str
    first_name:str
    last_name:str
    pwd:str

class 