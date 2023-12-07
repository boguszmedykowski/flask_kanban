from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from budget_app import db
from budget_app.transactions.forms import AddTransactionForm
from budget_app.models import Transaction, TransactionType

transactions = Blueprint('transactions', __name__)

# Dodawanie transakcji
@transactions.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = AddTransactionForm()

    if form.validate_on_submit():
        try:
            title = form.title.data
            amount = form.amount.data
            transaction_type = form.type.data

            print(f"Title: {title}, Amount: {amount}, Type: {transaction_type}")

            new_transaction = Transaction(
                title=title, amount=amount, type=transaction_type, user=current_user)

            db.session.add(new_transaction)
            db.session.commit()

            flash('Transaction added successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')

    return render_template('add_transaction.html', form=form)

# Usuwanie transakcji
@transactions.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        db.session.rollback()

    return redirect(url_for('dashboard'))

# Edycja transakcji
@transactions.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if request.method == 'POST':
        try:
            transaction.title = request.form['title']
            transaction.amount = float(request.form['amount'])
            transaction.type = TransactionType(request.form['type'])
            db.session.commit()
            return redirect(url_for('dashboard'))
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            db.session.rollback()
        except ValueError:
            print("Invalid data")

    return render_template('edit_transaction.html', transaction=transaction)

# Filtracja transakcji
@transactions.route('/filter_transactions', methods=['GET', 'POST'])
def filter_transactions():
    if request.method == 'POST':
        transaction_type = request.form['type']
        filtered_transactions = Transaction.query.filter(
            Transaction.type == TransactionType(transaction_type)).all()
        return render_template('dashboard.html', transactions=filtered_transactions)

    return render_template('filter_transactions.html')