
from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from db import get_db_con
from routes.dashboard import get_upcoming_unpaid_rents

reminders_api_bp = Blueprint("reminders_api", __name__)
@reminders_api_bp.route("/api/reminders", methods=["GET"])
@login_required
def get_reminders():
    user_id = current_user.id
    print("🔍 Checking unpaid rents for user:", user_id)
    print("hello")
    conn = get_db_con()
    rows = get_upcoming_unpaid_rents(conn, user_id)

    result = []
    for row in rows:
        result.append({
            "apartment": row["apartment_name"],
            "tenant": row["tenant_name"],
            "months": row["months"],
            "total_due": row["total_due"]
        })
    print("I checked")
    return jsonify(result)
