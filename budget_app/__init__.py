from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from budget_app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        initialize_extensions(app)
        db.create_all()

        from budget_app.main.routes import main
        from budget_app.transactions.routes import transactions
        from budget_app.users.routes import users
        app.register_blueprint(main)
        app.register_blueprint(transactions)
        app.register_blueprint(users)

    return app

def initialize_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)