from sqlalchemy import func, select, update, delete
from sqlalchemy.orm import Session

from app.api.db import Base
from app.api.models.product import Product


def get_total(db: Session) -> int:
    stmt = select(func.count(Product.id))
    return db.scalars(stmt).first()


def get_by_id(db: Session, id: int) -> Product:
    stmt = select(Product).where(Product.id == id)
    return db.scalars(stmt).first()


def get_by_title(db: Session, title: str) -> Product:
    stmt = select(Product).where(Product.title == title)
    return db.scalars(stmt).first()


def get_all(db: Session, skip: int = 0, limit: int = 12342) -> list[Product]:
    stmt = select(Product).limit(limit).offset(skip)
    return db.scalars(stmt).all()


async def create(db: Session) -> Product:
    pass


# TODO: update for all products with same id
async def update_by_id(db: Session, product: Product) -> Product:
    stmt = (
        update(Product)
        .where(Product.id == product.id)
        .values(
            title=product.title,
            current_price=product.current_price,
            color=product.color,
            size=product.size,
            is_active=product.is_active,
            quantity=product.quantity,
        )
    )
    db.scalars(stmt)
    db.commit()


# TODO: buggy
async def delete_by_id(db: Session, id: int) -> Product:
    stmt = delete(Product).where(Product.id == id)
    db.scalars(stmt)
    db.commit()
