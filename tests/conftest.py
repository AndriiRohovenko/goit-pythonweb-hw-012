import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User, Contacts
from src.repository.users import UserRepository
from src.repository.contacts import ContactsRepository


# ------------------------
# Users
# ------------------------
@pytest.fixture
def mock_user():
    return User(
        id=1,
        name="Test",
        surname="User",
        email="test@example.com",
        hashed_password="hashedpassword",
        is_verified=True,
        role="user",
        avatar=None,
        refresh_token="12345",
    )


@pytest.fixture
def mock_user_db_session(mock_user):
    mock_session = MagicMock(spec=AsyncSession)

    # async methods
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.delete = AsyncMock()

    # mock execute for user repo
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_user]
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = mock_result

    mock_session.add = MagicMock()
    yield mock_session


@pytest.fixture
def mock_user_repo(mock_user_db_session):
    return UserRepository(db=mock_user_db_session)


# ------------------------
# Contacts
# ------------------------
@pytest.fixture
def mock_contact(mock_user):
    return Contacts(
        id=1,
        name="John",
        email="john@example.com",
        phone="1234567890",
        birthdate=None,
        avatar=None,
        user_id=mock_user.id,
    )


@pytest.fixture
def mock_contacts_db_session(mock_contact):
    mock_session = MagicMock(spec=AsyncSession)

    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.delete = AsyncMock()

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_contact]
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_session.execute.return_value = mock_result

    mock_session.add = MagicMock()
    yield mock_session


@pytest.fixture
def mock_contacts_repo(mock_contacts_db_session):
    return ContactsRepository(db=mock_contacts_db_session)
