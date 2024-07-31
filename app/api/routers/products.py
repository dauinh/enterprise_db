from sqlalchemy.orm import Session
from api.models.products import Product


def get_total(session: Session):
    return session.query(Product).count()
