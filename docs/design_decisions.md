---
title: Design Decisions
toc_levels: [2]
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---
## Decision 01: Database Engine Choice – SQLite

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to choose a database system to persistently store and manage application data in RentTracker. Since our data structure was clearly relational — involving apartments, tenants, rental agreements, and monthly payments — we required a relational database. The choice had to support integration with Flask and suit the project scale and team expertise.

### Decision
{: .no_toc }

We chose SQLite as the database engine for the current version of the project.
Reasons:
- Our data model is strictly relational — easily mapped to SQL tables.
- SQLite is lightweight, serverless, and integrates seamlessly with Flask.
- Course materials and professor support focused on SQLite, lowering the learning curve.
- For an MVP-stage application, SQLite provides sufficient functionality and performance.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }

We regarded two alternative options:

+ PostgreSQL
+ MySQL

| Criterion | SQLite | PostgreSQL/MySQL |
| --- | --- | --- |
| **Integration with Flask** | ✔️ Native, simple | ✔️ Requires some setup, but is "doable" |
| **Relational structure** | ✔️ Fully supported | ✔️ Fully supported |
| **Learning curve** | ✔️ Easy, covered in course | ❌ Additional overhead |
| **Server setup** | ✔️ None (file-based) | ❌ Requires database server |
| **Scalability** | ❌ Limited | ✔️ Better for scaling |

---
## Decision 02: Core Data Model - Table Structure

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to define a consistent and logical data model that reflects the domain of rental property management. The goal was to store all relevant information about apartments, tenants, their rental agreements, and payment tracking — in a way that is normalized, efficient, and easy to query.

### Decision
{: .no_toc }

We defined the following core tables:
- apartments – uniquely identifies rental units.
- tenants – stores personal details of tenants.
- rental_agreements – models contracts between tenants and apartments, with start/end dates.
- rent_payments – tracks monthly rent payments per agreement.

The structure is normalized and supports all necessary relationships (e.g., one-to-many between apartments and agreements). This design allows clear querying for reminders, overdue rents, tenant histories, support for future automation features like reminders.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }

We considered alternative structures such as:

- Combining tenants and agreements (too limiting for contract history).
- Tracking rent directly under tenants (not clear design and not scalable).

---
## Decision 03: Selective Use of WTForms and Bootstrap
### Meta
{: .no_toc }

Status
: **Work in progress** - Decided - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

WTForms and Bootstrap were introduced late in the semester, around three weeks before project submission. We had already developed most of the application using raw HTML forms and manual validation, following the teaching materials provided earlier.

Refactoring the entire UI and form logic to use WTForms and Bootstrap would have consumed time needed for implementing missing core functionality. However, these tools provide benefits like automatic validation and consistent styling, and we wanted to explore them for learning purposes.

### Decision
{: .no_toc }

We decided to partially adopt WTForms and Bootstrap in selected areas of the app, rather than refactoring all templates and forms.

Use cases include:
- WTForms: used for authentication (login/signup) and for shared logic like deletion confirmation forms.
- Bootstrap: used selectively to enhance styling in certain templates (e.g., dashboard) without rewriting all existing CSS.

This strategy allowed us to:
- Focus on completing functional features,
- Still experiment with modern tools,
- Learn through practice while minimizing unnecessary refactor risks.

Decision taken by: Caren Kedis and Denis Cercasin

### Regarded options
{: .no_toc }


| Option | Pros | Cons |
| --- | --- | --- |
| **Full refactor to WTForms + BS** | ✔️ Consistent, modern codebase | ❌ Time intensive |
| **No use of WTForms/BS** | ✔️ No additional workload, stick to known tools | ❌ Missed opportunity to learn new things |
| **Selective use** | ✔️ functional progress + exploration | ❌ Inconsistent UI |

---

## Decision 04: Use of Flask Blueprints for Modular Routing

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

The RentTracker application involves multiple modules with separate CRUD logic.

Without structure, all route handlers would reside in a single app.py or in a large routes.py, making the codebase difficult to navigate, extend, or test.

Although Flask Blueprints were not emphasized deeply in the course materials, we needed to evaluate whether using them would help us manage project complexity more effectively.

### Decision
{: .no_toc }

We decided to adopt Flask Blueprints to organize our routes by module.

