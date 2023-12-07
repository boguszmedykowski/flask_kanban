from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import current_user
from budget.models import User

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
             raise ValidationError(
                  "There already is a user with that username. Choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")

class AddTransactionForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=1, max=100)])
    amount = FloatField(validators=[InputRequired()])
    type = SelectField(validators=[InputRequired()], choices=[
        ('Expense', 'Expense'),
        ('Income', 'Income')
    ])