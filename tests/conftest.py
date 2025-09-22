import pytest
from src.db.models import User, Contacts


@pytest.fixture(scope="session")
def mock_user():
    return User(
        name="Test",
        surname="User",
        email="test@example.com",
        hashed_password="hashedpassword",
        is_verified=False,
        role="user",
        avatar=None,
    )


@pytest.fixture(scope="session")
def mock_admin_user():
    return User(
        name="Admin",
        surname="User",
        email="admin@example.com",
        hashed_password="hashedpassword",
        is_verified=True,
        role="admin",
        avatar=None,
    )


@pytest.fixture(scope="session")
def mock_contact():
    return Contacts(
        name="John",
        email="john@example.com",
        phone="1234567890",
        birthdate="1990-01-01",
        avatar=None,
        user_id=1,
    )
