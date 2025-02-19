from fastapi import status, HTTPException, Depends, APIRouter
from database import get_db
import dbmodel, schema, utils
from sqlalchemy.orm import Session
from typing import List
from .emailsender import send_email
import oauth

router = APIRouter(prefix="/admin", tags=["Admin Only"])

@router.post('', response_model=schema.UserRes)
def new_user(user: schema.UserCreate, session: Session = Depends(get_db)):
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    new_user = dbmodel.UserCreate(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    body = """<h1>Oladimeji speaking</h1>"""
    send_email(user.email, body)
    return user

@router.get('', response_model=List[schema.UserRes])
def getall(session: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    print(current_user.id)
    print(current_user.first_name)
    all_user = session.query(dbmodel.UserCreate).all()
    return all_user

@router.get('/{user_id}', status_code=status.HTTP_200_OK)
def getsingle(user_id: int, session: Session = Depends(get_db)):
    single_user = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.id == user_id).first()
    if not single_user:
        raise HTTPException(detail=f"No user with id {user_id}", status_code=status.HTTP_404_NOT_FOUND)
    return single_user


@router.delete('{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def deluser(user_id: int, session: Session = Depends(get_db)):
    quser = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.id == user_id)
    if quser.first() == None:
        raise HTTPException(detail=f"No user with id {user_id}", status_code=status.HTTP_404_NOT_FOUND)
    quser.delete(synchronize_session=False)
    session.commit()
    return "removed successfully"


@router.put('{user_id}', status_code=status.HTTP_202_ACCEPTED)
def updateuser(user_id: int, request: schema.UserCreate, session: Session = Depends(get_db)):
    user = session.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.id == user_id)
    if not user.first(): 
        raise HTTPException(detail=f"User with id {user_id} not found", status_code=status.HTTP_404_NOT_FOUND)
    user.update(request, synchronize_session=False)
    session.commit()
    return "Updated"








