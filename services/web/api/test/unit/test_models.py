import uuid

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, email and password_hash fields are defined correctly
    """
    assert new_user.fName == 'Pat'
    assert new_user.lName == 'Kennedy'
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password_hash != 'Testing123'

def test_new_image_with_fixture(new_image):
    """
    GIVEN an Image model
    WHEN a new Image is created
    THEN check the image_id, owner_id, file_location, name are defined correctly
    """
    
    assert new_image.image_id == uuid.UUID('94c4131d-53b9-40ad-8948-7c1db0e61e0d')
    assert new_image.owner_id == 1
    assert new_image.file_location == '/images/uploaded/test.png'
    assert new_image.name == 'Test Image'