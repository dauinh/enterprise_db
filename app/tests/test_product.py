import pytest
import asyncio

from sqlalchemy import select

from app.api.models import Product
from app.api.repos.product import (
    get_total,
    get_by_id,
    get_by_title,
    get_all,
    create,
    update,
    delete,
    is_attr_quantities_equal_total,
)

pytest_plugins = ("pytest_asyncio",)


def test_get_total(db_session, seed):
    assert get_total(db_session) == 2


def test_get_by_id(db_session, seed):
    product = get_by_id(db_session, 1)
    assert product.id == 1
    assert product.title == "elephant spoon"
    assert product.cost == 2.5
    assert product.total_quantity == 15
    sizes = []
    for attr in product.attributes:
        assert attr.quantity == 5
        assert attr.color == "pink"
        sizes.append(attr.size)
    assert sizes == ["small", "medium", "large"]


def test_get_by_title(db_session, seed):
    product = get_by_title(db_session, "toilet toy")
    assert product.id == 2
    assert product.cost == 7.99
    assert product.total_quantity == 5
    for attr in product.attributes:
        assert attr.quantity == 5
        assert attr.color == "white"
        assert attr.size == ""


def test_get_all(db_session, seed):
    products = get_all(db_session)
    assert len(products) == 2
    assert products[0].title == "elephant spoon"
    assert products[1].title == "toilet toy"


def test_is_attr_quantities_equal_total(db_session, seed):
    assert is_attr_quantities_equal_total(db_session, 1) == True
    assert is_attr_quantities_equal_total(db_session, 2) == True


@pytest.mark.asyncio
async def test_create(db_session, seed):
    await create(
        db_session,
        Product(
            title="tiger plushie",
            cost=14.99,
            is_active=True,
            total_quantity=20,
        ),
    )
    new_product = db_session.query(Product).filter_by(title="tiger plushie").one()
    assert new_product.id == 3
    assert new_product.cost == 14.99
    assert new_product.total_quantity == 20


@pytest.mark.asyncio
async def test_update(db_session, seed):
    stmt = select(Product).where(Product.id == 1)
    product = db_session.scalars(stmt).one()
    assert product.title == "elephant spoon"
    await update(
        db_session,
        Product(
            id=1,
            title="elephant bowl",
            cost=14.99,
            is_active=True,
            total_quantity=20,
        ),
    )
    stmt = select(Product).where(Product.id == 1)
    updated = db_session.scalars(stmt).one()
    assert updated.title == "elephant bowl"
    assert updated.cost == 14.99
    assert updated.total_quantity == 20


@pytest.mark.asyncio
async def test_delete(db_session, seed):
    stmt = select(Product).where(Product.id == 3)
    product = db_session.scalars(stmt).one()
    await delete(db_session, product)
    assert get_total(db_session) == 2
