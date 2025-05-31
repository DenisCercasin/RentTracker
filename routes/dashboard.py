from flask import Blueprint, render_template, request, flash, redirect, url_for
from db import get_db_con
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_login import current_user

dashboard_bp = Blueprint ("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods = ["GET","POST"])
def index():

    if request.method=="GET":
        conn = get_db_con()

        # part with basic statistics
        total_apartments = conn.execute("SELECT COUNT(*) FROM apartment WHERE user_id = ?", (current_user.id,)).fetchone()[0]
        active_agreements = conn.execute("""
                                        SELECT COUNT(*) FROM rental_agreement
                                        WHERE DATE(start_date) <= DATE('now')
                                        AND (end_date IS NULL OR DATE(end_date) >= DATE('now')) AND user_id = ?
                                        """, (current_user.id,)).fetchone()[0]
        
        # payments for the upcoming month
        upcoming_unpaid = get_upcoming_unpaid_rents(conn, current_user.id)

        #part with cash flow projection
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
        WHERE ra.user_id = ?
        GROUP BY month
        """, (current_user.id,)).fetchall()

        collected_amount = conn.execute("""
        SELECT rp.month, SUM(ra.rent_amount) AS collected_income
        FROM rent_payment rp
        JOIN rental_agreement ra
        ON rp.apartment_id = ra.apartment_id
        AND DATE(rp.month || '-01') BETWEEN DATE(ra.start_date) AND IFNULL(DATE(ra.end_date), DATE('9999-12-31'))
        WHERE rp.month >= strftime('%Y-%m', 'now') AND rp.user_id = ?
        GROUP BY rp.month

        """,(current_user.id,)).fetchall()

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
        
        return render_template("dashboard.html", projection=projection, total_apartments = total_apartments, active_agreements = active_agreements, upcoming_unpaid = upcoming_unpaid)

def format_amount(value):
    return str(int(value)) if value == int(value) else f"{value:.2f}"

def get_upcoming_unpaid_rents(conn, user_id):
    today = date.today()
    relevant_months = [(today + relativedelta(months=delta)).strftime("%Y-%m") for delta in [-2, -1, 0, 1]]

    active_agreements = conn.execute("""
        SELECT 
            a.name AS apartment_name,
            t.name AS tenant_name,
            ra.rent_amount,
            ra.apartment_id,
            ra.tenant_id,
            ra.start_date,
            ra.end_date
        FROM rental_agreement ra
        JOIN apartment a ON ra.apartment_id = a.id
        JOIN tenant t ON ra.tenant_id = t.id
        WHERE ra.user_id = ?
    """, (user_id,)).fetchall()

    placeholders = ','.join(['?'] * len(relevant_months))
    query = f"""
    SELECT apartment_id, month FROM rent_payment
    WHERE user_id = ? AND month IN ({placeholders})
    """
    params = (user_id, *relevant_months)
    existing_payments = conn.execute(query, params).fetchall()

    paid_set = set((p["apartment_id"], p["month"]) for p in existing_payments)

    upcoming_unpaid = []
    for ag in active_agreements:
        unpaid_months = []
        for m in relevant_months:
            if m >= ag["start_date"][:7] and (not ag["end_date"] or m <= ag["end_date"][:7]):
                if (ag["apartment_id"], m) not in paid_set:
                    unpaid_months.append(m)

        if unpaid_months:
            upcoming_unpaid.append({
                "apartment_name": ag["apartment_name"],
                "tenant_name": ag["tenant_name"],
                "months": unpaid_months,
                "total_due": f"{ag['rent_amount'] * len(unpaid_months):.0f}€ ({ag['rent_amount']:.0f}€ x {len(unpaid_months)})"
            })

    return upcoming_unpaid