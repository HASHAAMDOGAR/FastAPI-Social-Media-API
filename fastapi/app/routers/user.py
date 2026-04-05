from fastapi import FastAPI,Response, status, HTTPException, Depends,APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import modals, schemas, utils 
from ..database import engine  , get_db

router = APIRouter(
        prefix="/users",
        tags=["Users"]
)

modals.Base.metadata.create_all(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
     hashed_password = utils.hash_password(user.password)
     new_user = modals.User(email=user.email, password=hashed_password)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return  new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
     user = db.query(modals.User).filter(modals.User.id == id).first()
     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
     return  user