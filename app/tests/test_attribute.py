import pytest

from app.api.repos.attribute import get_product_attr


def test_get_product_attr(db_session, seed):
    product1_attributes = get_product_attr(db_session, 1)
    sizes = []
    assert len(product1_attributes) == 3
    for attr in product1_attributes:
        assert attr['quantity'] == 5
        assert attr['color'] == 'pink'
        sizes.append(attr['size'])
    assert sizes == ['small', 'medium', 'large']

    product2_attributes = get_product_attr(db_session, 2)
    assert len(product2_attributes) == 1
    for attr in product2_attributes:
        assert attr['quantity'] == 5
        assert attr['color'] == 'white'
        assert attr['size'] == ''