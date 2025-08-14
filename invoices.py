from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Invoice

bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@bp.route('/')
@login_required
def list_invoices():
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(Invoice.created_at.desc()).all()
    return render_template('invoices.html', invoices=invoices, title='Invoices')

@bp.route('/new', methods=['GET','POST'])
@login_required
def new_invoice():
    if request.method == 'POST':
        inv = Invoice(
            user_id=current_user.id,
            date=request.form['date'],
            number=request.form['number'],
            client_name=request.form['client_name'],
            client_email=request.form.get('client_email',''),
            amount=float(request.form['amount']),
            status=request.form['status'],
            currency=request.form.get('currency','USD'),
            notes=request.form.get('notes','')
        )
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('invoices.list_invoices'))
    return render_template('invoice_form.html', invoice=None, title='New Invoice')

@bp.route('/<int:invoice_id>/edit', methods=['GET','POST'])
@login_required
def edit_invoice(invoice_id):
    inv = Invoice.query.filter_by(id=invoice_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        inv.date = request.form['date']
        inv.number = request.form['number']
        inv.client_name = request.form['client_name']
        inv.client_email = request.form.get('client_email','')
        inv.amount = float(request.form['amount'])
        inv.status = request.form['status']
        inv.currency = request.form.get('currency','USD')
        inv.notes = request.form.get('notes','')
        db.session.commit()
        return redirect(url_for('invoices.list_invoices'))
    return render_template('invoice_form.html', invoice=inv, title='Edit Invoice')