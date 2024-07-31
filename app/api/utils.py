import sys
import csv

from sqlalchemy.orm import sessionmaker

from .models.products import Product
from .db import engine, SessionLocal, Base


def insert_products(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/products.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        next(reader)
        for row in reader:
            try:
                row["current_price"] = (
                    float(row["current_price"]) if row["current_price"] else 0.0
                )
            except ValueError:
                row["current_price"] = 0.0

            try:
                row["color"] = row["color"] if row["color"] else ""
            except ValueError:
                row["color"] = ""

            try:
                row["size"] = row["size"] if row["size"] else ""
            except ValueError:
                row["size"] = ""

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


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    insert_products(db)
