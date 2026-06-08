"""Tests for the GET /activities endpoint"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""

    def test_get_activities_returns_success(self, client):
        """
        Test: GET /activities returns a successful response
        
        Arrange: No setup needed, activities are pre-populated in fixtures
        Act: Send GET request to /activities
        Assert: Response status is 200 OK
        """
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """
        Test: GET /activities returns all 9 activities
        
        Arrange: Activities fixture provides pre-loaded database
        Act: Send GET request to /activities
        Assert: Response contains exactly 9 activities
        """
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 9

    def test_get_activities_contains_chess_club(self, client):
        """
        Test: GET /activities includes Chess Club activity
        
        Arrange: Activities fixture provides pre-loaded database
        Act: Send GET request to /activities
        Assert: Response contains Chess Club key
        """
        response = client.get("/activities")
        activities = response.json()
        assert "Chess Club" in activities

    def test_get_activities_has_correct_structure(self, client, test_activity):
        """
        Test: Each activity has required fields (description, schedule, max_participants, participants)
        
        Arrange: Activities fixture provides pre-loaded database
        Act: Send GET request to /activities and examine test_activity
        Assert: Activity object contains all required keys
        """
        response = client.get("/activities")
        activities = response.json()
        activity = activities[test_activity]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

    def test_get_activities_participants_is_list(self, client, test_activity):
        """
        Test: The participants field is a list of emails
        
        Arrange: Activities fixture provides pre-loaded database
        Act: Send GET request to /activities
        Assert: Participants for test_activity is a list with email strings
        """
        response = client.get("/activities")
        activities = response.json()
        activity = activities[test_activity]
        
        assert isinstance(activity["participants"], list)
        assert len(activity["participants"]) > 0
        assert "@mergington.edu" in activity["participants"][0]
