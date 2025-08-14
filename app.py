import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, current_user
from dotenv import load_dotenv
from models import db, User, Invoice, Expense, Setting
from auth import bp as auth_bp
from invoices import bp as invoices_bp
from expenses import bp as expenses_bp
from reports import bp as reports_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_invoice.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(reports_bp)

    @app.route('/')
    @login_required
    def index():
        # Simple month-to-date metrics
        invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(Invoice.created_at.desc()).limit(5).all()
        expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.created_at.desc()).limit(5).all()
        total_income = round(sum(i.amount for i in Invoice.query.filter_by(user_id=current_user.id).all()), 2)
        total_expenses = round(sum(e.amount for e in Expense.query.filter_by(user_id=current_user.id).all()), 2)
        metrics = dict(income=total_income, expenses=total_expenses, balance=round(total_income-total_expenses,2))
        return render_template('index.html', metrics=metrics, recent_invoices=invoices, recent_expenses=expenses, title='Dashboard')

    @app.route('/settings', methods=['GET','POST'])
    @login_required
    def settings():
        s = Setting.query.filter_by(user_id=current_user.id).first()
        if request.method == 'POST':
            s.currency = request.form.get('currency','USD')
            s.tax = float(request.form.get('tax', 0.0))
            db.session.commit()
            return redirect(url_for('settings'))
        return render_template('settings.html', settings=s, title='Settings')

    @app.route('/toggle-theme', methods=['POST'])
    def toggle_theme():
        if current_user.is_authenticated:
            current_user.theme = 'dark' if current_user.theme == 'light' else 'light'
            db.session.commit()
        return ('', 204)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)