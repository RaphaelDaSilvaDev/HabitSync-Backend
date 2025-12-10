from http import HTTPStatus

import pytest

from app.schemas.response import BaseResponse
from app.schemas.user_schema import UserOut, UserOutFull


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        '/user/create',
        json={
            'username': 'john',
            'email': 'john@doe.com',
            'password': 'secret',
        },
    )

    response_schema = BaseResponse[UserOut].model_validate(response.json())

    assert response.status_code == HTTPStatus.CREATED
    assert response_schema.status == 'success'
    assert response_schema.message == 'User created successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.username == 'john'
    assert response_schema.data.email == 'john@doe.com'


@pytest.mark.asyncio
async def test_create_user_with_same_email(client):
    await client.post(
        '/user/create',
        json={
            'username': 'john',
            'email': 'john@doe.com',
            'password': 'secret',
        },
    )

    response = await client.post(
        '/user/create',
        json={
            'username': 'alice',
            'email': 'john@doe.com',
            'password': 'secret',
        },
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'Email already registered'


@pytest.mark.asyncio
async def test_update_user(client, user, token):
    response = await client.patch(
        '/user/update',
        json={'username': 'John Doe'},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[UserOut].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'User updated successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.username == 'John Doe'
    assert response_schema.data.email == 'john@doe.com'


@pytest.mark.asyncio
async def test_update_user_with_password(client, user, token):
    response = await client.patch(
        '/user/update',
        json={'password': 'secret', 'oldpassword': 'secret'},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[UserOut].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'User updated successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.username == 'John'
    assert response_schema.data.email == 'john@doe.com'


@pytest.mark.asyncio
async def test_update_user_without_old_password(client, user, token):
    response = await client.patch(
        '/user/update',
        json={'password': 'secret'},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'Old password required'


@pytest.mark.asyncio
async def test_update_user_with_no_match_password(client, user, token):
    response = await client.patch(
        '/user/update',
        json={'password': 'secret', 'oldpassword': 'pass'},
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'Old password not math'


@pytest.mark.asyncio
async def test_deactivate_user(client, user, token):
    response = await client.put(
        '/user/deactivate',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[UserOut].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'User deactivated successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.username == 'John'
    assert response_schema.data.email == 'john@doe.com'


@pytest.mark.asyncio
@pytest.mark.parametrize('user', [{'is_active': False}], indirect=True)
async def test_deactivate_user_already_deactivated(client, user, token):
    response = await client.put(
        '/user/deactivate',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'User alreary deactivate'


@pytest.mark.asyncio
@pytest.mark.parametrize('user', [{'is_active': False}], indirect=True)
async def test_activate_user(client, user, token):
    response = await client.put(
        '/user/activate',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[UserOut].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'User activated successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.username == 'John'
    assert response_schema.data.email == 'john@doe.com'


@pytest.mark.asyncio
async def test_activate_user_already_activated(client, user, token):
    response = await client.put(
        '/user/activate',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'User alreary activated'


@pytest.mark.asyncio
async def test_get_user(client, user, token):
    response = await client.get(
        '/user/',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[UserOut].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'User returned successfully'
    assert response_schema.data.id == 1
    assert response_schema.data.username == 'John'
    assert response_schema.data.email == 'john@doe.com'


@pytest.mark.asyncio
@pytest.mark.parametrize('user', [{'is_admin': True}], indirect=True)
async def test_get_all_users(client, user, token):
    response = await client.get(
        '/user/all-users',
        headers={'Authorization': f'Bearer {token}'},
    )

    response_schema = BaseResponse[list[UserOutFull]].model_validate(
        response.json()
    )

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'All users returned successfully'
    assert len(response_schema.data) == 1
    assert response_schema.data[0].id == 1
    assert response_schema.data[0].username == 'John'
    assert response_schema.data[0].email == 'john@doe.com'
    assert response_schema.data[0].is_admin
    assert response_schema.data[0].is_active
