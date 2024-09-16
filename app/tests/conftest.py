# https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2
import os
import pytest
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import sessionmaker

from app.api.db import Base
from app.api.models import (
    Product,
    Collection,
    ProductAttribute,
    User,
    Gender,
    Location,
    Transaction,
    Status,
)

load_dotenv()
TEST_DB_NAME = f'{os.getenv("DB_NAME")}_test'

url = URL.create(
    "mysql+mysqlconnector",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host="localhost",
    database=TEST_DB_NAME,
    port=3306,
)


def drop_create_test_db():
    # Create connection string without specify which database
    engine = create_engine(
        URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            host="localhost",
            port=3306,
        )
    )

    try:
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=False)
            try:
                conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
            except ProgrammingError:
                print("Could not drop the database, probably does not exist.")
            except OperationalError:
                print(
                    "Could not drop database because it’s being accessed by other users"
                )

            conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))
            print(f"{TEST_DB_NAME} created!")
    except Exception as e:
        print(f"Some other error", e)


@pytest.fixture(scope="session", autouse=True)
def engine():
    engine = create_engine(url, echo=True)
    yield engine
    engine.dispose()
    drop_create_test_db()


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def db_session(engine, tables):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.rollback()
    db_session.close()


@pytest.fixture(scope="session")
def seed(db_session):
    # define sample product items
    product1 = Product(
        title="elephant spoon",
        cost=2.5,
        is_active=True,
        total_quantity=15,
        attributes=[
            ProductAttribute(quantity=5, color="pink", size="small"),
            ProductAttribute(quantity=5, color="pink", size="medium"),
            ProductAttribute(quantity=5, color="pink", size="large"),
        ],
    )
    product2 = Product(
        title="toilet toy",
        cost=7.99,
        is_active=True,
        total_quantity=5,
        attributes=[ProductAttribute(quantity=5, color="white", size="")],
    )
    collection1 = Collection(name="everyday-tableware")
    collection2 = Collection(name="anniversary-best-sellers")

    # add relationships
    # collection1: product1
    # collection2: product1, product2
    product1.collections.append(collection1)
    product1.collections.append(collection2)
    product2.collections.append(collection2)

    db_session.add_all([product1, product2, collection1, collection2])
    db_session.commit()

    # define sample user and transaction items
    user1 = User(birth_year=1995, gender=Gender.female, location=Location.Boston)
    user2 = User(birth_year=2002, gender=Gender.male, location=Location.New_York)

    # transaction1 = Transaction(
    #     user_id=user1.id,
    #     product_id=product1.id,
    #     quantity=2,
    #     price=product1.price * 2,
    #     status=Status.complete
    # )

    db_session.add_all([user1, user2])
    db_session.commit()
