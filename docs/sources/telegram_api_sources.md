---
title: Telegram API Sources
parent: Sources
nav_order: 2
---

{: .label }
Denis Cercasin

# Telegram Bot API — Sources & References

This document lists the official references, tutorials, and code snippets that informed our implementation of Telegram bots in **Rent Tracker**.

---

## Official Documentation

- [Telegram Bot API Overview](https://core.telegram.org/bots/api)  
  Used as the main reference for understanding bot setup, commands, messages, and authentication.

- [Authorizing Your Bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)  
  Used to create and obtain the bot token via @BotFather.

- [python-telegram-bot Docs](https://docs.python-telegram-bot.org/en/stable/)  
  The official library documentation used for bot setup, polling, sending messages, and error handling.

---

## Code Snippets Referenced or Adapted

### 1. Registering `/start` command

```python
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Please link your account.")
```
Taken from Telegram Bot API examples, adapted to trigger our user-token binding logic.

### 2. Sending messages to a specific chat ID
```python
bot.send_message(chat_id=123456789, text="Your rent is due for June.")
```
Used in our daily reminder script. Syntax verified via official docs.

### 3. Using polling mode
```python
import telebot
bot = telebot.TeleBot("BOT_TOKEN")
bot.polling()
```
Used during development phase for local testing.

### 4. Preparing for webhooks (production)
We plan to switch from polling to webhooks for production deployment.
Reference used: [Webhook Setup Guide](https://core.telegram.org/bots/api#setwebhook)  

## Additional Community Threads
- [GitHub Issues – Handling expired tokens in bots](https://github.com/python-telegram-bot/python-telegram-bot/issues)

Provided insight into handling errors in long-lived sessions.

## Summary
We use two bots:
1. Registration Bot — for binding Telegram accounts using /start
2. Reminder Bot — sends monthly rent reminders based on unpaid records

Both rely on the python-telegram-bot library and were implemented using official API guidelines and adapted code snippets.