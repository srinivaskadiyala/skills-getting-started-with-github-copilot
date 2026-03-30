import pytest


class TestUnregister:
    def test_unregister_successful_from_activity(self, client):
        """Test successful unregister from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the student from participants"""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already in participants
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_non_existent_activity_returns_404(self, client):
        """Test that unregister from non-existent activity returns 404"""
        # Arrange
        activity_name = "Non-existent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_non_registered_student_returns_400(self, client):
        """Test that unregistering a non-registered student returns 400"""
        # Arrange
        activity_name = "Drama Club"
        email = "notregistered@mergington.edu"  # Not in participants
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not registered for this activity"

    def test_unregister_then_signup_again(self, client, sample_student_email):
        """Test that student can re-signup after unregistering"""
        # Arrange
        activity_name = "Art Studio"
        email = sample_student_email
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # Then unregister
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        # Then signup again
        response3 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

    def test_unregister_response_format(self, client):
        """Test that unregister response has correct format"""
        # Arrange
        activity_name = "Science Club"
        email = "sarah@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert isinstance(data["message"], str)
        assert activity_name in data["message"]
        assert email in data["message"]
