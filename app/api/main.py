from fastapi import FastAPI, Depends, Body, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.api.db import engine, SessionLocal, Base
from app.api.repos import product as ProductRepo
from app.api.models.product import Product

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
    return product.__dict__
    

@app.get("/products/")
def get_by_title(title: str, db: Session = Depends(get_db)):
    product = ProductRepo.get_by_title(db, title)
    if not product:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return product.__dict__


@app.get("/products/all/")
def get_all(skip: int = 0, limit: int = 12342, db: Session = Depends(get_db)):
    all_products = ProductRepo.get_all(db, skip, limit)
    if not all_products:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    for p in all_products:
        yield p.__dict__


@app.post("/products/", response_model=None)
async def create(title: str = Body(...), current_price: float = Body(...), total_quantity : int = Body(...), db: Session = Depends(get_db)):
    try:
        ProductRepo.get_by_title(db, title)
    except NoResultFound:
        await ProductRepo.create(db, Product(
            title=title,
            current_price=current_price,
            is_active=True,
            total_quantity=total_quantity,
        ))
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        print('Product exists!')
        return Response(status_code=status.HTTP_409_CONFLICT)
