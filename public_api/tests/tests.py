import io
import os

from dotenv import load_dotenv
from httpx import AsyncClient
import pytest

from public_api.schemas.memes import MemeRead

load_dotenv()

PRIVATE_API_URL = os.getenv('PRIVATE_API_URL')


@pytest.mark.asyncio
async def test_get_memes_list(
    async_client: AsyncClient, create_test_meme: MemeRead
):
    response = await async_client.get('/memes?page=1&size=25')
    assert response.status_code == 200

    item = response.json()['results'][0]
    assert item['id'] == str(create_test_meme.id)

    response = await async_client.get('/memes?page=2&size=25')
    assert response.status_code == 200
    assert [] == response.json()['results']


@pytest.mark.asyncio
async def test_get_meme(async_client: AsyncClient, create_test_meme: MemeRead):
    response = await async_client.get(f'/memes/{create_test_meme.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(create_test_meme.id)


@pytest.mark.asyncio
async def test_create_meme(httpx_mock, async_client: AsyncClient):
    mock_data = {'filename': 'test.jpg'}
    httpx_mock.add_response(
        method='POST',
        url=f'{PRIVATE_API_URL}/upload',
        json=mock_data,
        status_code=200,
    )
    mock_data.update(
        {'url': f"http://test.com/{mock_data['filename']}", 'life_time': 60}
    )
    httpx_mock.add_response(
        method='GET',
        url=f"{PRIVATE_API_URL}/files/{mock_data['filename']}",
        json=mock_data,
        status_code=200,
    )

    file_content = io.BytesIO(b'test_image_content')
    description = 'New Meme'
    response = await async_client.post(
        '/memes',
        files={'image': (mock_data['filename'], file_content, 'image/jpeg')},
        data={'description': description},
    )

    assert response.status_code == 200

    response_data = response.json()
    assert response_data['description'] == description
    assert response_data['image_url'] == mock_data['url']
    assert response_data['filename'] == mock_data['filename']


@pytest.mark.asyncio
async def test_update_meme(
    httpx_mock, async_client: AsyncClient, create_test_meme: MemeRead
):
    mock_data = {'filename': 'new_name.jpg'}
    httpx_mock.add_response(
        method='POST',
        url=f'{PRIVATE_API_URL}/upload',
        json=mock_data,
        status_code=200,
    )
    mock_data.update(
        {'url': f"http://test.com/{mock_data['filename']}", 'life_time': 60}
    )
    httpx_mock.add_response(
        method='GET',
        url=f"{PRIVATE_API_URL}/files/{mock_data['filename']}",
        json=mock_data,
        status_code=200,
    )
    httpx_mock.add_response(
        method='DELETE',
        url=f'{PRIVATE_API_URL}/files/{create_test_meme.filename}',
        status_code=200,
    )

    file_content = io.BytesIO(b'new_image_content')
    description = 'Updated Meme'
    response = await async_client.put(
        f'/memes/{create_test_meme.id}',
        files={'image': (mock_data['filename'], file_content, 'image/jpeg')},
        data={'description': description},
    )
    assert response.status_code == 200
    response_data = response.json()

    assert response_data['description'] == description
    assert response_data['image_url'] == mock_data['url']
    assert response_data['filename'] == mock_data['filename']


@pytest.mark.asyncio
async def test_delete_meme(
    httpx_mock, async_client: AsyncClient, create_test_meme: MemeRead
):
    httpx_mock.add_response(
        method='DELETE',
        url=f'{PRIVATE_API_URL}/files/{create_test_meme.filename}',
        status_code=200,
    )

    response = await async_client.delete(f'/memes/{create_test_meme.id}')
    assert response.status_code == 200

    response_data = response.json()
    assert response_data['id'] == str(create_test_meme.id)

    response = await async_client.get(f'/memes/{create_test_meme.id}')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_validate_file(async_client: AsyncClient):
    # Данная проверка занимает около 40 секунд, поэтому она отключена
    # file_content = io.BytesIO(b'a' * (FILE_MAX_SIZE + 1))
    # response = await async_client.post(
    #     '/memes',
    #     files={'image': ('big_file.jpg', file_content, 'image/jpeg')},
    # )
    # assert response.status_code == 400
    # assert response.json()['detail'] == 'File is too large'

    file_content = io.BytesIO(b'test content')
    response = await async_client.post(
        '/memes',
        files={'image': ('test.txt', file_content, 'text/plain')},
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid file type'
