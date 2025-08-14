from flask import Blueprint, render_template, send_file
from flask_login import login_required, current_user
from models import db, Invoice, Expense
import io, csv

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
def index():
    income = sum(i.amount for i in Invoice.query.filter_by(user_id=current_user.id).all())
    expenses = sum(e.amount for e in Expense.query.filter_by(user_id=current_user.id).all())
    profit = round(income - expenses, 2)
    totals = dict(income=round(income,2), expenses=round(expenses,2), profit=profit)
    return render_template('reports.html', totals=totals, title='Reports')

@bp.route('/export.csv')
@login_required
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Type','Date','Name/Category','Amount','Status'])
    for i in Invoice.query.filter_by(user_id=current_user.id).all():
        writer.writerow(['Invoice', i.date, i.client_name, i.amount, i.status])
    for e in Expense.query.filter_by(user_id=current_user.id).all():
        writer.writerow(['Expense', e.date, e.category, e.amount, ''])
    mem = io.BytesIO(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return send_file(mem, mimetype='text/csv', as_attachment=True, download_name='smart-invoice-report.csv')