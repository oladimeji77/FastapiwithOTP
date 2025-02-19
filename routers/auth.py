from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, schema, dbmodel, utils, oauth
from .emailsender import send_email
import pyotp

router = APIRouter(tags=['Login Authentication'])


# Secret key for OTP generation (should be stored securely per user)
#SECRET_KEY = "234567abcdefghi"  # Generate dynamically per user in production
#this is an improved sanjeev's code, it uses username or email



@router.post('/login', response_model=schema.Token)
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
    totp = pyotp.TOTP(user.totp_secret, interval=180)
    otp_code = totp.now() 
    body = f"""<h1>Login Notification</h1>
            <p>Your OTP code is: {otp_code}. It expires in 30 seconds.</p>"""
    send_email(user.email, body)   
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": user.username, "token_type": "bearer"}
    

# Generate and send OTP (Email)
@router.post("/verify", response_model=schema.Token)
def verify_2fa(otp: str, username: str, db: Session = Depends(database.get_db)):
    user = db.query(dbmodel.UserCreate).filter(dbmodel.UserCreate.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    totp = pyotp.TOTP(user.totp_secret, interval=180)
    print(totp.verify(otp))
    if not totp.verify(otp):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")
    
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", "user" : user}
    
    

