from flask_wtf import FlaskForm
import email_validator
from wtforms import validators
from wtforms import StringField, DateField,IntegerField,SelectField, TextField,SubmitField,FileField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import ValidationError, DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from main_app.models import User 





class RegistrationForm(FlaskForm):
    first_name = StringField( validators=[DataRequired()])
    last_name = StringField( validators=[DataRequired()])
    employee_id = IntegerField(validators=[DataRequired()])
    email = StringField( validators=[DataRequired(), Email(message="Not a valid email address ")])
    phone_number = IntegerField(validators=[Length(min=10,max=10,message="Telephone number should be 10 digits")])
    password = PasswordField(validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password',message='The passwords must match')])
    agreement = BooleanField(validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # def validate_id(self, field):
    #     user = User.query.filter_by(employ=field.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    # email = StringField('Email:',validators=[DataRequired(message='This must be filled'),Email(message= "This field must be an email")])
    employee_id = IntegerField(validators=[DataRequired(message='This field is required')])
    # username = StringField(validators=[DataRequired(message="This field cannot be blank")])
    password = PasswordField(validators = [DataRequired(message="This field is required")])
    submit= SubmitField('Log in')

class PostForm(FlaskForm):
        avatar = FileField('image',validators=[FileAllowed(['gif', 'jpg', 'jpeg', 'png'],'Images only can be uploaded')] )
        

class ImageUpload(FlaskForm):
    profile_upload = FileField(validators=[FileAllowed(['gif', 'jpg', 'jpeg', 'png'],'Images only can be uploaded')])
 
class ChangePassword(FlaskForm):
     old_password =PasswordField(validators = [DataRequired(message="This field is required"),Length(min=8)])
     new_password = PasswordField(validators = [DataRequired(message="This field is required"),Length(min=8)])
     confirm_password = PasswordField(validators =[DataRequired(message="This field is required "),EqualTo('new_password',message='The passwords must match')])

