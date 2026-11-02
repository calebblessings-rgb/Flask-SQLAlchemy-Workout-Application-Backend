
import os
import pytest

from datetime import date

# Configure the test database BEFORE importing the Flask application.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from server.app import app, db
from server.models import Workout, Exercise


@pytest.fixture
def client():
    app.config.update(TESTING=True)

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-11-03",
            "duration_minutes": 45,
            "notes": "Test workout"
        }
    )
    return response.get_json()["id"]


def create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Push-ups",
            "category": "Strength",
            "equipment_needed": False
        }
    )
    return response.get_json()["id"]


# WORKOUT TESTS

def test_get_all_workouts(client):
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-11-03",
            "duration_minutes": 45,
            "notes": "Morning workout"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["duration_minutes"] == 45


def test_get_workout_by_id(client):
    workout_id = create_workout(client)

    response = client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == workout_id


def test_get_missing_workout(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_create_workout_with_invalid_duration(client):
    response = client.post(
        "/workouts",
        json={
            "date": "2026-11-03",
            "duration_minutes": 0,
            "notes": "Invalid workout"
        }
    )

    assert response.status_code == 400


def test_delete_workout(client):
    workout_id = create_workout(client)

    response = client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 200

    missing = client.get(f"/workouts/{workout_id}")
    assert missing.status_code == 404


# EXERCISE TESTS

def test_get_all_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={
            "name": "Squats",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "Squats"


def test_get_exercise_by_id(client):
    exercise_id = create_exercise(client)

    response = client.get(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == exercise_id


def test_get_missing_exercise(client):
    response = client.get("/exercises/999")
    assert response.status_code == 404


def test_create_exercise_with_empty_name(client):
    response = client.post(
        "/exercises",
        json={
            "name": "",
            "category": "Strength",
            "equipment_needed": False
        }
    )

    assert response.status_code == 400


def test_delete_exercise(client):
    exercise_id = create_exercise(client)

    response = client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 200


# WORKOUT-EXERCISE ASSOCIATION TESTS

def test_add_exercise_to_workout(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"reps": 15, "sets": 3}
    )

    assert response.status_code == 201
    assert response.get_json()["reps"] == 15
    assert response.get_json()["sets"] == 3


def test_prevent_duplicate_exercise_association(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    url = (
        f"/workouts/{workout_id}/exercises/"
        f"{exercise_id}/workout_exercises"
    )

    client.post(url, json={"reps": 15, "sets": 3})
    response = client.post(url, json={"reps": 20, "sets": 4})

    assert response.status_code == 409


def test_reject_invalid_association_reps(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"reps": 0, "sets": 3}
    )

    assert response.status_code == 400


def test_reject_missing_workout_for_association(client):
    exercise_id = create_exercise(client)

    response = client.post(
        f"/workouts/999/exercises/{exercise_id}/workout_exercises",
        json={"reps": 10, "sets": 2}
    )

    assert response.status_code == 404


def test_reject_missing_exercise_for_association(client):
    workout_id = create_workout(client)

    response = client.post(
        f"/workouts/{workout_id}/exercises/999/workout_exercises",
        json={"reps": 10, "sets": 2}
    )

    assert response.status_code == 404


def test_prevent_deleting_associated_exercise(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"reps": 15, "sets": 3}
    )

    response = client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 409
