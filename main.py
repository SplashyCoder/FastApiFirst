from fastapi import  FastAPI

app = FastAPI()

print(app)

@app.get('/')
async def root () :
    return 'hola mundo'

@app.get('/url')
async def url () :
    return {
        'url' : 'https://google.com',
        'user' : 'splashyGnu'
    }

#IN ASUS PC
