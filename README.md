# Fastapi Redis

This package provides a client that integrates with Fastapi and provides a decorator to cache fastapi controllers responses.

## Installation

`$ pip install fastapi_redis`

## Usage

### Client

#### Setting the data

```python
import redis_client from fastapi_redis

redis_client.set('some_key', 'some_data')
```

Models can be saved as well and the client will serialize them to json:

```python
import redis_client from fastapi_redis
from pydantic.main import BaseModel

MyModel(BaseModel):
    data: str

redis_client.set('some_key', MyModel(data='some_data'))
redis_client.set('some_key', MyModel(data='some_data_that_expires'), expiration=timedelta(days=1))
```

The data can be saved using the [Fastapi Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) so it wouldn't generate any delay on the response to the user:

```python
import redis_client from fastapi_redis

@router.get('/')
async def my_controller_method(background_tasks: BackgroundTasks):
    redis_client.set_in_background(background_tasks, 'some_key', 'some_data')
    redis_client.set_in_background(background_tasks, 'some_key', MyModel(data='some_data_that_expires'), expiration=timedelta(days=1))
```

#### Getting the data

```python
import redis_client from fastapi_redis

some_data = redis_client.get('some_key')
```

### @redis_cache decorator

The `@redis_cache` decorator can be used to cache the response from a controller. Any argument of the controller can be used to specify the key of the data to store and if `background_tasks: BackgroundTasks` is defined as an argument it will store the data in the background as well:

```python
import redis_client from fastapi_redis


@router.get('/resource/{id}')
@router_cache('resource_{id}_{user.id}', timedelta(days=1))
async def my_controller_method(id: str,
                               user: User = Depends(get_current_user)
                               background_tasks: BackgroundTasks):
    return some_data_that_will_be_cached
```