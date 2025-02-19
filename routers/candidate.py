from fastapi import status, HTTPException, Depends, APIRouter
from database import get_db
import dbmodel, schema, utils
from sqlalchemy.orm import Session
from typing import List
import oauth

router = APIRouter(prefix="/candidate", tags=["Candidates"])

@router.post('', response_model=schema.Candidate)
async def new_user(candidate: schema.Candidate, session: Session = Depends(get_db)):    
    new_can = dbmodel.Candidate(**candidate.dict())
    session.add(new_can)
    session.commit()
    session.refresh(new_can)
    return new_can


@router.get('')
async def all_candidate(session: Session = Depends(get_db)):
    all_candidate = session.query(dbmodel.Candidate).all()
    return all_candidate