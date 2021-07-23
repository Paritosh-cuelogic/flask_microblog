from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.auth.models import BlogUser


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(30, 50)])
    submit = SubmitField('Save')

    def __init__(self, original_username, *args, **kargs):
        super(EditProfileForm, self).__init__(*args, **kargs)
        self.original_user = original_username

    def validate_username(self, username):
        if self.original_user != username.data:
            user = BlogUser.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('User different username')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
