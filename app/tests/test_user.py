import pytest
import asyncio

from sqlalchemy import select

from app.api.models import User, Gender, Location
from app.api.repos.user import get_total, get_by_id, get_all, create

pytest_plugins = ("pytest_asyncio",)


def test_get_total(db_session, seed):
    assert get_total(db_session) == 2


def test_get_by_id(db_session, seed):
    user = get_by_id(db_session, 1)
    assert user.id == 1
    assert user.birth_year == 1995
    assert user.gender == Gender.female
    assert user.location == Location.Boston


def test_get_all(db_session, seed):
    users = get_all(db_session)
    assert len(users) == 2
    assert users[0].birth_year == 1995
    assert users[1].birth_year == 2002


@pytest.mark.asyncio
async def test_create(db_session, seed):
    await create(
        db_session,
        User(birth_year=1989, gender=Gender.female, location=Location.Boston),
    )
    new_user = db_session.query(User).filter_by(birth_year=1989).one()
    assert new_user.id == 3
    assert new_user.gender == Gender.female
    assert new_user.location == Location.Boston
