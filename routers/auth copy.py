from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, schema, dbmodel, utils, oauth
from .emailsender import send_email

router = APIRouter(tags=['Login Authentication'])

#this is an improved sanjeev's code, it uses username or email
@router.post('/login',response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user_email = db.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.email == user_credentials.username).first()
    user_name = db.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.username == user_credentials.username).first()
    user = user_email
    if not user_email:
        user = user_name
        if not user_name:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token
    body = """<h1>Login Notification</h1>"""
    send_email(user.email, body)
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", "user" : user}