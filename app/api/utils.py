import sys, csv
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.api.db import engine, SessionLocal, Base
from app.api.models import (
    Product,
    Collection,
    Attribute,
    ProductAttribute,
    User,
    Gender,
    Location,
)


def insert_products(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/product.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row["id"] = i + 1
            try:
                row["cost"] = float(row["cost"]) if row["cost"] else None
            except ValueError:
                row["cost"] = None
            try:
                row["is_active"] = bool(row["is_active"])
            except ValueError:
                row["is_active"] = True

            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            # if i < 12335: continue
            session.add(Product(**row))
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row["title"])
                session.rollback()


def insert_collections(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/collection.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row["id"] = i + 1
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            session.add(Collection(**row))
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row["name"])
                session.rollback()


def insert_belongs(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/belongs.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row["product_id"] = int(row["product_id"]) + 1
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            # if i < 1: continue
            stmt = select(Collection).where(Collection.name == row["collection"])
            collection = session.scalars(stmt).one()
            # print(row['collection'], collection.id)
            stmt = select(Product).where(Product.id == row["product_id"])
            product = session.scalars(stmt).one()
            product.collections.append(collection)
            session.add(collection)
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row)
                session.rollback()


def insert_attr(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/attribute.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row["id"] = i + 1
            try:
                row["color"] = row["color"] if row["color"] else None
            except ValueError:
                row["color"] = None

            try:
                row["size"] = row["size"] if row["size"] else None
            except ValueError:
                row["size"] = None
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            session.add(Attribute(**row))
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row)
                session.rollback()


def insert_product_attr(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/product_attr.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row["product_id"] = int(row["product_id"]) + 1
            try:
                row["color"] = row["color"] if row["color"] else None
            except ValueError:
                row["color"] = None
            try:
                row["size"] = row["size"] if row["size"] else None
            except ValueError:
                row["size"] = None
            try:
                row["is_active"] = bool(row["is_active"])
            except ValueError:
                row["is_active"] = True
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            # if i < 7885: continue
            # if i > 7886: break
            association = ProductAttribute(
                is_active=row["is_active"], quantity=row["quantity"]
            )
            stmt = select(Attribute).where(
                Attribute.color == row["color"], Attribute.size == row["size"]
            )
            try:
                attr = session.scalars(stmt).one()
            except:
                print(row, attr.color, attr.size)
            stmt = select(Product).where(Product.id == row["product_id"])
            product = session.scalars(stmt).one()

            association.attributes = attr
            product.attributes.append(association)
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row)
                session.rollback()


def insert_user(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/user.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # if i > 5: break
            new_row = {
                "id": row["user_id"],
                "birth_year": datetime.now().year - int(row["age"]),
                "gender": (
                    Gender.female if row["gender"] == "['Female']" else Gender.male
                ),
            }

            if row["location"] == "['New York']":
                new_row["location"] = Location.New_York
            elif row["location"] == "['Boston']":
                new_row["location"] = Location.Boston
            elif row["location"] == "['Portland']":
                new_row["location"] = Location.Portland

            data.append(new_row)

    with Session as session:
        for i, row in enumerate(data):
            session.add(User(**row))
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row["title"])
                session.rollback()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # insert_products(db)
    # insert_collections(db)
    # insert_belongs(db)
    # insert_attr(db)
    # insert_product_attr(db)
    insert_user(db)
