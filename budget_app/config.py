import os

# Konfiguracja aplikacji
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///budget.db'
    SECRET_KEY = 'thisisasecretkey'