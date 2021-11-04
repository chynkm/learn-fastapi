from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog


router = APIRouter(tags=['Blogs'], prefix="/blogs")
get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
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
@router.delete('/{id}')
def destroy(id, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
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
