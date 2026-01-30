# REdI Trolley Audit System

> **Resuscitation Education Initiative (REdI)** - Comprehensive trolley audit management system for Royal Brisbane and Women's Hospital (RBWH)

A modern, standalone Django application for managing annual audits of approximately 76 resuscitation trolleys across the RBWH campus. Replaces legacy Microsoft Forms-based processes with a structured, role-based audit workflow featuring compliance scoring, issue tracking, and comprehensive reporting.

## Quick Links

- **Getting Started**: See [Installation](#installation)
- **Architecture**: See [Project Structure](#project-structure)
- **Data Model**: See [Database Schema](#database-schema-17-entities)
- **User Guide**: See [User Roles](#user-roles--access-control)
- **Deployment**: See [Scheduled Tasks](#scheduled-tasks)

---

## Project Overview

### Purpose

REdI streamlines the annual resuscitation trolley audit cycle at RBWH by:

1. **Centralizing audit data** - Single source of truth replacing fragmented spreadsheets and forms
2. **Enforcing audit workflow** - 5-step wizard ensures consistency and completeness
3. **Tracking compliance** - Weighted scoring algorithm (Documentation 25%, Equipment 40%, Condition 15%, Checks 20%)
4. **Managing issues** - 7-state lifecycle with SLA enforcement and auto-escalation
5. **Enabling analytics** - Service line compliance reports, trend analysis, export capabilities

### Why Django?

After initial design as a SharePoint/Power Platform solution, REdI was re-architected as a **standalone Django application** because:

- **Simplicity**: Single codebase vs. distributed SharePoint configuration
- **Control**: Direct database access for complex compliance algorithms
- **Scalability**: Suitable for single-hospital deployment with room to grow
- **Cost**: No SharePoint licensing required
- **Reliability**: Self-hosted or simple cloud deployment (PaaS ready)

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Runtime** | Python | 3.11+ |
| **Web Framework** | Django | 5.1 |
| **Database** | SQLite | 3 |
| **Frontend** | Bootstrap 5.3 | |
| **Interactivity** | HTMX | - |
| **Static Files** | WhiteNoise | 6.7+ |
| **Production WSGI** | Gunicorn | 23.0+ |
| **Task Scheduling** | Cron / APScheduler | - |
| **Email Delivery** | Power Automate API | - |
| **Branding** | REdI CSS Stylesheet | - |

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Step-by-Step Setup

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
- 7 service lines
- 8 equipment categories
- 89 equipment items
- 76 trolley locations
- Initial audit period (January 2026)

**6. Create authentication groups and roles**

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

## Project Structure

```
trolleys/
├── README.md                           # This file
├── backend/                            # Django application root
│   ├── manage.py                       # Django management CLI
│   ├── requirements.txt                # Python dependencies
│   ├── db.sqlite3                      # Database (auto-created)
│   │
│   ├── redi/                           # Django project settings
│   │   ├── __init__.py
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
│   │   ├── apps.py
│   │   │
│   │   ├── mixins.py                   # Role-based access control (LoginRequiredMixin, EducatorRequiredMixin, etc.)
│   │   ├── context_processors.py       # Global template context
│   │   │
│   │   ├── services/                   # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── compliance.py           # ComplianceScorer - weighted scoring algorithm
│   │   │   ├── issue_workflow.py       # IssueWorkflow - 7-state machine + SLA logic
│   │   │   ├── random_selection.py     # RandomAuditSelector - priority-weighted selection
│   │   │   └── notifications.py        # Email notifications (optional)
│   │   │
│   │   ├── management/commands/        # Custom management commands
│   │   │   ├── seed_data.py            # Load reference data (locations, equipment, etc.)
│   │   │   ├── setup_roles.py          # Create authentication groups
│   │   │   ├── check_sla.py            # Check issue SLAs and auto-escalate
│   │   │   └── generate_weekly_selection.py  # Run weekly audit selection
│   │   │
│   │   ├── migrations/                 # Database migrations (auto-generated)
│   │   │   └── 0001_initial.py         # Initial schema
│   │   │
│   │   ├── templatetags/               # Custom template tags
│   │   │   └── audit_tags.py           # Template filters and tags
│   │   │
│   │   ├── templates/audit/            # Django templates (Bootstrap 5)
│   │   │   ├── base.html               # Main layout
│   │   │   ├── dashboard.html
│   │   │   ├── trolley_list.html
│   │   │   ├── trolley_detail.html
│   │   │   ├── audit_wizard.html       # Multi-step audit wizard
│   │   │   ├── issue_list.html
│   │   │   ├── issue_detail.html
│   │   │   ├── random_selection_view.html
│   │   │   ├── reports.html
│   │   │   └── ...                     # 19 total templates
│   │   │
│   │   ├── static/audit/               # Static assets (CSS, JS, images)
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   │
│   │   └── tests/                      # Unit and integration tests (optional)
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_services.py
│   │
│   └── venv/                           # Virtual environment (not in git)
│
├── seed_data/                          # Reference data files (JSON)
│   ├── ServiceLine.json                # 7 service lines
│   ├── EquipmentCategory.json          # 8 categories
│   ├── Equipment.json                  # 89 items
│   ├── Location.json                   # 76 trolley locations
│   └── AuditPeriod.json                # Initial audit period
│
├── sharepoint_schemas/                 # Legacy SharePoint schemas (deprecated)
│   └── *.json
│
├── implementation_guides/              # Legacy implementation guides (deprecated)
│   └── *.md
│
└── .github/                            # CI/CD configuration
    └── workflows/                      # GitHub Actions
```

---

## Database Schema (17 Entities)

### Reference Data (3 models)

**ServiceLine**
- 7 hospital service lines/directorates that own trolley locations
- Fields: id, name, abbreviation, contact_email, is_active, timestamps

**EquipmentCategory**
- 8 categories grouping equipment (Top, Drawers 1-4, External Accessories, Medications, Specialty)
- Fields: id, category_name, sort_order, description, is_active, timestamps

**AuditPeriod**
- Configurable audit periods (Monthly/Quarterly/Annual)
- Fields: id, period_name, period_type, year, start_date, end_date, audit_deadline, is_active, timestamps

### Master Data (2 models)

**Equipment**
- 89 individual equipment items with sourcing and requirements
- Fields: id, category_fk, item_name, short_name, s4hana_code, supplier, standard_quantity, flags (standard_item, paediatric, altered_airway), defib_type, requires_expiry, critical_item, sort_order, is_active, timestamps

**Location**
- 76 physical trolley locations across RBWH campus
- Fields: id, service_line_fk, department_name, display_name, building, level, trolley_type, defibrillator_type, operating_hours, flags (has_paediatric_box, has_altered_airway, has_specialty_meds), last_audit_date, last_audit_compliance, status (Active/Inactive/Decommissioned), status_change_date, status_change_reason, timestamps
- Methods: `days_since_last_audit`, `audit_priority_score`

### Location Overrides (1 model)

**LocationEquipment**
- Per-location equipment customizations (custom quantities, exclusions)
- Fields: id, location_fk, equipment_fk, is_required, custom_quantity, notes, timestamps
- Unique Constraint: (location, equipment)

### Audit Workflow (6 models)

**Audit**
- A single audit performed on a trolley
- Fields: id, location_fk, period_fk, audit_type (Monthly/Random/FollowUp/Spot), triggered_by_issue_fk, auditor_name, auditor_user_fk, started_at, completed_at, submission_status (Draft/InProgress/Submitted/Reviewed), scores (overall, document, equipment, condition, check), requires_follow_up, follow_up_due_date, notes, timestamps

**AuditDocuments**
- Documentation checks performed during an audit (one-to-one with Audit)
- Fields: id, audit_fk, check_record_status, check_guidelines_status, bls_poster_present, equipment_list_status, timestamps

**AuditCondition**
- Physical condition assessment of trolley (one-to-one with Audit)
- Fields: id, audit_fk, is_clean, is_working_order, issue_type, issue_description, rubber_bands_used, o2_tubing_correct, inhalo_cylinder_ok, timestamps

**AuditChecks**
- Daily/weekly check count compliance (one-to-one with Audit)
- Fields: id, audit_fk, outside_check_count, inside_check_count, expected_outside, expected_inside, count_not_available, outside_compliance, inside_compliance, timestamps

**AuditEquipment**
- Result of checking a single equipment item (foreign key to Audit)
- Fields: id, audit_fk, equipment_fk, is_present, quantity_found, quantity_expected, expiry_ok, item_notes, timestamps
- Unique Constraint: (audit, equipment)

### Issue Tracking (3 models)

**Issue**
- A problem found during an audit or reported independently
- Fields: id, location_fk, audit_fk, issue_number (auto-generated ISS-YYYYMM-NNN), issue_category (Equipment/Documentation/Condition/Compliance/Process/Other), severity (Critical/High/Medium/Low), title, description, equipment_fk, reported_by, reported_date, assigned_to, assigned_date, target_resolution_date, status (Open/Assigned/InProgress/PendingVerification/Resolved/Closed/Escalated), resolution_summary, resolved_date, verified_by, closed_date, reopen_count, escalation_level, linked_follow_up_audit_fk, timestamps
- Auto-generates issue numbers on save

**CorrectiveAction**
- An action taken to resolve an issue
- Fields: id, issue_fk, action_number, action_type (Replacement/Repair/Restock/ProcessChange/Training/Other), description, action_taken_by, action_date, outcome_description, outcome_successful, evidence_attached, evidence_url, timestamps

**IssueComment**
- Comments or notes attached to an issue
- Fields: id, issue_fk, comment_text, comment_by, comment_date, is_internal, timestamps

### Random Selection (2 models)

**RandomAuditSelection**
- A weekly random audit selection batch
- Fields: id, week_start_date, week_end_date, generated_date, generated_by, selection_criteria, is_active, timestamps

**RandomAuditSelectionItem**
- Individual location selected for random audit (typically 10 per week)
- Fields: id, selection_fk, location_fk, selection_rank, priority_score, days_since_audit, audit_status (Pending/Completed/Skipped), audit_fk, skip_reason, timestamps
- Unique Constraint: (selection, location)

### Audit Trail (1 model)

**LocationChangeLog**
- Audit trail for location record changes (governance/compliance)
- Fields: id, location_fk, change_type (Created/Updated/StatusChange/Decommissioned), field_changed, old_value, new_value, change_reason, changed_by, changed_date, timestamps

---

## Key Features

### 1. Trolley Management

- **Master register** of 76 trolley locations with department, building, level, operating hours
- **Location types**: Standard, Paediatric, Specialty
- **Defibrillator tracking**: LIFEPAK 1000 AED, LIFEPAK 20/20e
- **Status tracking**: Active, Inactive, Decommissioned with change audit trail
- **Quick statistics**: Days since last audit, last compliance score, open issues

### 2. Audit Workflow

**5-step guided wizard** ensures complete, consistent audits:

1. **Documentation (25% weight)**
   - Resuscitation record status
   - Guidelines document status
   - BLS poster present
   - Equipment list status
   - Auto-calculates compliance percentage

2. **Equipment Checklist (40% weight)**
   - 89 items grouped by 8 categories
   - Track quantity found vs. expected
   - Expiry date verification for medications/consumables
   - Critical item highlighting
   - Equipment-specific notes

3. **Physical Condition (15% weight)**
   - Cleanliness assessment
   - Working order verification
   - Issue type and description
   - Specific checks: rubber bands, O2 tubing, INHALO cylinder
   - Links to issue creation

4. **Routine Checks (20% weight)**
   - Daily outside checks (24/7 trolleys)
   - Daily inside checks
   - Count validation vs. expected minimums
   - Compliance percentage calculation

5. **Review & Submit**
   - Summary of all findings
   - Overall compliance score (weighted average)
   - Option to flag for follow-up audit
   - Issue creation and linking
   - Final submission with timestamp and auditor confirmation

### 3. Compliance Scoring

**Weighted algorithm** (ComplianceScorer service):

```
Overall Compliance = (Doc_Score * 0.25) + (Equip_Score * 0.40) +
                     (Condition_Score * 0.15) + (Check_Score * 0.20)
```

Each sub-score calculated as:
```
Sub_Score = (Items_Passing / Items_Checked) * 100
```

Special handling for:
- N/A items (excluded from denominator)
- Critical items (flagged if non-compliant)
- Paediatric/specialty items (conditional based on trolley type)

### 4. Issue Management

**7-state lifecycle** with SLA enforcement:

```
Open → Assigned → InProgress → PendingVerification → Resolved → Closed
         ↓
      Escalated (from any state)
```

**Features:**
- Auto-generated issue numbers (ISS-202601-001)
- Severity levels: Critical, High, Medium, Low
- SLA timelines (per severity)
- Corrective actions tracking (1..N actions per issue)
- Comments/notes (internal and external)
- Escalation tracking
- Re-open management
- Linked follow-up audits

**SLA Auto-Escalation:**
- Critical: 24 hours
- High: 3 days
- Medium: 7 days
- Low: 14 days

### 5. Random Audit Selection

**Priority-weighted algorithm** (RandomAuditSelector service):

Selects ~10 trolleys per week based on:
- Days since last audit (primary)
- Compliance score trend (secondary)
- Service line distribution (tertiary)
- Status (Active only)

**Features:**
- Weekly batches (Monday morning cron)
- Detailed selection criteria logged
- Per-item audit status tracking (Pending/Completed/Skipped)
- Skip reason documentation
- Linked to actual audits when completed

### 6. Role-Based Access Control

| Role | Dashboard | Trolleys | Audits | Issues | Reports | Admin |
|------|-----------|----------|--------|--------|---------|-------|
| **System Admin** | Full | Full CRUD | Full CRUD | Full CRUD | Full | Full |
| **MERT Educator** | View | Full CRUD | Full CRUD | Full CRUD | Full | Config |
| **Service Line Manager** | View | View own | Manage own SL | Manage own SL | View own | - |
| **Auditor** | View | View | Create/Submit | Report | View | - |
| **Viewer** | View | View | View | View | View | - |

**Implementation:** Django groups + custom mixins (LoginRequiredMixin, AuditorRequiredMixin, EducatorRequiredMixin, ManagerRequiredMixin, ViewerRequiredMixin)

### 7. Reporting & Analytics

**Built-in Reports:**
- **Compliance Dashboard**: Service line trends, trolley compliance, open issues
- **Audit History**: All audits with details, filters by location/period/auditor
- **Issue Report**: Open issues by status/severity/service line
- **Equipment Audit**: Which items failed across all locations
- **Service Line Analytics**: Compliance scores, audit completion rates, top issues

**Export Capabilities:**
- Audit data to CSV
- Issue reports to CSV
- Compliance summary to Excel-compatible format

---

## User Roles & Access Control

### System Admin

**Full system access** - creates configuration, manages users, monitors health

- View and manage all trolleys, audits, issues
- Configure service lines, equipment, audit periods
- Manage user roles and permissions
- View all reports
- Access Django admin panel
- Run management commands

**Example Users:** Hospital IT, Clinical Engineering Manager

### MERT Educator

**Configuration and audit management** - sets up trolleys and oversees audit program

- Full access to trolley master data
- Full access to audits and issues
- Generate random audit selections
- Configure equipment and categories
- View all reports
- Cannot access Django admin

**Example Users:** Head of Resuscitation Education, Clinical Governance Officer

### Service Line Manager

**Service line oversight** - monitors audits and issues for their area

- View trolleys in their service line
- View and manage audits for their service line
- View and manage issues in their service line
- View reports for their service line only
- Cannot create audit periods or equipment

**Example Users:** Nursing Manager, Department Head

### Auditor

**Front-line audit entry** - performs audits and reports issues

- View all trolleys (read-only)
- Create and submit audits
- Create and comment on issues
- View their own audits
- View dashboard (read-only)
- Cannot manage or configure anything

**Example Users:** Nurse Educator, Resuscitation Officer, Nursing Staff

### Viewer

**Information access only** - consumes dashboards and reports

- View trolleys (read-only)
- View audit history (read-only)
- View issues (read-only)
- View reports (read-only)
- Cannot create or edit anything

**Example Users:** Executive Leadership, Quality Team (observers)

---

## Scheduled Tasks

Run these regularly via cron jobs or APScheduler:

### Daily: Check SLA Compliance

```bash
python manage.py check_sla
```

**What it does:**
- Iterates all Open/Assigned/InProgress/PendingVerification issues
- Checks target_resolution_date vs. current date
- Auto-escalates overdue issues
- Logs escalation details
- Sends escalation notifications (if configured)

**Recommended:** Daily at 8:00 AM

### Weekly: Generate Random Audit Selection

```bash
python manage.py generate_weekly_selection
```

**What it does:**
- Selects ~10 trolleys using priority-weighted algorithm
- Creates RandomAuditSelection batch with items
- Logs selection criteria and scores
- Deactivates previous week's selection
- Sends notifications to auditors

**Recommended:** Monday at 7:00 AM

### Optional: Email Notifications

If notifications service is configured via Power Automate API:
- Issue escalation emails
- Audit completion reminders
- Weekly selection notification

Email notifications require the `EMAIL_API_ENDPOINT` environment variable to be set. Configure your Power Automate Flow to handle the notification payloads sent by Django.

---

## Development

### Running Tests

```bash
python manage.py test audit
```

### Creating Migrations

After modifying `models.py`:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin Interface

Access at `/admin/` (superuser only)

Admin features:
- Browse all 17 models
- Create/edit reference data
- View audit trail
- Manage users and groups

### Management Commands

```bash
# Load reference data
python manage.py seed_data

# Create authentication groups
python manage.py setup_roles

# Check SLA compliance
python manage.py check_sla

# Generate weekly random selection
python manage.py generate_weekly_selection

# Django built-in commands
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic  # For production
```

---

## Production Deployment

### Environment Variables

Create `.env` file in `backend/` directory:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL in production

# Email - Power Automate API
EMAIL_API_ENDPOINT=https://your-power-automate-endpoint-url
EMAIL_API_TIMEOUT=30
```

**Email Configuration:**

The system uses Microsoft Power Automate's HTTP endpoint for email delivery instead of traditional SMTP. This provides:
- Better integration with Queensland Health's email infrastructure
- No need for SMTP credentials or email server configuration
- Centralized email template management in Power Automate
- Robust retry and delivery tracking

Configure `EMAIL_API_ENDPOINT` to point to your Power Automate Flow's HTTP trigger URL. The timeout value (in seconds) controls how long Django will wait for the API response.

### WSGI Server

**Gunicorn** is configured as the production WSGI server:

```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 redi.wsgi:application
```

### Static Files

**WhiteNoise** handles static file serving efficiently:

```bash
python manage.py collectstatic --noinput
```

### Database

For production, consider upgrading from SQLite to PostgreSQL:

1. Install PostgreSQL
2. Create database and user
3. Install psycopg2: `pip install psycopg2-binary`
4. Update `DATABASE_URL` in `.env`
5. Run migrations: `python manage.py migrate`
6. Load seed data: `python manage.py seed_data`

### Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS (SSL certificate)
- [ ] Configure CORS if needed
- [ ] Set strong database password
- [ ] Enable CSRF protection
- [ ] Use environment variables for secrets
- [ ] Set up log aggregation
- [ ] Configure backups

---

## Seed Data

The `seed_data/` directory contains JSON files for initial data loading:

| File | Records | Description |
|------|---------|-------------|
| ServiceLine.json | 7 | RBWH service lines/directorates |
| EquipmentCategory.json | 8 | Trolley sections and groupings |
| Equipment.json | 89 | All equipment items with sourcing |
| Location.json | 76 | All trolley locations across campus |
| AuditPeriod.json | 1 | Initial audit period (Jan 2026) |

**Load command:**

```bash
python manage.py seed_data
```

**To reset data:**

```bash
rm backend/db.sqlite3
python manage.py migrate
python manage.py seed_data
python manage.py setup_roles
```

---

## Troubleshooting

### Database locked error

If you see "database is locked" in production:

```bash
# This shouldn't happen with Gunicorn, but if using development server:
rm backend/db.sqlite3-*
python manage.py migrate
```

### Missing migrations

If you see "table doesn't exist" errors:

```bash
python manage.py migrate --fake-initial
# or
python manage.py migrate audit zero  # Reverse all migrations
python manage.py migrate audit       # Apply from scratch
```

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

### Permission denied errors

Ensure your user has write access to:
- `backend/db.sqlite3`
- `backend/staticfiles/` (if using collectstatic)

---

## Architecture Decisions

### Why SQLite for initial deployment?

- **Simplicity**: No additional database server to manage
- **Sufficient for scale**: 76 locations = minimal data volume
- **Migration path**: Can upgrade to PostgreSQL if needed
- **Offline capability**: Database file can be backed up/restored easily

### Why Django templates instead of React/Vue?

- **Simpler stack**: Python developers only, no JavaScript framework expertise needed
- **Server-side rendering**: Better for intranet/hospital network access
- **HTMX for interactivity**: Progressive enhancement without heavy SPA overhead
- **Accessibility**: Template-based approach naturally supports WCAG compliance

### Why BaseView mixins for access control?

- **Consistent enforcement**: Every protected view uses same access check
- **Maintainable**: Role requirements defined in view class, not scattered
- **Testable**: Easy to mock and test permission logic

### Why service classes for business logic?

- **Separation of concerns**: Complex algorithms (scoring, workflow) separate from views
- **Testable**: ComplianceScorer, IssueWorkflow testable independently
- **Reusable**: Services can be called from views, management commands, or other services

---

## API Reference

### Management Commands

#### `seed_data`

Loads reference data from JSON files.

```bash
python manage.py seed_data
```

**Loads:**
- 7 ServiceLines
- 8 EquipmentCategories
- 89 Equipment items
- 76 Locations
- 1 AuditPeriod

#### `setup_roles`

Creates Django groups for role-based access control.

```bash
python manage.py setup_roles
```

**Creates groups:**
- System Admin (superuser only)
- MERT Educator
- Service Line Manager
- Auditor
- Viewer

#### `check_sla`

Checks issue SLA compliance and auto-escalates overdue issues.

```bash
python manage.py check_sla
```

**Escalates:**
- Critical: 24 hours overdue
- High: 3 days overdue
- Medium: 7 days overdue
- Low: 14 days overdue

#### `generate_weekly_selection`

Generates weekly random audit selection batch.

```bash
python manage.py generate_weekly_selection
```

**Selects:** ~10 trolleys using priority-weighted algorithm
**Criteria:** Days since audit, compliance trend, service line balance

### View Classes

| View | URL | Method | Description |
|------|-----|--------|-------------|
| DashboardView | `/dashboard/` | GET | Main dashboard |
| TrolleyListView | `/trolleys/` | GET | List all trolleys |
| TrolleyDetailView | `/trolleys/<id>/` | GET | Trolley details + audit history |
| AuditCreateView | `/audits/create/` | GET, POST | Start new audit |
| AuditWizardView | `/audits/<id>/wizard/` | GET, POST | Multi-step audit wizard |
| IssueListView | `/issues/` | GET | List issues with filters |
| IssueDetailView | `/issues/<id>/` | GET | Issue detail + timeline |
| IssueCreateView | `/issues/create/` | GET, POST | Create new issue |
| RandomSelectionView | `/random-selection/` | GET | View current weekly selection |
| ReportsView | `/reports/` | GET | Compliance reports |

### Service Classes

**ComplianceScorer** (`audit/services/compliance.py`)
```python
from audit.services.compliance import ComplianceScorer

scorer = ComplianceScorer(audit)
overall = scorer.calculate_overall_score()
doc_score = scorer.calculate_document_score()
equipment_score = scorer.calculate_equipment_score()
condition_score = scorer.calculate_condition_score()
check_score = scorer.calculate_check_score()
```

**IssueWorkflow** (`audit/services/issue_workflow.py`)
```python
from audit.services.issue_workflow import IssueWorkflow

workflow = IssueWorkflow(issue)
workflow.assign(assigned_to='Jane Doe')
workflow.start_progress()
workflow.mark_pending_verification()
workflow.resolve(resolution_summary='...')
workflow.close(verified_by='Manager')
workflow.escalate(reason='SLA breach')
```

**RandomAuditSelector** (`audit/services/random_selection.py`)
```python
from audit.services.random_selection import RandomAuditSelector

selector = RandomAuditSelector()
selection = selector.generate_weekly_selection(
    selection_count=10,
    generated_by='automation'
)
active = selector.get_active_selection()
```

---

## Documentation

- **Models**: Detailed in [Database Schema](#database-schema-17-entities) section
- **Views**: Documented in view docstrings (`audit/views.py`)
- **Services**: See service module docstrings and inline comments
- **Forms**: See `audit/forms.py` for field validation
- **Templates**: See `audit/templates/audit/` for UI structure

---

## Support & Issues

Report bugs or request features via GitHub Issues.

For internal RBWH support, contact:
- System Admin: [email]
- Clinical Governance: [email]

---

## License

Internal use - Royal Brisbane and Women's Hospital

*Version: 2.0 | January 2026*
*Architecture: Django 5.1 + SQLite (migrated from SharePoint)*
