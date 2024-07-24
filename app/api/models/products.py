from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class RNA(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    collections = Column(list[String])
    current_price = Column(Integer)
    colors = Column(list[String])
    sizes = Column(list[String])
    is_active = Column(Boolean)
    quantity = Column(Integer)