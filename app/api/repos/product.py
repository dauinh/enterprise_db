from sqlalchemy import func, select, update, delete, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, ResourceClosedError, IntegrityError

from app.api.db import Base
from app.api.models.product import Product


def get_total(db: Session) -> int:
    stmt = select(func.count(Product.id))
    try:
        return db.scalars(stmt).one()
    except NoResultFound:
        print('Product model not found')


def get_by_id(db: Session, id: int) -> Product:
    stmt = select(Product).where(Product.id == id)
    try:
        return db.scalars(stmt).one()
    except NoResultFound:
        print(f'Product with id {id} not found')


def get_by_title(db: Session, title: str) -> Product:
    stmt = select(Product).where(Product.title == title)
    try:
        return db.scalars(stmt).one()
    except NoResultFound:
        print(f'Product with title {title} not found')


def get_all(db: Session, skip: int = 0, limit: int = 12342) -> list[Product]:
    stmt = select(Product).limit(limit).offset(skip)
    try:
        return db.scalars(stmt).all()
    except NoResultFound:
        print('Product model not found')


async def create(db: Session, product: Product):
    if get_by_title(db, product.title): 
        raise IntegrityError('Product already exists!')

    stmt = (
        insert(Product)
        .values(
            title=product.title,
            current_price=product.current_price,
            is_active=product.is_active,
            total_quantity=product.total_quantity,
        )
    )
    try:
        db.scalars(stmt)
        db.commit()
    except ResourceClosedError:
        print('Result object closed automatically')


async def update_by_id(db: Session, product: Product):
    stmt = (
        update(Product)
        .where(Product.id == product.id)
        .values(
            title=product.title,
            current_price=product.current_price,
            is_active=product.is_active,
            total_quantity=product.total_quantity,
        )
    )
    try:
        db.scalars(stmt)
        db.commit()
    except ResourceClosedError:
        print('Result object closed automatically')


async def delete_by_id(db: Session, id: int):
    stmt = delete(Product).where(Product.id == id)
    try:
        db.scalars(stmt)
        db.commit()
    except ResourceClosedError:
        print('Result object closed automatically')
