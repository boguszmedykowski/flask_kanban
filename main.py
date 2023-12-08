from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from enum import Enum
import io
import csv

# Konfiguracja aplikacji


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///budget.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
bcrypt = Bcrypt(app)
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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


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


# Inicjalizacja bazy danych
with app.app_context():
    db.create_all()

# Strona główna.


@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

# Dodawanie transakcji


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
