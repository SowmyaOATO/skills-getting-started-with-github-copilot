import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities_state():
    original_state = {
        name: {
            key: value.copy() if isinstance(value, list) else value
            for key, value in activity.items()
        }
        for name, activity in activities.items()
    }
    yield
    activities.clear()
    activities.update(original_state)


client = TestClient(app)


def test_unregister_participant_removes_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
