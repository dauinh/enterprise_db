import pytest

from api.models.products import Product


def test_product(db_session):
    product = Product(
        id=0,
        title="hello world",
        current_price=2.5,
        color="",
        size="",
        is_active=True,
        quantity=15
    )
    db_session.add(product)
    db_session.commit()

    res = db_session.query(Product).first()
    assert res.title == "hello world"
    assert res.id == 0