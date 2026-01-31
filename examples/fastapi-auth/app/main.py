from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import auth, users

app = FastAPI(title="VeilMail Auth Example")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "VeilMail + FastAPI Auth Example", "docs": "/docs"}
