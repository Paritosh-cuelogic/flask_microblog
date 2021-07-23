from tests.setup import client
# from setup import client


user = {
    'username': 'demousername',
    'password': 'demopassword',
    'email': 'demo@demo.com',
    'password2': 'demopassword'
}


def register(client, username, email, password, password2):
    return client.post('/register', data=dict(
        username=username,
        password=password,
        password2=password2,
        email=email
    ), follow_redirects=True)


def login(client, username, password):
    return client.post('/login', data=dict(
            username=username,
            password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_register_page_with_get(client):
    rv = client.get('/register')
    assert b'Register' in rv.data


def test_register_new_user(client):
    rv = register(client, user['username'], user['email'], user['password'], user['password2'])
    assert b'Registered successfully' in rv.data


def test_login_page_with_get(client):
    rv = client.get('/login')
    assert b'Sign In' in rv.data


def test_login_failed(client):
    rv = login(client, user['username'], user['username'])
    assert b'Invalid username or password' in rv.data


def test_login_success(client):
    register(client, user['username'], user['email'], user['password'], user['password2'])
    rv = login(client, user['username'], user['password'])
    assert b'Say Something' in rv.data


def test_logout_success(client):
    register(client, user['username'], user['email'], user['password'], user['password2'])
    login(client, user['username'], user['password'])
    rv = logout(client)
    assert b'Logout successfully' in rv.data


def test_forgot_password(client):
    rv = client.post('/forgot_password', data={
        'email': user['email']
    }, follow_redirects=True)
    assert b'Check your email for reset password link' in rv.data

# from datetime import datetime, timedelta
# import unittest
# from app import db
# from app.auth.models import BlogUser
# from app.post.models import Post
#
# from tests.setup import SetupTestSuite
#
#
# class UserModelCase(SetupTestSuite):
#
#     def test_password_hash(self):
#         u = BlogUser(username='Animal')
#         u.set_password('cat')
#         self.assertFalse(u.check_password('dog'))
#         self.assertTrue(u.check_password('cat'))
#
#     def test_follow(self):
#         u1 = BlogUser(username='paritosh', email='paritosh@demo.com')
#         u2 = BlogUser(username='tushar', email='tushar@demo.com')
#         db.session.add_all([u1, u2])
#         db.session.commit()
#         self.assertEqual(u1.followed.all(), [])
#         self.assertEqual(u1.followers.all(), [])
#
#         u1.follow(u2)
#         db.session.add(u1)
#         db.session.commit()
#         self.assertTrue(u1.is_following(u2))
#         self.assertEqual(u1.followed.count(), 1)
#         self.assertEqual(u1.followed.first().username, 'tushar')
#         self.assertEqual(u2.followers.count(), 1)
#         self.assertEqual(u2.followers.first().username, 'paritosh')
#
#         u1.unfollow(u2)
#         db.session.commit()
#         self.assertFalse(u1.is_following(u2))
#         self.assertEqual(u1.followed.count(), 0)
#         self.assertEqual(u2.followers.count(), 0)
#
#     def test_follow_post(self):
#         u1 = BlogUser(username='john', email='john@demo.com')
#         u2 = BlogUser(username='susan', email='susan@demo.com')
#         u3 = BlogUser(username='merry', email='merry@demo.com')
#         u4 = BlogUser(username='david', email='david@demo.com')
#         db.session.add_all([u1, u2, u3, u4])
#
#         now = datetime.utcnow()
#         p1 = Post(body='Post by john', author=u1, timestamp=now + timedelta(seconds=1))
#         p2 = Post(body='Post by Susan', author=u2, timestamp=now + timedelta(seconds=4))
#         p3 = Post(body='Post by merry', author=u3, timestamp=now + timedelta(seconds=3))
#         p4 = Post(body='Post by david', author=u4, timestamp=now + timedelta(seconds=2))
#         db.session.add_all([p1, p2, p3, p4])
#         db.session.commit()
#
#         u1.follow(u2)
#         u1.follow(u4)
#         u2.follow(u3)
#         u3.follow(u4)
#         db.session.commit()
#
#         # check the followed posts of each user
#         f1 = u1.followed_posts().all()
#         f2 = u2.followed_posts().all()
#         f3 = u3.followed_posts().all()
#         f4 = u4.followed_posts().all()
#         self.assertEqual(f1, [p2, p4, p1])
#         self.assertEqual(f2, [p2, p3])
#         self.assertEqual(f3, [p3, p4])
#         self.assertEqual(f4, [p4])
#
#
# if __name__ == '__main__':
#     unittest.main(verbosity=2)
#
