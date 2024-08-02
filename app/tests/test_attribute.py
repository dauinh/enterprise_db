import pytest

from app.api.models import Attribute
from app.api.repos.attribute import get_product_attribute


def test_get_product_attribute(db_session, seed):
    product1_attributes = get_product_attribute(db_session, 1)
    product2_attributes = get_product_attribute(db_session, 2)
    assert type(product1_attributes) == Attribute
    assert product1_attributes.color == 'pink'
    assert product1_attributes.size == 'medium'

    assert type(product2_attributes) == Attribute
    assert product2_attributes.color == 'white'
    assert product1_attributes.size == ''
