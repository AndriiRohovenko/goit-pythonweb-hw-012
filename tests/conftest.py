import pytest
from src.db.models import User, Contacts


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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
