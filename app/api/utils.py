import sys
import csv

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.api.db import engine, SessionLocal, Base
from app.api.models import Product, Collection


def insert_products(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/product.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            row['id'] = i + 1
            try:
                row["current_price"] = (
                    float(row["current_price"]) if row["current_price"] else 0.0
                )
            except ValueError:
                row["current_price"] = 0.0

            # try:
            #     row["color"] = row["color"] if row["color"] else ""
            # except ValueError:
            #     row["color"] = ""

            # try:
            #     row["size"] = row["size"] if row["size"] else ""
            # except ValueError:
            #     row["size"] = ""

            try:
                row["is_active"] = bool(row["is_active"])
            except ValueError:
                row["is_active"] = True

            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            # if i < 12335: continue
            product = Product(**row)
            session.add(product)
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
            row['id'] = i + 1
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            collection = Collection(**row)
            session.add(collection)
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
            row['product_id'] = int(row['product_id']) + 1
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            if i < 1: continue
            stmt = select(Collection).where(Collection.name == row['collection'])
            collection = session.scalars(stmt).one()
            # print(row['collection'], collection.id)
            stmt = select(Product).where(Product.id == row['product_id'])
            product = session.scalars(stmt).one()
            product.collections.append(collection)
            session.add(collection)
            try:
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", row)
                session.rollback()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # insert_products(db)
    # insert_collections(db)
    insert_belongs(db)
