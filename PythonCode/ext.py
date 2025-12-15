# ext.py
from datetime import datetime

def format_date(dt):
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "N/A"

def format_currency(amount):
    return f"${amount:.2f}" if amount else "$0.00"