import pytest

from app.api.models import Collection
from app.api.repos.collection import get_all, get_all_products_from_collection


def test_get_all(db_session, seed):
    collections = get_all(db_session)
    assert len(collections) == 2
    for c in collections:
        assert type(c) == Collection


def test_get_all_products_from_collection(db_session, seed):
    from_collection1 = get_all_products_from_collection(db_session, 1)
    from_collection2 = get_all_products_from_collection(db_session, 2)
    assert len(from_collection1) == 1
    assert len(from_collection2) == 2
