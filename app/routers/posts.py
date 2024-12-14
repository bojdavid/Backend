from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from ..import models, schemas, utils, oauth2
from sqlalchemy.orm import Session 
from ..database import engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
        tags=["Posts"] #structures the documentation places the posts in a Posts section
)

#get all posts
@router.get("/", response_model=List[schemas.PostOut] )
#@router.get("/")
def getPosts(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # Query to get posts with votes count
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")) \
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.title.contains(search)) \
        .group_by(models.Post.id) \
        .limit(limit) \
        .offset(skip) \
        .all()
    
    # Transform results into the expected response model
    posts_out = []
    for post, votes in results:
        post_out = schemas.PostOut(
            id=post.id,
            title=post.title,
            content=post.content,
            # Add other fields as necessary
            votes=votes  # Assuming you want to include the votes count in the response
        )
        posts_out.append(post_out)

    return posts_out


# create a post
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def createPost(data: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id = current_user.id, **data.dict())
    db.add(post)
    db.commit()
    db.refresh(post) #retrieve the new post that we added to the db 
       
    return post

#get a post
@router.get("/{id}", response_model=schemas.Post)
async def getPost(id : int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(current_user.email)
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail=f"Post with id of {id} was not found")


#delete a post
@router.delete("/{id}")
async def deletePost(id : int, db: Session = Depends(get_db, ),  current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    #delete the post if it exists or raise an exception
    if post.first() == None :
        raise HTTPException(status_code=404, detail=f"Post with id of {id} was not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    return {"Deleted": "success"}


# update a post
@router.put("/{id}")
async def updatePost(id : int, data : schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id of {id} was not found")
    if post.first().owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.update(data.dict(),synchronize_session=False)
    db.commit()
    return ({"Message" : post_query.first()})
 