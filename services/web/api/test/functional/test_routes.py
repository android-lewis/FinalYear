"""
User Route Tests
"""

def test_get_all_users(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/user/')
    assert response.status_code == 200