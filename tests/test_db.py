from dataclasses import asdict

import pytest
from sqlalchemy import select

from app.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='John',
            email='john@doe.com',
            password='pass',
        )

        session.add(new_user)
        await session.commit()

        user = await session.scalar(select(User).where(User.id == 1))

        assert asdict(user) == {
            'id': 1,
            'username': 'John',
            'email': 'john@doe.com',
            'password': 'pass',
            'is_active': True,
            'is_admin': False,
            'updated_at': time,
            'created_at': time,
        }
