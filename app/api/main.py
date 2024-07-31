from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .repos import product
from .db import engine, SessionLocal, Base

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
def get_total(db: Session = Depends(get_db)) -> int:
    return product.get_total(db)