Each core domain (e.g., tenants, apartments, auth) gets its own Blueprint file, grouped logically and registered with the app in app.py. This:

- Keeps the code modular and easier to maintain,
- Makes it easier to locate and isolate bugs,
- Allows better separation of concerns as the app grows,
- Allows to reuse code (e.g. same auth blueprint in multiple apps.)

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option | Pros | Cons |
| --- | --- | --- |
| **All routes in one file** | ✔️ Simpler for very small apps | ❌ Becomes unreadable and unscalable fast |
| **Manually structured files (separate route files with no Blueprints)** | ✔️ Some logical grouping | ❌ No Flask-native modularity, tricky app registration |
| **Blueprints** | ✔️ Modular, scalable, recommended for larger apps | ❌  Slight learning curve, extra initial setup |

---

## Decision 05: MVP Scope – No Tenant-Facing Interface

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

In the early planning phase, we discussed whether the RentTracker MVP should include a tenant-facing interface — where tenants could log in, view their rental details, or mark rent as paid.

Implementing such a feature would require:
-A separate user role system,
- Additional routing and authentication logic,
- Interface design for tenants,
- And possibly different database access rules.

Given limited time and the focus of the project on tracking and reminding from the owner's side, we had to evaluate the scope.

### Decision
{: .no_toc }

We decided not to include a tenant-side interface in the MVP. The app is built solely for landlords/owners.

Reasons:
- The core problem we wanted to solve was owner-side tracking of rent status and reminders.
- Most database and logic complexity lies on the owner side; tenant access would add marginal value for the first release.
- This allowed us to focus on core functionality and ensure a usable, testable MVP.

Decision taken by: Caren Kedis, Denis Cercasin, in consultation with course professor

### Regarded options
{: .no_toc }


| Option | Pros | Cons |
| --- | --- | --- |
| **Owner-side only (chosen)** | ✔️ Simpler scope | ❌ No direct tenant interaction |
| **Owner + Tenant roles** | ✔️ More realistic | ❌ More complexity |
| **Tenant-side only** | ❌ Not aligned with our core use case | ❌  Owners need full data control |

---

## Decision 06: Use of Provided Documentation Template

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

To document the development process of the RentTracker project, we needed a structured, consistent format that would allow us to explain decisions, architecture, and functionality.

With limited time and a large development workload, our goal was to use a simple, working solution that still looked clean and professional.

### Decision
{: .no_toc }

We chose to use the documentation template provided and recommended by our professor, which is hosted via GitHub Pages and uses the Just the Docs theme (a Jekyll-based static site generator).

This decision allowed us to:
- Quickly publish and structure the documentation without building it from scratch,
- Focus on content rather than layout or tooling,
- Ensure compatibility with evaluation criteria,
- Maintain a clear, navigable structure for decision logs, architecture notes, and user documentation.

The template was already known to us from course materials and easy to adapt to our specific needs.

Decision taken by: Caren Kedis, Denis Cercasin

### Regarded options
{: .no_toc }

We briefly considered building our own documentation site using tools like Sphinx, Docsify, or Docusaurus. While those would offer more control and features, they also introduced a steeper learning curve and higher setup effort.

Plain Markdown files in the repo were another option, but they lacked navigation and structure.

---

## Decision 07: Partial Use of SQLAlchemy ORM
### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We had to decide whether to use raw SQL or adopt SQLAlchemy as ORM for database interactions. SQLAlchemy was introduced only two weeks before the deadline, while most of our app already used plain SQL with SQLite.

### Decision
{: .no_toc }

We chose to stick with raw SQL for most of the app and experiment with SQLAlchemy only in the user model, where class-based structure was already needed for Flask-Login integration.

This approach allowed us to:
- Avoid time-consuming refactoring late in the project,
- -Still try out ORM concepts in one isolated case,
- Maximize development time for core features.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }

Full ORM migration was too late-stage and risky. Sticking entirely to raw SQL would limit learning. This hybrid approach gave us both stability and exposure.

Table taken from our professor's documentation:

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

---

## Decision 09: Include Secure Storage of Apartment and Tenant Documents
### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to decide whether secure upload and storage of documents (e.g., tenant IDs, utility identifiers, scanned contracts) was a valuable and realistic feature for our MVP.

Our professor requested justification, given scope constraints.

