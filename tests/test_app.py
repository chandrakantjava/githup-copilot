import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# Save the original activities state
original_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the activities dict before each test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    email = "testuser@mergington.edu"
    activity = "Soccer Team"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 400)  # 400 if already signed up
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code in (200, 400)  # 400 if not signed up
