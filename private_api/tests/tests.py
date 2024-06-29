from http import HTTPStatus
import io

from httpx import AsyncClient
import pytest

from private_api.core.constants import URL_LIFE_TIME_WITHOUT_ONE_MINUTE


@pytest.mark.asyncio
async def test_upload_file(async_client: AsyncClient):
    file_content = io.BytesIO(b'test content')
    response = await async_client.post(
        '/upload',
        files={'file': ('test.jpg', file_content, 'image/jpeg')},
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert 'filename' in response_data


@pytest.mark.asyncio
async def test_get_file_presigned_url(async_client: AsyncClient):
    file_content = io.BytesIO(b'test content')
    upload_response = await async_client.post(
        '/upload',
        files={'file': ('test.jpg', file_content, 'image/jpeg')},
    )
    filename = upload_response.json()['filename']

    response = await async_client.get(f'/files/{filename}')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert 'url' in response_data
    assert response_data['life_time'] == URL_LIFE_TIME_WITHOUT_ONE_MINUTE
    assert response_data['filename'] == filename


@pytest.mark.asyncio
async def test_remove_file(async_client: AsyncClient):
    file_content = io.BytesIO(b'test content')
    upload_response = await async_client.post(
        '/upload',
        files={'file': ('test.jpg', file_content, 'image/jpeg')},
    )
    filename = upload_response.json()['filename']

    response = await async_client.delete(f'/files/{filename}')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data['result']

    response = await async_client.get(f'/files/{filename}')
    assert response.status_code == HTTPStatus.NOT_FOUND
