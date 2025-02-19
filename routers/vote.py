from fastapi import status, HTTPException, Depends, APIRouter
from database import get_db
import dbmodel, schema, utils
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .emailsender import send_email
import oauth

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.get("/result")
def result(session:  Session = Depends(get_db)):
    results = session.query(dbmodel.Vote.candidate_name, func.count(dbmodel.Vote.candidate_name)).group_by(dbmodel.Vote.candidate_name).all()
    res = dict(results)
    print(dict(results))
    return res

@router.post('')
def new_user(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)): 

    check_candidate = db.query(dbmodel.Candidate).filter(dbmodel.Candidate.candidate_id == vote.candidate_id).first()
    check_voted = db.query(dbmodel.Vote).filter(dbmodel.Vote.voter_id == current_user.id).first()

    if not check_candidate:
        raise HTTPException(detail="Candidate don't exist", status_code=status.HTTP_404_NOT_FOUND)
    
    if check_voted:
        raise HTTPException(detail="You have already Voted!!!", status_code=status.HTTP_400_BAD_REQUEST)
 
    votingo = dbmodel.Vote(candidate_id = vote.candidate_id, voter_id = current_user.id, candidate_name = vote.candidate_name)
    db.add(votingo)
    db.commit()
    db.refresh(votingo)
    return votingo

@router.get('{user_id}', response_model=schema.VoteRes)
def vote(vote: schema.Vote, session:  Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    
    user = session.query(dbmodel.Vote).filter(dbmodel.UserCreate.id == current_user.id)
    print(current_user.id)
    print(current_user.first_name)
    if not user.first(): 
        raise HTTPException(detail=f"User with id {user_id} not found", status_code=status.HTTP_404_NOT_FOUND)
    user.update(vote, synchronize_session=False)
    session.commit()
    return "Sucessfully Voted"

