from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class RegisterForm(FlaskForm):
    team = StringField("Team Name: ", validators=[InputRequired()])
    captain = StringField("Captain's Name: ", validators=[InputRequired()])
    submit = SubmitField("Submit")

class HomeForm(FlaskForm):
    submit = SubmitField("Register a team")

class JoinForm(FlaskForm):
    name = StringField("Full Name: ", validators=[InputRequired()])
    position = SelectField("Position: ", choices=["Goal Keeper", "Defender", "Midfielder", "Forward"],
    default="Midfielder")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:")
    password = PasswordField("Password:")
    submit = SubmitField("Submit")
    
class AdminForm(FlaskForm):
    admin_id = StringField("Admin id:")
    admin_password = PasswordField("Password:")
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 =  PasswordField(" Confirm Password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")  

class UpdateForm(FlaskForm):
    points = StringField("Update Points: ")
    games = StringField("Update Games: ")
    submit = SubmitField("Submit")
    