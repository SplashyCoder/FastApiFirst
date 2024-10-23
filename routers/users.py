from fastapi import  FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/users', tags=['users'])
# Inicia el server: uvicorn users:app --reload

class User(BaseModel):
    id: int
    username: str
    surname: str
    url: str
    
users_list = [
    User(id=1, username='David', surname='Pacheco', url='https://google.com'),
    User(id=2,username='Alejandro', surname='Mora', url='https://facebook.com'),
    User(id=4,username='Splashy', surname='Gnu', url='https://twitter.com'),
    User(id=5,username='Oreo', surname='Gordita', url='https://twitter.com'),
    User(id=6,username='Moncho', surname='Gordito', url='https://twitter.com'),
    User(id=7,username='El tren', surname='Fofo', url='https://twitter.com'),

]


@router.get('/')
async def users() :
    return users_list
