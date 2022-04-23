import os


# APPLICATION CONFIG
DEBUG = bool(os.environ.get('DEBUG', True))
USE_TIMEZONE = bool(os.environ.get('USE_TIMEZONE', True))


# POSTGRESQL CONFIGS
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_NAME = os.environ.get('POSTGRES_NAME', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'root')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'secret')


# SYNC SQLALCHEMY CONFIGS
SYNC_SQLALCHEMY_URL = f'postgresql+psycopg2://' \
                      f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                      f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
SYNC_SQLALCHEMY_POOL_SIZE = int(os.environ.get(
    'SYNC_SQLALCHEMY_POOL_SIZE', 5
))
SYNC_SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get(
    'SYNC_SQLALCHEMY_POOL_SIZE', 5
))
SYNC_SQLALCHEMY_ECHO = bool(os.environ.get(
    'SYNC_SQLALCHEMY_ECHO',
    DEBUG
))


# ASYNC SQLALCHEMY CONFIGS
ASYNC_SQLALCHEMY_URL = f'postgresql+asyncpg://' \
                       f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                       f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
ASYNC_SQLALCHEMY_POOL_SIZE = int(os.environ.get(
    'ASYNC_SQLALCHEMY_POOL_SIZE', 20
))
ASYNC_SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get(
    'ASYNC_SQLALCHEMY_POOL_SIZE', 10
))
ASYNC_SQLALCHEMY_ECHO = bool(os.environ.get(
    'ASYNC_SQLALCHEMY_ECHO',
    DEBUG
))


# UVICORN CONFIGS
UVICORN_HOST = os.environ.get('UVICORN_HOST', 'localhost')
UVICORN_PORT = os.environ.get('UVICORN_PORT', 8000)