### Decision
{: .no_toc }

We decided to include this feature based on real-world needs from Romanian and Moldovan rental contexts, where utility IDs and scanned documents are often scattered across unsecure channels.

Our app addresses:
- Fragmented data (Excel, paper, chats),
- Legal and organizational risks,
- Need for centralized, structured access.

Decision taken by: Denis Cercasin, Caren Kedis

### Regarded options
{: .no_toc }

We considered skipping this for MVP scope reasons, but decided to include it due to its high practical value and positive feedback from potential users.

---

## Decision 10: Store File Paths in Database, Not BLOBs
### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

Having decided to support document uploads, we had to choose how to store the files: directly in the database as BLOBs, or as files on disk with paths stored in the DB.

### Decision
{: .no_toc }

We chose to store uploaded documents in the file system (e.g., uploads/) and save only the relative file path in the database.

Reasons:
- Keeps DB size manageable and easier to back up
- Better performance and debuggability
- Easier to support larger files and multiple uploads
- 
Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option | Pros | Cons |
|---|---|---|
| BLOB in database| ✔️ Everything in one place<br>✔️ Access control via Flask | ❌ Slower performance<br>❌ DB grows fast<br>❌ Harder to debug |
| ✅ File path (chosen) | ✔️ Lightweight DB<br>✔️ Scalable<br>✔️ Easy to inspect and back up | ❌ Needs file management<br>❌ Slightly more setup|

---

## Decision 11: Add Filtering to Rent Payments View

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

The rent payments view initially displayed a full table of all payments across all tenants, apartments, and months. As the dataset grows, this becomes overwhelming and difficult to use, especially for users managing multiple properties.

### Decision
{: .no_toc }

We introduced filtering options for the rent payments view:

- By apartment
- By tenant
- By month

This improves clarity, supports scalability, and aligns with real-world workflows.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option | Pros | Cons |
|---|---|----|
| Full table only (no filters)      | ✔️ Simple to implement<br>✔️ Shows complete history      | ❌ Hard to navigate<br>❌ Not scalable |
| ✅ Add filters (chosen)           | ✔️ Scalable<br>✔️ Better UX<br>✔️ Aligns with workflows   | ❌ More implementation effort   |

---

## Decision 12: Store One Rent Payment Entry Per Month

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

Landlords often receive rent payments covering multiple months. We had to decide how to store such entries: as a single database row listing multiple months, or as separate entries — one per month — even if submitted at once.

### Decision
{: .no_toc }

We implemented multi-month rent selection in the UI, but store each month as a separate row in the database.

Reasons:
- Clean, consistent data model (1 entry = 1 month)
- Simplifies filtering, reminders, and statistics
- Easier to support future automation (e.g., unpaid month alerts)

Decision taken by: Denis Cercasin, Caren Kedis

### Regarded options
{: .no_toc }


| Option    | Pros    | Cons    |
|------|--------|--------|
| One row for multiple months (comma-separated) | ✔️ Simple to implement<br>✔️ Matches single action         | ❌ Hard to filter/group<br>❌ Not normalized |
| ✅ One row per month (chosen)                | ✔️ Clean structure<br>✔️ Easy for analytics & reminders    | ❌ Slightly more logic needed    |

---

## Decision 13: Use GET Method for Rent Payment Filtering

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to implement filtering for the rent payments list. The question was whether to submit the filter form using GET or POST - redirecting therefore to a new route.

### Decision
{: .no_toc }

We used the GET method for filter submissions.

Reasons:
- Filtering doesn’t change data — it’s a read operation.
- GET parameters appear in the URL, making filtered views bookmarkable and shareable.
- Aligns with REST principles and improves caching behavior.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option     | Pros    | Cons   |
|---|----|-----|
| POST  | ✔️ Form data stays hidden   | ❌ Not RESTful<br>❌ No URLs/bookmarks |
| ✅ GET (chosen)   | ✔️ Bookmarkable<br>✔️ Semantic<br>✔️ Works with back button | ❌ Query string may get long    |

---

## Decision 14: Use Flask-Login with Global Access Control via `before_request`
### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We wanted users to stay logged in across visits without having to re-enter credentials each time, improving comfort and usability. We also needed to restrict access to sensitive routes (dashboard, payments, etc.) while keeping the codebase clean and manageable.

