from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.main import app
from app.models import User
from app.models.day import Day
from app.models.habit import Habit
from app.schemas.authenticate_schema import LoginReturn
from app.schemas.response import BaseResponse
from app.utils.database import Base, get_db
from app.utils.security import bcrypt_context


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


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        await conn.execute(
            Day.__table__.insert(),
            [
                {'id': 1, 'name': 'Domingo'},
                {'id': 2, 'name': 'Segunda'},
                {'id': 3, 'name': 'Terça'},
                {'id': 4, 'name': 'Quarta'},
                {'id': 5, 'name': 'Quinta'},
                {'id': 6, 'name': 'Sexta'},
                {'id': 7, 'name': 'Sábado'},
            ],
        )

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
async def user(
    request,
    session: AsyncSession,
):
    params = getattr(request, 'param', {})
    is_active = params.get('is_active', True)
    is_admin = params.get('is_admin', False)

    password = 'secret'
    user: User = User(
        username='John',
        email='john@doe.com',
        password=bcrypt_context.hash(password),
        is_active=is_active,
        is_admin=is_admin,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def another_user(
    request,
    session: AsyncSession,
):
    params = getattr(request, 'param', {})
    is_active = params.get('is_active', True)
    is_admin = params.get('is_admin', False)

    password = 'secret'
    user: User = User(
        username='Ane',
        email='ane@doe.com',
        password=bcrypt_context.hash(password),
        is_active=is_active,
        is_admin=is_admin,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def token(client, user):
    response = await client.post(
        '/auth/login',
        json={'email': user.email, 'password': user.clean_password},
    )

    response_schema = BaseResponse[LoginReturn].model_validate(response.json())

    return response_schema.data.access_token


@pytest_asyncio.fixture
async def habit(session: AsyncSession, user):

    get_days = await session.scalars(select(Day).where(Day.id.in_([1])))
    days = get_days.all()

    habit: Habit = Habit(
        name='Test', description='Test', frequency=days, user_id=user.id
    )

    session.add(habit)
    await session.commit()
    await session.refresh(habit)

    return habit


@pytest_asyncio.fixture
async def habit_another_user(session: AsyncSession, another_user):

    get_days = await session.scalars(select(Day).where(Day.id.in_([1])))
    days = get_days.all()

    habit: Habit = Habit(
        name='Test',
        description='Test',
        frequency=days,
        user_id=another_user.id,
    )

    session.add(habit)
    await session.commit()
    await session.refresh(habit)

    return habit
