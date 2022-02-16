import os

from setuptools import setup

setup(
    name='fastapi-redis',
    version='__version__',
    license='MIT',
    author='Comtura',
    author_email='info@comtura.ai',
    description='Fastapi Redis client with decorator for controllers',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=['fastapi_redis'],
    url='https://github.com/comtura-ai/fastapi-redis',
    download_url='https://github.com/comtura-ai/fastapi-redis/archive/refs/heads/main.zip',
    keywords=['fastapi', 'redis', 'cache'],
    install_requires=[
        'aioredis >= 2.0',
        'starlette >= 0.14',
        'pydantic >= 1.8',
        'pytest >= 6.2',
        'pytest-asyncio >= 0.15'
    ]
)
