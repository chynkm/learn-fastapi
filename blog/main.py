from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)


@app.post('/blogs', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# @app.get('/blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


@app.get(
    '/blogs/{id}',
    status_code=200,
    response_model=schemas.ShowBlog,
    tags=['blogs']
)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id: {id} does not exist'
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id: {id} does not exist'}

    return blog


# @app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
@app.delete('/blogs/{id}', tags=['blogs'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id: {id} does not exist'
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    # db.query(models.Blog).filter(models.Blog.id == id).update(
    # {'title': request.title, 'body': request.body},
    # synchronize_session=False
    # )
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id: {id} does not exist'
        )

    blog.update(request.dict())
    db.commit()
    return {'updated successfully'}


@app.post('/users', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id: {id} does not exist'
        )

    return user
