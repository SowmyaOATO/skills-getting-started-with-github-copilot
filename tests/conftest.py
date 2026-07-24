import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities_state():
    # Arrange
    original_state = {
        name: {
            key: value.copy() if isinstance(value, list) else value
            for key, value in activity.items()
        }
        for name, activity in activities.items()
    }

    yield

    # Teardown
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def client():
    return TestClient(app)
