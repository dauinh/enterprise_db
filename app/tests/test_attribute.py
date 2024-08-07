import pytest

from app.api.models import ProductAttribute, Attribute
from app.api.repos.attribute import get_product_attribute


def test_get_product_attribute(db_session, seed):
    product1_attributes = get_product_attribute(db_session, 1)
    product2_attributes = get_product_attribute(db_session, 2)
    sizes = []
    for assoc in product1_attributes:
        assert type(assoc) == ProductAttribute
        assert assoc.quantity == 5
        assert type(assoc.attributes) == Attribute
        assert assoc.attributes.color == 'pink'
        sizes.append(assoc.attributes.size)
    assert sizes == ['small', 'medium', 'large']

    assoc = product2_attributes[0]
    assert type(assoc) == ProductAttribute
    assert assoc.quantity == 5
    assert type(assoc.attributes) == Attribute
    assert assoc.attributes.color == 'white'
    assert assoc.attributes.size == ''
