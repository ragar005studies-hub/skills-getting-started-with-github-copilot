"""Pytest configuration and shared fixtures for FastAPI tests"""

import pytest
from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient for making HTTP requests to the FastAPI app.
    Ensures a fresh app instance for each test.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture: Resets the in-memory activities database to a clean state before each test.
    This ensures test isolation - each test starts with the original activity data.
    Runs automatically for all tests (autouse=True).
    """
    # Reset to initial state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Train for competitive soccer matches and improve teamwork",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "maya@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice shooting, passing, and game strategy for basketball",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["jason@mergington.edu", "nina@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["lily@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Develop acting skills and produce school plays and performances",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Prepare for science competitions with experiments and problem-solving",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["anna@mergington.edu", "marcus@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice debate techniques and compete in structured speaking events",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["olivia@mergington.edu", "sam@mergington.edu"]
        }
    }
    
    # Clear and repopulate the activities dictionary
    activities.clear()
    activities.update(original_activities)
    yield
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def test_activity():
    """
    Fixture: Provides a test activity name that exists in the database.
    Useful for tests that need a guaranteed valid activity.
    """
    return "Chess Club"


@pytest.fixture
def test_email():
    """
    Fixture: Provides a test email address for signup/unregister tests.
    Uses an email not already in any activity to avoid conflicts.
    """
    return "testuser@mergington.edu"


@pytest.fixture
def existing_email():
    """
    Fixture: Provides an email that's already registered for the test activity.
    Useful for testing duplicate signup scenarios.
    """
    return "michael@mergington.edu"
