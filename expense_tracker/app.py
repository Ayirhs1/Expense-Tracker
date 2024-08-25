from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import ExpenseForm
import secrets
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Expense {self.name}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            name=form.name.data,
            amount=form.amount.data,
            category=form.category.data
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify({'status': 'success', 'redirect': url_for('view_expenses')}), 200
    return render_template('add_expense.html', form=form), 200

@app.route('/expenses', methods=['GET'])
def view_expenses():
    expenses = Expense.query.all()
    return render_template('view_expense.html', expenses=expenses), 200  # Ensure 200 status code

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.name = form.name.data
        expense.amount = form.amount.data
        expense.category = form.category.data
        db.session.commit() 
        return jsonify({'status': 'success', 'redirect': url_for('view_expenses')}), 200

    return render_template('edit_expense.html', form=form, expense=expense), 200

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'status': 'success', 'redirect': url_for('view_expenses')}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
