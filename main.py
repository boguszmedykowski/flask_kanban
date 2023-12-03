from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum
import io
import csv

# Konfiguracja aplikacji


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///budget.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Enum dla typów transakcji


class TransactionType(Enum):
    EXPENSE = 'Expense'
    INCOME = 'Income'

# Model transakcji


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)


# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()

# Strona główna


@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

# Dodawanie transakcji


@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            title = request.form['title']
            amount = float(request.form['amount'])
            type = TransactionType(request.form['type'])

            new_transaction = Transaction(
                title=title, amount=amount, type=type)
            db.session.add(new_transaction)
            db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            db.session.rollback()
        except ValueError:
            print("Invalid data")

        return redirect(url_for('index'))

    # Obsługa żądań GET
    return render_template('add_transaction.html')


# Usuwanie transakcji


@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        db.session.rollback()

    return redirect(url_for('index'))

# Edycja transakcji


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if request.method == 'POST':
        try:
            transaction.title = request.form['title']
            transaction.amount = float(request.form['amount'])
            transaction.type = TransactionType(request.form['type'])
            db.session.commit()
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            print(f"Error: {e}")
            db.session.rollback()
        except ValueError:
            print("Invalid data")

    return render_template('edit_transaction.html', transaction=transaction)

# Podsumowanie finansowe


@app.route('/summary')
def summary():
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.EXPENSE).scalar()
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.INCOME).scalar()
    return render_template('summary.html', total_expense=total_expense, total_income=total_income)

# Filtracja transakcji


@app.route('/filter_transactions', methods=['GET', 'POST'])
def filter_transactions():
    if request.method == 'POST':
        transaction_type = request.form['type']
        filtered_transactions = Transaction.query.filter(
            Transaction.type == TransactionType(transaction_type)).all()
        return render_template('index.html', transactions=filtered_transactions)

    return render_template('filter_transactions.html')

# Eksport danych


@app.route('/export_transactions')
def export_transactions():
    transactions = Transaction.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Title', 'Amount', 'Type'])
    for transaction in transactions:
        cw.writerow([transaction.id, transaction.title,
                    transaction.amount, transaction.type.value])

    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=transactions.csv"})


if __name__ == '__main__':
    app.run(debug=True)
