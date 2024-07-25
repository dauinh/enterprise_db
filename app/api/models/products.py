from sqlalchemy import Column, Integer, String, Boolean

from ..db import Base


class Product(Base):
    __tablename__ = "products"

    # _uid = Column(String(36), primary_key=True, nullable=False, unique=True, default=uuid.uuid4)
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    title = Column(String(150))
    # collections = Column(list[String])
    current_price = Column(Integer)
    # colors = Column(list[String])
    # sizes = Column(list[String])
    is_active = Column(Boolean)
    quantity = Column(Integer)
