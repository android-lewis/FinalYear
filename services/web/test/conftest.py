from api.model.data_spec import User
from api import create_app
import pytest

@pytest.fixture(scope="module")
def new_user():
    user = User('Pat', 'Kennedy','patkennedy79@gmail.com')
    user.set_password('Testing123')
    return user

@pytest.fixture(scope='module')
def test_client():
    app = create_app("api.config.TestConfig")
    
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!