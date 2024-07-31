import pytest

from api.models.products import Product
from api.routers.products import get_total


def test_product(db_session, seed):
    res = db_session.query(Product).first()
    assert res.title == "hello world"
    assert res.id == 0


def test_get_total(db_session, seed):
    res = db_session.query(Product).all()
    assert get_total(db_session) == 1
