from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum

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


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        title = request.form['title']
        amount = float(request.form['amount'])
        type = TransactionType(request.form['type'])

        new_transaction = Transaction(title=title, amount=amount, type=type)
        db.session.add(new_transaction)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        db.session.rollback()
    except ValueError:
        print("Invalid data")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
