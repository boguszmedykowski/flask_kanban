from flask import render_template
from budget_app.models import Transaction
from budget_app import db

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Podsumowanie finansowe
@app.route('/summary')
@login_required
def summary():
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        type='Expense').scalar()
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        type='Income').scalar()
    return render_template('summary.html', total_expense=total_expense, total_income=total_income)