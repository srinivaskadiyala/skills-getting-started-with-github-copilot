import pytest


class TestSignup:
    def test_signup_successful_to_available_activity(self, client, sample_student_email):
        """Test successful signup for an activity with available spots"""
        # Arrange
        activity_name = "Chess Club"
        email = sample_student_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_adds_participant_to_activity(self, client, sample_student_email):
        """Test that signup actually adds the student to participants list"""
        # Arrange
        activity_name = "Programming Class"
        email = sample_student_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_non_existent_activity_returns_404(self, client, sample_student_email):
        """Test that signup for non-existent activity returns 404"""
        # Arrange
        activity_name = "Non-existent Activity"
        email = sample_student_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_attempt_returns_400(self, client):
        """Test that duplicate signup returns 400 error"""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_multiple_different_activities(self, client, sample_student_email):
        """Test that same student can sign up for multiple activities"""
        # Arrange
        email = sample_student_email
        activity1 = "Chess Club"
        activity2 = "Drama Club"
        
        # Act
        response1 = client.post(f"/activities/{activity1}/signup", params={"email": email})
        response2 = client.post(f"/activities/{activity2}/signup", params={"email": email})
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_response_format(self, client, sample_student_email):
        """Test that signup response has correct format"""
        # Arrange
        activity_name = "Soccer Team"
        email = sample_student_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert isinstance(data["message"], str)
        assert activity_name in data["message"]
        assert email in data["message"]
