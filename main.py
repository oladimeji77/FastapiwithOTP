from fastapi import FastAPI, Depends
from database import engine, Base, get_db, Base2, engine2
from routers import user, sms, auth, vote, candidate, admin
import time
from config import settings as ss
from fastapi.middleware.cors import CORSMiddleware
# Create all tables in the database
# Base.metadata.create_all(bind=engine)



app = FastAPI(title=ss.project_title,
              description=ss.project_description,
              version=ss.project_version)

# Set up CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def index():
    return f"{ss.WELCOME}"



while True:
    try:
        Base.metadata.create_all(bind=engine)
        print("Database 1 is active....")
        Base2.metadata.create_all(bind=engine2)
        print("Database 2 is also active....")
        break
    except Exception as error:
        print(f"Database not available {error}")
        time.sleep(5)

app.include_router(user.router)
app.include_router(sms.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(candidate.router)
app.include_router(admin.router)









