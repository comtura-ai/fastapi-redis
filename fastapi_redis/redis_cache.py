import logging

from datetime import timedelta
from functools import wraps

from fastapi_redis import redis_client


def redis_cache(cache_key_str: str, expiration: timedelta = None):
    """
    Decorator for FastAPI controllers to cache the responses using redis.

    This needs to be specified AFTER the @router.get fastapi decorator.

    The controller needs to have `background_tasks: BackgroundTasks`
    as an argument or this will raise an exception.

    :param cache_key_str: first argument of the @redis_cache. Is the
                          key that redis will use to store the data.
                          The arguments of the controller can be used
                          to template the key and make it dynamic.
                          For example: "listview_{crm_object}_{user.id}",
                          where crm_object and user are arguments of
                          the controller.
    :param expiration: timedelta of the expiration of the cache
    """

    def actual_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if the cache key is in the cache
            cache_key = cache_key_str.format(**kwargs)
            data = await redis_client.get(cache_key)
            if data:
                # Return the cached response
                return data

            # Run the wrapped function
            func_result = await func(*args, **kwargs)
            # Set the response in the background.
            if 'background_tasks' in kwargs:
                redis_client.set_in_background(kwargs.get('background_tasks'),
                                               name=cache_key,
                                               value=func_result,
                                               expiration_seconds=expiration)
            else:
                logging.error(
                    f'No background_tasks: BackgroundTasks in the controller arguments. Consider adding it to save the response of the controller after the response is sent to the user, making it faster.')
                await redis_client.set(name=cache_key,
                                       value=func_result,
                                       expiration_seconds=expiration)

            return func_result

        return wrapper

    return actual_decorator
