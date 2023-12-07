from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, logout_user, login_required
from budget_app import db, bcrypt
from budget_app.models import User, Transaction
from budget_app.users.forms import RegisterForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data)
         new_user = User(username=form.username.data, password=hashed_password)
         db.session.add(new_user)
         db.session.commit()
         flash('Konto utworzone!', 'success')
         return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('users.dashboard'))
        else:
            flash('Wrong username or password. Please try again.', 'error')

    return render_template('login.html', form=form)

@users.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    try:
        transactions = Transaction.query.all()
        return render_template('dashboard.html', transactions=transactions)
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return "An error occurred while retrieving transactions."

@users.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect(url_for('main.index'))

# Podsumowanie finansowe
@users.route('/summary', methods=['GET', 'POST'])
@login_required
def summary():
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        type='Expense').scalar()
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        type='Income').scalar()
    return render_template('users.summary.html', total_expense=total_expense, total_income=total_income)