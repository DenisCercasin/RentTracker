from datetime import date
from dateutil.relativedelta import relativedelta

def get_upcoming_unpaid_rents_api(conn, user_id):
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
    existing_payments = conn.execute(f"""
        SELECT apartment_id, month FROM rent_payment
        WHERE user_id = ? AND month IN ({placeholders})
    """, (user_id, *relevant_months)).fetchall()

    paid_set = set((p["apartment_id"], p["month"]) for p in existing_payments)

    results = []
    for ag in active_agreements:
        unpaid_months = [
            m for m in relevant_months
            if m >= ag["start_date"][:7]
            and (not ag["end_date"] or m <= ag["end_date"][:7])
            and (ag["apartment_id"], m) not in paid_set
        ]

        if unpaid_months:
            results.append({
                "apartment_name": ag["apartment_name"],
                "tenant_name": ag["tenant_name"],
                "months": unpaid_months,
                "monthly_rent": float(ag["rent_amount"]),
                "month_count": len(unpaid_months),
                "total_due": float(ag["rent_amount"]) * len(unpaid_months)
            })

    return results