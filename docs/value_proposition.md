---
title: Value Proposition
nav_order: 1
---
{: .label }
Denis Cercasin

{: .label }
Caren Kedis

{: .no_toc }
# Value proposition

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## ❗ Problem

Landlords in Romania, Moldova, and Ukraine often manage their rental operations manually, typically using paper notebooks to track tenant data and payment statuses across multiple apartments. 

Each month, they manually check who needs to pay, remember payment timelines, and follow up with tenants. Since tenants pay irregularly (some in advance, some late), tracking becomes error-prone and time-consuming. 

These manual systems are vulnerable to loss, damage, and human error, making it hard to stay organized, especially when managing many properties.


## 💡 Our solution

*Rent Tracker* is a user-friendly web application designed for landlords to digitalize their rental management process. It enables:
- Automatic detection of unpaid and upcoming payments
- Manual entry of monthly rent payments through simple forms
- Secure storage of tenant and apartment information (including ID photo, phone, email)
- Easy assignment of tenants to apartments through rental agreements
- Monthly reminders and summaries via email or Telegram — depending on the landlord’s preference

This eliminates manual work, reduces errors, and helps landlords stay in control—anytime, anywhere. The platform will launch in **English first**, with later versions in **Romanian, Ukrainian, and Russian** languages, reflecting our focus on landlords from Eastern Europe.

## 🎯 Target users


Our primary users are **independent landlords** from **Romania, Moldova, and Ukraine** who own and lease out **multiple residential apartments**, often juggling Excel sheets, paper contracts, and late-night text messages from tenants.

### Persona Snapshot

Meet **Elena**, a 45-year-old landlord from Chișinău who manages 6 rental units across the city. She’s tech-comfortable but not a developer, tired of forgetting who paid what, and loves the idea of getting a clean monthly rent summary and Telegram reminders — without needing to build a system herself.

Whether it's **Mihai from Cluj**, **Dmytro in Lviv**, or **Oleg with flats in Iași and a cat named Pixel**, our users are looking for:

- **Clear rent tracking**  
- **Tenant contract management**  
- **Automated, no-stress reminders**

**Rent Tracker** is built for these self-sufficient owners — people who don’t want bloated property management software, but need more than a notebook and hope.

## 🧭 Customer journey Overview (Landlord Perspective)

The following table illustrates the **customer journey for a landlord using RentTracker**, outlining each step from initial access to successful rent tracking and reminder automation. It highlights key user actions, goals, touchpoints, and emotional states at each stage of the journey, helping to understand how the app supports landlords in their monthly workflow.

For a more detailed view, including slide-by-slide screen flows and captions, refer to the PDF version:  
[RentTracker Customer Journey – Happy Path (PDF)](./RentTracker_Customer_Journey_Happy_Path.pdf)


| Stage             | User Goal                                      | Touchpoints                               | User Actions                                                  | Emotions               | Opportunities for Rent Tracker                                 |
|-------------------|------------------------------------------------|--------------------------------------------|----------------------------------------------------------------|------------------------|----------------------------------------------------------------|
| 1. Awareness       | Find a simple way to track rents & tenants     | Google search, Telegram community, referral | Landlord hears about Rent Tracker from another landlord         | Curious, skeptical     | Highlight simplicity, offline-friendliness, Telegram bot       |
| 2. Onboarding      | Register & set up the account                  | Website, Signup/Login page                 | Creates account, logs in, sees clean dashboard                  | Hopeful, unsure        | Guide setup steps, show empty state hints                      |
| 3. Setup           | Add apartments, tenants, and rental contracts | Dashboard → Apartments → Add Tenant       | Enters apartments, links tenants with start/end dates           | Focused, overwhelmed   | Use smart forms (WTForms), provide example inputs              |
| 4. First Usage     | View rent status, receive first reminders     | Dashboard, Rent Month Overview, Telegram   | Notices pending/unpaid rent, gets Telegram reminder             | Impressed, reassured   | Reminder customization, confirm rent paid in one click         |
| 5. Regular Use     | Monitor payments & tenants monthly            | Dashboard, Telegram bot                    | Checks dashboard monthly, relies on reminders                   | Confident, relaxed     | Auto-sorting, upcoming tenant start notifications              |
| 6. Advanced Features | Manage Telegram settings, edit tenant history | Settings, Tenant edit page                | Updates Telegram bot, modifies a past record                    | In control, appreciative| Offer backup/export options, activity log                      |
| 7. Support/Feedback| Resolve questions, suggest features           | FAQ, Contact page, Telegram support        | Asks for help connecting bot or understanding rent logic        | Frustrated or thankful | Add contextual tooltips, offer simple feedback form            |
| 8. Retention       | Continue using monthly, recommend to others   | Word of mouth, bot referral                | Recommends to other landlords, adds another property            | Loyal, satisfied       | Add referral system, new apartment templates                   |

{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}