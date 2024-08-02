from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.models import Collection


def get_all(db: Session, skip: int = 0, limit: int = 162) -> list[Collection]:
    stmt = select(Collection).limit(limit).offset(skip)
    return db.scalars(stmt).all()
