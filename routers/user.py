from fastapi import status, HTTPException, Depends, APIRouter
from database import get_db
import dbmodel, schema, utils
from sqlalchemy.orm import Session
from typing import List
from .emailsender import send_email
import oauth
import pyotp

router = APIRouter(prefix="/user", tags=["User Profile"])

@router.post('', response_model=schema.UserRes)
def new_user(user: schema.UserCreate, session: Session = Depends(get_db)):
    existing_user = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.email == user.username).first()
    existing_email = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.username == user.email).first()
    if existing_user or existing_email:
        raise HTTPException(status_code=400, detail="User already exists")
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    totp_secret = pyotp.random_base32()
    new_user = dbmodel.UserCreate(**user.dict(), totp_secret=totp_secret)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    body = """<h1>Oladimeji speaking</h1>"""
    send_email(user.email, body)
    return user


@router.get('', status_code=status.HTTP_200_OK, response_model=schema.UserRes)
async def userProfile(session: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    single_user = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.id == current_user.id).first()
    if not single_user:
        raise HTTPException(detail=f"No user with this profile exist", status_code=status.HTTP_404_NOT_FOUND)
    return single_user

@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def deluser(session: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    quser = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.id == current_user.id)
    if quser.first() == None:
        raise HTTPException(detail=f"No user with this profile", status_code=status.HTTP_404_NOT_FOUND)
    quser.delete(synchronize_session=False)
    session.commit()
    return "removed successfully"


@router.put('', status_code=status.HTTP_202_ACCEPTED)
async def updateuser(request: schema.UserUpdate, session: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    user = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.id == current_user.id)
    if not user.first(): 
        raise HTTPException(detail=f"User with id not found", status_code=status.HTTP_404_NOT_FOUND)
    user.update(request.dict(), synchronize_session=False)
    session.commit()
    return "Updated"

#To set the fields to update, adjust your request schema, make fields that are not required 
#mandatory check check






