from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Auth'])


@router.post('/login')
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with email: {request.username} does not exist'
        )

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
