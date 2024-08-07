# https://johncox-38620.medium.com/creating-a-test-database-pytest-sqlalchemy-97356f2f02d2
import os
import pytest
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import sessionmaker

from app.api.db import Base
from app.api.models import Product, Collection, Attribute, ProductAttribute

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
    # define sample data items
    product1 = Product(
        title="hello world",
        current_price=2.5,
        is_active=True,
        total_quantity=15,
    )
    product2 = Product(
        title="toilet toy",
        current_price=7.99,
        is_active=True,
        total_quantity=5,
    )
    collection1 = Collection(name="everyday-tableware")
    collection2 = Collection(name="anniversary-best-sellers")

    product1_a1 = ProductAttribute(quantity=5)
    product1_a2 = ProductAttribute(quantity=5)
    product1_a3 = ProductAttribute(quantity=5)
    product2_a1 = ProductAttribute(quantity=5)

    product1_a1.attributes = Attribute(color='pink', size='small')
    product1_a2.attributes = Attribute(color='pink', size='medium')
    product1_a3.attributes = Attribute(color='pink', size='large')
    product2_a1.attributes = Attribute(color='white', size='')

    product1.attributes.append(product1_a1)
    product1.attributes.append(product1_a2)
    product1.attributes.append(product1_a3)
    product2.attributes.append(product2_a1)

    db_session.add_all([product1, product2, collection1, collection2])

    # add relationships
    product1.collections.append(collection1)
    product1.collections.append(collection2)
    product2.collections.append(collection2)

    collection1.products.append(product1)
    collection2.products.append(product2)
    collection2.products.append(product1)

    db_session.commit()
