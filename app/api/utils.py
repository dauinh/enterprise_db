import sys
import csv

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert

from models.products import Product


def import_data(Session: sessionmaker) -> None:
    file_path = sys.path[0] + '/../../data/clean_products.csv'
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(row)


    with Session as session:
        for i, row in enumerate(data):
            if i > 0: break
            id, title, _, current_price, _, _, is_active, quantity = row
            
            statement = (
                insert(Product).
                values(id=id, title=title, current_price=float(current_price),
                    is_active=bool(is_active), quantity=quantity)
            )
            try:
                session.execute(statement)
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()
        
        statement = select(Product)
        rows = session.execute(statement)
        print(next(rows))
    
