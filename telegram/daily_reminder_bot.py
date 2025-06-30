import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import sqlite3
from dotenv import load_dotenv
from telegram import Bot
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from services.reminders_service import get_upcoming_unpaid_rents_api


load_dotenv()

conn = sqlite3.connect("../instance/rent_tracker.sqlite")
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
    cur.execute("""
    SELECT id, name, email, telegram_chat_id, telegram_token, use_email, use_telegram 
    FROM user 
    WHERE reminder_day = ? AND reminder_enabled = 1""", (today_day,))    
    users = cur.fetchall()
    return users

def send_email_notification(to_email, subject, html_content):
    message = Mail(
        from_email='rent.tracker.hwr@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            print(f"Email sent to {to_email}")
        else:
            print(f"Failed to send email: {response.status_code}, {response.body}")
    except Exception as e:
        print(f"Exception while sending email to {to_email}: {e}")

def send_reminders():
    users = get_users_with_today_as_reminder()
    if not users:
        print("No users to notify today.")
        return
    for user in users:
            # FOR TELEGRAM USERS — use the API
        if user["use_telegram"] and user["telegram_chat_id"] and user["telegram_token"]:
            try:
                response = requests.get(
                    "http://localhost:5000/api/reminders/today",
                    params={"token": user["telegram_token"]},
                    timeout=5
                )
                data = response.json()
                if data.get("status") != "success" or not data.get("data"):
                    continue

                message = f"🔔 *Reminder for {user['name']}*\n\n"
                for rent in data["data"]:
                    message += (
                        f"🏠 Apartment: {rent['apartment_name']}\n"
                        f"👤 Tenant: {rent['tenant_name']}\n"
                        f"📆 Month(s): {', '.join(format_month(m) for m in rent['months'])}\n"
                        f"💰 Total Due: {float(rent['total_due']):.0f}€\n\n"
                    )

                bot.send_message(chat_id=user["telegram_chat_id"], text=message, parse_mode="Markdown")
                print(f"Telegram reminder sent to {user['name']}")
            except Exception as e:
                print(f"Telegram failed for {user['name']}: {e}")

        # FOR EMAIL USERS — use service function directly
        if user["use_email"] and user["email"]:
            try:
                rents = get_upcoming_unpaid_rents_api(conn, user["id"])
                if not rents:
                    continue

                email_html = f"<h3>Reminder for {user['name']}</h3>"
                for rent in rents:
                    email_html += f"""
                    <p>
                    <strong>🏠 Apartment:</strong> {rent['apartment_name']}<br>
                    <strong>👤 Tenant:</strong> {rent['tenant_name']}<br>
                    <strong>📆 Month(s):</strong> {', '.join(format_month(m) for m in rent['months'])}<br>
                    <strong>💰 Total Due:</strong> {rent['total_due']}€
                    </p>
                    <hr>
                    """
                send_email_notification(
                    to_email=user["email"],
                    subject="Your Rent Payment Reminder",
                    html_content=email_html
                )
                print(f"Email reminder sent to {user['name']}")
            except Exception as e:
                print(f"Email failed for {user['name']}: {e}")

if __name__ == "__main__":
    send_reminders()