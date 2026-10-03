# JobNest — Django Job Search & Hiring Platform

A database-driven job portal inspired by the core candidate and recruiter workflows of major job boards. Built with Django, SQLite, HTML, CSS and JavaScript.

## What is included

### Candidate side
- Candidate registration/login
- Candidate profile and resume upload
- Search and filter by keyword, location, category, job type, work mode and experience
- 20+ ready-made sample jobs across multiple companies
- Job detail pages
- Save/unsave jobs with JavaScript AJAX
- Apply with cover letter and resume
- Application tracking dashboard

### Company side
- Company registration/login
- Company profile
- Post a job with category, salary, openings, deadline and featured status
- Edit/pause/delete own jobs
- Company dashboard
- View and filter applications
- Update candidate application status

### Marketplace features
- Company directory with live hiring stats
- Job alert subscriptions for keyword and location preferences
- Sorting and filtering for job search results

### Admin side
- Django admin at `/admin/`
- Manage users, profiles, jobs, applications and saved jobs

## Database

SQLite is configured as `db.sqlite3`.

The migration `portal/migrations/0003_seed_jobs.py` automatically creates demo companies and many job listings when you run:

```bash
python manage.py migrate
```

Therefore a fresh setup is **not empty**.

## Windows setup

### Option 1 — automatic
Double-click `setup_windows.bat`.

### Option 2 — VS Code terminal

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

If PowerShell blocks script activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open `http://127.0.0.1:8000/`.

## Demo accounts

After `migrate`, sample company accounts and a candidate account are created.

Password for demo accounts: `Demo@12345`

Company usernames include:
- `brightbyte`
- `cloudnest`
- `finpulse`
- `designorbit`

Candidate username: `democandidate`

## Create admin

```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`.

## Project structure

```text
job_portal/
├── manage.py
├── requirements.txt
├── setup_windows.bat
├── config/
├── portal/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── management/commands/seed_demo.py
├── templates/
└── static/
```
