import os

import mysql.connector
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
    port=5432
)

# Establish connection via SQLAlchemy
engine = create_engine(url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
