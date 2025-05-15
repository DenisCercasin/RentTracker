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
- Present a clean, usable, and extensible codebase to be able to enhance the project in the future
- Give our MVP to the first customers, collect/interpret their feedback

---

### 💻 Project Goals
> The following project goals were derived from a combination of the module **Full-Stack Web Development** requirements, real-world pain points of our target users, our personal learning objectives, and the limited timeframe available for implementation. 
>  
> All goals are prioritized using the **MoSCoW method**. See the [MoSCoW Prioritization](../wiki/MoSCoW-Prioritization-Method.md/) page for more details.
>
> All project goals are evaluated based on our internal [Definition of Done](/wiki/definition-of-done/) - standards each feature must meet before being marked as finished.


#### ✅ Must Have
These features are core to the MVP and will be implemented first:
- Admin (landlord) can log in, register, and stay logged in via sessions
- Manage apartments with full CRUD (address and basic details)
- Manage tenants with full CRUD (name, contact)
- Create rental agreements (tenant ↔ apartment with start/end/rent price)
- Track monthly payments (who paid, for what apartment and month)
- Generate monthly summary of unpaid rent (automatically)
- One JSON API endpoint (e.g. for listing unpaid rents)
- All frontend views rendered with Jinja2, styled with basic HTML/CSS
- At least 10 Flask routes across different HTTP methods

#### 🟡 Should Have
Important features that improve the experience but aren’t critical:
- Email notifications to landlords with monthly summaries
- Filter option in table "Paid Months" by apartment
- Better input validation and flash messages for user feedback
- Possibility to upload ID of the tenant

#### 🟢 Could Have
Nice additions if time permits:
- Tenant login with access to their payment history
- Optional Telegram bot integration for reminders

#### 🚫 Won’t Have (for now)
These features are out of scope for this release:
- Online payment integration (e.g. Stripe, PayPal)
- Real-time dashboard or analytics graphs
- Mobile app version
- Search options in tables (e.g filter payments by month) 
- Multilingual support (Romanian, Ukrainian, Russian)
- Export summary as PDF

---

### 👤 Personal Goals

#### **Denis Cercasin**
- Strengthen backend development skills using **Flask**, focusing on route structure, session handling, and user authentication
- Improve understanding of **database modeling** and efficient data handling with **SQLite**
- Advance proficiency in **Python** by applying it in a full-stack context
- Gain hands-on experience with the **entire development lifecycle**, from UI prototyping in Figma to frontend integration, backend logic, and deployment
- Learn how to **design and consume external APIs**, including integration of services like the **Telegram Bot API**
- Develop a structured approach to **project planning and task management** using GitHub Projects and agile-style workflows
- Enhance teamwork and **collaboration skills** through shared responsibilities, code review, and communication
- Contribute to producing a well-documented and maintainable MVP that aligns with both academic and real-world standards

#### **Caren Kedis**
- Focus on **frontend development** using **Jinja2 templating**, semantic **HTML/CSS**, and responsive layout structures
- Learn how to **integrate dynamic forms** with Flask, including handling form validation, user feedback, and error messaging
- Develop a clear understanding of how to **structure and organize views** to ensure clarity, usability, and maintainability
- Lead the **UI/UX prototyping process** by translating wireframes and hand-drawn sketches into interactive designs using **Figma**
- Build confidence with **Git and Github** for version control, branching and collaborative code management
- Enhance skills in building **user-friendly interfaces** that align with backend functionality and project requirements
- Improve fluency in working within a **full-stack development workflow**, coordinating frontend logic with backend routes and database integration
