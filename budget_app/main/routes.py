from flask import render_template, Blueprint

main = Blueprint('main', __name__)

# Strona główna
@main.route('/')
def index():
    return render_template('index.html')