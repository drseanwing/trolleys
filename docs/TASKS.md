# REdI Trolley Audit System - Implementation Task List

> Comprehensive task breakdown for completing the REdI (Resuscitation Education Initiative)
> Trolley Audit System as a standalone Django web application.
>
> **Hospital:** Royal Brisbane and Women's Hospital (RBWH)
> **Stack:** Django 5.1 / PostgreSQL / Bootstrap 5 / HTMX / Chart.js
> **Infrastructure:** Rootless Docker, ports 11000-11010, host-level nginx

---

## Current State Summary

### What EXISTS and is COMPLETE

| Layer | Files | Status |
|-------|-------|--------|
| Django project | `redi/settings.py`, `urls.py`, `wsgi.py`, `asgi.py` | Working (SQLite) |
| Models | `audit/models.py` -- 17 models, all fields defined | Complete |
| Admin | `audit/admin.py` -- all 17 models registered with inlines | Complete |
| Forms | `audit/forms.py` -- 8 form classes | Complete |
| Views | `audit/views.py` -- 20 view classes, fully implemented | Complete |
| URLs | `audit/urls.py` -- 15 URL patterns, all wired | Complete |
| Services | `compliance.py`, `issue_workflow.py`, `random_selection.py`, `notifications.py`, `email_backend.py` | Complete |
| Mixins | `audit/mixins.py` -- 6 role-based access mixins | Complete |
| Context processors | `audit/context_processors.py` -- user role flags | Complete |
| Template tags | `audit/templatetags/audit_tags.py` -- 2 filters | Complete |
| Templates | 19 HTML templates in `audit/templates/` | Complete (functional) |
| Static CSS | `static/css/redi.css` -- full REdI brand design system (880 lines) | Complete |
| Seed data loader | `management/commands/seed_data.py` | Complete |
| Role setup | `management/commands/setup_roles.py` -- 5 groups | Complete |
| SLA checker | `management/commands/check_sla.py` | Complete |
| Weekly selection | `management/commands/generate_weekly_selection.py` | Complete |
| Email backend | `services/email_backend.py` -- Power Automate HTTP API | Complete |
| CI workflows | `ci.yml`, `release.yml`, `security.yml`, `playwright.yml` (placeholder) | Scaffolded |
| GitHub config | `CODEOWNERS`, issue templates, PR template, dependabot, labels | Complete |
| Procfile | `web: gunicorn redi.wsgi` | Complete |
| Requirements | Django, gunicorn, whitenoise, requests, django-extensions, django-filter | Complete |
| DevContainer | `.devcontainer/Dockerfile` (Python 3.11 dev image) | Complete |

### What NEEDS WORK

| Area | Gap |
|------|-----|
| Docker (production) | No `Dockerfile`, no `docker-compose.yml`, no `docker-compose.prod.yml` |
| PostgreSQL | Settings hardcoded to SQLite; no `psycopg` in requirements |
| Environment config | `.env.example` missing DB vars; no `DATABASE_URL` parsing |
| Static files | No JS files; no HTMX; no Chart.js; CSS exists but no favicon/logo assets |
| Templates | Functional but lack HTMX interactivity, chart containers, polished UX |
| Tests | Zero test files exist anywhere |
| Email | Power Automate backend works but needs SMTP fallback option |
| Seed data directory | `seed_data/` referenced by loader but JSON files not in repo tree |
| Scheduled tasks | Management commands exist but no cron/celery/APScheduler config |
| Export | CSV export works; no Excel (openpyxl) export |
| Documentation | No user guide, deployment guide, or API docs |

---

## Phase 1: Infrastructure & Docker (P0)

