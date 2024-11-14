from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 
from passlib.context import CryptContext 
from datetime import datetime , timedelta

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=['bcrypt'])

ALGORITH = 'H5356'
ACCESS_TOKEN_DURATION = 1

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
        "disable": True,
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


@app.get("/")
async def root():
    return users_db

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)  # Aquí corregimos `user_db` a `users_db`
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    expired = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub" : user.username,
        "exp" : expired
    }
    
    return {"access_token": access_token , "token_type": "bearer"}