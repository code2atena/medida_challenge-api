import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(scope='module')
def test_user():
    """
    Fixture to provide test user data
    """
    return {"username": "user1", "password": "password1"}


def test_login_for_access_token(test_user):
    """
    Test case for testing user authentication and token generation
    """
    response = client.post("/token", data=test_user)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_incorrect():
    """
    Test case for testing user authentication with incorrect credentials
    """
    response = client.post("/token", data={"username": "wrong_user", "password": "wrong_password"})
    assert response.status_code == 401


def test_polling_events(test_user):
    """
    Test case for testing retrieval of events with valid parameters
    """
    response = client.post("/token", data=test_user)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    events_request = {"startDate": "2023-01-01", "endDate": "2023-12-31"}
    response = client.post("/events", headers={"Authorization": f"Bearer {access_token}"}, json=events_request)
    assert response.status_code == 200


def test_polling_events_unauthorized():
    """
    Test case for testing retrieval of events without authentication (unauthorized)
    """
    events_request = {"startDate": "2023-01-01", "endDate": "2023-12-31"}
    response = client.post("/events", json=events_request)
    assert response.status_code == 401


def test_invalid_request_data():
    """
    Test case for testing retrieval of events with invalid parameters
    """
    invalid_request_data = {"startDate": "2023-01-01", "endDate": "2022-12-31"}
    response = client.post("/events", headers={"Authorization": "Bearer dummy_token"}, json=invalid_request_data)
    assert response.status_code == 422


def test_edge_cases():
    """
    Test case for testing edge cases, such as very small date range
    """
    events_request = {"startDate": "2024-01-01", "endDate": "2024-01-01"}
    response = client.post("/events", headers={"Authorization": "Bearer dummy_token"}, json=events_request)
    assert response.status_code == 200
    assert len(response.json()) == 0
