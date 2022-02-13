import asyncio
from datetime import timedelta
from time import sleep

import pytest
from pydantic import BaseModel

from fastapi_redis import redis_client


@pytest.fixture(scope='session')
def event_loop():
    """
    Setup the event loop for the tests.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_redis_set():
    await redis_client.set('object', {'redis': 'test'})
    await redis_client.set('string', 'this is a redis test')
    await redis_client.set('number', 100)
    await redis_client.set('list', [1, 2, '3'])


@pytest.mark.asyncio
async def test_redis_get():
    assert await redis_client.get('object') == {'redis': 'test'}
    assert await redis_client.get('string') == 'this is a redis test'
    assert await redis_client.get('number') == 100
    assert await redis_client.get('list') == [1, 2, '3']


class RedisTestModel(BaseModel):
    value: str
@pytest.mark.asyncio
async def test_redis_get_model():
    await redis_client.set('model', RedisTestModel(value='test'))

    model = await redis_client.get('model', model=RedisTestModel)
    assert type(model) == RedisTestModel
    assert model.value == 'test'


@pytest.mark.asyncio
async def test_redis_remove():
    await redis_client.delete('number')
    assert await redis_client.get('number') is None


@pytest.mark.asyncio
async def test_redis_expiration():
    await redis_client.set('number', 100, expiration=timedelta(minutes=1/60))
    assert await redis_client.get('number') == 100

    sleep(2)
    assert await redis_client.get('number') is None