### Decision
{: .no_toc }

We used the Flask-Login package to handle authentication and session persistence via secure cookies.

For route protection, we implemented a global before_request handler to check authentication status. Only specific endpoints (login, signup, static assets) are allowed without login.

This avoids manually decorating every view with @login_required and ensures consistent access control.

Decision taken by: Caren Kedis, Denis Cercasin

### Regarded options
{: .no_toc }

| Option   | Pros  | Cons  |
|----|---|---|
| Manual `@login_required` decorators  | ✔️ Fine-grained control<br>✔️ Explicit per route             | ❌ Repetitive<br>❌ Risk of forgetting one |
| ✅ Global `before_request` (chosen)   | ✔️ Centralized control<br>✔️ Clean codebase<br>✔️ Always enforced | ❌ Slightly harder to debug route access   |

---

## Decision 15: Host Reminder Bot as Standalone Script via GitHub Actions

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

The rent reminder bot (`bot_send_reminders.py`) runs independently of the Flask app. It checks daily who should be notified and sends messages via Telegram.

We needed to decide where and how to host and trigger this script regularly, ideally without adding infrastructure complexity.

### Decision
{: .no_toc }

We decided to run the bot as a standalone Python script, triggered once daily using GitHub Actions with cron.

Reasons:
- Simple to set up
- Runs separately from Flask, avoiding blocking or session issues
- Free tier covers our needs during development and testing
- Can be moved to cron or cloud scheduler later if needed

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }

| Option | Pros  | Cons  |
|----|----|---|
| Celery + Redis              | ✔️ Scalable<br>✔️ Industry standard                   | ❌ Complex setup<br>❌ Overkill for now      |
| APScheduler in Flask        | ✔️ Easy to use                                        | ❌ Tied to app runtime<br>❌ Not reliable in prod |
| System Cron (Linux)         | ✔️ Simple, effective                                  | ❌ Requires server setup                     |
| GitHub Actions + cron (chosen) | ✔️ Fast to deploy<br>✔️ Free<br>✔️ Portable         | ❌ Limited logging/debugging                 |

---

## Decision 16: Use Python 3.11 for Compatibility with `python-telegram-bot v20+`

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We initially set up our project using Python 3.13.1, the latest version available. While Flask and most of our libraries worked fine, we encountered compatibility issues with the python-telegram-bot package (v20+), which is core to our reminder system.

This package does not yet support Python 3.13+ — installation fails or runtime errors occur due to missing or deprecated internals.

### Decision
{: .no_toc }

We downgraded the project’s virtual environment to Python 3.11.0, which is officially supported by python-telegram-bot v20+.

This ensured:
- Stable operation of the Telegram bot,
- Full compatibility with async features,
- A common version also supported by GitHub Actions and hosting environments.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                | Pros                                                    | Cons                                           |
|-----------------------|----------------------------------------------------------|------------------------------------------------|
| Python 3.13.1         | ✔️ Latest features<br>✔️ Default on some new systems    | ❌ Telegram bot fails to install/run           |
| Python 3.11.0 (chosen) | ✔️ Fully compatible with `python-telegram-bot v20+`<br>✔️ Stable | ❌ Slightly older, but no practical downsides |

---

## Decision 17: Use Telegram for Rent Reminders

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to choose a channel for sending rent reminder notifications to property owners. Options included email, Telegram, Viber, and WhatsApp.

Our goals were:
- Fast setup and easy testing,
- Real-time, mobile-friendly notifications,
- A chance to explore external API integration in practice.

### Decision
{: .no_toc }

We chose to implement reminders using a Telegram bot, integrated with the Telegram Bot API.

Reasons:
- Easy to register and control bots via Telegram Bot API.
- No manual pairing required.
- Fun and practical opportunity to work with real-world APIs.
- Telegram is widely adopted among our target users, especially in Eastern Europe.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option         | Pros                                                  | Cons                                                   |
|----------------|--------------------------------------------------------|--------------------------------------------------------|
| ✅ Telegram     | ✔️ Easy bot setup<br>✔️ Real-time<br>✔️ Fun API project | ❌ Requires user to have Telegram                     |
| Viber          | ✔️ Popular in some regions                             | ❌ Bot setup complex<br>❌ Limited docs/support        |
| WhatsApp       | ✔️ Popular globally                                    | ❌ Business-only API<br>❌ Not free/easy to test bots  |
| Email          | ✔️ Universal<br>✔️ Familiar UX                         | ❌ Less engaging<br>❌ Not real-time<br>❌ Boring 😉    |

