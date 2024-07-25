from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .routers import products
from .db import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/total")
def get_total(db: Session = Depends(get_db)):
    return products.get_total(db)