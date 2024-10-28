from fastapi import FastAPI, Depends, HTTPException, status
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

users_db = {
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
    if username in users_db:
        return UserDB(users_db[username])
    
def get_current_user(token: str = Depends(oauth2)):
    
    user = search_user(token)

    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='No autorizado',
            headers={"WWW-Authenticate": "Bearer"}
                            )
    return user
    
@app.get('/')
async def root () :
    return users_db


@app.post('login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = user_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail='El usuario no es correcto')

    user = search_user(form.username)

    if not form.password == user.password:
        raise HTTPException(status_code=400, detail='La contraseña no es correcta')
    
    return {'access_token': user.username, 'token_type': 'bearer'}

@app.get('/users/me')
async def me(user: User = Depends(get_current_user)):
    return user 