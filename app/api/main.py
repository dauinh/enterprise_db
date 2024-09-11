from fastapi import FastAPI, Depends, Body, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.api.db import engine, SessionLocal, Base
from app.api.models import Product, Collection
from app.api.repos import product as ProductRepo
from app.api.repos import collection as CollectionRepo


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3039",
    "http://localhost:3039/*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/products/total")
def get_total(db: Session = Depends(get_db)) -> int:
    return ProductRepo.get_total(db)


@app.get("/products/all/")
def get_all(skip: int = 0, limit: int = 1561, db: Session = Depends(get_db)):
    all_products = ProductRepo.get_all(db, skip, limit)
    if not all_products:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    for p in all_products:
        yield p.__dict__


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


@app.post("/products/")
async def create(
    title: str = Body(...),
    current_price: float = Body(...),
    total_quantity: int = Body(...),
    db: Session = Depends(get_db),
):
    # Input validation
    if not title:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Empty title")

    try:
        ProductRepo.get_by_title(db, title)
    except NoResultFound:
        await ProductRepo.create(
            db,
            Product(
                title=title,
                current_price=current_price,
                is_active=True,
                total_quantity=total_quantity,
            ),
        )
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_409_CONFLICT, content="Product exists!")


@app.put("/products/{product_id}")
async def update_by_id(
    product_id: int,
    title: str = Body(...),
    current_price: float = Body(...),
    is_active: bool = Body(...),
    total_quantity: int = Body(...),
    db: Session = Depends(get_db),
):
    try:
        ProductRepo.get_by_id(db, product_id)
    except NoResultFound:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content="Product not found"
        )
    else:
        await ProductRepo.update_by_id(
            db,
            Product(
                id=product_id,
                title=title,
                current_price=current_price,
                is_active=is_active,
                total_quantity=total_quantity,
            ),
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/products/{product_id}")
async def delete_by_id(product_id: int, db: Session = Depends(get_db)):
    product = None
    try:
        product = ProductRepo.get_by_id(db, product_id)
    except NoResultFound:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content="Product not found"
        )
    else:
        await ProductRepo.delete_by_id(db, product)
        return Response(status_code=status.HTTP_202_ACCEPTED)


# TODO: testing
@app.get("/collections/all/")
def get_all(skip: int = 0, limit: int = 12342, db: Session = Depends(get_db)):
    collections = CollectionRepo.get_all(db, skip, limit)
    if not collections:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    for c in collections:
        yield c.__dict__


@app.get("/collections/{collection_id}")
def get_by_id(collection_id: int, db: Session = Depends(get_db)):
    products = ProductRepo.get_all_products_from_collection(db, collection_id)
    if not products:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return products.__dict__