---

## Decision 18: Telegram Reminder Workflow via API + Autonomous Bot

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We wanted to implement Telegram-based rent reminders without manually collecting users’ chat IDs. The system should be easy to use, secure, and support fully autonomous, scheduled reminder sending in the future.

Our professor also required us to include an API in our project - this presented a chance to design a clean interface between the Flask app and the Telegram bot.

### Decision
{: .no_toc }

We designed a two-part integration between the Flask app and Telegram:

1. User Chat ID Linking
- Users click a "Connect Telegram" button in the UI.
- They are redirected to our Telegram bot (t.me/OurBotName).
- On /start, the bot reads the user’s chat_id and passes it back to the Flask app, linked via a one-time token.
- The app stores this chat_id in the users table.

2. Reminder Execution
- The bot runs as a scheduled script, hosted via GitHub Actions.
- It calls a Flask API endpoint (e.g., /api/reminders/today) to fetch a list of users who should receive reminders.
- Then it sends messages using the Telegram Bot API.

This clean separation allows independent scaling and easy testing. It also fulfills the API requirement without adding unnecessary frontend complexity.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                                  | Pros                                                       | Cons                                               |
|-----------------------------------------|-------------------------------------------------------------|----------------------------------------------------|
| Manual entry of chat_id                 | ✔️ Simple                                                  | ❌ Bad UX<br>❌ Error-prone                         |
| ✅ Auto-link via Telegram + token (chosen) | ✔️ Seamless UX<br>✔️ Secure<br>✔️ No manual steps           | ❌ Needs some bot-side logic                       |
| Bot queries DB directly                 | ✔️ Direct access                                           | ❌ Tightly coupled<br>❌ Harder to scale            |
| ✅ Bot calls Flask API (chosen)         | ✔️ Clean separation<br>✔️ Reusable<br>✔️ Matches project API goal | ❌ Needs endpoint & auth                           |

**Note on polling vs. webhook:**
For simplicity, we use polling in the development phase. Webhooks may be added later for real-time responsiveness and hosting efficiency.

---

## Decision 19: Support Per-User Custom Reminder Day

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

The initial reminder logic was static: all users would receive Telegram notifications on a hardcoded day each month (e.g., the 28th). This approach lacked flexibility and didn’t reflect how landlords manage rent collection in real life.

To make reminders more useful and personal, we needed to let each user choose which day of the month they want to receive reminders.

### Decision
{: .no_toc }

We extended the reminder system to allow per-user reminder day selection, stored in the database (e.g., reminder_day column in the users table).

Each day, the scheduled bot script:
- Checks the current day (e.g., 31),
- Queries all users with `reminder_enabled` = 1 and `reminder_day` = 31,
- Sends reminders only to those matching users.

This makes reminders personal, aligns with the app’s real-world use case, and enhances user value.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                             | Pros                                                | Cons                                    |
|------------------------------------|------------------------------------------------------|-----------------------------------------|
| Hardcoded day (e.g. 28th)          | ✔️ Simple to implement                              | ❌ No personalization<br>❌ Less useful  |
| ✅ User-defined day (chosen)        | ✔️ Realistic<br>✔️ User-friendly<br>✔️ Easy to extend | ❌ Slightly more DB/query logic         |

