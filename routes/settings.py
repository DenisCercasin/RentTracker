import uuid
from flask import redirect, url_for, render_template, Blueprint, jsonify, request
from flask_login import login_required, current_user
from db.db import get_db_con
from datetime import datetime

settings_bp = Blueprint ("settings", __name__)

@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required #nur Eingelogter 
def settings():
    settings_saved = request.args.get("settings_saved") == "true"
    conn = get_db_con()
    cur = conn.cursor()
    preferences = cur.execute("SELECT reminder_day, reminder_enabled, use_telegram, use_email FROM user WHERE id = ?", (current_user.id,)).fetchone()
    conn.close()
    if preferences:
        current_user.reminder_day = preferences["reminder_day"]
        current_user.reminder_enabled = preferences["reminder_enabled"]
        current_user.use_telegram = preferences["use_telegram"]
        current_user.use_email = preferences["use_email"]

    return render_template("settings/settings.html", settings_saved=settings_saved)

@settings_bp.route("/connect_telegram")
@login_required
def connect_telegram():
    token = str(uuid.uuid4())

 # Speichere das Token in der Datenbank für den aktuellen Nutzer
    conn = get_db_con()
    cur = conn.cursor()
    cur.execute("UPDATE user SET telegram_token = ? WHERE id = ?", (token, current_user.id))
    conn.commit()
    conn.close()

    telegram_bot_username = "RentTracker_bot"  
    telegram_link = f"https://t.me/{telegram_bot_username}?start={token}"

    return render_template("settings/connect_telegram.html", telegram_link=telegram_link)

@settings_bp.route("/settings/update_reminders", methods=["POST"])
@login_required
def update_reminder_settings():
    reminder_day = request.form.get("reminder_day")
    reminder_enabled = 1 if request.form.get("reminder_enabled") == "on" else 0
    use_telegram = 1 if request.form.get("use_telegram") == "on" else 0
    use_email = 1 if request.form.get("use_email") == "on" else 0

    conn = get_db_con()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user 
        SET reminder_day = ?, reminder_enabled = ?, use_telegram = ?, use_email = ?
        WHERE id = ?
    """, (reminder_day, reminder_enabled, use_telegram, use_email, current_user.id))
    conn.commit()
    conn.close()
    
    return redirect(url_for("settings.settings", settings_saved="true"))
