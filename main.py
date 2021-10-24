from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return 'hi'


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': {'id': id}}
