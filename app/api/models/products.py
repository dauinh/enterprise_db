from sqlalchemy import Column, Integer, String, Boolean, Numeric
import uuid

from api.db import Base


class ModelBase(Base):
    __abstract__ = True
    


class Product(Base):
    __tablename__ = "products"

    _uid = Column(String(36), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    id = Column(Integer, nullable=False)
    title = Column(String(150))
    current_price = Column(Numeric)
    color = Column(String(50))
    size = Column(String(50))
    is_active = Column(Boolean)
    quantity = Column(Integer)
