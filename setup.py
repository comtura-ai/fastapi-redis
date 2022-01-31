from setuptools import setup, find_packages

setup(
    name = 'fastapi-redis',
    version = '0.1.0',
    description = 'Fastapi Redis client with decorator for controllers',
    packages = find_packages(),
    install_requires = [
        'aioredis',
        'starlette'
    ]
)