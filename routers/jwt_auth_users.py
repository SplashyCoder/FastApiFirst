from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext 
from datetime import datetime , timedelta

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=['bcrypt'])

ALGORITM = 'HS256'
ACCESS_TOKEN_DURATION = 1
SECRET = 'f7a48fb1a9043b9627b48bd4bc49a0c0fe2764af4d6c367ca18272cb2bdde193'

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

# Base de datos de usuarios de ejemplo
users_db = {
    "splashycoder": {
        "username": "splashycoder",
        "full_name": "David Alejandro Pacheco Mora",
        "email": "davida.pacheco@hotmail.com",
        "disable":False,
        "password": "$2a$12$8KiXkIl7AgsUwwBHMNYYieD6Avbb/A7qBqyUYi8GNYKFZQ4J7KJ1S"
    },
    "moncho": {
        "username": "moncho",
        "full_name": "Simon el gato",
        "email": "simon@hotmail.com",
        "disable": True,
        "password": "$2a$12$qGVmgN1u0HsxJ.UDnV6tZOzdooF3d1WMH8a5rEhJR9U4pfJDr95xy"
    },
    "oreo": {
        "username": "oreo",
        "full_name": "Oreo la gata",
        "email": "Oreo@hotmail.com",
        "disable": True,
        "password": "$2a$12$GGP5y5WOXkfoo9HgVPwiNeYoV5UgfML0h7Jdsqurp5uqYEfSLC0Wy"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


@router.get("/usersdb/")
async def root():
    return users_db

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)  # Aquí corregimos `user_db` a `users_db`
    if  not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    expired = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub" : user.username,
        "exp" : expired
    }
    
    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITM) , "token_type": "bearer"}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        
        username = jwt.decode(token, SECRET, algorithms=[ALGORITM]).get('sub')
        if username is None:
            raise exception
        
    except JWTError:
        raise exception 
    
    return search_user(username)

        

async def get_current_user(user: User = Depends(auth_user)):
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está desactivado"
        )
    return user


@router.get("/users/me")
async def me(user: User = Depends(get_current_user)):
    return user