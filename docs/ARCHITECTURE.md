# REdI Trolley Audit System -- Architecture Document

> Standalone Django web application for managing resuscitation trolley audits
> at Royal Brisbane and Women's Hospital (RBWH).

**Version:** 1.0
**Last updated:** February 2026
**Stack:** Django 5.1 / PostgreSQL 16 / Bootstrap 5.3 / HTMX / Docker (rootless)

---

## Table of Contents

1. [Overview and Purpose](#1-overview-and-purpose)
2. [System Context](#2-system-context)
3. [Technology Stack and Decisions](#3-technology-stack-and-decisions)
4. [Infrastructure and Deployment](#4-infrastructure-and-deployment)
5. [Application Architecture](#5-application-architecture)
6. [Data Model Summary](#6-data-model-summary)
7. [Security Architecture](#7-security-architecture)
8. [Business Logic Services](#8-business-logic-services)
9. [Frontend Architecture](#9-frontend-architecture)
10. [API Design](#10-api-design)
11. [Scheduled Tasks](#11-scheduled-tasks)
12. [Monitoring and Logging](#12-monitoring-and-logging)
13. [Development Workflow](#13-development-workflow)

---

## 1. Overview and Purpose

### Problem

RBWH maintains approximately **76 resuscitation trolleys** spread across 7
service lines.  Each trolley must be audited regularly to verify that
documentation is current, all 89 equipment items are present and unexpired,
physical condition is acceptable, and routine daily/weekly checks have been
performed.

The previous process relied on Microsoft Forms and fragmented spreadsheets.
There was no central compliance scoring, no SLA enforcement on issues, and no
priority-weighted random selection of trolleys for audit.

### Solution

REdI (Resuscitation Education Initiative) is a **standalone Django web
application** that replaces the legacy process with:

- A **5-step audit wizard** with weighted compliance scoring.
- A **7-state issue lifecycle** with SLA-based auto-escalation.
- **Priority-weighted random audit selection** (~10 trolleys/week).
- **5 user roles** enforced at view, template, and URL levels.
- **Dashboard, reports, and CSV/Excel export** for governance.

### Migration History

The system was originally designed for SharePoint/Power Platform.  It was
re-architected as a standalone Django application for simplicity, cost, and
direct control over compliance algorithms.  The current database is SQLite for
development; production targets PostgreSQL 16.

---

## 2. System Context

```
                          +---------------------+
                          |   Hospital Staff     |
                          |  (Browser / HTMX)    |
                          +----------+----------+
                                     |
                                     | HTTPS (TLS terminated at host nginx)
                                     |
                        +------------v-------------+
                        |    nginx (host-level)    |
                        |    reverse proxy         |
                        |    :443 -> :11000        |
                        +------------+-------------+
                                     |
                    +----------------v------------------+
                    |        Docker (rootless)          |
                    |                                   |
                    |  +-----------------------------+  |
                    |  |  web  (Gunicorn + Django)   |  |
                    |  |  port 11000                 |  |
                    |  |  WhiteNoise static files    |  |
                    |  +-------------+--------------+   |
                    |                |                   |
                    |  +-------------v--------------+   |
                    |  |  db  (PostgreSQL 16)        |  |
                    |  |  port 11001 (internal only) |  |
                    |  +----------------------------+   |
                    |                                   |
                    |  Named volumes:                   |
                    |    redi_pgdata   (database)       |
                    |    redi_static   (collectstatic)  |
                    +-----------------------------------+
                                     |
                    +----------------v------------------+
                    |   Power Automate HTTP Trigger     |
                    |   (email delivery via QH infra)   |
                    +-----------------------------------+
```

### External Integrations

| System | Protocol | Purpose |
|--------|----------|---------|
| **Power Automate** | HTTPS POST (JSON) | Email delivery for notifications, escalations, weekly selection alerts |
| **nginx (host)** | HTTP reverse proxy | TLS termination, request routing to container port 11000 |
| **GitHub Actions** | CI/CD | Automated testing, linting, security scanning, Docker image publishing |
| **GHCR** | Container registry | `ghcr.io` image storage for tagged releases |

---

## 3. Technology Stack and Decisions

### Stack Summary

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Runtime | Python | 3.12+ | CI tests against 3.11, 3.12, 3.13 |
| Web Framework | Django | 5.1 | LTS-adjacent; `redi` project, `audit` app |
| Database (dev) | SQLite | 3 | Zero-config local development |
| Database (prod) | PostgreSQL | 16 | Named volume `redi_pgdata` |
| Frontend | Bootstrap 5.3 + HTMX | -- | Server-rendered templates with progressive enhancement |
| Static Files | WhiteNoise | 6.7+ | `CompressedManifestStaticFilesStorage` |
| WSGI Server | Gunicorn | 23.0+ | Multi-worker production server |
| Email | Power Automate API | -- | HTTP POST, replaces SMTP |
| Filtering | django-filter | 24.0+ | Queryset filtering for list views |
| Utilities | django-extensions | 3.2+ | Development helpers |
| HTTP Client | requests | 2.31+ | Power Automate API calls |
| Containerization | Docker Compose | -- | Rootless, named volumes, unprivileged ports |
| CI/CD | GitHub Actions | -- | `ci.yml`, `release.yml`, `security.yml`, `playwright.yml` |
| Reverse Proxy | nginx | host-level | NOT in the Docker stack |
| Linting | Ruff | -- | Fast Python linter in CI |
| Security Scanning | pip-audit + TruffleHog | -- | Weekly dependency audit + secret detection |

### Key Architectural Decisions

**Why Django over SharePoint/Power Platform?**
- Single codebase vs. distributed SharePoint configuration.
- Direct control over compliance scoring algorithms (Decimal arithmetic).
- No SharePoint licensing cost.
- Simple deployment: one container + one database.

**Why server-rendered templates + HTMX over a SPA?**
- Python-only team; no frontend framework expertise required.
- HTMX provides partial page updates without a JavaScript build pipeline.
- Better accessibility for hospital intranet users.
- Simpler testing: Django test client covers the full request cycle.

**Why WhiteNoise over nginx static serving?**
- Simplifies the Docker image to a single process (Gunicorn).
- `CompressedManifestStaticFilesStorage` handles gzip and cache-busting.
- Adequate performance for the expected user base (~50 concurrent users).

**Why Power Automate over SMTP?**
- Queensland Health infrastructure does not expose SMTP relays to internal apps.
- Power Automate provides delivery tracking and retry logic natively.
- Template management stays within the Microsoft 365 ecosystem.

**Why SQLite for development, PostgreSQL for production?**
- SQLite is zero-config for local development and CI.
- PostgreSQL provides `SELECT ... FOR UPDATE` needed by the Issue
  auto-numbering logic (`ISS-YYYYMM-NNN`) and better concurrency under
  Gunicorn's multi-worker model.

---

## 4. Infrastructure and Deployment

### Constraints

| Constraint | Detail |
|-----------|--------|
| **nginx at host level** | Dev and prod servers run nginx on the host, NOT inside Docker. The Docker stack must not include an nginx service. |
| **Rootless Docker** | Containers run without root privileges. No privileged ports (<1024). |
| **Named volumes only** | Bind mounts are not used. All persistent data uses Docker named volumes. |
| **Unprivileged ports** | Port block `11000-11010` is allocated to this application. |

### Port Allocation

| Port | Service | Exposure |
|------|---------|----------|
| **11000** | Gunicorn (Django web app) | Exposed to host; nginx proxies to this |
| **11001** | PostgreSQL | Internal only (container-to-container) |
| 11002-11010 | Reserved | Future services (Redis, Celery worker, etc.) |

### Docker Compose Structure (Target)

```yaml
# docker-compose.yml (production target)
services:
  web:
    image: ghcr.io/<org>/trolleys:latest
    ports:
      - "11000:11000"
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DJANGO_DEBUG=False
      - DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}
      - DATABASE_URL=postgres://redi:${DB_PASSWORD}@db:5432/redi
      - EMAIL_API_ENDPOINT=${EMAIL_API_ENDPOINT}
    volumes:
      - redi_static:/app/staticfiles
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=redi
      - POSTGRES_USER=redi
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - redi_pgdata:/var/lib/postgresql/data
    # No port exposure to host -- internal only

volumes:
  redi_pgdata:
  redi_static:
```

### Host nginx Configuration (Excerpt)

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

### Release Pipeline

```
Tag v*.*.* push  -->  GitHub Actions (release.yml)
                       |
                       +-> Generate changelog (git-cliff)
                       +-> Create GitHub Release
                       +-> Build Docker image
                       +-> Push to ghcr.io
                       +-> Deploy (manual pull on server)
```

### Environment Variables (Production)

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SECRET_KEY` | Yes | Cryptographic key for sessions, CSRF |
| `DJANGO_DEBUG` | Yes | Must be `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Yes | Comma-separated hostnames |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `EMAIL_API_ENDPOINT` | No | Power Automate HTTP trigger URL |
| `EMAIL_API_TIMEOUT` | No | Timeout in seconds (default: 30) |
| `DB_PASSWORD` | Yes | PostgreSQL password (Compose interpolation) |

---

## 5. Application Architecture

### Django Project Layout

```
backend/
  manage.py
  redi/                         # Django project package
    __init__.py
    settings.py                 # Single settings file, env-var driven
    urls.py                     # Root URL conf: admin + auth + audit
    wsgi.py                     # Gunicorn entry point
    asgi.py                     # ASGI entry point (unused currently)

  audit/                        # Single Django app (all domain logic)
    models.py                   # 17 models
    views.py                    # 22 view classes
    forms.py                    # 8 form classes
    urls.py                     # 23 URL patterns (app_name = 'audit')
    admin.py                    # Django admin registration for all models
    apps.py                     # AppConfig
    mixins.py                   # 6 role-based access mixins
    context_processors.py       # Global template role flags

    services/                   # Business logic layer
      __init__.py
      compliance.py             # ComplianceScorer
      issue_workflow.py         # IssueWorkflow (state machine)
      random_selection.py       # RandomAuditSelector
      notifications.py          # NotificationService
      email_backend.py          # PowerAutomateEmailService

    management/commands/        # CLI commands for cron and setup
      seed_data.py              # Load reference data from JSON
      setup_roles.py            # Create Django groups and permissions
      check_sla.py              # Daily SLA check and auto-escalation
      generate_weekly_selection.py  # Weekly random selection

    templates/audit/            # Django templates (Bootstrap 5)
    static/audit/               # CSS, JS, images
    templatetags/audit_tags.py  # Custom template filters
    migrations/                 # Schema migrations
```

### Layered Architecture

```
+---------------------------------------------------------+
|                    URL Routing Layer                     |
|  redi/urls.py -> audit/urls.py (23 patterns)            |
+---------------------------------------------------------+
|                    View Layer (22 views)                 |
|  Class-based views with role mixins                     |
|  AuditOwnershipMixin for wizard integrity               |
+---------------------------------------------------------+
|                    Form Layer (8 forms)                  |
|  ModelForms with Bootstrap widget classes                |
+---------------------------------------------------------+
|                    Service Layer                         |
|  ComplianceScorer | IssueWorkflow | RandomAuditSelector  |
|  NotificationService | PowerAutomateEmailService         |
+---------------------------------------------------------+
|                    Model Layer (17 models)               |
|  Django ORM with UUID primary keys                      |
|  Decimal fields for compliance scores                   |
+---------------------------------------------------------+
|                    Database                              |
|  SQLite (dev) / PostgreSQL 16 (prod)                    |
+---------------------------------------------------------+
```

### Request Flow

```
Browser
  -> nginx (host, TLS termination)
    -> Gunicorn :11000
      -> Django middleware stack
        -> SecurityMiddleware
        -> WhiteNoiseMiddleware (static files short-circuit)
        -> SessionMiddleware
        -> CommonMiddleware
        -> CsrfViewMiddleware
        -> AuthenticationMiddleware
        -> MessageMiddleware
        -> XFrameOptionsMiddleware
      -> URL routing (redi/urls.py -> audit/urls.py)
      -> Role mixin check (ViewerRequired / AuditorRequired / etc.)
      -> View logic (calls services if needed)
      -> Template rendering (Bootstrap 5 + HTMX attributes)
  <- HTML response
```

---

## 6. Data Model Summary

### Entity Relationship Overview

17 models organized into 6 domains:

```
REFERENCE DATA              MASTER DATA              AUDIT WORKFLOW
+--------------+          +------------+          +-------------+
| ServiceLine  |<---+     | Equipment  |          | AuditPeriod |
| (7 records)  |    |     | (89 items) |          +------+------+
+--------------+    |     +-----+------+                 |
                    |           |                         |
                    |     +-----v----------+       +-----v------+
                    +---->| Location       |<------| Audit      |
                          | (76 trolleys)  |       | (main)     |
                          +---+---+--------+       +--+--+--+--++
                              |   |                   |  |  |  |
                 +------------+   |    +--------------+  |  |  +----------+
                 |                |    |                  |  |             |
        +--------v-------+ +----v----v-----+  +----------v-+ +---------v------+
        |LocationEquipment| |LocationChange | |AuditDocuments| |AuditEquipment |
        |(overrides)      | |Log (trail)    | |AuditCondition| |(per-item)     |
        +----------------+ +---------------+ |AuditChecks   | +---------------+
                                              +-------------+
                                                     |
ISSUE TRACKING                            RANDOM SELECTION
+----------+                              +-------------------+
| Issue     |<----+                       | RandomAudit       |
| (7-state) |    |                        | Selection         |
+--+-----+--+    |                        +--------+----------+
   |     |       |                                  |
+--v--+ +v------++-+                     +----------v---------+
|Corr.| |Issue     |                     | RandomAuditSelection|
|Action| |Comment   |                     | Item                |
+-----+ +---------+                      +--------------------+
```

### Model Counts and Relationships

| Domain | Model | Records | Key Relationships |
|--------|-------|---------|-------------------|
| **Reference** | ServiceLine | 7 | -> Location (1:N) |
| | EquipmentCategory | 8 | -> Equipment (1:N) |
| | AuditPeriod | per month | -> Audit (1:N) |
| **Master** | Equipment | 89 | -> EquipmentCategory (N:1) |
| | Location | 76 | -> ServiceLine (N:1), -> Audit (1:N), -> Issue (1:N) |
| | LocationEquipment | varies | -> Location (N:1), -> Equipment (N:1); unique(location, equipment) |
| **Audit** | Audit | grows | -> Location (N:1), -> AuditPeriod (N:1), -> User (N:1) |
| | AuditDocuments | 1:1 Audit | Documentation check results |
| | AuditCondition | 1:1 Audit | Physical condition assessment |
| | AuditChecks | 1:1 Audit | Routine check counts |
| | AuditEquipment | N:1 Audit | Per-item check result; unique(audit, equipment) |
| **Issues** | Issue | grows | -> Location (N:1), -> Audit (N:1, nullable), auto-numbered `ISS-YYYYMM-NNN` |
| | CorrectiveAction | N:1 Issue | Actions taken to resolve |
| | IssueComment | N:1 Issue | Comments with internal/external flag |
| **Selection** | RandomAuditSelection | weekly | Weekly batch header |
| | RandomAuditSelectionItem | ~10/week | -> Selection (N:1), -> Location (N:1); unique(selection, location) |
| **Trail** | LocationChangeLog | grows | -> Location (N:1); field-level change audit trail |

### Key Design Choices

- **UUID primary keys** on all models (`uuid.uuid4`). Prevents enumeration attacks
  and supports future multi-site federation.
- **Decimal fields** for compliance scores (`max_digits=5, decimal_places=2`).
  Avoids floating-point rounding in compliance calculations.
- **`on_delete=PROTECT`** on Location foreign keys in Audit and Issue to prevent
  accidental data loss.
- **`on_delete=SET_NULL`** on optional relationships (auditor_user, triggered_by_issue).
- **Atomic issue numbering** with `select_for_update()` and retry loop to handle
  concurrent issue creation safely.

---

## 7. Security Architecture

### Authentication

- **Django's built-in authentication** (`django.contrib.auth`).
- Session-based login via `django.contrib.auth.urls` (`/accounts/login/`, `/accounts/logout/`).
- No SSO or LDAP integration currently (planned future enhancement).

### Session Management

| Setting | Value | Rationale |
|---------|-------|-----------|
| `SESSION_COOKIE_AGE` | 28800 (8 hours) | Covers a full hospital shift |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | `True` | Shared workstation protection |
| `SESSION_COOKIE_SECURE` | `True` in prod | HTTPS-only cookie transmission |
| `CSRF_COOKIE_SECURE` | `True` in prod | HTTPS-only CSRF token |

### Authorization (RBAC)

Five roles implemented as **Django Groups** with a layered mixin hierarchy:

```
ViewerRequiredMixin          -- any authenticated user with a group
  AuditorRequiredMixin       -- Viewer + Auditor
    ManagerRequiredMixin     -- Auditor + Service Line Manager
      EducatorRequiredMixin  -- Manager + MERT Educator
        AdminRequiredMixin   -- System Admin only
```

All mixins extend `RoleRequiredMixin`, which:
1. Requires `LoginRequiredMixin` (redirects to `/accounts/login/`).
2. Calls `UserPassesTestMixin.test_func()` to check group membership.
3. Grants automatic access to `is_superuser` users.

| Role | Group Name | Capabilities |
|------|-----------|--------------|
| **System Admin** | `System Admin` | Full access; Django admin; user management |
| **MERT Educator** | `MERT Educator` | Full CRUD on trolleys, audits, issues; generate selections; configure equipment |
| **Service Line Manager** | `Service Line Manager` | Manage audits/issues within their service line; CSV export |
| **Auditor** | `Auditor` | Create/submit audits; report issues; add comments |
| **Viewer** | `Viewer` | Read-only access to all dashboards and reports |

### Template-Level Authorization

The `user_roles` context processor injects boolean flags into every template:

```python
# Available in all templates:
is_admin, is_educator, is_manager, is_auditor, is_viewer
```

This allows conditional rendering of navigation items and action buttons without
duplicating role logic in views.

### CSRF Protection

- Django's `CsrfViewMiddleware` is active on all POST requests.
- HTMX requests include the CSRF token via `hx-headers` or Django's
  `{% csrf_token %}` template tag.

### Additional Security Measures

- **XFrameOptionsMiddleware**: Prevents clickjacking via `X-Frame-Options: DENY`.
- **SecurityMiddleware**: Sets `X-Content-Type-Options`, `Strict-Transport-Security`.
- **Secrets in environment variables**: `SECRET_KEY`, `DATABASE_URL`, `EMAIL_API_ENDPOINT`
  are never hardcoded in production.
- **`ALLOWED_HOSTS` enforcement**: Prevents HTTP Host header attacks.
- **Export whitelist**: `ExportView.ALLOWED_EXPORT_TYPES` prevents arbitrary export
  type injection.
- **Audit ownership validation**: `AuditOwnershipMixin` ensures only the original
  auditor (or superuser) can modify an in-progress audit.

### CI Security

- **pip-audit**: Weekly dependency vulnerability scanning (`security.yml`).
- **TruffleHog**: Secret detection on every push to main.

---

## 8. Business Logic Services

All complex business logic lives in `audit/services/`, separate from views and
models.  Services are stateless classes instantiated per-request.

### 8.1 ComplianceScorer

**File:** `audit/services/compliance.py`

Calculates the 4-factor weighted compliance score for a completed audit.

```
Overall = (Documentation * 0.25) + (Equipment * 0.40) +
          (Condition * 0.15) + (Checks * 0.20)
```

| Component | Weight | Calculation |
|-----------|--------|-------------|
| Documentation | 25% | 4 binary checks (record, guidelines, BLS poster, equipment list) |
| Equipment | 40% | Critical items weighted 60%, non-critical 40%; checks presence, quantity, expiry |
| Condition | 15% | 5 binary checks (clean, working, rubber bands, O2 tubing, INHALO cylinder) |
| Routine Checks | 20% | (outside_actual/outside_expected + inside_actual/inside_expected) / 2 |

All arithmetic uses `Decimal` with `ROUND_HALF_UP` to 2 decimal places.

Equipment scoring has a **critical item sub-weighting**:
```
Equipment Score = (Critical Score * 0.60) + (Non-Critical Score * 0.40)
```

Where each sub-score is `passing_items / total_items * 100`.  An item passes if
it is present, quantity meets expectation, and expiry is OK (when applicable).

### 8.2 IssueWorkflow

**File:** `audit/services/issue_workflow.py`

Implements a **7-state finite state machine** with SLA enforcement.

**State Transition Diagram:**

```
  +-------+     +----------+     +------------+     +-------------------+
  | Open  +---->| Assigned +---->| InProgress +---->| PendingVerification|
  +---^---+     +----+-----+     +-----+------+     +--------+----------+
      |              |                  |                     |
      |              |                  |            +--------v-----+
      |              +---->Escalated<---+            | Resolved     |
      |                    +----+                    +--------+-----+
      |                         |                             |
      +-------------------------+                    +--------v-----+
      |         (de-escalate to Assigned)            | Closed       |
      +----------------------------------------------+----+---------+
                         (reopen from Resolved or Closed)
```

**Valid Transitions:**

| From | To |
|------|----|
| Open | Assigned, Escalated |
| Assigned | InProgress, Escalated |
| InProgress | PendingVerification, Escalated |
| PendingVerification | Resolved, InProgress (rejection) |
| Resolved | Closed, Open (reopen) |
| Closed | Open (reopen) |
| Escalated | Assigned (de-escalation) |

**SLA Targets:**

| Severity | SLA Hours | Calendar Equivalent |
|----------|-----------|---------------------|
| Critical | 24 | 1 day |
| High | 72 | 3 business days |
| Medium | 120 | 5 business days |
| Low | 240 | 10 business days |

**Auto-escalation:** The `check_and_auto_escalate()` method is called by the
`check_sla` management command.  If an issue's SLA target has passed and it is
not already Resolved, Closed, or Escalated, the system transitions it to
Escalated and creates an internal comment.

**Max escalation level:** 5.  Beyond this, `needs_management_review()` returns
`True` for UI flagging.

Every transition creates an `IssueComment` with `is_internal=True` documenting
the old state, new state, and reason.

### 8.3 RandomAuditSelector

**File:** `audit/services/random_selection.py`

Selects ~10 trolleys per week using a **priority-weighted algorithm** with
service line distribution.

**Priority Scoring:**

| Days Since Last Audit | Base Score |
|-----------------------|-----------|
| Never audited | 1000 |
| > 180 days | 500 + days |
| > 90 days | 250 + days |
| > 60 days | 100 + days |
| > 30 days | 50 + days |
| 0-30 days | 10 + days |

**Selection Algorithm:**
1. Score all active locations.
2. **Phase 1 -- Service line distribution:** Pick the highest-priority location
   from each service line (up to 7).
3. **Phase 2 -- Fill remaining slots:** From the remaining pool, shuffle within
   score tiers (rounded to nearest 10) for randomness, then pick top scorers.
4. Create `RandomAuditSelection` + `RandomAuditSelectionItem` records.
5. Deactivate previous active selections.

### 8.4 NotificationService

**File:** `audit/services/notifications.py`

Sends HTML email notifications via the `PowerAutomateEmailService` backend.

| Event | Recipients | Importance |
|-------|-----------|------------|
| Audit completed | Service line contacts | Normal |
| Critical issue created | All MERT Educators | High |
| Issue assigned | Assigned user | Normal |
| SLA breach warning | Service line contacts + MERT Educators | High |
| Weekly selection generated | All MERT Educators | Normal |

### 8.5 PowerAutomateEmailService

**File:** `audit/services/email_backend.py`

Thin HTTP client that POSTs JSON payloads to a Power Automate HTTP trigger
endpoint.  Replaces Django's SMTP email backend entirely.

**Payload format:**
```json
{
  "to": "user@health.qld.gov.au",
  "subject": "[REdI] Audit Completed: ED Resus Bay",
  "body": "<h2>Audit Completed</h2>...",
  "importance": "Normal"
}
```

Gracefully handles missing configuration (`EMAIL_API_ENDPOINT` not set),
timeouts, and HTTP errors by logging warnings and returning `False`.

---

## 9. Frontend Architecture

### Rendering Strategy

**Server-side rendered** Django templates with **progressive enhancement** via
HTMX.  No JavaScript build pipeline or SPA framework.

### Template Hierarchy

```
templates/
  audit/
    base.html                   # Root layout: navbar, sidebar, messages, footer
    dashboard.html              # KPIs, recent audits, recent issues, charts
    trolley_list.html           # Filterable, paginated location list
    trolley_detail.html         # Location detail + audit history + issues
    trolley_edit.html           # Location edit form
    audit_list.html             # Filterable audit history
    audit_detail.html           # Read-only audit review
    audit_documents.html        # Wizard step 1: documentation
    audit_equipment.html        # Wizard step 2: equipment checklist
    audit_condition.html        # Wizard step 3: physical condition
    audit_checks.html           # Wizard step 4: routine checks
    audit_review.html           # Wizard step 5: review + score preview
    issue_list.html             # Filterable issue list with status counts
    issue_detail.html           # Issue detail + workflow actions + comments
    issue_create.html           # New issue form
    random_selection.html       # Current + past weekly selections
    reports.html                # Reports landing page
    compliance_report.html      # Service line compliance breakdown
```

### CSS Framework

**Bootstrap 5.3** loaded from CDN or local static files.  All form widgets use
Bootstrap classes (`form-control`, `form-select`) applied at the Django form
level via widget `attrs`.

Custom REdI branding is applied via an additional stylesheet overriding Bootstrap
variables for hospital colour scheme.

### HTMX Integration

HTMX provides partial page updates for:
- Filter changes on list views (trolleys, audits, issues).
- Inline form submissions in the audit wizard.
- Comment posting on issue detail pages.
- Dashboard widget refresh.

Pattern: views detect `HX-Request` header and return partial HTML fragments
instead of full page renders when appropriate.

### JavaScript

Minimal custom JavaScript for:
- Equipment checklist bulk operations (select all, quantity helpers).
- Client-side form validation enhancements.
- Chart rendering on dashboard (if Chart.js is included).

No bundler, no npm, no node_modules.

---

## 10. API Design

### Current: Server-Rendered Views

The application currently uses **Django views returning HTML**.  There is no
dedicated REST API layer.  All interactions happen through standard form
submissions and HTMX requests.

### URL Patterns (23 routes)

| Pattern | View | Methods | Access |
|---------|------|---------|--------|
| `/` | DashboardView | GET | Login required |
| `/trolleys/` | TrolleyListView | GET | Viewer+ |
| `/trolleys/<uuid>/` | TrolleyDetailView | GET | Viewer+ |
| `/trolleys/<uuid>/edit/` | TrolleyEditView | GET, POST | Educator+ |
| `/audits/` | AuditListView | GET | Viewer+ |
| `/audits/start/<uuid>/` | AuditStartView | POST | Auditor+ |
| `/audits/<uuid>/` | AuditDetailView | GET | Viewer+ |
| `/audits/<uuid>/documents/` | AuditDocumentsView | GET, POST | Auditor+ (owner) |
| `/audits/<uuid>/equipment/` | AuditEquipmentView | GET, POST | Auditor+ (owner) |
| `/audits/<uuid>/condition/` | AuditConditionView | GET, POST | Auditor+ (owner) |
| `/audits/<uuid>/checks/` | AuditChecksView | GET, POST | Auditor+ (owner) |
| `/audits/<uuid>/review/` | AuditReviewView | GET | Auditor+ (owner) |
| `/audits/<uuid>/submit/` | AuditSubmitView | POST | Auditor+ (owner) |
| `/issues/` | IssueListView | GET | Viewer+ |
| `/issues/create/` | IssueCreateView | GET, POST | Auditor+ |
| `/issues/<uuid>/` | IssueDetailView | GET | Viewer+ |
| `/issues/<uuid>/transition/<action>/` | IssueTransitionView | POST | Manager+ |
| `/issues/<uuid>/comment/` | IssueCommentView | POST | Auditor+ |
| `/selection/` | RandomSelectionView | GET | Educator+ |
| `/selection/generate/` | GenerateSelectionView | POST | Educator+ |
| `/reports/` | ReportsView | GET | Viewer+ |
| `/reports/compliance/` | ComplianceReportView | GET | Viewer+ |
| `/reports/export/` | ExportView | GET | Manager+ |
| `/admin/` | Django Admin | -- | Superuser |
| `/accounts/*` | Django Auth views | -- | Public |

### Future: REST API

If mobile access or external integrations are needed, a REST API layer using
Django REST Framework would be added under `/api/v1/`.  The service layer
(`audit/services/`) is already decoupled from views, making this straightforward.

### CSV Export Endpoints

`/reports/export/?type=<audits|issues|locations>` returns CSV files.
The `ALLOWED_EXPORT_TYPES` whitelist prevents injection of arbitrary export types.

---

## 11. Scheduled Tasks

Two management commands are designed to run on a schedule:

### Daily: SLA Check and Auto-Escalation

```bash
python manage.py check_sla
```

**Schedule:** Daily at 08:00 AEST (Australia/Brisbane)

**Logic:**
1. Query all issues with status in (Open, Assigned, InProgress, PendingVerification).
2. For each, call `IssueWorkflow.check_and_auto_escalate()`.
3. If SLA is breached: transition to Escalated, create internal comment, send
   notification.

### Weekly: Random Audit Selection

```bash
python manage.py generate_weekly_selection
```

**Schedule:** Monday at 07:00 AEST

**Logic:**
1. Score all active locations by days since last audit.
2. Select ~10 with service line distribution.
3. Create selection batch and items.
4. Deactivate previous week's selection.
5. Send notification to MERT Educators.

### Scheduling Options

Since the current stack does not include Celery or Redis:

| Option | Pros | Cons |
|--------|------|------|
| **Host crontab** | Simplest; no extra containers | Requires host access; not containerized |
| **docker exec cron** | Runs inside existing container | Needs cron in image or sidecar |
| **APScheduler in-process** | No external dependency | Tied to Gunicorn process lifecycle |
| **django-celery-beat + Redis** | Production-grade; dashboard | Adds Redis container (port 11002) |

**Recommended for initial deployment:** Host crontab calling
`docker exec redi-web python manage.py <command>`.

**Future:** Migrate to django-celery-beat with Redis on port 11002 when task
volume or reliability requirements increase.

### Crontab Examples

```crontab
# /etc/cron.d/redi-audit
# Daily SLA check at 8:00 AM Brisbane time
0 8 * * * docker exec redi-web python manage.py check_sla >> /var/log/redi/sla.log 2>&1

# Weekly random selection at 7:00 AM Monday
0 7 * * 1 docker exec redi-web python manage.py generate_weekly_selection >> /var/log/redi/selection.log 2>&1
```

---

## 12. Monitoring and Logging

### Django Logging

Django's standard logging framework (`logging` module) is used throughout:

| Logger | Level | Purpose |
|--------|-------|---------|
| `audit.views` | INFO/WARNING | View-level events, permission denials |
| `audit.services.notifications` | INFO/WARNING/ERROR | Email send success/failure |
| `audit.services.email_backend` | INFO/ERROR | Power Automate API errors, timeouts |
| `audit.management.commands` | INFO | Scheduled task execution |

### Recommended Production Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'audit': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

In a Docker context, logging to stdout/stderr is preferred. Container log
drivers (json-file, syslog) handle aggregation.

### Health Checks

Recommended health check endpoint (to be implemented):

```
GET /health/ -> 200 OK + {"status": "ok", "db": "ok"}
```

nginx or Docker health checks can poll this endpoint.

### Key Metrics to Monitor

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Audit submission rate | Audit table | < 5/week |
| Open issues count | Issue table (not Closed/Resolved) | > 50 |
| SLA breach rate | Issue escalation events | > 20% of active issues |
| Email delivery failures | email_backend logs | Any ERROR |
| Response time (P95) | nginx access log | > 2 seconds |
| Container restart count | Docker | Any restart |

---

## 13. Development Workflow

### Local Development

```bash
# Clone and set up
git clone <repo> && cd trolleys/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Initialize database
python manage.py migrate
python manage.py seed_data       # 7 SLs, 8 categories, 89 items, 76 locations
python manage.py setup_roles     # 5 Django groups
python manage.py createsuperuser

# Run dev server
python manage.py runserver       # http://localhost:8000
```

### Management Commands Reference

| Command | Purpose | When to Run |
|---------|---------|-------------|
| `seed_data` | Load reference data from `seed_data/*.json` | Initial setup, database reset |
| `setup_roles` | Create 5 Django groups with permissions | Initial setup, after migrations |
| `check_sla` | Check issue SLAs, auto-escalate breached | Daily cron |
| `generate_weekly_selection` | Generate random audit selection | Weekly cron (Monday) |
| `createsuperuser` | Create admin account | Initial setup |
| `collectstatic` | Gather static files for WhiteNoise | Before production deploy |

### CI/CD Pipeline

Four GitHub Actions workflows:

| Workflow | Trigger | Jobs |
|----------|---------|------|
| **CI** (`ci.yml`) | Push/PR to main | `test` (Python 3.11/3.12/3.13): install deps, system checks, migrate, seed, check migrations. `lint`: Ruff linter. |
| **Release** (`release.yml`) | Tag `v*.*.*` | Generate changelog (git-cliff), create GitHub Release, build + push Docker image to GHCR. |
| **Security** (`security.yml`) | Push to main + weekly Monday | pip-audit dependency scan, TruffleHog secret detection. |
| **Playwright** (`playwright.yml`) | (Configured) | End-to-end browser testing. |

### Branching Strategy

- **main**: Production-ready code. Protected branch.
- **feature/<name>**: Feature development branches. PR to main.
- **fix/<name>**: Bug fix branches. PR to main.
- **Tags**: `v*.*.*` triggers release pipeline.

### Code Quality

- **Ruff** for linting (configured in CI).
- **Django system checks** (`manage.py check --deploy`) run in CI.
- **Migration integrity** verified via `makemigrations --check --dry-run`.

### Database Reset (Development)

```bash
rm backend/db.sqlite3
python manage.py migrate
python manage.py seed_data
python manage.py setup_roles
python manage.py createsuperuser
```

---

## Appendix A: Seed Data Summary

| File | Model | Records | Description |
|------|-------|---------|-------------|
| `seed_data/ServiceLine.json` | ServiceLine | 7 | Hospital service lines |
| `seed_data/EquipmentCategory.json` | EquipmentCategory | 8 | Trolley sections (Top, Drawers 1-4, External, Meds, Specialty) |
| `seed_data/Equipment.json` | Equipment | 89 | All equipment items with S/4HANA codes, quantities, flags |
| `seed_data/Location.json` | Location | 76 | All trolley locations with building, level, type, defib |
| `seed_data/AuditPeriod.json` | AuditPeriod | 1 | Initial audit period (January 2026) |

## Appendix B: Compliance Scoring Formula

```
Overall = (Doc * 0.25) + (Equip * 0.40) + (Cond * 0.15) + (Checks * 0.20)

Doc     = (current_items / 4) * 100
Equip   = (critical_pass/critical_total * 0.60 + noncrit_pass/noncrit_total * 0.40) * 100
Cond    = (passing_checks / 5) * 100
Checks  = ((outside_actual/outside_expected) * 0.50 + (inside_actual/inside_expected) * 0.50) * 100

All values: Decimal, ROUND_HALF_UP, 2 decimal places
Thresholds: < 80% triggers follow-up audit (14-day deadline)
```

## Appendix C: Issue Number Format

```
ISS-YYYYMM-NNN

Example: ISS-202601-001

Generated atomically in Issue.save() using:
1. Prefix from current month: ISS-{now.strftime('%Y%m')}-
2. SELECT ... FOR UPDATE on existing issues with same prefix
3. Increment last sequence number
4. Retry loop (3 attempts) for concurrent creation
```
