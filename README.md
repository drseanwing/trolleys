# REdI Trolley Audit System

> **Resuscitation Education Initiative (REdI)** - Comprehensive trolley audit management system for Royal Brisbane and Women's Hospital (RBWH)

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Django 5.1](https://img.shields.io/badge/django-5.1-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-blue.svg)](https://www.postgresql.org/)
[![License: Internal](https://img.shields.io/badge/license-Internal-red.svg)](LICENSE)

A modern, standalone Django application for managing annual audits of approximately 76 resuscitation trolleys across the RBWH campus. Features a structured 5-step audit workflow, weighted compliance scoring, priority-based issue tracking with SLA enforcement, and comprehensive reporting capabilities.

---

## Overview

### What It Does

REdI streamlines the annual resuscitation trolley audit cycle at RBWH by providing:

1. **Centralized audit data** - Single source of truth replacing fragmented spreadsheets and forms
2. **Structured audit workflow** - 5-step wizard ensures consistency and completeness across all audits
3. **Weighted compliance tracking** - Sophisticated scoring algorithm (Documentation 25%, Equipment 40%, Condition 15%, Checks 20%)
4. **Issue lifecycle management** - 7-state workflow with SLA enforcement and automatic escalation
5. **Analytics and reporting** - Service line compliance reports, trend analysis, CSV/Excel export capabilities

### Why Django?

After initial design as a SharePoint/Power Platform solution, REdI was re-architected as a **standalone Django application** for:

- **Simplicity**: Single codebase vs. distributed SharePoint configuration
- **Control**: Direct database access enabling complex compliance algorithms with Decimal precision
- **Scalability**: Suitable for single-hospital deployment with room to grow
- **Cost**: No SharePoint licensing required
- **Reliability**: Self-hosted or simple cloud deployment (PaaS ready)
- **Maintainability**: Python-only stack with no JavaScript build pipeline required

---

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Runtime** | Python | 3.12+ | Application platform |
| **Web Framework** | Django | 5.1 | MVC framework, ORM, admin interface |
| **Database (dev)** | SQLite | 3 | Zero-config local development |
| **Database (prod)** | PostgreSQL | 16 | Production database with concurrency support |
| **Frontend** | Bootstrap | 5.3 | Responsive UI framework |
| **Interactivity** | HTMX | 2.x | Progressive enhancement without SPA overhead |
| **Static Files** | WhiteNoise | 6.7+ | Efficient static file serving |
| **WSGI Server** | Gunicorn | 23.0+ | Multi-worker production server |
| **Email** | Power Automate API | -- | Email delivery via QH infrastructure |
| **Filtering** | django-filter | 24.0+ | Queryset filtering for list views |
| **Containerization** | Docker Compose | -- | Rootless containers, named volumes |
| **CI/CD** | GitHub Actions | -- | Automated testing, linting, security scanning |

---

## Quick Start

### Prerequisites

- Python 3.12 or higher
- Git
- Virtual environment tool (venv recommended)

### Local Development Setup

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/trolleys.git
cd trolleys/backend
```

**2. Create and activate virtual environment**

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Initialize the database**

```bash
python manage.py migrate
```

**5. Load reference data**

```bash
python manage.py seed_data
```

This loads:
- 7 service lines (Emergency, ICU, Cardiology, etc.)
- 8 equipment categories (Top, Drawers 1-4, External, Medications, Specialty)
- 89 equipment items with SAP codes and specifications
- 76 trolley locations across RBWH campus
- Initial audit period (January 2026)

**6. Create user roles and permissions**

```bash
python manage.py setup_roles
```

This creates 5 Django groups:
- System Admin
- MERT Educator
- Service Line Manager
- Auditor
- Viewer

**7. Create superuser account**

```bash
python manage.py createsuperuser
```

Follow prompts to create your first admin account.

**8. Run development server**

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

---

## Docker Deployment

### Development with Docker

```bash
# Start all services (web + PostgreSQL)
docker compose up -d

# Initialize database and seed data
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_data
docker compose exec web python manage.py setup_roles
docker compose exec web python manage.py createsuperuser

# View logs
docker compose logs -f web

# Stop services
docker compose down
```

### Production Deployment

**Infrastructure constraints:**
- nginx reverse proxy runs at HOST level (not in Docker stack)
- Rootless Docker containers with named volumes
- Port block: 11000-11010 allocated to this application
  - 11000: Web application (exposed to host)
  - 11001: PostgreSQL (internal only)

**Environment variables** (create `.env` file):

```bash
# Django core
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=redi.rbwh.health.qld.gov.au

# Database
DATABASE_URL=postgres://redi:password@db:5432/redi

# Email (Power Automate)
EMAIL_API_ENDPOINT=https://your-power-automate-endpoint
EMAIL_API_TIMEOUT=30
```

**Production deployment:**

```bash
# Use production override
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

**Host nginx configuration** (reference):

```nginx
server {
    listen 443 ssl;
    server_name redi.rbwh.health.qld.gov.au;

    ssl_certificate     /etc/ssl/certs/redi.crt;
    ssl_certificate_key /etc/ssl/private/redi.key;

    location / {
        proxy_pass http://127.0.0.1:11000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Project Structure

```
trolleys/
├── README.md                           # This file
├── backend/                            # Django application root
│   ├── manage.py                       # Django management CLI
│   ├── requirements.txt                # Python dependencies
│   │
│   ├── redi/                           # Django project settings
│   │   ├── settings.py                 # Configuration, installed apps, middleware
│   │   ├── urls.py                     # Root URL routing
│   │   ├── wsgi.py                     # WSGI entry point (production)
│   │   └── asgi.py                     # ASGI entry point (async)
│   │
│   ├── audit/                          # Main Django application
│   │   ├── models.py                   # 17 database models
│   │   ├── views.py                    # 22+ view classes
│   │   ├── forms.py                    # 8 form classes
│   │   ├── admin.py                    # Django admin configuration
│   │   ├── urls.py                     # 23 URL patterns
│   │   ├── mixins.py                   # Role-based access control mixins
│   │   ├── context_processors.py       # Global template context
│   │   │
│   │   ├── services/                   # Business logic services
│   │   │   ├── compliance.py           # ComplianceScorer - weighted scoring
│   │   │   ├── issue_workflow.py       # IssueWorkflow - 7-state machine
│   │   │   ├── random_selection.py     # RandomAuditSelector - priority weighting
│   │   │   ├── notifications.py        # NotificationService
│   │   │   └── email_backend.py        # PowerAutomateEmailService
│   │   │
│   │   ├── management/commands/        # Custom management commands
│   │   │   ├── seed_data.py            # Load reference data
│   │   │   ├── setup_roles.py          # Create authentication groups
│   │   │   ├── check_sla.py            # Check SLAs and auto-escalate
│   │   │   └── generate_weekly_selection.py  # Weekly audit selection
│   │   │
│   │   ├── templates/audit/            # Django templates (Bootstrap 5)
│   │   ├── static/audit/               # CSS, JS, images
│   │   └── templatetags/               # Custom template filters
│   │
│   └── db.sqlite3                      # Development database (auto-created)
│
├── seed_data/                          # Reference data files (JSON)
│   ├── ServiceLine.json                # 7 service lines
│   ├── EquipmentCategory.json          # 8 categories
│   ├── Equipment.json                  # 89 equipment items
│   ├── Location.json                   # 76 trolley locations
│   └── AuditPeriod.json                # Initial audit period
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                 # System architecture details
│   └── TASKS.md                        # Implementation task list (121 tasks)
│
├── docker/                             # Docker configuration
│   ├── Dockerfile                      # Production image
│   └── entrypoint.sh                   # Container startup script
│
├── docker-compose.yml                  # Development Docker setup
├── docker-compose.prod.yml             # Production overrides
│
└── .github/                            # CI/CD configuration
    └── workflows/                      # GitHub Actions
        ├── ci.yml                      # Tests and linting
        ├── release.yml                 # Release automation
        └── security.yml                # Security scanning
```

---

## Data Model

REdI uses 17 database models organized into 4 tiers:

### Reference Data Tier (3 models)

| Model | Description |
|-------|-------------|
| **ServiceLine** | 7 hospital service lines/directorates that own trolley locations |
| **EquipmentCategory** | 8 categories grouping equipment (Top, Drawers 1-4, External, Medications, Specialty) |
| **AuditPeriod** | Configurable audit periods (Monthly/Quarterly/Annual) |

### Master Data Tier (2 models)

| Model | Description |
|-------|-------------|
| **Equipment** | 89 individual equipment items with SAP codes, sourcing, and requirements |
| **Location** | 76 physical trolley locations across RBWH campus with building, level, type, defibrillator |

### Transactional Tier (11 models)

| Domain | Models | Description |
|--------|--------|-------------|
| **Location Config** | LocationEquipment | Per-location equipment customizations and overrides |
| **Audit Workflow** | Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment | Complete audit records with 5-step wizard data |
| **Issue Management** | Issue, CorrectiveAction, IssueComment | 7-state issue lifecycle with SLA tracking |
| **Random Selection** | RandomAuditSelection, RandomAuditSelectionItem | Weekly priority-weighted trolley selection |

### Audit Trail Tier (1 model)

| Model | Description |
|-------|-------------|
| **LocationChangeLog** | Field-level change audit trail for location records (governance/compliance) |

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed entity relationships and field specifications.

---

## Key Features

### 1. Five-Step Audit Wizard

Structured workflow ensures complete, consistent audits:

**Step 1: Documentation (25% weight)**
- Resuscitation record status
- Guidelines document status
- BLS poster presence
- Equipment list status

**Step 2: Equipment Checklist (40% weight)**
- 89 items grouped by 8 categories
- Quantity verification (found vs. expected)
- Expiry date checking for medications/consumables
- Critical item highlighting

**Step 3: Physical Condition (15% weight)**
- Cleanliness assessment
- Working order verification
- Specific checks: rubber bands, O2 tubing, INHALO cylinder
- Issue creation and linking

**Step 4: Routine Checks (20% weight)**
- Daily outside checks (24/7 trolleys)
- Daily inside checks
- Count validation vs. expected minimums

**Step 5: Review & Submit**
- Summary of all findings
- Overall compliance score preview
- Follow-up audit flagging
- Final submission with auditor confirmation

### 2. Weighted Compliance Scoring

Sophisticated algorithm implemented in `ComplianceScorer` service:

```
Overall Compliance = (Documentation × 0.25) + (Equipment × 0.40) +
                     (Condition × 0.15) + (Routine Checks × 0.20)
```

**Equipment sub-weighting:**
- Critical items: 60% of equipment score
- Non-critical items: 40% of equipment score

All calculations use Decimal arithmetic with ROUND_HALF_UP to 2 decimal places.

**Compliance thresholds:**
- Below 80% triggers automatic follow-up audit requirement (14-day deadline)
- Critical items flagged separately for immediate attention

### 3. Seven-State Issue Workflow

Comprehensive issue lifecycle with SLA enforcement:

```
Open → Assigned → InProgress → PendingVerification → Resolved → Closed
         ↓
      Escalated (from any state)
```

**SLA targets by severity:**
- Critical: 24 hours
- High: 3 days
- Medium: 7 days
- Low: 14 days

**Features:**
- Auto-generated issue numbers (`ISS-YYYYMM-NNN`)
- Corrective actions tracking (1 to many per issue)
- Internal and external comments
- Automatic escalation on SLA breach
- Re-open management with tracking

### 4. Priority-Weighted Random Selection

Smart algorithm selects ~10 trolleys per week based on:

**Priority scoring:**
- Never audited: 1000 base score
- Days since last audit (primary factor)
- Compliance score trend (secondary factor)
- Service line distribution (tertiary factor)

**Selection process:**
1. Score all active locations
2. Pick highest-priority from each service line (up to 7)
3. Fill remaining slots from top scorers
4. Create weekly batch with tracking

### 5. Role-Based Access Control

Five user roles implemented as Django groups with custom mixins:

| Role | Dashboard | Trolleys | Audits | Issues | Reports | Admin |
|------|-----------|----------|--------|--------|---------|-------|
| **System Admin** | Full | Full CRUD | Full CRUD | Full CRUD | Full | Full |
| **MERT Educator** | View | Full CRUD | Full CRUD | Full CRUD | Full | Config |
| **Service Line Manager** | View | View own | Manage own | Manage own | View own | - |
| **Auditor** | View | View | Create/Submit | Report | View | - |
| **Viewer** | View | View | View | View | View | - |

---

## User Roles

### System Admin

**Full system access** - configuration, user management, system health

- View and manage all trolleys, audits, issues
- Configure service lines, equipment, audit periods
- Manage user roles and permissions
- Access Django admin panel
- Run management commands

**Example users:** Hospital IT, Clinical Engineering Manager

### MERT Educator

**Configuration and audit management** - program oversight

- Full access to trolley master data
- Full access to audits and issues
- Generate random audit selections
- Configure equipment and categories
- View all reports
- No Django admin access

**Example users:** Head of Resuscitation Education, Clinical Governance Officer

### Service Line Manager

**Service line oversight** - departmental monitoring

- View trolleys in their service line
- Manage audits for their service line
- Manage issues in their service line
- View reports for their service line only

**Example users:** Nursing Manager, Department Head

### Auditor

**Front-line audit entry** - operational staff

- View all trolleys (read-only)
- Create and submit audits
- Create and comment on issues
- View their own audit history

**Example users:** Nurse Educator, Resuscitation Officer, Nursing Staff

### Viewer

**Information access only** - dashboard consumers

- Read-only access to all views
- Cannot create or edit anything

**Example users:** Executive Leadership, Quality Team

---

## Management Commands

| Command | Purpose | Schedule |
|---------|---------|----------|
| `seed_data` | Load reference data from JSON files (7 service lines, 8 categories, 89 items, 76 locations) | Initial setup |
| `setup_roles` | Create 5 Django groups with permissions | Initial setup |
| `check_sla` | Check issue SLA compliance and auto-escalate breached issues | Daily (8:00 AM) |
| `generate_weekly_selection` | Generate priority-weighted random audit selection (~10 trolleys) | Weekly (Monday 7:00 AM) |
| `createsuperuser` | Create Django superuser account | Initial setup |
| `collectstatic` | Gather static files for WhiteNoise (production) | Before deployment |

**Example usage:**

```bash
# Local development
python manage.py seed_data
python manage.py check_sla

# Docker production
docker compose exec web python manage.py generate_weekly_selection
```

**Scheduling options:**
- Host crontab (simplest for initial deployment)
- docker-cron service with supercronic
- APScheduler (in-process)
- django-celery-beat + Redis (production-grade)

---

## Architecture

REdI follows a layered architecture pattern:

```
┌─────────────────────────────────────────┐
│         URL Routing Layer               │
│   redi/urls.py → audit/urls.py          │
├─────────────────────────────────────────┤
│         View Layer (22 views)           │
│   Class-based views with role mixins    │
├─────────────────────────────────────────┤
│         Form Layer (8 forms)            │
│   ModelForms with Bootstrap widgets     │
├─────────────────────────────────────────┤
│         Service Layer                   │
│   ComplianceScorer | IssueWorkflow      │
│   RandomAuditSelector | Notifications   │
├─────────────────────────────────────────┤
│         Model Layer (17 models)         │
│   Django ORM with UUID primary keys     │
├─────────────────────────────────────────┤
│         Database                        │
│   SQLite (dev) / PostgreSQL 16 (prod)   │
└─────────────────────────────────────────┘
```

**Key design decisions:**
- **Server-rendered templates + HTMX** over SPA for simplicity and accessibility
- **Service layer** separates complex business logic from views
- **UUID primary keys** prevent enumeration attacks
- **Decimal fields** for compliance scores avoid floating-point rounding
- **Role-based mixins** enforce consistent access control

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for comprehensive architecture documentation.

---

## Task List

REdI implementation is tracked across **121 tasks** organized into **10 phases**:

1. **Phase 1: Infrastructure & Docker** (P0) - 13 tasks
2. **Phase 2: Core Views & Template Polish** (P0) - 14 tasks
3. **Phase 3: Audit Workflow Hardening** (P0) - 8 tasks
4. **Phase 4: Issue Management** (P1) - 9 tasks
5. **Phase 5: Random Selection & Scheduling** (P1) - 8 tasks
6. **Phase 6: Reporting & Analytics** (P1) - 11 tasks
7. **Phase 7: Email & Notifications** (P1) - 4 tasks
8. **Phase 8: Testing** (P2) - 29 tasks
9. **Phase 9: Security Hardening** (P2) - 6 tasks
10. **Phase 10: Deployment & Documentation** (P2) - 8 tasks

**Priority breakdown:**
- P0 (blockers): 26 tasks - Week 1-2
- P1 (important): 55 tasks - Week 2-4
- P2 (nice to have): 39 tasks - Week 4-6
- P3 (future): 1 task - Backlog

See [docs/TASKS.md](docs/TASKS.md) for the complete task list with dependencies.

---

## Contributing

### Branch Naming

- `feature/<name>` - New features
- `fix/<name>` - Bug fixes
- `docs/<name>` - Documentation updates

### Pull Request Process

1. Create feature branch from `main`
2. Make changes with clear commit messages
3. Ensure CI passes (tests, linting, security checks)
4. Submit PR with description and testing notes
5. Address review feedback
6. Merge requires 1 approval

### CI Requirements

All PRs must pass:
- **Linting**: Ruff code quality checks
- **System checks**: `python manage.py check --deploy`
- **Migration integrity**: `makemigrations --check --dry-run`
- **Security**: pip-audit dependency scan, TruffleHog secret detection

### Code Style

- Follow Django conventions and PEP 8
- Use class-based views with role mixins
- Keep business logic in service classes
- Write docstrings for complex functions
- Use meaningful variable names

---

## License

**Internal use** - Royal Brisbane and Women's Hospital

This application is for internal RBWH use only. Not licensed for external distribution.

---

## Support

For internal RBWH support:
- **System Admin**: [Contact IT Department]
- **Clinical Governance**: [Contact MERT Team]
- **Issues**: Report via GitHub Issues (internal repo)

---

**Version:** 2.0
**Last Updated:** February 2026
**Architecture:** Django 5.1 + PostgreSQL 16 (migrated from SharePoint)
