import pytest


class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class", 
                              "Basketball Team", "Soccer Team", "Drama Club", 
                              "Art Studio", "Science Club", "Debate Team"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert all(activity in activities for activity in expected_activities)

    def test_get_activities_returns_correct_structure(self, client):
        """Test that each activity has required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert all(field in activity_data for field in required_fields)

    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is a list"""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_data in activities.values():
            assert isinstance(activity_data["participants"], list)
            assert all(isinstance(p, str) for p in activity_data["participants"])

    def test_get_activities_max_participants_is_integer(self, client):
        """Test that max_participants is an integer"""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_data in activities.values():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0
