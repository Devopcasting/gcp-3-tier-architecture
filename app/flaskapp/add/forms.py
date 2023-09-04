from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired,Email,ValidationError
from flaskapp import apiurl, headers
import requests

# Employee Form
class EmployeeFrom(FlaskForm):
    emp_name = StringField("Name",validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    department = SelectField('Department', choices=[('Finance','Finance'),('IT','IT'),('Human Resource','Human Resource')])
    submit = SubmitField('Add')

    def validate_email(self,email):
        valid_gmail_id = email.data
        email_data = {"email":valid_gmail_id}
        response = requests.post(apiurl+"/validemail",json=email_data,headers=headers)
        json_response = response.json()

        if valid_gmail_id.split('@')[1] != "gmail.com":
            raise ValidationError('Please enter valid gmail id')
        
        if json_response['status'] == 'error':
            raise ValidationError('Gmail id is already taken')