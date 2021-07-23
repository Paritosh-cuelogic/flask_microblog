from app import create_app, db
from app.auth.models import BlogUser
from app.post.models import Post

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'BlogUser': BlogUser, 'Post': Post}
