import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from src.db.models import User
from sqlalchemy.future import select
from tests.integration.conftest import TestingSessionLocal
from src.conf.config import config
from src.db.models import Contacts
from src.schemas.contacts import ContactSchema


@pytest.mark.asyncio
async def test_create_user_contact(client: TestClient, get_token):

    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "birthdate": "1990-01-01",
    }

    response = client.post("/api/contacts/", json=data, headers=headers)

    assert response.status_code == 201
    data = response.json()
    ContactSchema.model_validate(data)
    assert data["name"] == data["name"]
    assert data["email"] == data["email"]
    assert data["phone"] == data["phone"]
    assert data["birthdate"] == data["birthdate"]
    # Verify that the contact is actually in the database
    async with TestingSessionLocal() as session:
        result = await session.execute(
            select(Contacts).where(Contacts.email == data["email"])
        )
        db_contact = result.scalars().first()
        assert db_contact is not None
        assert db_contact.name == data["name"]
        assert db_contact.email == data["email"]
        assert db_contact.phone == data["phone"]
        assert str(db_contact.birthdate) == data["birthdate"]


@pytest.mark.asyncio
async def test_get_user_contacts(client: TestClient, get_token):

    token = get_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/contacts/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        ContactSchema.model_validate(item)


@pytest.mark.asyncio
async def test_get_user_contact_by_id(client: TestClient, get_token):

    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/contacts/{1}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    contact = ContactSchema.model_validate(data)
    assert contact.name == "John Doe"
    assert contact.email == "john@example.com"
    assert contact.phone == "1234567890"
    assert str(contact.birthdate) == "1990-01-01"


@pytest.mark.asyncio
async def test_delete_user_contact(client: TestClient, get_token):

    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/api/contacts/{1}", headers=headers)
    assert response.status_code == 204

    async with TestingSessionLocal() as session:
        result = await session.execute(select(Contacts).where(Contacts.id == 1))
        db_contact = result.scalars().first()
        assert not db_contact
