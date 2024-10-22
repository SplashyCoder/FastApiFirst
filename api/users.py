from fastapi import  FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
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

@app.get('/usersjson')
async def users_json () :
    return [{
            'username':'david',
            'surname':'Pacheco',
            'url':'Google.com'
            },{
            'username':'Alejandro',
            'surname':'Mora',
            'url':'facebook.com'
            },{
            'username':'Juan',
            'surname':'Sanchez',
            'url':'twitter.com'
            }]

@app.get('/users')
async def users() :
    return users_list

@app.get('/user/{id}')
async def user(id:int):
    return search_user(id)

@app.get('/user/')
async def user(id:int):
    return search_user(id)
    
@app.post('/user/',response_model=User,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
        
        
    users_list.append(user)
    return user
        

@app.delete('/user/')
async def user(id:int):
    found = False
    for index,saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return user

    if found == False:
        return {'error':'User not deleted'}
        

@app.put('/user/')
async def user(user:User):
    found = False
    
    for index,saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return user
    
    if not found:
        return {'error':'User not updated'}

    
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(users)[0]
    except:
        return {'error':'User not found'}