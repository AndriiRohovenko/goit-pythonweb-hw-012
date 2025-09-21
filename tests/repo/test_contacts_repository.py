import pytest
from src.db.models import Contacts
from src.schemas.contacts import ContactSchema
from datetime import date


@pytest.mark.asyncio
async def test_get_all_contacts(mock_contacts_repo, mock_user):
    result = await mock_contacts_repo.get_all(limit=10, skip=0, user=mock_user)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Contacts)
    assert result[0].email == "john@example.com"


@pytest.mark.asyncio
async def test_get_contact_by_id(mock_contacts_repo, mock_user, mock_contact):
    result = await mock_contacts_repo.get_by_id(contact_id=1, user=mock_user)
    assert result == mock_contact


@pytest.mark.asyncio
async def test_get_contact_by_email(mock_contacts_repo, mock_user, mock_contact):
    result = await mock_contacts_repo.get_by_email(
        email="john@example.com", user=mock_user
    )
    assert result == mock_contact


@pytest.mark.asyncio
async def test_create_contact(mock_contacts_repo, mock_contacts_db_session, mock_user):
    contact_data = ContactSchema(
        name="John",
        email="john@example.com",
        phone="1234567890",
        birthdate=date(1990, 1, 1),
        avatar=None,
        user_id=mock_user.id,
    )
    result = await mock_contacts_repo.create(contact_data, user=mock_user)
    assert isinstance(result, Contacts)
    assert result.email == contact_data.email
    assert result.name == contact_data.name
    assert result.phone == contact_data.phone
    assert result.birthdate == contact_data.birthdate
    mock_contacts_db_session.add.assert_called_once_with(result)
    mock_contacts_db_session.commit.assert_awaited_once()
    mock_contacts_db_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_update_contact(
    mock_contacts_repo, mock_contacts_db_session, mock_contact
):
    update_data = {"name": "Jane", "surname": "Smith"}
    await mock_contacts_repo.update(mock_contact, update_data)
    assert mock_contact.name == "Jane"
    assert mock_contact.surname == "Smith"
    mock_contacts_db_session.commit.assert_awaited_once()
    mock_contacts_db_session.refresh.assert_awaited_once_with(mock_contact)


@pytest.mark.asyncio
async def test_delete_contact(
    mock_contacts_repo, mock_contacts_db_session, mock_contact
):
    await mock_contacts_repo.delete(mock_contact)
    mock_contacts_db_session.delete.assert_awaited_once_with(mock_contact)
    mock_contacts_db_session.commit.assert_awaited_once()
