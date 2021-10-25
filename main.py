from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()


@app.get('/')
def index():
    return 'hi'


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.get('/blogs/{id}')
def show(id: int):
    return {'data': {'id': id}}


# ?limit=10&published=true
@app.get('/blogs')
def all_blogs(limit=10, published=True, sort: Optional[str] = None):
    if published:
        return {'data': {'limit': f'{limit} published blogs from the DB'}}

    return {'data': {'limit': f'{limit} blogs from the DB'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blogs')
def create_blog(blog: Blog):
    return {'data': f'Blog is created with title: {blog.title}'}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
