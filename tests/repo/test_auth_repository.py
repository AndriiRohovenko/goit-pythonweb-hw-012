import pytest
from src.schemas.auth import UserCreate
from src.db.models import User


@pytest.mark.asyncio
async def test_get_all_users(mock_user_repo):
    result = await mock_user_repo.get_all(limit=10, skip=0)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], User)
    assert result[0].email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id(mock_user_repo, mock_user):

    result = await mock_user_repo.get_by_id(mock_user.id)
    assert isinstance(result, User)
    assert result.id == mock_user.id
    assert result == mock_user
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email(mock_user_repo, mock_user):
    email = mock_user.email
    result = await mock_user_repo.get_by_email(email)
    assert isinstance(result, User)
    assert result == mock_user
    assert result.email == email


@pytest.mark.asyncio
async def test_create_user(mock_user_repo, mock_user_db_session):
    # Setup
    user_create_data = UserCreate(
        name="testuser",
        surname="Test",
        email="testuser@example.com",
        password="password",
    )

    result = await mock_user_repo.create(user_create_data)

    # Assertions
    assert isinstance(result, User)
    assert result.email == "testuser@example.com"
    assert result.surname == "Test"
    assert result.name == "testuser"
    mock_user_db_session.add.assert_called_once()
    mock_user_db_session.commit.assert_awaited_once()
    mock_user_db_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_update_user(mock_user_repo, mock_user_db_session, mock_user):
    # Setup
    update_data = {"name": "updatedname", "surname": "Updated"}

    result = await mock_user_repo.update(mock_user, update_data)

    # Assertions
    assert isinstance(result, User)
    assert result.name == "updatedname"
    assert result.surname == "Updated"
    mock_user_db_session.commit.assert_awaited_once()
    mock_user_db_session.refresh.assert_awaited_once_with(mock_user)


@pytest.mark.asyncio
async def test_delete_user(mock_user_repo, mock_user_db_session, mock_user):
    result = await mock_user_repo.delete(mock_user)
    assert result is True
    mock_user_db_session.add.assert_not_called()
    mock_user_db_session.commit.assert_awaited_once()
    mock_user_db_session.refresh.assert_not_awaited()


@pytest.mark.asyncio
async def test_confirm_user_email(mock_user_repo, mock_user_db_session, mock_user):
    await mock_user_repo.confirm_email(mock_user)
    assert mock_user.is_verified is True
    mock_user_db_session.commit.assert_awaited_once()
    mock_user_db_session.refresh.assert_awaited_once_with(mock_user)


@pytest.mark.asyncio
async def test_update_avatar_url(mock_user_repo, mock_user_db_session, mock_user):
    new_avatar_url = "http://example.com/new_avatar.png"
    result = await mock_user_repo.update_avatar_url(mock_user.email, new_avatar_url)
    assert result is None
    assert mock_user.avatar == new_avatar_url
    mock_user_db_session.commit.assert_awaited_once()
    mock_user_db_session.refresh.assert_awaited_once_with(mock_user)


@pytest.mark.asyncio
async def test_get_by_refresh_token(mock_user_repo, mock_user):
    user = await mock_user_repo.get_by_email(mock_user.email)
    token = user.refresh_token
    result = await mock_user_repo.get_user_by_refresh_token(token)
    assert isinstance(result, User)
    assert result == mock_user
    assert result.refresh_token == token
    assert result.email == mock_user.email
