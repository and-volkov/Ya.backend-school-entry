import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


pytest_plugins = [
    'tests.fixtures.fixture_database',
    'tests.fixtures.fixture_data',
]
