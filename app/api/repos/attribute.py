from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.models import Product


def get_product_attribute(db: Session, product_id: int) -> list[Product]:
    product = db.get(Product, product_id)
    return product.attributes
