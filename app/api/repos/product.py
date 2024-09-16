from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.models import Product


def get_total(db: Session) -> int:
    stmt = select(func.count(Product.id))
    return db.scalars(stmt).one()


def get_by_id(db: Session, id: int) -> Product:
    stmt = select(Product).where(Product.id == id)
    return db.scalars(stmt).one()


def get_by_title(db: Session, title: str) -> Product:
    stmt = select(Product).where(Product.title == title)
    return db.scalars(stmt).one()


def get_all(db: Session, skip: int = 0, limit: int = 1561) -> list[Product]:
    stmt = select(Product).limit(limit).offset(skip)
    return db.scalars(stmt).all()


async def create(db: Session, product: Product):
    db.add(product)
    db.commit()


async def update(db: Session, product: Product):
    db.merge(product)
    db.commit()


async def delete(db: Session, product: Product):
    db.delete(product)
    db.commit()


def is_attr_quantities_equal_total(db: Session, product_id: int) -> bool:
    stmt = select(Product).where(Product.id == product_id)
    product = db.scalars(stmt).one()
    total = product.total_quantity
    count = 0
    for attr in product.attributes:
        count += attr.quantity
    return total == count
