from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ExpenseForm(FlaskForm):
    # Form fields and validators
    name = StringField('Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Bills', 'Bills'), ('Other', 'Other')])
    submit = SubmitField('Add Expense')
