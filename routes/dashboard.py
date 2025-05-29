from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import get_db_con
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

dashboard_bp = Blueprint ("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def index():
    conn = get_db_con()
    expected_amount = conn.execute("""
    SELECT 
    strftime('%Y-%m', months.month) AS month,
    SUM(ra.rent_amount) AS expected_income
    FROM (
        SELECT date('now', 'start of month', '+' || n || ' months') AS month 
        FROM (SELECT 0 AS n UNION ALL SELECT 1 
              UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5)
        ) AS months -- table called months with column month, dynamically creating a table with 1 column called month (asterix) and 6 lines - 6 months
    JOIN rental_agreement ra
    ON DATE(months.month) BETWEEN DATE(ra.start_date) AND IFNULL(DATE(ra.end_date), DATE('9999-12-31'))
    GROUP BY month
    """).fetchall()

    collected_amount = conn.execute("""
    SELECT rp.month, SUM(ra.rent_amount) AS collected_income
    FROM rent_payment rp
    JOIN rental_agreement ra
    ON rp.apartment_id = ra.apartment_id
    AND DATE(rp.month || '-01') BETWEEN DATE(ra.start_date) AND IFNULL(DATE(ra.end_date), DATE('9999-12-31'))
    WHERE rp.month >= strftime('%Y-%m', 'now')
    GROUP BY rp.month

    """).fetchall()

    expected_dict = {row['month']: row['expected_income'] for row in expected_amount} #using dictionary comprehension
    collected_dict = {row['month']: row['collected_income'] for row in collected_amount} #same

    months = sorted(set(expected_dict.keys()) | set(collected_dict.keys())) # list of all months from both dict with no duplicates in chronological order

    projection = []

    for m in months:
        expected_val = expected_dict.get(m, 0)
        collected_val = collected_dict.get(m, 0)
        projection.append({
            "month": datetime.strptime(m, "%Y-%m").strftime("%B %Y"),
            "expected": format_amount(expected_val),
            "collected": format_amount(collected_val),
            "missing": format_amount(max(expected_val - collected_val, 0))
        })
    
    return render_template("dashboard.html", projection=projection)

def format_amount(value):
    return str(int(value)) if value == int(value) else f"{value:.2f}"