import json
import os
from datetime import timedelta
from typing import Any, Awaitable, Type, Union

from aioredis.client import Redis, KeyT
from aioredis.connection import EncodableT

from starlette.background import BackgroundTasks
from pydantic.main import BaseModel


class RedisClient(Redis):
    async def get(self, name: KeyT, model: Type[BaseModel] = None) -> Any:
        """
        Gets a value with key 'name', None if not found

        :param name: key name
        :param model: model to parse the result to
        :return: saved value
        """
        response = await super().get(name=name)
        if response:
            data = json.loads(response)
            return model(**data) if data and model else data

    async def set(
            self,
            name: KeyT,
            value: Union[EncodableT, Type[BaseModel]],
            expiration: timedelta = None,
            nx: bool = False,
            xx: bool = False,
            keepttl: bool = False,
    ) -> Awaitable:
        """
        Set a value with key 'name' and 'value'

        :param name:
        :param value:
        :param expiration:
        :param nx:
        :param xx:
        :param keepttl:
        :return:
        """
        if issubclass(type(value), BaseModel):
            value = value.dict()
        value = json.dumps(value)
        return await super().set(name=name,
                                 value=value,
                                 ex=expiration,
                                 nx=nx,
                                 xx=xx,
                                 keepttl=keepttl)

    def set_in_background(self,
                          background_tasks: BackgroundTasks,
                          name: KeyT,
                          value: EncodableT,
                          expiration: timedelta = None):
        """
        Set a value using the fastapi background tasks.

        :param background_tasks:
        :param name:
        :param value:
        :param expiration:
        :return:
        """
        background_tasks.add_task(self.set,
                                  name=name,
                                  value=value,
                                  expiration=expiration)


host = os.getenv('REDIS_HOST', 'localhost')
port = os.getenv('REDIS_PORT', 6379)
redis_client = RedisClient(host=host, port=port)
