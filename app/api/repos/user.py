from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.models import User


def get_total(db: Session) -> int:
    stmt = select(func.count(User.id))
    return db.scalars(stmt).one()


def get_by_id(db: Session, id: int) -> User:
    stmt = select(User).where(User.id == id)
    return db.scalars(stmt).one()


def get_all(db: Session, skip: int = 0, limit: int = 1561) -> list[User]:
    stmt = select(User).limit(limit).offset(skip)
    return db.scalars(stmt).all()


async def create(db: Session, user: User):
    db.add(user)
    db.commit()

