from fastapi import  FastAPI
from pydantic import BaseModel

app = FastAPI()

# print(app)

class User(BaseModel):
    id: int
    username: str
    surname: str
    url: str
    
users_list = [
    User(id=1, username='David', surname='Pacheco', url='https://google.com'),
    User(id=2,username='Alejandro', surname='Mora', url='https://facebook.com'),
    User(id=3,username='Juan', surname='Sanchez', url='https://twitter.com'),
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