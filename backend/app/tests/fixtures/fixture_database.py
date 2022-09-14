import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from backend.app.settings import db_settings

engine = create_engine(db_settings.uri)
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
