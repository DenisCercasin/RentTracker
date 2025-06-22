import os
import requests
import sqlite3
from dotenv import load_dotenv
from telegram import Bot
from datetime import datetime
from routes.dashboard import get_upcoming_unpaid_rents

load_dotenv()

conn = sqlite3.connect("instance/rent_tracker.sqlite")
conn.row_factory = sqlite3.Row
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

def format_month(month_str):
    """Converts 'YYYY-MM' to 'Month YYYY'"""
    try:
        dt = datetime.strptime(month_str, "%Y-%m")
        return dt.strftime("%B %Y")  # e.g., 'June 2025'
    except Exception:
        return month_str  # fallback in case of format error


def get_users_with_today_as_reminder():
    cur = conn.cursor()
    today_day = datetime.today().day
    cur.execute("SELECT id, name, telegram_chat_id, telegram_token FROM user WHERE reminder_day = ? AND telegram_token IS NOT NULL", (today_day,))
    users = cur.fetchall()
    return users

def send_reminders():
    users = get_users_with_today_as_reminder()
    if not users:
        print("No users to notify today.")
        return

    for user in users:

        if not user["telegram_chat_id"] or not user ["telegram_token"]: 
            continue

        try:
            response = requests.get(
                "http://localhost:5000/api/reminders/today",
                params={"token": user["telegram_token"]},
                timeout=5
            )
            data = response.json()
            print(data)
        except Exception as e:
            print(f"❌ API call failed for {user['name']}: {e}")
            continue

        if data.get("status") != "success" or not data.get("data"):
            continue

        message = f"🔔 *Reminder for {user['name']}*\n\n"
        for rent in data["data"]:
            message += (
                f"🏠 Apartment: {rent['apartment_name']}\n"
                f"👤 Tenant: {rent['tenant_name']}\n"
                f"📆 Month(s): {', '.join(format_month(m) for m in rent['months'])}\n"
                f"💰 Total Due: {rent['total_due']}\n\n"
            )

        try:
            bot.send_message(chat_id=user["telegram_chat_id"], text=message, parse_mode="Markdown")
            print(f"✅ Reminder sent to {user['name']}")
        except Exception as e:
            print(f"⚠️ Failed to send to {user['name']}: {e}")

    conn.close()

if __name__ == "__main__":
    send_reminders()