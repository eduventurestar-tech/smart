from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Expense

bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@bp.route('/')
@login_required
def list_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.created_at.desc()).all()
    return render_template('expenses.html', expenses=expenses, title='Expenses')

@bp.route('/new', methods=['GET','POST'])
@login_required
def new_expense():
    if request.method == 'POST':
        ex = Expense(
            user_id=current_user.id,
            date=request.form['date'],
            category=request.form['category'],
            amount=float(request.form['amount']),
            method=request.form.get('method','Cash')
        )
        db.session.add(ex)
        db.session.commit()
        return redirect(url_for('expenses.list_expenses'))
    return render_template('expense_form.html', expense=None, title='Add Expense')

@bp.route('/<int:expense_id>/edit', methods=['GET','POST'])
@login_required
def edit_expense(expense_id):
    ex = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        ex.date = request.form['date']
        ex.category = request.form['category']
        ex.amount = float(request.form['amount'])
        ex.method = request.form.get('method','Cash')
        db.session.commit()
        return redirect(url_for('expenses.list_expenses'))
    return render_template('expense_form.html', expense=ex, title='Edit Expense')