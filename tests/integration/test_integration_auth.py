import pytest
from src.schemas.auth import UserCreate, UserSchema, Token, RefreshTokenRequest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from src.db.models import User
from sqlalchemy.future import select
from tests.integration.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_register_user(client: TestClient, monkeypatch):
    user_data = UserCreate(
        name="newuser",
        surname="New",
        email="newuser@example.com",
        password="password",
        role="user",
    )

    mock_send_email = Mock()
    monkeypatch.setattr("src.services.email.send_verification_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data.model_dump())

    assert response.status_code == 201
    data = response.json()
    UserSchema.model_validate(data)
    assert data["email"] == user_data.email
    assert "id" in data
    assert data["name"] == user_data.name
    assert data["surname"] == user_data.surname
    assert data["role"] == user_data.role
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_login_user(client: TestClient, mock_user):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(
            select(User).where(User.email == mock_user.email)
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.is_verified = True
            await session.commit()
        response = client.post(
            "api/auth/login",
            data={"username": mock_user.email, "password": mock_user.hashed_password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    assert response.status_code == 200
    data = response.json()
    Token.model_validate(data)
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_token(client: TestClient, mock_user):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(
            select(User).where(User.email == mock_user.email)
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.is_verified = True
            await session.commit()

        data = RefreshTokenRequest(refresh_token=current_user.refresh_token)
        response = client.post("api/auth/refresh", json=data.model_dump())

    assert response.status_code == 200
    data = response.json()
    print(f"Response data: {data}")
    Token.model_validate(data)
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data
