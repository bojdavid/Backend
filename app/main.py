from fastapi import FastAPI, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session 
from .routers import users, posts, auth, votes

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

get_db()

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

#test connection
@app.get("/test")
async def test( db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)