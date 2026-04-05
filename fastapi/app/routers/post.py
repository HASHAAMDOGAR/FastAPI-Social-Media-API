from fastapi import FastAPI,Response, status, HTTPException, Depends,APIRouter
from passlib.context import CryptContext
import psycopg2
from typing import Optional
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import modals, schemas, oauth2  
from ..database import engine  , get_db


router = APIRouter(
     prefix="/posts",
     tags=["Posts"]
)



@router.get("/", response_model=list[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = db.query(
        modals.Post,
        func.count(modals.Vote.post_id).label("votes")
    ).join(
        modals.Vote,
        modals.Vote.post_id == modals.Post.id,
        isouter=True
    ).group_by(
        modals.Post.id
    ).filter(
        modals.Post.owner_id == current_user.id,
        modals.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    return [{"post": post, "votes": votes} for post, votes in results]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post = modals.Post(owner_id=current_user.id,**post.model_dump(exclude={"rating"}))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post



@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    result = db.query(
        modals.Post,
        func.count(modals.Vote.post_id).label("votes")
    ).join(
        modals.Vote,
        modals.Vote.post_id == modals.Post.id,
        isouter=True
    ).group_by(
        modals.Post.id
    ).filter(
        modals.Post.id == id
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    post, votes = result
    return {"post": post, "votes": votes}

     

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     post_query = db.query(modals.Post).filter(modals.Post.id == id)
     
     post = post_query.first()

     if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
     if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
     
     post_query.delete(synchronize_session=False)
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)

 

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
        post_query = db.query(modals.Post).filter(modals.Post.id == id)
        found_post = post_query.first()
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        if found_post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        post_query.update(post.model_dump(exclude={"rating"}), synchronize_session=False)
        db.commit()
        return  post_query.first()
        
