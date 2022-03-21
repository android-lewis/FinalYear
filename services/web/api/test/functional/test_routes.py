import json
import logging

mylogger =  logging.getLogger(__name__)

"""
User Route Tests
"""

def test_register(test_client):
    """
    Register user
    """
    data = {
        'f_name': 'Lewis',
        'l_name': 'Baston',
        'email': 'test@test.com',
        'password': 'Test@123'
    }
    response = test_client.post('/user/register', data=json.dumps(data), headers={"Content-Type": "application/json"})
    mylogger.info(response)
    assert response.status_code in [200, 409]

def login(test_client):
    data = {
        'email': 'test@test.com',
        'password': 'Test@123'
    }
    return test_client.post('/user/login', data=json.dumps(data), headers={"Content-Type": "application/json"})

def test_login(test_client):
    """
    Get a token by logging in

    """
    response = login(test_client)
    mylogger.info(response)
    assert response.status_code == 200

def test_get_all_users(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/user/')
    assert response.status_code == 200

def test_get_current_user(test_client):
    """
    Needs a token
    """
    logindetails = login(test_client)
    print(json.loads(logindetails.data)["token"])
    response = test_client.get('/user/get', headers={'x-access-tokens': f'{json.loads(logindetails.data)["token"]}' })
    assert response.status_code == 200

"""
Image Route Tests
"""



