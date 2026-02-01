# REdI Trolley Audit System

## Project Overview
Standalone Django web application for managing resuscitation trolley audits at Royal Brisbane and Women's Hospital (RBWH). Replaces a legacy Microsoft Forms process with a structured audit workflow, compliance scoring, issue tracking, and reporting.

## Quick Reference
- **Framework**: Django 5.1 / Python 3.12+
- **Database**: PostgreSQL 16 (SQLite for local dev)
- **Frontend**: Django templates + Bootstrap 5.3 + HTMX
- **Deployment**: Docker (rootless, named volumes, port 11000)
- **CI/CD**: GitHub Actions

## Project Structure
```
trolleys/
├── backend/              # Django application
│   ├── redi/            # Django project (settings, urls, wsgi)
│   ├── audit/           # Main app (models, views, forms, services)
│   │   ├── models.py    # 17 database models
│   │   ├── views.py     # View classes
│   │   ├── forms.py     # Form classes
│   │   ├── services/    # Business logic (compliance, workflow, selection)
│   │   ├── management/  # Custom commands (seed_data, setup_roles, check_sla)
│   │   ├── mixins.py    # Role-based access control mixins
│   │   └── templates/   # Django templates
│   └── static/          # Static assets
├── seed_data/           # Reference data JSON files
├── docs/                # Documentation
│   ├── ARCHITECTURE.md  # System architecture
│   ├── TASKS.md         # Implementation task list
│   └── archive/         # Legacy SharePoint design docs
├── docker/              # Docker configuration
└── docker-compose.yml   # Container orchestration
```

## Key Commands
```bash
# Development
cd backend
python manage.py runserver
python manage.py migrate
python manage.py seed_data          # Load 76 locations, 89 equipment items
python manage.py setup_roles        # Create 5 permission groups
python manage.py check_sla          # Check issue SLA compliance
python manage.py generate_weekly_selection  # Generate random audit batch

# Docker
docker compose up -d                # Start all services
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_data
```

## Data Model (17 Entities)
- **Reference**: ServiceLine (7), EquipmentCategory (8), AuditPeriod
- **Master**: Equipment (89), Location (76), LocationEquipment
- **Audit**: Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment
- **Issues**: Issue (7-state workflow), CorrectiveAction, IssueComment
- **Selection**: RandomAuditSelection, RandomAuditSelectionItem
- **Trail**: LocationChangeLog

## Business Logic
- **Compliance Score**: Weighted average (Docs 25%, Equipment 40%, Condition 15%, Checks 20%)
- **Issue Workflow**: Open -> Assigned -> InProgress -> PendingVerification -> Resolved -> Closed (+ Escalated)
- **SLA**: Critical 24h, High 3d, Medium 7d, Low 14d
- **Random Selection**: ~10 trolleys/week, priority-weighted by days since last audit

## User Roles (5)
1. System Admin - full access
2. MERT Educator - manage trolleys, audits, issues
3. Service Line Manager - manage own service line
4. Auditor - create/submit audits, report issues
5. Viewer - read-only

## Infrastructure Constraints
- nginx is at HOST level (not in this stack)
- Docker runs ROOTLESS - use named volumes, unprivileged ports
- Port block: 11000-11010 (11000=web app)
- No bind mounts in production

## Conventions
- Django class-based views with role-based mixins
- Services layer for complex business logic (compliance, workflow, selection)
- Bootstrap 5.3 for UI with REdI branding (Navy #1B3A5F, Coral #E55B64, Teal #2B9E9E)
- HTMX for progressive enhancement
- All seed data in seed_data/ directory as JSON
