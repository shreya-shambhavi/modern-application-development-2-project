# Influencer Engagement & Sponsorship Coordination Platform (IESCP)

A full-stack web application that connects **Sponsors** (brands/companies) with **Influencers** for marketing campaigns and ad requests, with an **Admin** layer for platform moderation and analytics.

The platform allows sponsors to create and manage advertising campaigns, influencers to discover and apply to campaigns (or receive direct requests), and admins to monitor, approve, and moderate all platform activity.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Background Jobs (Celery)](#background-jobs-celery)
- [Default Credentials](#default-credentials)
- [API Overview](#api-overview)
- [License](#license)

---

## Features

### 👤 Role-Based Access
Three distinct user roles managed via **Flask-Security**: `Admin`, `Sponsor`, and `Influencer`, each with a dedicated dashboard and permission set.

### 🛡️ Admin
- Approve or reject newly registered sponsors
- View, search, and moderate all influencers, sponsors, campaigns, and ad requests
- Flag/unflag sponsors, influencers, and campaigns
- View aggregated platform-wide statistics (active campaigns, ad request counts, flagged entities, etc.)

### 🏢 Sponsor
- Create, update, and delete advertising campaigns (public or private)
- Search and filter influencers by category/reach
- Send and receive ad requests to/from influencers
- Monitor active influencer tasks and their progress
- Review completed tasks and track total payments made
- Export campaign data as a downloadable CSV (asynchronous job)

### 📣 Influencer
- Browse and search public campaigns by name, budget, or target audience
- Send and receive ad requests to/from sponsors
- Track active tasks with a live progress indicator (0% → 100% → payment)
- View completed tasks and total earnings
- Manage a personal profile with category, reach, and description

### ⚙️ Platform-Wide
- Secure token-based authentication (`Flask-Security-Too`)
- RESTful CRUD API (`Flask-RESTful`) for all core resources
- Server-side response caching (`Flask-Caching` + Redis)
- Asynchronous background processing (`Celery` + Redis broker)
- Automated daily reminder emails and monthly performance reports
- CSV export of campaign data via background worker

---

## Tech Stack

### Backend
| Component | Technology |
|---|---|
| Framework | Flask |
| ORM | Flask-SQLAlchemy (SQLite) |
| Auth & RBAC | Flask-Security-Too |
| REST API | Flask-RESTful |
| Caching | Flask-Caching (Redis) |
| Background Jobs | Celery (Redis broker/backend) |
| Email | smtplib (SMTP) |
| CSV Export | Flask-Excel / pyexcel |
| Templating | Jinja2 |

### Frontend
| Component | Technology |
|---|---|
| Framework | Vue 3 (Composition-ready, Options API used) |
| Routing | Vue Router 4 |
| State Management | Vuex 4 |
| HTTP Client | Axios |
| UI | Bootstrap 5 |
| Build Tool | Vue CLI 5 |

---

## Architecture

```
┌─────────────────┐        REST/JSON        ┌──────────────────┐
│   Vue 3 SPA     │ ───────────────────────▶ │   Flask API      │
│ (Vuex + Router) │ ◀─────────────────────── │ (Flask-RESTful)  │
└─────────────────┘                          └────────┬─────────┘
                                                       │
                                     ┌─────────────────┼─────────────────┐
                                     ▼                 ▼                 ▼
                              ┌───────────┐     ┌─────────────┐   ┌────────────┐
                              │  SQLite   │     │ Redis Cache │   │   Celery   │
                              │ (SQLAlchemy)     │(Flask-Caching)│  Worker    │
                              └───────────┘     └─────────────┘   └─────┬──────┘
                                                                        │
                                                              ┌─────────┴─────────┐
                                                              │  SMTP Mail Server │
                                                              │  (reminders/reports)│
                                                              └───────────────────┘
```

---

## Project Structure

```
├── app.py                    # Application factory & entry point
├── extensions.py             # Shared Flask extension instances (db, security, cache)
├── models.py                 # SQLAlchemy models (User, Role, Influencer, Sponsor, Campaign, AdRequest)
├── datastore.py               # Flask-Security user datastore
├── create_initial_data.py    # Seeds default roles and an Admin account
├── resources.py               # Flask-RESTful CRUD resources (/api/*)
├── views.py                   # Application routes (dashboards, auth, search, jobs)
├── tasks.py                    # Celery tasks (CSV export, reminders, monthly reports)
├── worker.py                   # Celery application factory
├── celeryconfig.py             # Celery broker/backend/timezone configuration
├── mail_service.py              # SMTP email helper
├── report.html                 # Jinja2 template for monthly sponsor report emails
├── requirements.txt             # Python dependencies
│
├── src/
│   ├── main.js                 # Vue app entry point
│   ├── App.vue                  # Root component
│   ├── router/index.js          # Route definitions & navigation guards
│   ├── store/index.js            # Vuex store (auth state, login/logout)
│   ├── assets/axios.js           # Preconfigured Axios instance
│   ├── components/Navbar.vue      # Role-aware navigation bar
│   └── views/                     # Page-level components (Admin/Sponsor/Influencer views)
│
├── package.json                 # Frontend dependencies & scripts
└── vue.config.js                 # Vue CLI configuration
```

---

## Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- Redis server (used as both Celery broker and cache backend)

---

## Backend Setup

1. **Clone the repository and navigate to the backend directory.**

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start Redis** (required for caching and Celery):
   ```bash
   redis-server
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

   On first run, the application automatically creates the SQLite database (`iescpdata.sqlite3`), seeds the `Admin`, `Sponsor`, and `Influencer` roles, and creates a default Admin account.

5. **Start the Celery worker** (in a separate terminal, with the virtual environment activated):
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

6. **Start the Celery beat scheduler** (for periodic tasks, in a separate terminal):
   ```bash
   celery -A app.celery_app beat --loglevel=info
   ```

---

## Frontend Setup

1. **Navigate to the frontend directory and install dependencies:**
   ```bash
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm run serve
   ```
   The application will be available at `http://localhost:8080`.

3. **Build for production:**
   ```bash
   npm run build
   ```

> **Note:** The frontend's Axios instance is configured to point to `http://127.0.0.1:5000` and CORS on the backend is restricted to `http://localhost:8080`. Update these values in `assets/axios.js` and `app.py` respectively if your ports differ.

---

## Background Jobs (Celery)

| Task | Trigger | Description |
|---|---|---|
| `create_csv` | On demand (Sponsor clicks "Export Data as CSV") | Generates a CSV of a sponsor's campaigns and makes it available for download |
| `daily_reminder` | Scheduled — daily at 18:00 | Emails influencers with pending ad requests |
| `monthly_report` | Scheduled — 1st of every month at 08:00 | Emails each active sponsor a performance report (campaigns, ad requests, budget, completion stats) |

Broker and result backend run on Redis, configured in `celeryconfig.py` (timezone: `Asia/Kolkata`).

---

## API Overview

All CRUD resources are exposed under the `/api` prefix and require a valid authentication token (`Authentication-Token` header) except where noted.

| Resource | Endpoint | Methods |
|---|---|---|
| User | `/api/user`, `/api/user/<id>` | GET, POST, PUT, DELETE |
| Influencer | `/api/influencer`, `/api/influencer/<id>` | GET, POST, PUT, DELETE |
| Sponsor | `/api/sponsor`, `/api/sponsor/<id>` | GET, POST, PUT, DELETE |
| Campaign | `/api/campaign`, `/api/campaign/<id>` | GET, POST, PUT, DELETE |
| AdRequest | `/api/adrequest`, `/api/adrequest/<id>` | GET, POST, PUT, DELETE |

Additional application routes handle authentication (`/user/login`, `/user/registration`), role-specific dashboards (`/admin/*`, `/sponsor/*`, `/influencer/*`), search (`/search-influencers`, `/search-campaigns`), and background job triggers (`/sponsor/export_campaigns`, `/download_campaigns/<task_id>`).
