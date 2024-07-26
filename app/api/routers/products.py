from sqlalchemy.orm import Session
from api.models.products import Product


def get_total(db: Session):
    return db.query(Product).count()