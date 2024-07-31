from sqlalchemy.orm import Session
from app.api.models.product import Product


def get_total(session: Session) -> int:
    return session.query(Product).count()


def get_product_by_id(session: Session) -> Product:
    pass


def get_all_product(session: Session) -> Product:
    pass


def create_product(session: Session) -> Product:
    pass


def update_product(session: Session) -> Product:
    pass


def delete_product(session: Session) -> Product:
    pass