**Related Decision:**
See [Decision 18](#decision-18-telegram-reminder-workflow-via-api--autonomous-bot) for how the Telegram bot fetches reminders via the API.

---

## Decision 20: Use SendGrid for Email Delivery Instead of Flask-Mail or SMTP

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to send confirmation/reset emails from our Flask app. Initial attempts using Flask-Mail, direct SMTP, and Gmail failed due to:

- Blocked ports on our development machines,
- Gmail rejecting test emails due to security checks,
- Flaky and slow delivery, especially during testing.

SMS was considered, but requires phone verification and external APIs, which added complexity and costs.

### Decision
{: .no_toc }

We switched to SendGrid for email delivery, based on our professor's recommendation and its easy Flask integration via API.

We also used the `itsdangerous` package to generate secure, time-limited tokens for reset links and email confirmations.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option             | Pros                                                  | Cons                                                |
|--------------------|--------------------------------------------------------|-----------------------------------------------------|
| Flask-Mail + SMTP  | ✔️ Simple setup in theory                              | ❌ Blocked ports<br>❌ Gmail restrictions            |
| Gmail via API      | ✔️ Familiar                                              | ❌ Setup overhead<br>❌ Spam/virus checks           |
| SMS                | ✔️ Fast, mobile-first                                   | ❌ Costly<br>❌ Complex<br>❌ Needs verified numbers |
| ✅ SendGrid (chosen) | ✔️ Works behind firewalls<br>✔️ API-based<br>✔️ OK free tier | ❌ Slight delay to some inboxes<br>❌ 60-day trial   |

---

## Decision 21: Use Shared Database with User-Based Row-Level Isolation

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

Initially, the app was built assuming a single user (landlord) managing data. As we moved toward multi-user support, we had to decide how to isolate user data to prevent cross-access.

Options included:
- Creating a separate database per user,
- Or enforcing row-level filtering within a shared database.

### Decision
{: .no_toc }

We chose to keep **one shared relational database** and enforce row-level isolation using a user_id foreign key on relevant tables (e.g., apartments, tenants, rental_agreements, payments).

We use current_user.id from Flask-Login to:
- Filter all user-owned data in queries,
- Assign ownership when creating new entries.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                        | Pros                                                | Cons                                              |
|-------------------------------|------------------------------------------------------|---------------------------------------------------|
| Separate DB per user          | ✔️ Full isolation                                   | ❌ Complex setup<br>❌ Not scalable                |
| Shared DB + user_id (chosen) | ✔️ Simple<br>✔️ Scalable<br>✔️ Works with Flask-Login | ❌ Requires careful query filtering                |
| No isolation (single user only) | ✔️ Easiest for MVP                                 | ❌ Not secure<br>❌ No support for real users      |

---

## Decision 22: Resolve Tenant Info at Read-Time Instead of Storing in `rent_payment`

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

Originally, we stored the `tenant_id` directly in the `rent_payment` table. This required SQL logic to look up the active rental agreement (per apartment and month) during insertion. The logic assumed only one valid agreement at a time.

However, this approach:
- Violated normalization principles,
- Created unnecessary complexity during data insertion,
- Risked inconsistency if rental agreements changed later.
  
### Decision
{: .no_toc }

We removed `tenant_id` from the `rent_payment` table and now resolve tenant data dynamically at read-time using a JOIN with the rental_agreement table.

This ensures:
- Cleaner schema (normalized),
- Historical accuracy (data doesn’t become stale if agreements change),
- Correct tenant shown for past, current, and even future months.

Tenant selection is based on the agreement where:

`DATE(?month) BETWEEN start_date AND IFNULL(end_date, DATE(?month))`

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                                  | Pros                                                  | Cons                                         |
|-----------------------------------------|--------------------------------------------------------|----------------------------------------------|
| Store `tenant_id` in `rent_payment`     | ✔️ Easier querying later                               | ❌ Redundant<br>❌ Risk of stale/invalid data |
| ✅ Resolve tenant at read-time (chosen)  | ✔️ Accurate<br>✔️ Normalized<br>✔️ Works with changes  | ❌ Slightly more query logic                 |

---

## Decision 23: Resolve Foreign Key Relationships in SQL, Not in Templates
### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to decide where to “translate” foreign keys (e.g., tenant_id, apartment_id) into human-readable names:
- Inside the SQL query using JOINs
- Or later in Jinja templates using manual lookups
  
### Decision
{: .no_toc }

We resolved all foreign key relationships (e.g., tenant name, apartment title) directly in SQL queries using JOINs.

Reasons:
- Keeps templates clean and readable
- Leverages SQL's optimized JOIN capabilities
- Allows easier filtering and sorting at the database level
- Avoids extra lookups or nested loops in Jinja

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                     | Pros                                               | Cons                                        |
|----------------------------|----------------------------------------------------|---------------------------------------------|
| ✅ SQL JOINs (chosen)       | ✔️ Efficient<br>✔️ Simple templates<br>✔️ Filterable | ❌ Requires more JOINs in queries           |
| Template-level resolution  | ✔️ May look flexible at first                      | ❌ Messy Jinja logic<br>❌ Slower/more complex |

---

## Decision 24: Keep AUTOINCREMENT IDs with Gaps and Use Loop Index for UI Displays

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

When deleting a record (e.g., apartment with ID 3) and adding a new one, the database assigns a new ID (e.g., 4), leaving gaps in the sequence. This is default behavior when using AUTOINCREMENT.

Some users may find the missing IDs confusing if exposed directly in the interface.
  
### Decision
{: .no_toc }

We kept the default AUTOINCREMENT behavior for all primary keys. IDs are:

- Unique,
- Stable,
- Not reused after deletion.

For UI tables (e.g., apartments, tenants), we show `loop.index` instead of raw database IDs to provide a clean, sequential display.

This avoids confusion, keeps logic simple, and follows best practices.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                          | Pros                                                  | Cons                                           |
|---------------------------------|--------------------------------------------------------|------------------------------------------------|
| ✅ Keep AUTOINCREMENT (chosen)   | ✔️ Safe<br>✔️ Referential integrity<br>✔️ No surprises | ❌ Gaps in raw ID sequence                     |
| Reset AUTOINCREMENT manually     | ✔️ Restores sequence                                  | ❌ Risky in production<br>❌ Breaks references |
| Assign custom IDs                | ✔️ Full control                                        | ❌ Complex<br>❌ Error-prone                    |

---

## Decision 25: Use Simple Primary Keys for rental_agreement and rent_payment

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We needed to design primary keys for rental_agreement and rent_payment. The initial idea used composite keys (e.g., apartment_id + tenant_id) but this made it hard to:
- Track agreement history over time,
- Support overlapping tenants across months,
- Record multiple payments from the same tenant.

### Decision
{: .no_toc }

We introduced simple, unique id primary keys in both tables:

`rental_agreement`:
- Has its own id
- Enforces one active agreement per apartment during a given date range
- Supports multiple historical agreements (e.g., tenant history)

`rent_payment`:
- Has its own id
- Allows multiple payments per tenant (e.g., advance payments for several months)

This design avoids duplicates, allows flexibility, and improves query simplicity.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Table             | Option                          | Pros                                                  | Cons                                               |
|-------------------|----------------------------------|--------------------------------------------------------|----------------------------------------------------|
| rental_agreement  | ✅ `id` as PK (chosen)           | ✔️ Tracks history<br>✔️ Clean relations                | ❌ Requires overlap-check logic                    |
|                   | Composite PK (apartment+tenant)  | ✔️ Enforces uniqueness                                | ❌ No history<br>❌ Can't handle changing tenants   |
| rent_payment      | ✅ `id` as PK (chosen)           | ✔️ Multiple payments allowed<br>✔️ Easy referencing   | ❌ More entries, requires validation logic         |
|                   | Composite PK (month+tenant)      | ✔️ Enforces 1 payment/month                           | ❌ Blocks prepayments<br>❌ Complex queries         |

---

## Decision 26: Implement Dashboard as a Cash Flow Projection Tool

### Meta
{: .no_toc }

Status
: Work in progress - **Decided** - Obsolete

Updated: 21-06-2025

### Problem statement
{: .no_toc }

We initially considered the dashboard as a simple home screen with basic navigation. However, our professor suggested a more meaningful use: a cash flow projection to help landlords understand both current and upcoming rental income.

The idea was to avoid short-term optimism when tenants pay in advance, and instead track when future payments will actually be due.

### Decision
{: .no_toc }

We redesigned the dashboard to focus on cash flow awareness, including:

- Number of owned apartments
- Number of active rental agreements
- Overview of months that are:
   * Already paid in advance
   * Still unpaid
- Highlight of upcoming payment deadlines

This adds practical value, improves financial planning, and helps users avoid liquidity gaps.

Decision taken by: Denis Cercasin

### Regarded options
{: .no_toc }


| Option                          | Pros                                              | Cons                                |
|---------------------------------|----------------------------------------------------|-------------------------------------|
| Navigation only   | ✔️ Easy to build                                  | ❌ Low value<br>❌ No financial insights |
| ✅ Cash flow projection (chosen) | ✔️ Real-world helpful<br>✔️ Better UX             | ❌ Requires more dynamic data logic |