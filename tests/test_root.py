class TestRoot:
    def test_root_redirect_to_static_index(self, client):
        """Test that GET / redirects to /static/index.html"""
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code in [307, 308]  # Redirect status codes
        assert "static/index.html" in response.headers.get("location", "")

    def test_root_redirect_follows_to_index(self, client):
        """Test that following redirect from / leads to index page"""
        # Arrange
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
