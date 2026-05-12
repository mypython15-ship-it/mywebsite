from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Optional, ValidationError
from datetime import date


def validate_future_date(form, field):
        if field.data and field.data < date.today():
            raise ValidationError("Deadline must be today or in the future.")


class TextToMorseForm(FlaskForm):
    text = StringField("Enter the text you want to convert:", validators=[DataRequired()])
    submit = SubmitField("Convert")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")



class TaskCreationForm(FlaskForm):
    name = StringField("Name of the Task", validators=[DataRequired()])
    deadline = DateField("By when should this task be completed?", validators=[Optional(), validate_future_date])
    repetition = IntegerField("Repetition: Every X Days?", validators=[Optional()])
    category = SelectField("Category", choices=[
        ("household", "Household"),
        ("study", "Study"),
        ("workout", "Workout"),
        ("other", "Other")
    ])
    submit = SubmitField("Submit")


    

class EmptyForm(FlaskForm):
    pass
