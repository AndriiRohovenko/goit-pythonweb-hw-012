import pytest
from src.schemas.users import UserUploadAvatarResponceSchema
from src.schemas.auth import UserSchema
from fastapi.testclient import TestClient
from unittest.mock import Mock
from src.db.models import User
from sqlalchemy.future import select
from tests.integration.conftest import TestingSessionLocal
from src.conf.config import config
from src.db.models import UserRole


@pytest.mark.asyncio
async def test_get_me(client: TestClient, mock_user, get_token):
    response = client.get(
        "api/users/me", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    UserSchema.model_validate(data)
    assert data["email"] == mock_user.email
    assert data["name"] == mock_user.name
    assert data["surname"] == mock_user.surname
    assert data["role"] == mock_user.role
    assert "id" in data


# @pytest.mark.asyncio
# async def test_update_user_avatar_by_admin(
#     client: TestClient, mock_admin_user, get_admin_token
# ):
#     print(f"token: {get_admin_token}")
#     async with TestingSessionLocal() as session:
#         result = await session.execute(
#             select(User).where(User.email == mock_admin_user.email)
#         )
#         user_in_db = result.scalars().first()
#         print(f"user role: {user_in_db.role}")
#         print(f"admin email: {mock_admin_user.email}")
#     with open("tests/files/test_image.jpg", "rb") as image_file:
#         response = client.patch(
#             "/api/users/avatar",
#             headers={"Authorization": f"Bearer {get_admin_token}"},
#             files={"file": ("test_image.jpg", image_file, "image/jpeg")},
#         )
#     assert response.status_code == 200
#     data = response.json()
#     UserUploadAvatarResponceSchema.model_validate(data)
#     assert "avatar" in data
#     # Verify that the avatar URL is updated in the database
#     async with TestingSessionLocal() as session:
#         result = await session.execute(
#             select(User).where(User.email == mock_admin_user.email)
#         )
#         user_in_db = result.scalars().first()
#         assert user_in_db.avatar == data["avatar"]
