import sys
import csv

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert

from .models.products import Product
from .db import engine, SessionLocal, Base


def insert_products(Session: sessionmaker) -> None:
    file_path = sys.path[0] + "/../data/clean_products.csv"
    data = []
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(row)

    with Session as session:
        for i, row in enumerate(data):
            if i > 0: break
            id, title, _, current_price, color, size, is_active, quantity = row

            statement = insert(Product).values(
                id=id,
                title=title,
                current_price=float(current_price) if current_price else 0,
                color=color if color else "",
                size=size if size else "",
                is_active=bool(is_active),
                quantity=quantity,
            )
            try:
                session.execute(statement)
                session.commit()
            except Exception as e:
                print(e)
                print("Cannot insert", title)
                session.rollback()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    insert_products(db)

    with db as session:
        statement = select(Product.title)
        rows = session.execute(statement).all()
        for r in rows:
            print(r)
        