import os

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DB_URL = os.getenv(
    'DB_URI', default='postgresql+psycopg2://andrey:example@db:5432/disk'
)

engine = create_engine(DB_URL)
TestSession = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = TestSession(bind=connection, autocommit=False)
    yield session
    session.close()
    transaction.rollback()
