from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Length

class AddTransactionForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=1, max=100)])
    amount = FloatField(validators=[InputRequired()])
    type = SelectField(validators=[InputRequired()], choices=[
        ('Expense', 'Expense'),
        ('Income', 'Income')
    ])