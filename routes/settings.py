import uuid
from flask import redirect, url_for, render_template, Blueprint, jsonify, request
from flask_login import login_required, current_user
from db import get_db_con
from datetime import datetime

settings_bp = Blueprint ("settings", __name__)

@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    settings_saved = request.args.get("settings_saved") == "true"
    return render_template("settings.html", settings_saved=settings_saved)

@settings_bp.route("/connect_telegram")
@login_required
def connect_telegram():
    token = str(uuid.uuid4())

    # Store the token for the current user
    conn = get_db_con()
    conn.execute("UPDATE user SET telegram_token = ? WHERE id = ?", (token, current_user.id))
    conn.commit()
    conn.close()

    telegram_bot_username = "RentTracker_bot"  
    telegram_link = f"https://t.me/{telegram_bot_username}?start={token}"

    return render_template("connect_telegram.html", telegram_link=telegram_link)

# @settings_bp.route("/api/reminders/today", methods=["GET"])
# def api_reminders_today():
#     today = datetime.today().strftime("%Y-%m-%d")
#     conn = get_db_con()

#     # Example: fetch users with a telegram_chat_id and due rent today (customize this!)
#     result = conn.execute("""
#         SELECT u.telegram_chat_id, u.name, a.name AS apartment_name, ra.rent_amount
#         FROM user u
#         JOIN rental_agreement ra ON ra.user_id = u.id
#         JOIN apartment a ON a.id = ra.apartment_id
#         WHERE u.telegram_chat_id IS NOT NULL
#         AND strftime('%d', ?) = '28'  -- Just for testing: simulate 28th logic
#     """, (today,)).fetchall()

#     conn.close()

#     # Convert to JSON
#     reminders = [
#         {
#             "chat_id": row["telegram_chat_id"],
#             "message": f"Hello {row['name']}, don't forget to pay {row['rent_amount']} for {row['apartment_name']}."
#         }
#         for row in result
#     ]

#     return jsonify(reminders)

@settings_bp.route("/settings/update_reminders", methods=["POST"])
@login_required
def update_reminder_settings():
    reminder_day = request.form.get("reminder_day")
    enabled = 1 if request.form.get("reminder_enabled") == "on" else 0

    conn = get_db_con()
    conn.execute(
        "UPDATE user SET reminder_day = ?, reminder_enabled = ? WHERE id = ?",
        (reminder_day, enabled, current_user.id)
    )
    conn.commit()
    return redirect(url_for("settings.settings", settings_saved="true"))
