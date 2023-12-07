from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from budget import db, bcrypt
from budget.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data)
         new_user = User(username=form.username.data, password=hashed_password)
         db.session.add(new_user)
         db.session.commit()
         return redirect(url_for('login'))
    else:
        flash('something went wrong, try again', 'error')

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
        else:
            flash('Wrong username or password. Please try again.', 'error')

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    try:
        transactions = Transaction.query.all()
        return render_template('dashboard.html', transactions=transactions)
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return "An error occurred while retrieving transactions."

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
     logout_user()
     return redirect(url_for('index'))