import pytest
import asyncio

from sqlalchemy import select

from app.api.models.product import Product
from app.api.repos.product import (
    get_total,
    get_by_id,
    get_by_title,
    get_all,
    create,
    update_by_id,
    delete_by_id,
)

pytest_plugins = ('pytest_asyncio',)

def test_get_total(db_session, seed):
    assert get_total(db_session) == 2


def test_get_by_id(db_session, seed):
    product = get_by_id(db_session, 1)
    assert product.id == 1
    assert product.title == "hello world"


def test_get_by_title(db_session, seed):
    product = get_by_title(db_session, "hello world")
    assert product.id == 1


def test_get_all(db_session, seed):
    products = get_all(db_session)
    assert len(products) == 2


@pytest.mark.skip
@pytest.mark.asyncio
async def test_create(db_session, seed):
    await create(
        Product(
            id=2,
            title="elephant plushie",
            current_price=14.99,
            is_active=True,
            quantity=20,
        )
    )
    new_product = await db_session.query(Product).filter_by(title="elephant plushie").one()
    assert new_product.id == 2
    assert new_product.color == "blue"
    assert new_product.size == ""
    assert new_product.quantity == 20


@pytest.mark.asyncio
async def test_update_by_id(db_session, seed):
    stmt = select(Product).where(Product.id == 1)
    product = db_session.scalars(stmt).one()
    assert product.title == "hello world"
    await update_by_id(db_session, Product(
        id=1,
        title="elephant plushie",
        current_price=14.99,
        is_active=True,
        total_quantity=20,
    ))
    stmt = select(Product).where(Product.id == 1)
    updated = db_session.scalars(stmt).one()
    assert updated.title == "elephant plushie"


@pytest.mark.asyncio
async def test_delete_by_id(db_session, seed):
    await delete_by_id(db_session, 1)
    assert get_total(db_session) == 1
