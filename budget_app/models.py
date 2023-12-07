from budget_app import db, login_manager
from flask_login import UserMixin
from enum import Enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Enum dla typów transakcji
class TransactionType(Enum):
    EXPENSE = 'Expense'
    INCOME = 'Income'

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Model transakcji
class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)