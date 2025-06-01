import os
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


def get_users_with_today_as_reminder():
    cur = conn.cursor()
    today_day = datetime.today().day
    cur.execute("SELECT id, name, telegram_chat_id FROM user WHERE reminder_day = ?", (today_day,))
    users = cur.fetchall()
    return users

def send_reminders():
    users = get_users_with_today_as_reminder()
    if not users:
        print("No users to notify today.")
        return

    for user in users:

        if not user["telegram_chat_id"]:
            continue
        unpaid_rents = get_upcoming_unpaid_rents(conn, user["id"])
        if not unpaid_rents:
            continue

        message = f"🔔 *Reminder for {user['name']}*\n\n"
        for rent in unpaid_rents:
            message += (
                f"🏠 Apartment: {rent['apartment_name']}\n"
                f"👤 Tenant: {rent['tenant_name']}\n"
                f"📆 Month(s): {rent['months']}\n"
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
