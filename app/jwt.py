from app.auth.models import BlogUser


def authenticate(username, password):
    user = BlogUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return BlogUser.query.filter_by(id=user_id).first()



