from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # Expense or Income


# Inicjalizacja bazy danych w kontekście aplikacji
with app.app_context():
    db.create_all()

# Strona główna z formularzem do dodawania transakcji


@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

# Dodawanie nowej transakcji


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    title = request.form['title']
    amount = float(request.form['amount'])
    type = request.form['type']

    new_transaction = Transaction(title=title, amount=amount, type=type)

    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
