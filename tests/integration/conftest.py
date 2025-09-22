import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.db.models import Base, User
from src.db.configurations import get_db_session as get_db
from src.services.auth import create_access_token
from src.services.utils import Hash
from src.conf.config import config
from tests.conftest import mock_user

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap(mock_user: User):
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = Hash().get_password_hash(mock_user.hashed_password)
            current_user = User(
                name=mock_user.name,
                surname=mock_user.surname,
                email=mock_user.email,
                hashed_password=hash_password,
                is_verified=mock_user.is_verified,
                avatar=mock_user.avatar,
            )
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def client():
    # Dependency override

    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception as err:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest_asyncio.fixture()
async def get_token(mock_user: User):
    token = await create_access_token(
        data={"sub": mock_user.email},
        expires_delta=24 * config.JWT_EXPIRATION_SECONDS,
    )
    return token


@pytest_asyncio.fixture()
async def get_admin_token(mock_admin_user: User):
    token = await create_access_token(
        data={"sub": mock_admin_user.email},
        expires_delta=24 * config.JWT_EXPIRATION_SECONDS,
    )
    return token
