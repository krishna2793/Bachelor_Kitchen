from bachelor_kitchen.models import User, Post
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField, RadioField, DecimalField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from datetime import datetime, date


def phone_length_check(form, field):
    if (len(str(field.data)) != 10):
        raise ValidationError('Phone number must be 10 digits')


class RegistrationForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(),
                                       Length(min=2, max=20),
                                       Regexp('^\w+$', message="Only alphanumeric and underscore allowed")])
    firstname = StringField('Firstname',
                            validators=[DataRequired(),
                                        Length(min=2, max=20),
                                        Regexp('^[.0-9a-zA-Z\s-]+$', message="Not a valid name")])
    lastname = StringField('LastName',
                           validators=[DataRequired(),
                                       Length(min=2, max=20),
                                       Regexp('^[.0-9a-zA-Z\s-]+$', message="Not a valid name")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$', message="Must have atleast 1 uppercase, 1 lowercase, 1 digit and of size 6")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    phonenum = StringField('Phone Number', render_kw={"placeholder": "XXX-XXX-XXXX"},
                           validators=[DataRequired(),
                                       Regexp('^\d{3}-\d{3}-\d{4}$', message='Phone number is not valid. Enter in xxx-xxx-xxxx format')])
    address = TextAreaField('Address', validators=[Regexp(
        '^[#.0-9a-zA-Z\s,-]+$', message="Not a valid address")])
    city = TextAreaField('City', validators=[Regexp(
        '^[#.0-9a-zA-Z\s,-]+$', message="Not a valid city")])
    zipcode = TextAreaField('Zip Code', validators=[Regexp(
        '^[#.0-9a-zA-Z\s,-]+$', message="Not a valid zipcode")])
    state = TextAreaField('state', validators=[Regexp(
        '^[#.0-9a-zA-Z\s,-]+$', message="Not a valid state")])
    dob = DateField('Date of Birth', format='%m/%d/%Y',
                    validators=[DataRequired()], render_kw={"placeholder": "MM/DD/YYYY"})
    university = TextAreaField('University', validators=[Regexp(
        '^[#.0-9a-zA-Z\s,-]+$', message="Not a valid university")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That userid is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_dob(self, dob):
        dob_val = dob.data
        if(dob_val >= date.today()):
            raise ValidationError('Date of Birth is not valid!')

    def validate_phonenum(self, phonenum):
        phone = User.query.filter_by(phonenum=phonenum.data).first()
        if phone:
            raise ValidationError(
                'That phone number is already registered with us.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
