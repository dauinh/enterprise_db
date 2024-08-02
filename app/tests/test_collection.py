import pytest

from app.api.repos.collection import get_all
from app.api.models import Collection


def test_get_all(db_session, seed):
    collections = get_all(db_session)
    assert len(collections) == 2
    for c in collections:
        assert type(c) == Collection

