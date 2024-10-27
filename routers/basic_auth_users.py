from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl='login')


class User(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    disable: bool
    password: int
    
class UserDB(User):
    password: str

user_db = {
    'David':{
        'id': 1,
        'username': 'SplashyCoder',
        'full_name': 'David Alejandro Pacheco Mora',
        'email': 'davida.pacheco@hotmail.com',
        'disable': False,
        'password': 1234
    },
    'Moncho':{
        'id': 2,
        'username': 'MonchoLeon',
        'full_name': 'Simon el gato',
        'email': 'simon@hotmail.com',
        'disable': False,
        'password': 3456
    },
    'Oreo':{
        'id':3,
        'username': 'OreoTiti',
        'full_name': 'Oreo la gata',
        'email': 'Oreo@hotmail.com',
        'disable': False,
        'password': 1987
    }


}

def search_user(username: str):
    if username in user_db:
        return UserDB(user_db[username])

@app.post('login'):
async def login(form: OAuth2PasswordRequestForm = Depends()):


@app.get('/')
async def root () :
    return user_db