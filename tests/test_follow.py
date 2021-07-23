import datetime
from tests.setup import client
from app import db
from app.auth.models import BlogUser
from app.post.models import Post


def test_follow(client):
    u1 = BlogUser(username='paritosh', email='paritosh@demo.com')
    u2 = BlogUser(username='tushar', email='tushar@demo.com')
    db.session.add_all([u1, u2])
    db.session.commit()
    assert u1.followed.all() == []
    assert u1.followers.all() == []

    u1.follow(u2)
    db.session.add(u1)
    db.session.commit()
    assert u1.is_following(u2) is True
    assert u1.followed.count() == 1
    assert u1.followed.first().username == 'tushar'
    assert u2.followers.count() == 1
    assert u2.followers.first().username == 'paritosh'

    u1.unfollow(u2)
    db.session.commit()
    assert u1.is_following(u2) is False
    assert u1.followed.count() == 0
    assert u2.followers.count() == 0


def test_follow_post(client):
    u1 = BlogUser(username='john', email='john@demo.com')
    u2 = BlogUser(username='susan', email='susan@demo.com')
    u3 = BlogUser(username='merry', email='merry@demo.com')
    u4 = BlogUser(username='david', email='david@demo.com')
    db.session.add_all([u1, u2, u3, u4])

    now = datetime.datetime.utcnow()
    p1 = Post(body='Post by john', author=u1, timestamp=now + datetime.timedelta(seconds=1))
    p2 = Post(body='Post by Susan', author=u2, timestamp=now + datetime.timedelta(seconds=4))
    p3 = Post(body='Post by merry', author=u3, timestamp=now + datetime.timedelta(seconds=3))
    p4 = Post(body='Post by david', author=u4, timestamp=now + datetime.timedelta(seconds=2))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()

    u1.follow(u2)
    u1.follow(u4)
    u2.follow(u3)
    u3.follow(u4)
    db.session.commit()

    # check the followed posts of each user
    f1 = u1.followed_posts().all()
    f2 = u2.followed_posts().all()
    f3 = u3.followed_posts().all()
    f4 = u4.followed_posts().all()
    assert f1 == [p2, p4, p1]
    assert f2 == [p2, p3]
    assert f3 == [p3, p4]
    assert f4 == [p4]
