from fastapi import APIRouter, Depends
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session


router = APIRouter()


@router.get('/blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
