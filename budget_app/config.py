import os

# Konfiguracja aplikacji
class Config:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    database_filename = 'budget.db'
    absolute_path = f"sqlite:///{os.path.join(current_directory, database_filename)}"

    SQLALCHEMY_DATABASE_URI = absolute_path

    SECRET_KEY = 'thisisasecretkey'