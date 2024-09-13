import uuid, enum
from datetime import datetime, UTC

from sqlalchemy import DateTime, Table, ForeignKey, Column, Integer, String, Boolean, Numeric, Enum
from sqlalchemy.orm import relationship

from app.api.db import Base


class Status(enum.Enum):
    complete = 1
    pending = 2
    refunded = 3

class Gender(enum.Enum):
    male = 1
    female = 2

class Location(enum.Enum):
    New_York = 1
    Boston = 2
    Portland = 3


# Relationship table between Product and Collection
product_collection = Table(
    "product_collection",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.id")),
    Column("collection_id", Integer, ForeignKey("collection.id")),
)

# Relationship table between ProductAttribute and Transaction
class Sales(Base):
    __tablename__ = "sales"

    transaction_id = Column(ForeignKey("transaction.id"), primary_key=True)
    product_attribute_id = Column(ForeignKey("product_attribute.id"), primary_key=True)

    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(precision=2), nullable=False)

    product_attributes = relationship("ProductAttribute", back_populates="transactions")
    transactions = relationship("Transaction", back_populates="product_attributes")


class Product(Base):
    __tablename__ = "product"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    title = Column(String(150))
    cost = Column(Numeric(precision=2))
    is_active = Column(Boolean)
    total_quantity = Column(Integer)

    collections = relationship(
        "Collection", secondary=product_collection, back_populates="products"
    )
    attributes = relationship("ProductAttribute", back_populates="products")
    # transactions = relationship("Transaction", back_populates="products")


class Collection(Base):
    __tablename__ = "collection"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    name = Column(String(150))

    products = relationship(
        "Product", secondary=product_collection, back_populates="collections"
    )


class ProductAttribute(Base):
    __tablename__ = "product_attribute"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    product_id = Column(ForeignKey("product.id"))
    color = Column(String(50))
    size = Column(String(50))
    
    cost = Column(Numeric(precision=2))
    quantity = Column(Integer)
    is_active = Column(Boolean)


class User(Base):
    __tablename__ = "user"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    birth_year = Column(Integer)
    gender = Column(Enum(Gender))
    location = Column(Enum(Location))

    transactions = relationship("Transaction", back_populates="users")


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    user_id = Column(ForeignKey("user.id"), nullable=False)
    status = Column(Enum(Status))
    timestamp = Column(DateTime, default=datetime.now(UTC))
