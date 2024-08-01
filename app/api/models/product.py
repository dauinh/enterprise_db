import uuid

from sqlalchemy import Column, Integer, String, Boolean, Numeric

from app.api.db import Base


class Product(Base):
    __tablename__ = "product"

    _uid = Column(
        String(36),
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    title = Column(String(150))
    current_price = Column(Numeric)
    is_active = Column(Boolean)
    total_quantity = Column(Integer)
