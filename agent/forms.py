from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from agent.models import users

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                             validators = [DataRequired(), Length(min = 2, max = 20)])

    email = StringField('Email',
                            validators = [DataRequired(), Email()])

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
    plotname = StringField('Plotname',
                             validators = [DataRequired(), Length(min = 2, max = 20)])
    image = FileField(validators=[FileAllowed(['jpg','png']), FileRequired(u'File was empty!')])
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