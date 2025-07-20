---
title: User Evaluation
nav_order: 4
---

{: .label }
Denis Cercasin

{: .no_toc }
# User evaluation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 02: MVP Feedback

### Meta

Status
: Work in progress - **Done** - Obsolete

Updated
: 16.07.2025

### Goal

To evaluate how well our MVP meets the needs of small-scale landlords in Romania by understanding (a) whether the core functionalities are useful and sufficient, and (b) what improvements or missing features they consider most critical. In particular, we wanted to understand the value of the reminder system and the desirability of a potential tenant-facing portal.

### Method

We shared the MVP with three potential customers, same ones from User Evaluation #1 from 16.04.2025 - small landlords from Cluj-Napoca, Romania. All three own 2–4 apartments and have direct personal contact with their tenants.  
The evaluation was done in two parts:

1. **Feature-oriented survey/interview**: we guided the users through the MVP and asked open-ended questions like:
   - What features are useful or missing?
   - How would you ideally use such a system?
   - How do you currently remind tenants?
   - Would tenant access be relevant?

2. **Usability-focused feedback**: we asked participants to interact with the system (including dashboard, reminders, adding payments) and report:
   - Which parts were intuitive or confusing?
   - How could the user flow be improved?
   - What kind of reminder timing fits their workflow?

Feedback was collected via notes and transcribed summaries. No formal scoring system was used due to the small sample size.

### Results


**Reminder System**  
- All users highly appreciated the Telegram integration, preferring it over email due to faster visibility and mobile-friendly format.  
- They proposed an enhanced model: each tenant joins the platform, and the Telegram bot creates a group chat with the landlord, tenant, and bot - so that rent reminders are visible to both parties at once.
- This was seen as a “perfect solution” and the most critical enhancement, as it replaces their current manual communication.

**Tenant Access and Payment**  
- A tenant login portal and online payment option were mentioned as desirable but classified as “nice to have.”
- The main priority was communication and accountability through automation - not payments.

**Usability Feedback**  
- Users requested two rent reminders:
  - One before the rent is due (e.g., on the 28th of the previous month).
  - One after to remind the landlord to confirm whether the payment was collected.
- One practical request was a quick-access button on the dashboard to enter payments more easily - avoiding multiple clicks.

### Implications

This evaluation showed that our MVP provides real value, especially with the automated reminders. However, we identified the following improvements for future versions:

- Explore a group-chat reminder model where the Telegram bot messages both landlord and tenant in one space.
- Open question: Should landlords also receive a separate monthly summary for all tenants, or is the chat-based flow sufficient?
- Introduce pre-rent and post-rent reminders to support better landlord workflows.
- Add a quick-add payment button to improve usability and reduce friction.
- Tenant login and payment integration can be explored later, but are not currently urgent.

We plan to iterate based on this feedback and possibly run a follow-up evaluation after the group reminder prototype is developed.

---

## 01: Early Needs Discovery

Status
: Work in progress - **Done** - Obsolete

Updated
: 16.04.2025

### Goal

To understand the most urgent pain points and expectations of small landlords before development began, with the aim of aligning our MVP feature set with real-world needs.  
Main question: **“What tasks in your rental workflow are most annoying or repetitive, and what kind of tool would actually help you?”**

### Method

We conducted 3 semi-structured interviews with small landlords in Cluj-Napoca, Romania, each managing between 2–4 apartments. These interviews took place during the first two weeks of the project.  
Each interview lasted ~30 minutes and was guided by the following prompts:

- Describe your typical process for collecting rent
- How do you remind tenants about payments?
- Where do you keep track of who paid and who didn’t?
- What would an ideal solution look like for you?
- What annoys you the most in this process?

Notes were taken manually. Interviews were conducted in Romanian and later summarized in English.

### Results

Several strong themes emerged across all three interviews:

- **Manual communication is the biggest pain point**:  
  All participants rely on messaging apps (WhatsApp, Telegram, Facebook) to remind tenants about rent. It’s time-consuming and easy to forget.

- **They manually track rent payments - and it’s error-prone**:  
  Each month, landlords manually check who paid, how much, and when. Some use notebooks or Excel, but all admitted that it's easy to forget to update, lose track, or make small errors, especially if reminders or records are delayed.

- **They want automation - but not complexity**:  
  Landlords don’t necessarily want a “full system” with dashboards, filters, or statistics. What they really need is a smart reminder tool that just works.

- **Telegram is the preferred channel**:  
  All three landlords already use Telegram with their tenants. Email is used for official stuff but ignored for reminders. A Telegram bot sending reminders was seen as a perfect fit.


### Implications

These interviews helped us shape the first version of our MVP, focusing on:

- Keeping the interface simple and avoiding feature bloat
- Prioritizing reminder logic over UI complexity

We believe this user input significantly improved our project scope and helped avoid unnecessary features. Follow-up evaluation was planned after MVP completion.


{: .fs-2 }
Last build: {{ site.time | date: '%d %b %Y, %R%:z' }}