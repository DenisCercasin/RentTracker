from telegram.ext import Updater, CommandHandler
from config import Config
import sqlite3

def start(update, context):
    if context.args:
        token = context.args[0]
        chat_id = update.message.chat_id

        # Save chat_id in database for this user
        conn = sqlite3.connect("instance/rent_tracker.sqlite")
        cur = conn.cursor()
        cur.execute("UPDATE user SET telegram_chat_id = ? WHERE telegram_token = ?", (chat_id, token))
        conn.commit()
        conn.close()

        update.message.reply_text("✅ Telegram successfully connected to your RentTracker account.")
    else:
        update.message.reply_text("❗ Invalid or missing token. Please use the link from the settings page.")

def main():
    updater = Updater(Config.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("🤖 Telegram bot is now running (polling)...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
