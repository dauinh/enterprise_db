from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .routers import product
from .db import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/total")
def get_total(session: Session = Depends(get_session)) -> int:
    return product.get_total(session)
