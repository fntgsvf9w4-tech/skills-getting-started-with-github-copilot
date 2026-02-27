from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    # sanity check that activities endpoint returns the dict
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unenroll():
    activity = "Science Club"
    email = "newstudent@mergington.edu"

    # ensure initial state doesn't contain the email
    assert email not in activities[activity]["participants"]

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # sign up again should error
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400

    # unenroll
    resp = client.post(f"/activities/{activity}/unenroll", params={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # unenroll again should error
    resp = client.post(f"/activities/{activity}/unenroll", params={"email": email})
    assert resp.status_code == 400
