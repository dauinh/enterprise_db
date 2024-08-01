import json

from fastapi import FastAPI, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.repos import product as ProductRepo
from app.api.db import engine, SessionLocal, Base

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
    return ProductRepo.get_total(db)


@app.get("/products/{product_id}")
def get_by_id(product_id: int, db: Session = Depends(get_db)):
    product = ProductRepo.get_by_id(db, product_id)
    if not product:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return json.dumps(product)
    

@app.get("/products/")
def get_by_title(title: str, db: Session = Depends(get_db)):
    product = ProductRepo.get_by_title(db, title)
    if not product:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return json.dumps(product)