from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234"
    },
    "moncho": {
        "username": "moncho",
        "full_name": "Simon el gato",
        "email": "simon@hotmail.com",
        "disable": True,
        "password": "3456"
    },
    "oreo": {
        "username": "oreo",
        "full_name": "Oreo la gata",
        "email": "Oreo@hotmail.com",
        "disable": True,
        "password": "1987"
    }
}

# Función para buscar un usuario
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Dependencia para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está desactivado"
        )
    return user

# Ruta raíz de ejemplo
@app.get("/")
async def root():
    return users_db

# Ruta para el login
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)  # Aquí corregimos `user_db` a `users_db`
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

# Ruta para obtener el usuario actual
@app.get("/users/me")
async def me(user: User = Depends(get_current_user)):
    return user
