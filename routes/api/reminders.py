from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from db.db import get_db_con
from services.reminders_service import get_upcoming_unpaid_rents_api

reminders_api_bp = Blueprint("reminders_api", __name__)

@reminders_api_bp.route("/api/reminders/today", methods=["GET"])
def get_reminders_for_telegram_bot():
    token = request.args.get("token")
    if not token:
        return jsonify({"status": "error", "message": "Missing token"}), 401

    conn = get_db_con()
    user = conn.execute("SELECT id FROM user WHERE telegram_token = ?", (token,)).fetchone()

    if not user:
        return jsonify({"status": "error", "message": "Invalid token"}), 403

    reminders = get_upcoming_unpaid_rents_api(conn, user["id"])
    conn.close()

    return jsonify({
        "status": "success",
        "reminder_count": len(reminders),
        "data": reminders
    }), 200