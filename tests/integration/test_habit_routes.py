from datetime import date
from http import HTTPStatus

import pytest
from freezegun import freeze_time

from app.schemas.habit_schema import HabitConclusionReturn, HabitReturn
from app.schemas.response import BaseResponse


@pytest.mark.asyncio
async def test_create_habit(client, token):
    response = await client.post(
        '/habit/create',
        json={'name': 'Test', 'description': 'Test', 'frequency': [1]},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[HabitReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert response_schema.message == 'Habit created successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.name == 'Test'
    assert response_schema.data.description == 'Test'
    assert 'Domingo' in response_schema.data.frequency


@pytest.mark.asyncio
async def test_create_same_habit(client, token):
    await client.post(
        '/habit/create',
        json={'name': 'Test', 'description': 'Test', 'frequency': [1]},
        headers={'Authorization': f'Bearer {token}'},
    )

    response = await client.post(
        '/habit/create',
        json={'name': 'Test', 'description': 'Test', 'frequency': [1]},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[HabitReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.message == 'This habit alreary exists'


@pytest.mark.asyncio
async def test_get_all_user_habit(client, token, habit):
    response = await client.get(
        '/habit/', headers={'Authorization': f'Bearer {token}'}
    )

    response_schema = BaseResponse[list[HabitReturn]].model_validate(
        response.json()
    )

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'Get all habit for this user'
    assert response_schema.data[0].id == 1
    assert response_schema.data[0].name == 'Test'
    assert response_schema.data[0].description == 'Test'
    assert 'Domingo' in response_schema.data[0].frequency


@pytest.mark.asyncio
async def test_delete_habit_by_id(client, token, habit):
    response = await client.delete(
        f'/habit/delete/{habit.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_delete_not_existent_habit_by_id(client, token):
    response = await client.delete(
        '/habit/delete/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_schema.status == 'error'
    assert response_schema.message == 'Habit not found'


@pytest.mark.asyncio
async def test_delete_habit_by_id_another_user(
    client, token, habit_another_user
):
    response = await client.delete(
        f'/habit/delete/{habit_another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_schema.status == 'error'
    assert (
        response_schema.message
        == 'You do not have permission to perform this action.'
    )


@pytest.mark.asyncio
async def test_mark_done_habit(client, token, habit):
    with freeze_time('2025-12-07 12:00:00'):
        response = await client.post(
            f'/habit/mark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        response_schema = BaseResponse[HabitConclusionReturn].model_validate(
            response.json()
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response_schema.status == 'success'
        assert response_schema.message == 'Habit marked done successfully'
        assert response_schema.data.id == 1
        assert response_schema.data.habit.id == habit.id
        assert response_schema.data.habit.name == 'Test'
        assert response_schema.data.habit.description == 'Test'


@pytest.mark.asyncio
async def test_mark_done_not_existent_habit(client, token):
    response = await client.post(
        '/habit/mark-done/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_schema.status == 'error'
    assert response_schema.message == 'Habit not found'


@pytest.mark.asyncio
async def test_mark_done_habit_another_user(client, token, habit_another_user):
    response = await client.post(
        f'/habit/mark-done/{habit_another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_schema.status == 'error'
    assert (
        response_schema.message
        == 'You do not have permission to perform this action.'
    )


@pytest.mark.asyncio
async def test_mark_done_habit_out_of_date(client, token, habit):
    with freeze_time('2025-12-08 12:00:00'):
        response = await client.post(
            f'/habit/mark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        response_schema = BaseResponse.model_validate(response.json())

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_schema.status == 'error'
        assert response_schema.message == 'This habit is not set for today'


@pytest.mark.asyncio
async def test_mark_done_habit_already_done(client, token, habit):
    with freeze_time('2025-12-07 12:00:00'):
        await client.post(
            f'/habit/mark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        response = await client.post(
            f'/habit/mark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        response_schema = BaseResponse.model_validate(response.json())

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_schema.status == 'error'
        assert (
            response_schema.message
            == 'This habit has already been established today.'
        )


@pytest.mark.asyncio
async def test_unmark_done_habit(client, token, habit):
    with freeze_time('2025-12-07 12:00:00'):
        response_done = await client.post(
            f'/habit/mark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response_done.status_code == HTTPStatus.CREATED

        response = await client.delete(
            f'/habit/unmark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_unmark_done_not_existent_habit(client, token):
    response = await client.delete(
        '/habit/unmark-done/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_schema.status == 'error'
    assert response_schema.message == 'Habit not found'


@pytest.mark.asyncio
async def test_unmark_done_habit_another_user(
    client, token, habit_another_user
):
    response = await client.delete(
        f'/habit/unmark-done/{habit_another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_schema.status == 'error'
    assert (
        response_schema.message
        == 'You do not have permission to perform this action.'
    )


@pytest.mark.asyncio
async def test_unmark_done_habit_not_done(client, token, habit):
    with freeze_time('2025-12-07 12:00:00'):
        await client.post(
            f'/habit/unmark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        response = await client.delete(
            f'/habit/unmark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        response_schema = BaseResponse.model_validate(response.json())

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_schema.status == 'error'
        assert response_schema.message == 'This habit was not conclusion yet'


@pytest.mark.asyncio
async def test_get_completed_by_day(client, token, habit):
    date_params = date.today()

    with freeze_time('2025-12-07 12:00:00'):
        response = await client.post(
            f'/habit/mark-done/{habit.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.CREATED

    response = await client.get(
        '/habit/completed',
        params={'date': date_params},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[list[HabitReturn]].model_validate(
        response.json()
    )

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == f'Habits completed in date {date_params}'
    assert len(response_schema.data) == 1


@pytest.mark.asyncio
async def test_get_upcoming_habits(client, token, habit):
    with freeze_time('2025-12-07 12:00:00'):
        response = await client.get(
            '/habit/upcoming',
            headers={'Authorization': f'Bearer {token}'},
        )

        response_schema = BaseResponse[list[HabitReturn]].model_validate(
            response.json()
        )

        assert response.status_code == HTTPStatus.OK
        assert response_schema.status == 'success'
        assert response_schema.message == 'Habits upcoming today'
        assert len(response_schema.data) == 1


@pytest.mark.asyncio
async def test_get_habit_by_id(client, token, habit):
    response = await client.get(
        f'/habit/{habit.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[HabitReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'Habit return successfully'
    assert response_schema.data.name == 'Test'


@pytest.mark.asyncio
async def test_get_not_found_habit_by_id(client, token):
    response = await client.get(
        '/habit/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_schema.status == 'error'
    assert response_schema.message == 'Habit not found'


@pytest.mark.asyncio
async def test_get_another_user_habit_by_id(client, token, habit_another_user):
    response = await client.get(
        f'/habit/{habit_another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_schema.status == 'error'
    assert (
        response_schema.message
        == 'You do not have permission to perform this action.'
    )


@pytest.mark.asyncio
async def test_update_habit_by_id(client, token, habit):
    response = await client.patch(
        f'/habit/{habit.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'New Test',
            'description': 'New Test',
            'frequency': [1, 2],
        },
    )

    response_schema = BaseResponse[HabitReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'Habit updated successfully'
    assert response_schema.data.name == 'New Test'
    assert response_schema.data.description == 'New Test'
    assert response_schema.data.frequency == ['Domingo', 'Segunda']


@pytest.mark.asyncio
async def test_update_not_found_habit_by_id(client, token):
    response = await client.patch(
        '/habit/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'New Test',
            'description': 'New Test',
            'frequency': [1, 2],
        },
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_schema.status == 'error'
    assert response_schema.message == 'Habit not found'


@pytest.mark.asyncio
async def test_update_another_user_habit_by_id(
    client, token, habit_another_user
):
    response = await client.patch(
        f'/habit/{habit_another_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'New Test',
            'description': 'New Test',
            'frequency': [1, 2],
        },
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_schema.status == 'error'
    assert (
        response_schema.message
        == 'You do not have permission to perform this action.'
    )
