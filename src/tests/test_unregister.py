"""Tests for the POST /activities/{activity_name}/unregister endpoint"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities"""

    def test_unregister_success(self, client, test_activity, existing_email):
        """
        Test: Student successfully unregisters from an activity
        
        Arrange: existing_email is registered in test_activity
        Act: Send POST request to unregister endpoint with existing_email
        Assert: Response status is 200, email removed from participants
        """
        # Arrange: Verify email is in activity initially
        response = client.get("/activities")
        activity_data = response.json()
        assert existing_email in activity_data[test_activity]["participants"]
        initial_count = len(activity_data[test_activity]["participants"])
        
        # Act: Unregister from activity
        unregister_response = client.post(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_email}
        )
        
        # Assert: Check response status and message
        assert unregister_response.status_code == 200
        assert "Unregistered" in unregister_response.json()["message"]
        assert existing_email in unregister_response.json()["message"]
        
        # Assert: Verify email removed from participants
        verify_response = client.get("/activities")
        updated_activity = verify_response.json()[test_activity]
        assert existing_email not in updated_activity["participants"]
        assert len(updated_activity["participants"]) == initial_count - 1

    def test_unregister_student_not_registered_returns_error(self, client, test_activity, test_email):
        """
        Test: Attempting to unregister a student not in the activity fails
        
        Arrange: test_email is not registered in test_activity
        Act: Send POST request to unregister with test_email
        Assert: Response status is 400, error message about not being registered
        """
        # Arrange: Verify email is NOT in activity
        response = client.get("/activities")
        assert test_email not in response.json()[test_activity]["participants"]
        
        # Act: Attempt to unregister email not in activity
        unregister_response = client.post(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        
        # Assert: Check for 400 Bad Request
        assert unregister_response.status_code == 400
        assert "not registered" in unregister_response.json()["detail"]

    def test_unregister_from_invalid_activity_returns_error(self, client, existing_email):
        """
        Test: Attempting to unregister from nonexistent activity fails
        
        Arrange: existing_email is valid, but activity name does not exist
        Act: Send POST request to unregister from "Nonexistent Activity"
        Assert: Response status is 404, error message about activity not found
        """
        # Act: Attempt to unregister from activity that doesn't exist
        response = client.post(
            "/activities/Nonexistent Activity/unregister",
            params={"email": existing_email}
        )
        
        # Assert: Check for 404 Not Found
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_then_can_register_again(self, client, test_activity, test_email):
        """
        Test: A student can sign up again after unregistering
        
        Arrange: test_email not in test_activity initially
        Act: Sign up, then unregister, then sign up again
        Assert: All operations succeed, final state has email registered
        """
        # Act: Sign up
        signup_response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        assert signup_response.status_code == 200
        
        # Verify: Email now in activity
        verify1 = client.get("/activities")
        assert test_email in verify1.json()[test_activity]["participants"]
        
        # Act: Unregister
        unregister_response = client.post(
            f"/activities/{test_activity}/unregister",
            params={"email": test_email}
        )
        assert unregister_response.status_code == 200
        
        # Verify: Email no longer in activity
        verify2 = client.get("/activities")
        assert test_email not in verify2.json()[test_activity]["participants"]
        
        # Act: Sign up again
        signup_again_response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        assert signup_again_response.status_code == 200
        
        # Assert: Email is back in activity
        verify3 = client.get("/activities")
        assert test_email in verify3.json()[test_activity]["participants"]

    def test_unregister_preserves_other_participants(self, client, test_activity, existing_email):
        """
        Test: Unregistering one student doesn't affect other participants
        
        Arrange: Identify existing_email and another participant in test_activity
        Act: Unregister existing_email
        Assert: Other participants remain in the list
        """
        # Arrange: Get list of existing participants
        response = client.get("/activities")
        existing_participants = response.json()[test_activity]["participants"].copy()
        other_participants = [p for p in existing_participants if p != existing_email]
        
        # Act: Unregister existing_email
        client.post(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_email}
        )
        
        # Assert: Other participants still present
        verify_response = client.get("/activities")
        final_participants = verify_response.json()[test_activity]["participants"]
        for participant in other_participants:
            assert participant in final_participants
