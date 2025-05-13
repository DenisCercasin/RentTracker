---
title: Goals
parent: Team Evaluation
nav_order: 1
---

{: .label }
Caren Kedis
{: .label }
Denis Cercasin

{: .no_toc }
## 🎯 Goals

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

### 👥 Group Goals

As a team, we aim to:
- Deliver a fully functional MVP focused on landlord-side operations
- Follow best practices in software architecture, version control, and documentation
- Use agile-style iterations, starting from Figma designs through backend and frontend integration
- Present a clean, usable, and extensible codebase

---

### 💻 Project Goals


#### ✅ Must Have
These features are core to the MVP and will be implemented first:
- Admin (landlord) can log in, register, and stay logged in via sessions
- Manage apartments with full CRUD (address and basic details)
- Manage tenants with full CRUD (name, contact, ID upload)
- Create rental agreements (tenant ↔ apartment with start/end/rent)
- Track monthly payments (who paid, for what apartment and month)
- Generate monthly summary of unpaid rent (automatically)
- One JSON API endpoint (e.g. for listing unpaid rents)
- All frontend views rendered with Jinja2, styled with basic HTML/CSS
- At least 10 Flask routes across different HTTP methods

#### 🟡 Should Have
Important features that improve the experience but aren’t critical:
- Email notifications to landlords with monthly summaries
- Optional Telegram bot integration for reminders
- Search and filter options in tables (e.g. filter payments by month)
- Better input validation and flash messages for user feedback
- Tenant CRUD: assign tenant to a new apartment on update

#### 🟢 Could Have
Nice additions if time permits:
- Tenant login with access to their payment history
- Multilingual support (Romanian, Ukrainian, Russian)
- Apartment image upload or gallery
- Export summary as PDF

#### 🚫 Won’t Have (for now)
These features are out of scope for this release:
- Online payment integration (e.g. Stripe, PayPal)
- Real-time dashboard or analytics graphs
- Mobile app version
- Full admin panel with role management

---

### 👤 Personal Goals

#### **Denis Cercasin**
- Improve backend skills with Flask and database modeling
- Learn session management, user roles, and secure form handling
- Gain experience in the full app lifecycle — from Figma to deployment
- Strengthen project planning and collaboration skills

#### **Caren Kedis**
- Focus on frontend development using Jinja2, HTML/CSS, and layout structure
- Work on integrating forms and feedback loops with Flask
- Learn how to structure views for clarity and usability
- Lead the visual prototyping using Figma
---

## Goals achieved and missed
TBD
