import json
from typing import Any, Awaitable, Optional

from aioredis.client import Redis, KeyT, ExpiryT
from aioredis.connection import EncodableT

from starlette.background import BackgroundTasks


class RedisClient(Redis):

    async def get(self, name: KeyT) -> Any:
        """
        Gets a value with key 'name', None if not found

        :param name: key name
        :return: saved value
        """
        response = await super().get(name=name)
        if response:
            return json.loads(response)

    async def set(
            self,
            name: KeyT,
            value: EncodableT,
            expiration_seconds: Optional[ExpiryT] = None,
            expiration_milliseconds: Optional[ExpiryT] = None,
            nx: bool = False,
            xx: bool = False,
            keepttl: bool = False,
    ) -> Awaitable:
        """
        Set a value with key 'name' and 'value'

        :param name:
        :param value:
        :param expiration_seconds:
        :param expiration_milliseconds:
        :param nx:
        :param xx:
        :param keepttl:
        :return:
        """
        value = json.dumps(value)
        return await super().set(name=name,
                                 value=value,
                                 ex=expiration_seconds,
                                 px=expiration_milliseconds,
                                 nx=nx,
                                 xx=xx,
                                 keepttl=keepttl)

    def set_in_background(self,
                          background_tasks: BackgroundTasks,
                          name: KeyT,
                          value: EncodableT,
                          expiration_seconds: Optional[ExpiryT] = None,
                          expiration_milliseconds: Optional[ExpiryT] = None):
        """
        Set a value using the fastapi background tasks.

        :param background_tasks:
        :param name:
        :param value:
        :param expiration_seconds:
        :param expiration_milliseconds:
        :return:
        """
        background_tasks.add_task(self.set,
                                  name=name,
                                  value=value,
                                  expiration_seconds=expiration_seconds,
                                  expiration_milliseconds=expiration_milliseconds)


host = os.getenv('REDIS_HOST', 'localhost')
port = os.getenv('REDIS_PORT', 6379)
redis_client = RedisClient(host=host, port=port)
