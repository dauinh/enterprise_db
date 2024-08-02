import uuid

from sqlalchemy import Table, ForeignKey, Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.db import Base


# Relationship table between Product and Collection
belongs = Table(
    "belongs",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.id")),
    Column("collection_id", Integer, ForeignKey("collection.id")),
)


class Product(Base):
    __tablename__ = "product"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    title = Column(String(150))
    current_price = Column(Numeric)
    is_active = Column(Boolean)
    total_quantity = Column(Integer)
    collections = relationship(
        "Collection", secondary=belongs, back_populates="products"
    )


class Collection(Base):
    __tablename__ = "collection"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    name = Column(String(150))
    products = relationship("Product", secondary=belongs, back_populates="collections")
