# Smart Invoice (MVP)

A lightweight, global-ready invoice & expense tracker (Flask + SQLite). Mobile-friendly with light/dark mode.

## Features (MVP)
- Sign up / login
- Dashboard with KPIs
- Invoices: CRUD, status, currency
- Expenses: CRUD, category & method
- Reports: totals + CSV export
- Settings: currency & tax
- Theme toggle with persistence

## Quick Start
1. Install Python 3.10+
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure env:
   ```bash
   cp .env.example .env
   # edit SECRET_KEY in .env (optional)
   ```
5. Run:
   ```bash
   python app.py
   ```
6. Open http://127.0.0.1:5000 — register a user and start.

## Next Up (Phase 2)
- PDF invoice generation & email sending
- Multi-currency FX display
- Stripe/PayPal payment links on invoices
- Multi-user teams & roles
- Attach receipts
- Import/export Excel

## Tech
- Flask, SQLAlchemy, Flask-Login
- SQLite (local dev)
- Pure CSS (no Bootstrap) for speed

---
This is a developer-friendly starter you can deploy to Render/Heroku/Fly.io or Docker easily.