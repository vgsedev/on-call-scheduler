from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import ValidationError
from wtforms.fields.html5 import TelField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
    remember_me = BooleanField('Remember me')


def validate_extension(form, field):
    if not field.data.isdigit() or len(field.data) > 11:
        raise ValidationError('Extension or Phone number must be digits only and less than 11 or more than 2 digits')


def validate_sm_number(form, field):
    if not field.data.isdigit() or len(field.data) > 11 or len(field.data) < 10:
        raise ValidationError('Smart Number must be 11 digits long')


class SetupForm(FlaskForm):
    destination_ext = TelField('Default Destination Extension', [validators.InputRequired(), validate_extension])
    smart_did = TelField('Smart Number', [validators.InputRequired(), validate_sm_number])
    nx_app_id = StringField('Nexmo Application ID', [validators.InputRequired()])





