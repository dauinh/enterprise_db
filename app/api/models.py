import uuid

from sqlalchemy import Table, ForeignKey, Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship

from app.api.db import Base


# Relationship table between Product and Collection
product_collection = Table(
    "product_collection",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.id")),
    Column("collection_id", Integer, ForeignKey("collection.id")),
)


# Relationship table between Product and Attribute
class ProductAttribute(Base):
    __tablename__ = "product_attribute"
    product_id_id = Column(ForeignKey("product.id"), primary_key=True)
    attribute_id = Column(ForeignKey("attribute.id"), primary_key=True)
    quantity = Column(Integer)
    products = relationship("Product", back_populates="attributes")
    attributes = relationship("Attribute", back_populates="products")


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
        "Collection", secondary=product_collection, back_populates="products"
    )
    attributes = relationship("ProductAttribute", back_populates="products")


class Collection(Base):
    __tablename__ = "collection"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    name = Column(String(150))
    products = relationship("Product", secondary=product_collection, back_populates="collections")


class Attribute(Base):
    __tablename__ = "attribute"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    color = Column(String(50))
    size = Column(String(50))
    products = relationship("ProductAttribute", back_populates="attributes")