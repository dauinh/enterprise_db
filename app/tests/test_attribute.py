import pytest

from app.api.models import Attribute
from app.api.repos.attribute import get_product_attribute


def test_get_product_attribute(db_session, seed):
    product1_attributes = get_product_attribute(db_session, 1)
    product2_attributes = get_product_attribute(db_session, 2)
    attr = product1_attributes[0]
    assert type(attr) == Attribute
    assert attr.color == 'pink'
    assert attr.size == 'medium'

    attr = product2_attributes[0]
    assert type(attr) == Attribute
    assert attr.color == 'white'
    assert attr.size == ''
