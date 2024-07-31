import pytest

from app.api.models.product import Product
from app.api.routers.product import (
    get_total,
    get_by_id,
    get_by_title,
    get_all,
    create,
    update,
    delete_by_id,
)


def test_product(db_session, seed):
    res = db_session.query(Product).first()
    assert res.id == 0
    assert res.title == "hello world"


def test_get_total(db_session, seed):
    assert get_total(db_session) == 1


def test_get_product_by_id(db_session, seed):
    product = get_by_id(db_session, 0)
    assert product.id == 0
    assert product.title == "hello world"


def test_get_by_title(db_session, seed):
    product = get_by_title(db_session, "hello world")
    assert product.id == 0


def test_get_all(db_session, seed):
    products = get_all(db_session)
    assert len(products) == 2


def test_create(db_session, seed):
    create(
        Product(
            id=2,
            title="elephant plushie",
            current_price=14.99,
            color="blue",
            size="",
            is_active=True,
            quantity=20,
        )
    )
    new_product = db_session.query(Product).filter_by(title="elephant plushie")
    assert new_product.id == 2
    assert new_product.color == "blue"
    assert new_product.size == ""
    assert new_product.quantity == 20


def test_update_product(db_session, seed):
    product = get_by_id(db_session, 0)
    assert product.title == "hello world"
    update(
        id=0,
        title="elephant plushie",
        current_price=14.99,
        color="blue",
        size="",
        is_active=True,
        quantity=20,
    )
    updated = db_session.query(Product).filter_by(title="elephant plushie").all()
    assert len(update) == 1
    assert updated[0].id == 0


def test_delete_by_id(db_session, seed):
    delete_by_id(1)
    assert get_total(db_session) == 1
