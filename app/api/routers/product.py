from sqlalchemy.orm import Session
from app.api.models.product import Product


def get_total(session: Session) -> int:
    return session.query(Product).count()


def get_by_id(session: Session) -> Product:
    pass


def get_by_title(session: Session) -> Product:
    pass


def get_all(session: Session) -> Product:
    pass


def create(session: Session) -> Product:
    pass


def update(session: Session) -> Product:
    pass


def delete_by_id(session: Session) -> Product:
    pass