Core infrastructure that everything else depends on.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 1.1.1 | Production Dockerfile | Create `Dockerfile` in repo root: Python 3.11-slim, non-root user (UID 1000), install system deps (libpq-dev), pip install requirements, collectstatic, gunicorn entrypoint. Expose port 11000. | Not Started | P0 |
| 1.1.2 | Entrypoint script | Create `docker/entrypoint.sh`: wait-for-db, run migrate, run collectstatic --noinput, then exec gunicorn. | Not Started | P0 |
| 1.1.3 | docker-compose.yml (dev) | Create `docker-compose.yml` for local development: web (Django) on port 11000, postgres on port 11001, named volumes `redi_pgdata` and `redi_static`. Use `.env` file. Build from Dockerfile with dev overrides (DEBUG=True, volume mount for live reload). | Not Started | P0 |
| 1.1.4 | docker-compose.prod.yml | Create `docker-compose.prod.yml` override: no volume mounts for code, DEBUG=False, DJANGO_SECRET_KEY from env, restart policy, health checks, resource limits. | Not Started | P0 |
| 1.1.5 | .dockerignore | Create `.dockerignore`: exclude `.git`, `__pycache__`, `*.pyc`, `db.sqlite3`, `.env`, `node_modules`, `docs/`, `.github/`, `.devcontainer/`. | Not Started | P0 |
| 1.2.1 | Add psycopg to requirements | Add `psycopg[binary]>=3.1` (or `psycopg2-binary`) to `requirements.txt` for PostgreSQL support. | Not Started | P0 |
| 1.2.2 | Database settings refactor | Refactor `redi/settings.py` DATABASES to parse `DATABASE_URL` env var (use `dj-database-url` or manual parsing). Fall back to SQLite when `DATABASE_URL` is not set (dev without Docker). | Not Started | P0 |
| 1.2.3 | Update .env.example | Add `DATABASE_URL=postgres://redi:redi@localhost:11001/redi`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` to `.env.example`. | Not Started | P0 |
| 1.3.1 | Seed data JSON files | Verify `seed_data/` directory exists at repo root with all 5 JSON files (`ServiceLine.json`, `EquipmentCategory.json`, `Equipment.json`, `Location.json`, `AuditPeriod.json`). Create if missing with representative RBWH data. | Not Started | P0 |
| 1.3.2 | Docker seed data command | Add optional seed-data step to entrypoint (gated by `SEED_DATA=true` env var) so first `docker compose up` auto-populates. | Not Started | P0 |
| 1.4.1 | Update CI to test with PostgreSQL | Update `.github/workflows/ci.yml` to use `services: postgres` for test job. Set `DATABASE_URL` in env. Run tests (once they exist). | Not Started | P0 |
| 1.4.2 | Add test runner to CI | Add `python manage.py test` step to CI pipeline (currently missing -- only runs checks and migrations). | Not Started | P0 |
| 1.4.3 | Lint as hard fail | Change `ruff check . || true` to `ruff check .` in CI so lint failures block merge. Add `ruff.toml` or `[tool.ruff]` config. | Not Started | P1 |
| 1.5.1 | Makefile / justfile | Create a `Makefile` (or `justfile`) with targets: `up`, `down`, `build`, `migrate`, `seed`, `shell`, `test`, `lint`, `logs`, `prod-up`, `prod-down`. | Not Started | P2 |

---

## Phase 2: Core Views & Template Polish (P0)

Views and URL routing are already functional. This phase focuses on UX polish, HTMX interactivity, and ensuring all templates render correctly with real data.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 2.1.1 | Add HTMX to base template | Add HTMX CDN script (`htmx.org 2.x`) to `base.html` before closing `</body>`. Add `django-htmx` to requirements and middleware if desired (optional -- CDN-only is fine). | Not Started | P0 |
| 2.1.2 | Add Chart.js to base template | Add Chart.js CDN script to `base.html` `extra_js` block (or globally). Only needed on dashboard/report pages -- consider conditional inclusion. | Not Started | P1 |
| 2.1.3 | Favicon and logo assets | Add REdI favicon (`favicon.ico`, `favicon-32x32.png`) and navbar logo to `static/img/`. Reference in `base.html` `<head>`. | Not Started | P2 |
| 2.1.4 | Mobile sidebar toggle | The sidebar is `d-none d-md-block` -- add a hamburger menu toggle for mobile using Bootstrap offcanvas or collapse. | Not Started | P2 |
| 2.2.1 | Dashboard chart containers | Add `<canvas>` elements to `dashboard.html` for: (a) compliance trend line chart, (b) issues by severity doughnut chart, (c) audits per month bar chart. Wire with Chart.js in `extra_js` block. | Not Started | P1 |
| 2.2.2 | Dashboard HTMX refresh | Add HTMX `hx-get` polling or manual refresh button on dashboard KPI cards so they update without full page reload. | Not Started | P2 |
| 2.2.3 | Dashboard period filter | Add date range or period selector to dashboard so users can filter KPIs to current month/quarter/year. Wire view to accept query params. | Not Started | P2 |
| 2.3.1 | Trolley list HTMX filtering | Convert trolley list filter form to use `hx-get` with `hx-target="#trolley-table"` so filtering does not cause full page reload. Create a partial template for the table body. | Not Started | P1 |
| 2.3.2 | Trolley detail compliance sparkline | On trolley detail page, add a small inline Chart.js sparkline showing compliance trend over last 12 audits. | Not Started | P2 |
| 2.4.1 | Audit wizard step indicator component | Extract the step indicator (Documents > Equipment > Condition > Checks > Review) into a reusable `_audit_steps.html` include. Dynamically highlight current and completed steps based on URL. | Not Started | P1 |
| 2.4.2 | Audit equipment HTMX save | Add inline HTMX save on the equipment checklist so each row auto-saves on change (or save-all button that does not navigate away). Add visual feedback (green flash on success). | Not Started | P2 |
| 2.4.3 | Audit review score preview styling | Style the review page compliance preview scores with color-coded progress bars and clear pass/fail indicators. | Not Started | P1 |
| 2.5.1 | Login page styling | Style `registration/login.html` with REdI branding: centered card, logo, gradient bar, hospital name. Currently unstyled. | Not Started | P0 |
| 2.5.2 | Password change view | Add password change URL pattern and template. Django's `auth.urls` include it but template needs to be created at `registration/password_change_form.html`. | Not Started | P1 |
| 2.5.3 | 403/404/500 error templates | Create custom error templates at `templates/403.html`, `templates/404.html`, `templates/500.html` with REdI branding. | Not Started | P2 |
| 2.6.1 | Pagination helper include | Extract pagination markup into `_pagination.html` partial. Currently duplicated across list templates. Include preserves query string params. | Not Started | P2 |
| 2.6.2 | Empty state illustrations | Add styled empty-state messages with icons for all list views when no data exists (trolleys, audits, issues, selections). | Not Started | P2 |

---

## Phase 3: Audit Workflow Hardening (P0)

The 5-step audit wizard views are implemented. This phase hardens validation, edge cases, and user experience.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 3.1.1 | Prevent duplicate in-progress audits | In `AuditStartView.post()`, check if an InProgress audit already exists for the same location. If so, redirect to it with a message instead of creating a new one. | Not Started | P0 |
| 3.1.2 | Audit type from context | When starting an audit from a random selection item, set `audit_type='Random'` and link `triggered_by_issue` if applicable. Currently always defaults to 'Monthly'. | Not Started | P1 |
| 3.1.3 | Mark selection item completed | After submitting an audit for a location that was in the active random selection, auto-update the `RandomAuditSelectionItem.audit_status` to 'Completed' and link the audit. | Not Started | P1 |
| 3.2.1 | Equipment bulk save with transaction | The equipment POST handler already uses `transaction.atomic()`. Verify it rolls back correctly on partial failure. Add a test for this. | Not Started | P1 |
| 3.2.2 | Equipment "select all present" button | Add a JavaScript "Mark All Present" toggle button on the equipment checklist to quickly check/uncheck all `is_present` checkboxes. | Not Started | P2 |
| 3.2.3 | Equipment category collapse | Make equipment categories collapsible (Bootstrap accordion or `<details>`) so long checklists are navigable. Show item count per category. | Not Started | P2 |
| 3.3.1 | Compliance score persistence | Verify `ComplianceScorer.calculate_overall_score()` correctly persists all 5 score fields on the Audit model. Ensure `update_fields` list is complete. | Not Started | P0 |
| 3.3.2 | Follow-up audit creation | When compliance < 80% triggers `requires_follow_up`, add a button on the audit detail page for educators to start a follow-up audit (type='FollowUp') linked to the original. | Not Started | P1 |
| 3.4.1 | Abandon audit action | Add ability for the auditor or an admin to abandon/cancel an InProgress audit. Set status to 'Draft' and optionally delete related records. | Not Started | P2 |
| 3.4.2 | Audit timeout warning | If an audit has been InProgress for > 24 hours, show a warning banner on the wizard pages. Consider auto-expiring stale audits via management command. | Not Started | P2 |

---

## Phase 4: Issue Management (P1)

Issue CRUD and workflow transitions are implemented. This phase adds corrective actions, UX polish, and SLA visibility.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 4.1.1 | Corrective action form | Create `CorrectiveActionForm` in `forms.py`. Add a "Record Action" form on the issue detail page that creates a `CorrectiveAction` record. | Not Started | P1 |
| 4.1.2 | Corrective action view | Create `CorrectiveActionCreateView` (POST handler) in `views.py`. Wire URL pattern `issues/<uuid:pk>/action/`. | Not Started | P1 |
| 4.1.3 | Corrective action display | Display corrective actions timeline on issue detail page with action type badges, dates, and success/failure indicators. | Not Started | P1 |
| 4.2.1 | Issue edit view | Create `IssueEditView` (UpdateView) so managers can edit issue title, description, severity, category after creation. Currently no edit capability exists. | Not Started | P1 |
| 4.2.2 | Issue assignment dropdown | Replace the free-text `assigned_to` field with a dropdown of users in the Auditor/Manager/Educator groups. Fall back to free text if no users. | Not Started | P2 |
| 4.3.1 | SLA countdown display | On issue detail and issue list, show a human-readable SLA countdown ("2d 5h remaining" or "Overdue by 3d"). Use template tag or filter. | Not Started | P1 |
| 4.3.2 | SLA badge on issue list | Add a visual SLA badge (green/amber/red) to each issue in the list view based on time remaining vs. SLA target. | Not Started | P1 |
| 4.4.1 | Issue transition confirmation | Add confirmation modals (or HTMX confirm) for destructive transitions: close, escalate, reopen. Prevent accidental clicks. | Not Started | P2 |
| 4.4.2 | Issue activity log | Display a combined timeline on issue detail showing both comments and status transitions in chronological order (currently shown separately). | Not Started | P2 |
| 4.5.1 | Bulk issue operations | On issue list, add checkboxes and a bulk action dropdown: "Close Selected", "Assign Selected To...". Manager-only. | Not Started | P2 |

---

## Phase 5: Random Selection & Scheduling (P1)

Random selection logic is implemented. This phase adds UI integration and scheduled execution.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 5.1.1 | Selection detail view | Create a detail view for a single `RandomAuditSelection` showing all items with their status, linked audits, and completion progress bar. | Not Started | P1 |
| 5.1.2 | Selection item actions | On the selection detail view, add buttons per item: "Start Audit" (links to AuditStartView), "Skip" (with reason form). Update `RandomAuditSelectionItem` status. | Not Started | P1 |
| 5.1.3 | Selection history pagination | Paginate past selections on the random selection page. Currently limited to last 10. | Not Started | P2 |
| 5.2.1 | Scheduled selection generation | Configure weekly auto-generation of random selections. Options: (a) cron calling `manage.py generate_weekly_selection`, (b) django-crontab, (c) APScheduler. Document chosen approach in deployment guide. | Not Started | P1 |
| 5.2.2 | Scheduled SLA check | Configure periodic SLA check execution. Run `manage.py check_sla` daily via cron or scheduler. Add email notification on breach. | Not Started | P1 |
| 5.2.3 | Docker cron container | Add a `cron` service to docker-compose that runs scheduled management commands. Use `supercronic` or `ofelia` for containerized cron. | Not Started | P1 |
| 5.3.1 | Selection notification email | After generating a weekly selection, call `NotificationService.notify_weekly_selection()` to email educators. Verify this works end-to-end. | Not Started | P1 |
| 5.3.2 | Selection configurable count | Add a form field or settings entry to configure how many trolleys are selected per week (currently hardcoded to 10 in `RandomAuditSelector.DEFAULT_SELECTION_COUNT`). | Not Started | P2 |

---

## Phase 6: Reporting & Analytics (P1)

Basic reports and CSV export exist. This phase adds charts, Excel export, and richer analytics.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 6.1.1 | Compliance trend chart | On the reports page, add a line chart (Chart.js) showing average compliance per month over the last 12 months. Query audits grouped by month. | Not Started | P1 |
| 6.1.2 | Compliance by service line chart | Add a horizontal bar chart showing current average compliance per service line. Color bars by compliance threshold (green/amber/red). | Not Started | P1 |
| 6.1.3 | Issue severity breakdown chart | Add a doughnut/pie chart showing open issues by severity. | Not Started | P1 |
| 6.1.4 | Audit volume chart | Add a bar chart showing number of audits completed per month, optionally stacked by audit type (Monthly, Random, FollowUp, Spot). | Not Started | P2 |
| 6.2.1 | Chart data API endpoints | Create JSON API views (or use `JsonResponse`) to serve chart data. URL pattern: `reports/api/compliance-trend/`, `reports/api/issues-by-severity/`, etc. Consumed by Chart.js `fetch()`. | Not Started | P1 |
| 6.2.2 | Reports date range filter | Add date range picker (start/end) to the reports page. Filter all charts and tables by selected period. Pass as query params to API endpoints. | Not Started | P2 |
| 6.3.1 | Excel export with openpyxl | Add `openpyxl` to requirements. Add Excel export option alongside CSV on the export view. Format headers, auto-column-widths, and sheet names. | Not Started | P1 |
| 6.3.2 | Export date range filter | Allow export view to accept `start_date` and `end_date` query params to limit exported data to a period. | Not Started | P2 |
| 6.3.3 | Export equipment detail | Add a new export type `equipment` that exports the full equipment checklist results for all audits (one row per AuditEquipment record). | Not Started | P2 |
| 6.4.1 | Print-friendly audit report | Add a print-specific template for audit detail (or print stylesheet) that renders a clean single-page audit report suitable for printing/PDF. | Not Started | P2 |
| 6.4.2 | Service line report page | Create a per-service-line report page showing all locations, their compliance history, and open issues. Linked from compliance report. | Not Started | P2 |

---

## Phase 7: Email & Notifications (P1)

Power Automate email backend is implemented. This phase adds SMTP fallback and notification configuration.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 7.1.1 | SMTP email backend fallback | Add Django SMTP backend configuration to settings. When `EMAIL_API_ENDPOINT` is empty, fall back to `django.core.mail.backends.smtp.EmailBackend`. Add `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` to settings/env. | Not Started | P1 |
| 7.1.2 | Abstract email service interface | Refactor `NotificationService` to use Django's `send_mail()` as default and Power Automate as optional backend. Make the notification service backend-agnostic. | Not Started | P1 |
| 7.1.3 | Console email backend for dev | Set `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` when `DEBUG=True` so dev emails print to stdout instead of trying to send. | Not Started | P0 |
| 7.2.1 | Email template system | Create HTML email templates (in `templates/email/`) instead of inline HTML strings in `notifications.py`. Use Django's `render_to_string()`. | Not Started | P2 |
| 7.2.2 | Notification preferences | Add a user preference model or settings to allow users to opt out of non-critical email notifications. | Not Started | P3 |

---

## Phase 8: Testing (P2)

No tests exist. This phase builds a comprehensive test suite.

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 8.1.1 | Test directory structure | Create `backend/audit/tests/` package with `__init__.py`, `test_models.py`, `test_services.py`, `test_views.py`, `test_forms.py`, `test_commands.py`, `conftest.py` (or `factories.py`). | Not Started | P0 |
| 8.1.2 | Test factories / fixtures | Create model factories using `factory_boy` (add to requirements) or Django fixtures for: ServiceLine, EquipmentCategory, Equipment, Location, AuditPeriod, User (with role groups). | Not Started | P0 |
| 8.2.1 | Model tests -- core entities | Test ServiceLine, EquipmentCategory, Equipment model creation, str methods, constraints, and properties. | Not Started | P1 |
| 8.2.2 | Model tests -- Location | Test Location creation, `days_since_last_audit`, `audit_priority_score`, `get_absolute_url`, status choices. | Not Started | P1 |
| 8.2.3 | Model tests -- Audit hierarchy | Test Audit creation with related AuditDocuments, AuditCondition, AuditChecks, AuditEquipment. Test cascading deletes. | Not Started | P1 |
| 8.2.4 | Model tests -- Issue numbering | Test `Issue.save()` auto-numbering: sequential generation, retry on conflict, prefix format. | Not Started | P1 |
| 8.3.1 | Service tests -- ComplianceScorer | Test all 4 component scores and overall score calculation. Test edge cases: zero equipment, all missing, all present, mixed critical/non-critical. | Not Started | P0 |
| 8.3.2 | Service tests -- IssueWorkflow | Test all 7 state transitions, invalid transitions (expect `InvalidTransitionError`), SLA calculation, auto-escalation logic, max escalation level. | Not Started | P0 |
| 8.3.3 | Service tests -- RandomAuditSelector | Test priority scoring, service line distribution, selection count, deactivation of previous selections. | Not Started | P1 |
| 8.3.4 | Service tests -- NotificationService | Mock email backend and test all 5 notification methods fire correctly with expected data. Test graceful failure when backend is unconfigured. | Not Started | P1 |
| 8.4.1 | View tests -- authentication | Test that all views return 302 redirect to login for anonymous users. Test that role-restricted views return 403 for insufficient roles. | Not Started | P0 |
| 8.4.2 | View tests -- DashboardView | Test dashboard renders with context data, handles zero data gracefully. | Not Started | P1 |
| 8.4.3 | View tests -- TrolleyListView | Test filtering by service line, status, building, search. Test pagination. | Not Started | P1 |
| 8.4.4 | View tests -- AuditStartView | Test audit creation, related record creation, equipment filtering by trolley config (defib type, paediatric, altered airway). | Not Started | P0 |
| 8.4.5 | View tests -- Audit wizard flow | Test full wizard flow: documents -> equipment -> condition -> checks -> review -> submit. Verify compliance scores are saved and location is updated. | Not Started | P0 |
| 8.4.6 | View tests -- AuditOwnershipMixin | Test that non-owner users get 403. Test that submitted audits cannot be modified. | Not Started | P1 |
| 8.4.7 | View tests -- IssueCreateView | Test issue creation, auto-numbering, SLA target date assignment. | Not Started | P1 |
| 8.4.8 | View tests -- IssueTransitionView | Test all transition actions (assign, start, submit_verification, verify, reject, close, reopen, escalate). Test invalid transitions return error message. | Not Started | P1 |
| 8.4.9 | View tests -- ExportView | Test CSV export for all 3 types (audits, issues, locations). Verify headers and row content. Test invalid export type returns 400. | Not Started | P1 |
| 8.5.1 | Form tests | Test all 8 forms: valid submission, required field validation, widget classes. | Not Started | P2 |
| 8.5.2 | Command tests -- seed_data | Test `seed_data` command: successful load, --flush option, missing file error, duplicate handling (get_or_create). | Not Started | P2 |
| 8.5.3 | Command tests -- setup_roles | Test that 5 groups are created with correct names. Test idempotency. | Not Started | P2 |
| 8.5.4 | Command tests -- check_sla | Test SLA breach detection and auto-escalation. | Not Started | P2 |
| 8.6.1 | Coverage configuration | Add `coverage` to requirements. Configure `.coveragerc` to measure `audit/` excluding migrations. Target 80% coverage. | Not Started | P1 |
| 8.6.2 | Coverage CI integration | Add `coverage run manage.py test && coverage report --fail-under=80` to CI pipeline. | Not Started | P1 |
| 8.7.1 | E2E test setup (Playwright) | Set up Playwright Python: add `playwright` to dev requirements, create `tests/e2e/` directory, configure `playwright.yml` workflow. | Not Started | P2 |
| 8.7.2 | E2E test -- login flow | Test login with valid credentials, redirect to dashboard. Test login with invalid credentials shows error. | Not Started | P2 |
| 8.7.3 | E2E test -- full audit flow | Test complete audit wizard: login -> select trolley -> start audit -> fill all 4 sections -> review -> submit -> verify completion. | Not Started | P2 |
| 8.7.4 | E2E test -- issue lifecycle | Test issue creation from audit, assignment, resolution, and closure flow. | Not Started | P2 |

---

## Phase 9: Security Hardening (P2)

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 9.1.1 | CSRF protection audit | Verify all POST forms include `{% csrf_token %}`. Verify AJAX/HTMX requests include CSRF header. | Not Started | P0 |
| 9.1.2 | Security headers middleware | Add `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS = 'DENY'`, `SECURE_REFERRER_POLICY` to production settings. | Not Started | P1 |
| 9.1.3 | Rate limiting | Add `django-ratelimit` or `django-axes` for login attempt throttling. Configure lockout after 5 failed attempts. | Not Started | P2 |
| 9.2.1 | Secret key generation | Ensure `DJANGO_SECRET_KEY` is generated uniquely per deployment. Add key generation helper to docs/Makefile. Never fall back to hardcoded key in production. | Not Started | P0 |
| 9.2.2 | Debug mode safety | Add a startup check that refuses to run with `DEBUG=True` when `DJANGO_ALLOWED_HOSTS` contains non-localhost values. | Not Started | P1 |
| 9.3.1 | Session security | Review session settings: `SESSION_COOKIE_HTTPONLY=True` (add explicitly), `SESSION_COOKIE_SAMESITE='Lax'`. Verify 8-hour timeout is appropriate. | Not Started | P1 |
| 9.3.2 | HTTPS enforcement in prod | Add `SECURE_SSL_REDIRECT = True`, `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS` to production settings (behind nginx, so may need PROXY header config). | Not Started | P1 |

---

## Phase 10: Deployment & Documentation (P2)

| ID | Task | Description | Status | Priority |
|----|------|-------------|--------|----------|
| 10.1.1 | nginx configuration | Create `docker/nginx.conf` (for host-level reference): upstream to port 11000, static file serving, SSL termination, proxy headers. | Not Started | P1 |
| 10.1.2 | Backup strategy | Document PostgreSQL backup approach: `pg_dump` cron script, volume backup, retention policy. Create `docker/backup.sh`. | Not Started | P1 |
| 10.1.3 | Log configuration | Configure Django logging in settings: file handler for production (or stdout for Docker), structured JSON format, separate audit trail log. | Not Started | P1 |
| 10.1.4 | Health check endpoint | Create `/health/` endpoint that returns 200 OK with DB connectivity check. Useful for Docker health checks and monitoring. | Not Started | P1 |
| 10.2.1 | Deployment guide | Create `docs/DEPLOYMENT.md`: prerequisites, Docker installation, environment setup, first-run steps, seed data loading, user creation, nginx configuration, SSL, backup setup. | Not Started | P1 |
| 10.2.2 | Development setup guide | Create `docs/DEVELOPMENT.md`: local setup without Docker, Docker dev setup, running tests, code style, branch workflow. | Not Started | P1 |
| 10.2.3 | User guide | Create `docs/USER_GUIDE.md`: role descriptions, login, dashboard overview, conducting an audit (step by step), managing issues, viewing reports, random selection process. | Not Started | P2 |
| 10.2.4 | Architecture overview | Create `docs/ARCHITECTURE.md`: system diagram, model relationships (ER diagram description), service layer design, compliance scoring formula, issue workflow state machine. | Not Started | P2 |
| 10.3.1 | Admin user creation command | Create `management/commands/create_admin.py` that creates a superuser with a prompted password and assigns to 'System Admin' group. For first-run setup. | Not Started | P1 |
| 10.3.2 | Data migration plan | Document migration path from any existing SharePoint/Excel data into the system via seed_data or admin import. | Not Started | P2 |

---

## Dependency Graph

Tasks should generally be completed in this order. Items within a phase can be parallelized.

```
Phase 1 (Infrastructure)
  |
  +---> Phase 2 (Templates/UX)
  |       |
  |       +---> Phase 3 (Audit Hardening)
  |       |       |
  |       |       +---> Phase 5 (Selection/Scheduling)
  |       |
  |       +---> Phase 4 (Issue Management)
  |       |
  |       +---> Phase 6 (Reporting)
  |
  +---> Phase 7 (Email) -- can run parallel with Phase 2
  |
  +---> Phase 8 (Testing) -- start after Phase 2; grows with each phase
  |
  +---> Phase 9 (Security) -- can run parallel after Phase 1
  |
  +---> Phase 10 (Deployment/Docs) -- after Phase 1; grows throughout
```

---

## Priority Legend

| Priority | Meaning | Timeline |
|----------|---------|----------|
| **P0** | Blocker -- must be done for the system to be usable | Week 1-2 |
| **P1** | Important -- needed for production readiness | Week 2-4 |
| **P2** | Nice to have -- improves UX and maintainability | Week 4-6 |
| **P3** | Future -- aspirational enhancements | Backlog |

---

## Quick Stats

| Metric | Count |
|--------|-------|
| Total tasks | 121 |
| P0 (blocker) | 26 |
| P1 (important) | 55 |
| P2 (nice to have) | 39 |
| P3 (future) | 1 |
| Phases | 10 |
