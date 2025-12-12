from http import HTTPStatus

import pytest
from freezegun import freeze_time

from app.schemas.authenticate_schema import LoginReturn
from app.schemas.response import BaseResponse
from app.schemas.token_schema import RefreshTokenResponse


@pytest.mark.asyncio
async def test_login(client, user):
    response = await client.post(
        '/auth/login',
        json={'email': user.email, 'password': user.clean_password},
    )

    response_schema = BaseResponse[LoginReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'User logged successfully'
    assert response_schema.data.token_type == 'bearer'
    assert response_schema.data.access_token
    assert response_schema.data.refresh_token


@pytest.mark.asyncio
async def test_login_with_wrong_email(client, user):
    response = await client.post(
        '/auth/login',
        json={'email': 'user@email.com', 'password': user.clean_password},
    )

    response_schema = BaseResponse[LoginReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'Invalid email or password'


@pytest.mark.asyncio
async def test_login_with_wrong_password(client, user):
    response = await client.post(
        '/auth/login',
        json={'email': user.email, 'password': 'pass123'},
    )

    response_schema = BaseResponse[LoginReturn].model_validate(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_schema.status == 'error'
    assert response_schema.message == 'Invalid email or password'


@pytest.mark.asyncio
async def test_login_without_information(client, user):
    response = await client.post(
        '/auth/login',
        json={'email': user.email},
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response_schema.status == 'error'
    assert response_schema.message == 'Invalid request data'
    assert response_schema.data[0]['message'] == 'Field required'


@pytest.mark.asyncio
async def test_refresh_token(client, user):
    response_login = await client.post(
        '/auth/login',
        json={'email': user.email, 'password': user.clean_password},
    )

    login_schema = BaseResponse[LoginReturn].model_validate(
        response_login.json()
    )

    response = await client.get(
        '/auth/refresh-token',
        headers={'Authorization': f'Bearer {login_schema.data.refresh_token}'},
    )

    response_schema = BaseResponse[RefreshTokenResponse].model_validate(
        response.json()
    )

    assert response.status_code == HTTPStatus.OK
    assert response_schema.status == 'success'
    assert response_schema.message == 'Token generated successfully'
    assert response_schema.data.access_token


@pytest.mark.asyncio
async def test_invalid_token(client):
    response = await client.put(
        '/user/deactivate', headers={'Authorization': 'Bearer inalid_token'}
    )

    response_schema = BaseResponse.model_validate(response.json())

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response_schema.status == 'error'
    assert response_schema.message == 'Invalid Token'


@pytest.mark.asyncio
async def test_token_expired(client, user):
    with freeze_time('2025-12-11 12:00:00'):
        response = await client.post(
            '/auth/login',
            json={'email': user.email, 'password': user.clean_password},
        )

        login_schema = BaseResponse[LoginReturn].model_validate(
            response.json()
        )

        assert response.status_code == HTTPStatus.OK
        token = login_schema.data.access_token

    with freeze_time('2025-12-11 12:31:00'):
        response = await client.put(
            '/user/deactivate',
            headers={'Authorization': f'Bearer {token}'},
        )

        response_schema = BaseResponse.model_validate(response.json())

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response_schema.status == 'error'
        assert response_schema.message == 'Token has expired'
