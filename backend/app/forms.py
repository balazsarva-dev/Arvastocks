from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# This file contains the form classes used in the application.
# Each form class corresponds to a specific form in the application and defines the fields and validation rules for that form.
# The forms are used to handle user input and validate it before processing.

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    
    password = PasswordField("Password",
                            validators=[DataRequired(), Length(min=6, max=20)])
    
    confirm_password = PasswordField("Confirm Password",
                                    validators=[DataRequired(), EqualTo("password")])
    
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username",
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField("Password",
                            validators=[DataRequired()])
    
    submit = SubmitField("Submit")
    
    remember = BooleanField("Remember Me")


class ContactForm(FlaskForm):
    name = StringField("Name",
                        validators=[DataRequired()])
    
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    
    message = TextAreaField("Message",
                        validators=[DataRequired()])
    
    submit = SubmitField("Send Message")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password",
                                validators=[DataRequired()])
    
    new_password = PasswordField("New Password",
                                validators=[DataRequired(), Length(min=6, max=20)])
    
    confirm_password = PasswordField("Confirm Password",
                                validators=[DataRequired(), EqualTo("new_password")])
    
    submit = SubmitField("Submit")


class UpdateEmailForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    
    confirm_email = StringField("Confirm Email",
                        validators=[DataRequired(), Email(), EqualTo("email")])
    
    password = PasswordField("Password",
                            validators=[DataRequired()])
    
    submit = SubmitField("Submit")
