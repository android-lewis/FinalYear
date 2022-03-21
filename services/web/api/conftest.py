from api.model.data_spec import ( User, Image, Gallery )
from api import create_app
import uuid
import pytest

@pytest.fixture(scope="module")
def new_user():
    user = User('Pat', 'Kennedy','patkennedy79@gmail.com')
    user.set_password('Testing123')
    return user

@pytest.fixture(scope="module")
def new_image():
    image = Image(uuid.UUID('94c4131d-53b9-40ad-8948-7c1db0e61e0d'), 1, '/images/uploaded/test.png','Test Image', 'Generated')
    return image

@pytest.fixture(scope="module")
def new_gallery():
    gallery = Gallery(1, "Test", 1)
    return gallery

@pytest.fixture(scope='module')
def test_client():
    app = create_app("api.config.TestConfig")
    
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!