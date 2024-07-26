from sqlalchemy import Column, Integer, String, Boolean
import uuid

from api.db import Base


class Product(Base):
    __tablename__ = "products"

    _uid = Column(String(36), primary_key=True, nullable=False, unique=True, default=str(uuid.uuid1()))
    id = Column(Integer, nullable=False, unique=True)
    title = Column(String(150))
    # collections = Column(list[String])
    current_price = Column(Integer)
    color = Column(String(50))
    size = Column(String(50))
    is_active = Column(Boolean)
    quantity = Column(Integer)
