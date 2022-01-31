from setuptools import setup, find_packages

setup(
    name = 'fastapi-redis',
    version = '0.1.0',
    author='Comtura',
    author_email='info@comtura.ai',
    description = 'Fastapi Redis client with decorator for controllers',
    long_description=open('README.txt').read(),
    packages = ['fastapi_redis'],
    install_requires = [
        'aioredis >= 2.0.0',
        'starlette >= 0.14'
    ]
)
