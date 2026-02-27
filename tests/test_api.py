from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    """Test that the activities endpoint returns the activities dictionary."""
    # Arrange
    # (no setup needed; activities are pre-loaded)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success():
    """Test successful signup for an activity."""
    # Arrange
    activity = "Art Studio"
    email = "newtestuser@mergington.edu"
    assert email not in activities[activity]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]


def test_signup_for_activity_already_registered():
    """Test that signing up twice returns a 400 error."""
    # Arrange
    activity = "Basketball Team"
    email = "duplicateuser@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})

    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Student already signed up for this activity"
    )


def test_unenroll_from_activity_success():
    """Test successful unenrollment from an activity."""
    # Arrange
    activity = "Tennis Club"
    email = "unrolluser@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    assert email in activities[activity]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/unenroll", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_unenroll_from_activity_not_enrolled():
    """Test that unenrolling a non-enrolled student returns a 400 error."""
    # Arrange
    activity = "Drama Club"
    email = "neverenrolled@mergington.edu"
    assert email not in activities[activity]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/unenroll", params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not enrolled in this activity"
