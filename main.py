from fastapi import  FastAPI
from routers import products, users, user
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(user.router)
app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get('/')
async def root () :
    return 'principal page'

@app.get('/url')
async def url () :
    return {
        'url' : 'https://google.com',
        'user' : 'splashyGnu'
    }

