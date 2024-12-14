from fastapi import FastAPI, HTTPException, Depends, APIRouter
from ..import models, schemas, utils
from sqlalchemy.orm import Session 
from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"] #structures the documentation places the users in a Users section
)

@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    #the password -user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(404, detail=f"User with id of {id} was not found")
    
    return user