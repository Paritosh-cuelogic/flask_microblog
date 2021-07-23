from tests.setup import client
from tests.test_auth import register, login, user


def test_create_new_post_success(client):
    register(client, user['username'], user['email'], user['password'], user['password2'])
    login(client, user['username'], user['password'])
    rv = client.post('/', data=dict(
        post='This is an sample post'
    ), follow_redirects=True)
    assert b'Post submitted successfully' in rv.data


def test_explore_posts(client):
    rv = client.get('/explore')
    assert b'Hi,' in rv.data


def test_accessing_post_without_login_fail(client):
    rv = client.get('/', follow_redirects=True)
    assert b'Please login to access this page' in rv.data
