from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_meeting():
    meeting_data = {
        "place": "Test Meeting Place",
        "time": "Test Meeting Time"
    }
    response = client.post("/meetings/", json=meeting_data)
    assert response.status_code == 200
    assert response.json()["place"] == meeting_data["place"]
    assert response.json()["time"] == meeting_data["time"]


def test_get_meetings():
    response = client.get("/meetings/")
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_get_single_meeting():
    meeting_data = {
        "place": "Test Meeting Place",
        "time": "Test Meeting Time"
    }
    create_response = client.post("/meetings/", json=meeting_data)
    assert create_response.status_code == 200
    meeting_id = create_response.json()["id"]

    response = client.get(f"/meetings/{meeting_id}")
    assert response.status_code == 200
    assert response.json()["place"] == meeting_data["place"]
    assert response.json()["time"] == meeting_data["time"]
