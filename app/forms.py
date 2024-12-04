from flask_wtf import FlaskForm
# Importing FlaskForm for creating forms with WTForms

from wtforms import StringField, PasswordField, SubmitField
# Importing field types for the form (text, password, and submit button)

from wtforms.validators import DataRequired, Email, EqualTo
# Importing validators to enforce specific input rules (e.g., required fields, email format, and matching passwords)

class RegistrationForm(FlaskForm):
    # Defines a registration form using Flask-WTF

    username = StringField('Username', validators=[DataRequired()])
    # Text input field for the username, required

    email = StringField('Email', validators=[DataRequired(), Email()])
    # Text input field for the email, required and must follow a valid email format

    password = PasswordField('Password', validators=[DataRequired()])
    # Password input field, required

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Password confirmation field, required and must match the password field

    submit = SubmitField('Register')
    # Submit button to submit the form
