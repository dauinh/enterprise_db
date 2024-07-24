import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Create connection string
url = URL.create(
    "mysql+mysqlconnector",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host="localhost",
    database=os.getenv("DB_NAME"),
    port=3306
)

# Establish connection via SQLAlchemy
engine = create_engine(url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

# Import data
from models.products import Product, Base
from sqlalchemy import select


# with Session() as session:
#     statement = select(Product)
#     rows = session.execute(statement)
#     for r in rows:
#         print(r)
    
