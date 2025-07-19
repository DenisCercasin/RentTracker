
# 🏠 Rent Tracker – Full Stack Rent Management App
**Rent Tracker** is a full-stack web application developed as part of a university project for the module _Full-Stack Web Development_ at HWR Berlin. The app supports property owners in managing apartments, tenants, rent payments, and monthly reminders via Telegram and Email integration.

---

## Table of Contents


- [🏠 Rent Tracker – Full Stack Rent Management App](#-rent-tracker--full-stack-rent-management-app)
  - [Table of Contents](#table-of-contents)
  - [Project Context](#project-context)
  - [Getting Started](#getting-started)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Create a virtual environment \& install dependencies](#2-create-a-virtual-environment--install-dependencies)
    - [3. Set up environment variables](#3-set-up-environment-variables)
    - [4. Initialize the database](#4-initialize-the-database)
    - [5. Run the app](#5-run-the-app)
  - [Demo User for Testing](#demo-user-for-testing)
    - [Insert Sample Data](#insert-sample-data)
    - [Test Credentials](#test-credentials)
  - [Environment Variables](#environment-variables)
  - [Reminders \& Integrations](#reminders--integrations)
  - [Documentation](#documentation)
  - [Final Presentation](#final-presentation)
  - [⚖️ License](#️-license)

---

## Project Context

- 📅 **Project Start:** 10 April 2025  
- 🎤 **Final Presentation:** 03 July 2025  
- 📌 **Final Submission Deadline:** 20 July 2025  

This application was developed by **Denis Cercasin** and **Caren Kedis** as part of the summer semester curriculum.

---

## Getting Started

To run this project locally:

### 1. Clone the repository
```bash
    git clone https://github.com/DenisCercasin/RentTracker.git
    cd renttracker
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a .env file in the root directory and define your secrets (see [below](#environment-variables)).

### 4. Initialize the database
```bash
flask init-db
```

### 5. Run the app
```bash
flask run
```
The app will be available at http://127.0.0.1:5000.

---

## Demo User for Testing
The registration flow in RentTracker requires a working SendGrid API key to send confirmation emails.
However, if you want to try out the app without setting up SendGrid, you can use a predefined test account.

### Insert Sample Data
Visit the following route in your browser:
```bash
http://127.0.0.1:5000/insert_sample
```
You’ll see a confirmation message:

> Database flushed and populated with some sample data.

This will create:
- A test user with id = 1
- Sample apartments
- Tenants
- Rental agreements
- Rent payments

### Test Credentials
You can now go back to the landing page and go to login or directly log in at http://127.0.0.1:5000/login using:

- Email: test@email.com
- Password: Asdf.12345!

Note: This user is automatically confirmed and fully functional.
You can access the dashboard, add/edit/delete entries, and explore all features freely. Reminder service will not work without the corresponding API keys.

## Environment Variables

The app uses the following environment variables stored in a `.env` file:

| Variable Name        | Required? | Description                                               |
|----------------------|-----------|-----------------------------------------------------------|
| `FLASK_SECRET_KEY`   | ✅ Yes    | Secret key for Flask session & CSRF protection            |
| `SENDGRID_API_KEY`   | ✅ Yes    | Required for sending registration confirmation emails, but test account can be used without it     |
| `TELEGRAM_BOT_TOKEN` | ❌ Optional | Enables Telegram integration for rent reminders          |

> **Note:** If you don’t want to use SendGrid, use the [demo user](#demo-user-for-testing) instead.  
> **Telegram integration** is optional – you can use email reminders only.

## Reminders & Integrations

Rent Tracker supports automated monthly rent reminders via **Telegram Bot** and **Email**.

- Email reminders work out of the box using SendGrid
- Telegram reminders require a connected bot (see integration guide)

For instructions on setting up the Telegram bot and reminder system, refer to our [Architecture Guide](./docs/technical_docs/architecture.md)

## Documentation

All documentation is available on our GitHub Pages site:

[Project Documentation (GitHub Pages)](https://deniscercasin.github.io/RentTracker/)

Includes:

- Architecture Overview  
- Data Model  
- Design Decisions  
- User Evaluation  
- Development Workflow  

---

## Final Presentation

Download our final project presentation (PDF) from 03 July 2025 here:  
👉 [RentTracker – Final Presentation (July 2025)](./docs/static/Presentation.pdf)

---

## ⚖️ License

This project is open-source and available under the [MIT License](./LICENSE)
