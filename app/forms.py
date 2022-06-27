from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    #Check if customised validation is required for password and username -> Validators need to be increased
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


from wtforms import Form, StringField, SelectField
class SearchForm(Form):
    choices = [('Content', 'Content')]
    select = SelectField(choices=choices)
    search = StringField('')