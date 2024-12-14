from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    #prefix="/users",
    tags= ["auth"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials :OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    #the user_credentials is a form that contains the username and password
    #the 0auth2passwordrequestform only contains username  and password, that is why we used user_credentials.username
    #we could have used schema.userlogin for our user credentials 

    user =  db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(403, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(403, detail="Invalid credentials")
    
    #create a token
    #return token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return { "access_token": access_token, "token_type": "bearer" }