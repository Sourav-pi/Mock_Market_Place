from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        username = User.query.filter_by(username=username_to_check.data).first()
        if username :
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email_address(self,email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('An account already exist whith this email address. Please use different email address or login using username and password.')


    username = StringField(label='User Name',validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Account')
