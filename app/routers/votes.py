from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Response
from ..import models, schemas, utils, oauth2
from sqlalchemy.orm import Session 
from ..database import engine, get_db
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
        tags=["Votes"] #structures the documentation places the votes in a votes section
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        else:
            new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message" : "Successfully added vote"}
    elif vote.dir == 0:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Direction can only be 0 or 1")