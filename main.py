from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
db = SQLAlchemy(app)


# Inicjalizacja bazy danych w kontekście aplikacji


# Strona główna z formularzem do dodawania transakcji


# Dodawanie nowej transakcji


if __name__ == '__main__':
    app.run(debug=True)
