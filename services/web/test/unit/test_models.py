from api.model.data_spec import User, Gallery, Image, LikedImage

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