---
title: Goals Achieved and Missed
parent: Goals
grand_parent: Team Evaluation
nav_order: 1
---

{: .label }
Caren Kedis

{: .label }
Denis Cercasin

## Goals Achieved and Missed

These achievements and gaps are based on the goals we defined at the beginning of the project. You can find the original list of goals [here](goals.md).

### 👥 Group Goals

| Goal | Status | Notes |
|------|--------|-------|
| Deliver a fully functional MVP focused on landlord-side operations | ✅ Achieved | Core functionality for landlords was successfully implemented and tested. |
| Follow best practices in software architecture, version control, and documentation | 🟡 Partially Achieved | We aimed for clean code and good documentation, but there's room for improvement and consistency. |
| Use agile-style iterations, starting from Figma designs through backend and frontend integration | 🟡 Partially Achieved | Agile flow was applied, but sometimes interrupted due to changing workloads from other modules. |
| Present a clean, usable, and extensible codebase to be able to enhance the project in the future | ✅ Achieved (self-assessed) | Based on modularity and separation of concerns, we believe the codebase is future-proof. |
| Give our MVP to the first customers, collect/interpret their feedback | ✅ Achieved | MVP was tested with initial users and feedback was collected and partially applied. |

---

### 💻 Project Goals (MoSCoW Prioritization)

#### ✅ Must Have

| Feature | Status |
|---------|--------|
| Admin (landlord) can log in, register, and stay logged in via sessions | ✅ Achieved |
| Manage apartments with full CRUD (address and basic details) | ✅ Achieved |
| Manage tenants with full CRUD (name, contact) | ✅ Achieved |
| Create rental agreements (tenant ↔ apartment with start/end/rent price) | ✅ Achieved |
| Track monthly payments (who paid, for what apartment and month) | ✅ Achieved |
| Generate monthly summary of unpaid rent (automatically) | ✅ Achieved |
| One JSON API endpoint (e.g. for listing unpaid rents) | ✅ Achieved |
| All frontend views rendered with Jinja2, styled with basic HTML/CSS | ✅ Achieved |
| At least 10 Flask routes across different HTTP methods | ✅ Achieved |

#### 🟡 Should Have

| Feature | Status | Notes |
|---------|--------|-------|
| Email notifications to landlords with monthly summaries | ✅ Achieved |
| Filter option in table “Paid Months” by apartment | ✅ Achieved |
| Better input validation and flash messages for user feedback | 🟡 Partially Achieved | Present in login/register flows; limited elsewhere. |
| Possibility to upload ID of the tenant | ✅ Achieved |

#### 🟢 Could Have

| Feature | Status | Notes |
|---------|--------|-------|
| Tenant login with access to their payment history | ❌ Missed | Not implemented due to time constraints. |
| Optional Telegram bot integration for reminders | ✅ Achieved |

#### 🚫 Won’t Have (Out of Scope)

As planned, we did **not** implement the following features:

- Online payment integration (e.g. Stripe, PayPal)
- Real-time dashboard or analytics graphs
- Mobile app version
- Search options in tables
- Multilingual support (Romanian, Ukrainian, Russian)
- Export summary as PDF

---

### 👤 Personal Goals

#### Denis Cercasin

| Goal | Status |
|------|--------|
| Strengthen backend development skills using Flask | ✅ Achieved |
| Improve understanding of database modeling and SQLite usage | ✅ Achieved |
| Advance proficiency in Python within full-stack context | ✅ Achieved |
| Experience the full development lifecycle incl. Figma, backend, frontend, deployment | ✅ Achieved |
| Learn and integrate external APIs (e.g., Telegram Bot API) | ✅ Achieved |
| Apply structured project planning via GitHub Projects and agile workflow | 🟡 Partially Achieved |
| Improve teamwork, code review, communication | ✅ Achieved |
| Contribute to a well-documented and maintainable MVP | ✅ Achieved |

#### Caren Kedis

| Goal | Status |
|------|--------|
| Focus on frontend development with Jinja2, HTML/CSS, responsive design | ✅ Achieved |
| Work with dynamic Flask forms and validation | ✅ Achieved |
| Improve structure and usability of views | ✅ Achieved |
| Lead UI/UX prototyping in Figma | ✅ Achieved |
| Gain confidence with Git & GitHub for collaboration | ✅ Achieved |
| Improve full-stack fluency, esp. frontend/backend integration | ✅ Achieved |

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}