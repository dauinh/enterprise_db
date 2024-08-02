from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.models import Collection, Product


def get_all(db: Session, skip: int = 0, limit: int = 162) -> list[Collection]:
    stmt = select(Collection).limit(limit).offset(skip)
    return db.scalars(stmt).all()


def get_all_products_from_collection(db: Session, collection_id: int) -> list[Product]:
    collection = db.query(Collection).get(collection_id)
    return collection.products