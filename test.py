from asyncio import current_task, run
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from alchemy_provider.provider.examples import *
from alchemy_provider.provider.provider_on_class import *


DB_HOST = 'localhost'
DB_NAME = 'auth'
DB_USER = 'root'
DB_PASSWORD = 'secret'
DB_PORT = 5432

SQLALCHEMY_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
ASYNC_SQLALCHEMY_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# sync_engine = create_engine(SQLALCHEMY_URL, echo=True)
# Base.metadata.create_all(sync_engine)

engine = create_async_engine(
    ASYNC_SQLALCHEMY_URL,
    echo=True
)
session_factory = sessionmaker(engine, class_=AsyncSession)
scoped_session = async_scoped_session(session_factory, scopefunc=current_task)


async def main():
    queries = await Provider.select(
        MeterInlineMeterTypeQuery,
        session=scoped_session()
    )
    import pdb
    pdb.set_trace()


run(main())