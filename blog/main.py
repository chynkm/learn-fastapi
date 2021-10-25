from fastapi import FastAPI
from . import schemas, models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post('/blogs')
def create(request: schemas.Blog):
    return request
