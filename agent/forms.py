from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from agent.models import users

class RegistrationForm(FlaskForm):
    firstName = StringField('First name',
                             validators = [DataRequired(), Length(min = 2, max = 20)])
    lastName = StringField('Last name',
                             validators = [DataRequired(), Length(min = 2, max = 20)])

    email = StringField('Email',
                            validators = [DataRequired(), Email()])
    phoneNumber = StringField('Phone number',
                             validators = [DataRequired(), Length(min = 2, max = 20)])

    password =  PasswordField('Password', 
                                validators = [DataRequired()])

    confirm_password =  PasswordField('Confirm Password', 
                                validators = [DataRequired(), EqualTo('password')]) 

    submit = SubmitField('Sign up')    
    def validate_username(self, username) :
        user = users.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError(' That username is taken, please use another username!!') 
            
    def validate_email(self, email) :
        user = users.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError(' The user already exist')                  


class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators = [DataRequired(), Email()])
    
    password =  PasswordField('Password', 
                                validators = [DataRequired()])
    
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')                       

class UploadForm(FlaskForm):
    category = SelectField(choices=[('Single room','Single room'), ('Bed sitter','Bed sitter'),
                                ('One bedroom','One bedroom'),('Two bedroom','Two bedroom'),
                                ('Three bedroom','Three bedroom')])
    plotname = StringField('Plotname',
                             validators = [DataRequired(), Length(min = 2, max = 20)])
    estate = StringField('Estate',
                             validators = [DataRequired(), Length(min = 1, max = 20)])
    roomNumber = StringField('Room number',
                             validators = [DataRequired(), Length(min = 2, max = 20)])
    price = DecimalField('Price',
                          places=2, validators = [DataRequired()])
    image = FileField(render_kw={'multiple': True}, validators=[FileAllowed(['jpg','png','jpeg']),
                                         FileRequired(u'File was empty!')])
    description = TextAreaField('Description')
    submit = SubmitField(u'Upload')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                            validators = [DataRequired(), Email()])
    submit = SubmitField('Request reset password')

    def validate_email(self, email):
        user = users.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError(' There is no account with that email, register first!!') 

class ResetPasswordForm(FlaskForm):
    password =  PasswordField('Password', 
                                validators = [DataRequired()])

    confirm_password =  PasswordField('Confirm Password', 
                                validators = [DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Reset password')