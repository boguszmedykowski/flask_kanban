from flask import url_for, current_app
from models import Transaction
from io import StringIO
from csv import writer

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