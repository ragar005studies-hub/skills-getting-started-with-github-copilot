"""Tests for the POST /activities/{activity_name}/signup endpoint"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students to activities"""

    def test_signup_for_activity_success(self, client, test_activity, test_email):
        """
        Test: Student successfully signs up for an activity
        
        Arrange: Test email not yet in Chess Club participants
        Act: Send POST request to /activities/Chess Club/signup with test email
        Assert: Response status is 200, confirmation message returned, email added to participants
        """
        # Arrange: Verify email not in activity initially
        response = client.get("/activities")
        activity_data = response.json()
        initial_participants = activity_data[test_activity]["participants"].copy()
        assert test_email not in initial_participants
        
        # Act: Sign up for activity
        signup_response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # Assert: Check response status and message
        assert signup_response.status_code == 200
        assert "Signed up" in signup_response.json()["message"]
        assert test_email in signup_response.json()["message"]
        
        # Assert: Verify email added to participants
        verify_response = client.get("/activities")
        updated_activity = verify_response.json()[test_activity]
        assert test_email in updated_activity["participants"]
        assert len(updated_activity["participants"]) == len(initial_participants) + 1

    def test_signup_duplicate_email_returns_error(self, client, test_activity, existing_email):
        """
        Test: Attempting to sign up with an email already registered fails
        
        Arrange: existing_email fixture provides an email already in test_activity
        Act: Send POST request to sign up with existing_email
        Assert: Response status is 400, error message about duplicate signup
        """
        # Act: Attempt to sign up with email already in activity
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Check for 400 Bad Request and appropriate error message
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_invalid_activity_returns_error(self, client, test_email):
        """
        Test: Attempting to sign up for nonexistent activity fails
        
        Arrange: test_email is valid, but activity name does not exist
        Act: Send POST request to sign up for "Nonexistent Activity"
        Assert: Response status is 404, error message about activity not found
        """
        # Act: Attempt to sign up for activity that doesn't exist
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": test_email}
        )
        
        # Assert: Check for 404 Not Found
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_multiple_students_same_activity(self, client, test_activity):
        """
        Test: Multiple different students can sign up for the same activity
        
        Arrange: Use two different test emails, both not in test_activity
        Act: Sign up both emails sequentially for the same activity
        Assert: Both emails successfully added, participant count increased by 2
        """
        # Arrange: Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()[test_activity]["participants"])
        
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act: Sign up first student
        response1 = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": email1}
        )
        
        # Act: Sign up second student
        response2 = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": email2}
        )
        
        # Assert: Both successful
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Assert: Both emails added
        verify_response = client.get("/activities")
        final_participants = verify_response.json()[test_activity]["participants"]
        assert email1 in final_participants
        assert email2 in final_participants
        assert len(final_participants) == initial_count + 2

    def test_signup_preserves_existing_participants(self, client, test_activity, test_email):
        """
        Test: Signing up a new student doesn't affect existing participants
        
        Arrange: Get the list of existing participants before signup
        Act: Sign up a new student
        Assert: All existing participants still in the list
        """
        # Arrange: Get existing participants
        response = client.get("/activities")
        existing_participants = response.json()[test_activity]["participants"].copy()
        
        # Act: Sign up new student
        client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # Assert: All existing participants still present
        verify_response = client.get("/activities")
        final_participants = verify_response.json()[test_activity]["participants"]
        for participant in existing_participants:
            assert participant in final_participants
