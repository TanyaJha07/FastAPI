from fastapi import FastAPI

from fastapi.params import Body

app = FastAPI()

@app.get('/') # "@' = decorator. it is used to add a new route to the API.(get = http method & '/' = path(route))
async def root(): #async is used to make the function asynchronous(non-blocking)
    return {'message': 'WELCOME TO THE FIRST API'}

@app.get('/posts')
def get_posts():
    return {"posts": "This is the posts"}

@app.post('/createposts')
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "Succesfully created posts"}
   