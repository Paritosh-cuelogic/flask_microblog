from tests.setup import client
from tests.test_auth import register, login, user


def test_user_profile_update(client):
    register(client, user['username'], user['email'], user['password'], user['password2'])
    login(client, user['username'], user['password'])
    rv = client.post('/edit-profile', data={
        'username': user['username'],
        'about_me': 'I am an sample user............'
    }, follow_redirects=True)
    assert b'Profile updated successfully' in rv.data
