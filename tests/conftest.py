from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.main import app
from app.models import User
from app.utils.auth_login import verify_token
from app.utils.database import Base, get_db


@pytest_asyncio.fixture
async def client(session):
    async def get_session_override():
        return session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_db] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_with_user(session, user):
    async def get_session_override():
        return session

    async def get_token_override():
        return user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_db] = get_session_override
        app.dependency_overrides[verify_token] = get_token_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_with_admin(session, user_admin):
    async def get_session_override():
        return session

    async def get_token_override():
        return user_admin

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_db] = get_session_override
        app.dependency_overrides[verify_token] = get_token_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_deactivated(session, user_deactivated):
    async def get_session_override():
        return session

    async def get_token_override():
        return user_deactivated

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_db] = get_session_override
        app.dependency_overrides[verify_token] = get_token_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_with_invalid_credentials(session):
    class FakeUser:
        id = 9999  # ID inexistente
        is_admin = True

    async def get_session_override():
        return session

    async def get_token_override():
        return FakeUser()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_db] = get_session_override
        app.dependency_overrides[verify_token] = get_token_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    user: User = User(
        username='John',
        email='john@doe.com',
        password='$2a$12$lrO3cQbMMTiVDyxbFbQjOux.rwtUhdaE6CMwLFRaSJPuOaH6OqzFm',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def user_admin(session: AsyncSession):
    user: User = User(
        username='John',
        email='john@doe.com',
        password='$2a$12$lrO3cQbMMTiVDyxbFbQjOux.rwtUhdaE6CMwLFRaSJPuOaH6OqzFm',
        is_admin=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def user_deactivated(session: AsyncSession):
    user: User = User(
        username='John',
        email='john@doe.com',
        password='$2a$12$lrO3cQbMMTiVDyxbFbQjOux.rwtUhdaE6CMwLFRaSJPuOaH6OqzFm',
        is_active=False,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
