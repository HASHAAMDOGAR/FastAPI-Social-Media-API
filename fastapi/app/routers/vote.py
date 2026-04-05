from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, modals, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(modals.Post).filter(modals.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    # 1. Check if the post even exists first (Good practice)
    post = db.query(modals.Post).filter(modals.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {vote.post_id} does not exist")

    # 2. Define the QUERY (don't call .first() yet)
    vote_query = db.query(modals.Vote).filter(
        modals.Vote.post_id == vote.post_id, 
        modals.Vote.user_id == current_user.id
    )
    
    # 3. Get the RESULT
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
            )
        
        new_vote = modals.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Vote does not exist"
            )

        # Use the query object to perform the deletion
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}