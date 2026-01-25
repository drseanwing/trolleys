# RBWH Resuscitation Trolley Audit System

A SharePoint/PowerApps solution for managing annual audits of resuscitation trolleys across the Royal Brisbane and Women's Hospital campus.

## Repository Structure

```
trolleys/
├── RBWH_Trolley_Audit_Task_List.md         # Master task list with 165 tasks
├── RBWH_Trolley_Audit_Program_Specification_v2 (1).md  # Program specification
├── RBWH_Resuscitation_Trolley_Audit_Schema.md          # Data schema specification
├── audit_erd_v2 (1).mermaid                # Entity relationship diagram
├── equipment_master_list.json              # Source equipment data
├── locations_master_cleaned.csv            # Source location data
├── sharepoint_schemas/                     # SharePoint list configurations
│   ├── ServiceLine.json                    # Service line reference data schema
│   ├── EquipmentCategory.json              # Equipment category schema
│   ├── AuditPeriod.json                    # Audit period configuration schema
│   ├── Equipment.json                      # Master equipment list schema
│   ├── Location.json                       # Trolley location master schema
│   ├── LocationChangeLog.json              # Location change audit trail schema
│   ├── Audit.json                          # Main audit record schema
│   ├── AuditDocuments.json                 # Documentation checks schema
│   ├── AuditCondition.json                 # Physical condition checks schema
│   ├── AuditChecks.json                    # Routine check counts schema
│   └── AuditEquipment.json                 # Equipment item checks schema
├── seed_data/                              # Import-ready data files
│   ├── ServiceLine.json                    # 7 service lines
│   ├── EquipmentCategory.json              # 8 equipment categories
│   ├── AuditPeriod.json                    # Initial audit period
│   ├── Equipment.json                      # 89 equipment items
│   └── Location.json                       # 76 trolley locations
└── implementation_guides/                  # Step-by-step implementation guides
    ├── phase1_1_sharepoint_site_setup.md   # SharePoint site setup guide
    └── phase1_6_powerapp_foundation.md     # PowerApp foundation guide
```

## Implementation Progress

### Phase 1: Foundation (Weeks 1-4)

| Section | Tasks | Completed | Status |
|---------|-------|-----------|--------|
| 1.1 SharePoint Site Setup | 4 | 0 | 📋 Guide Ready |
| 1.2 Reference Data Lists | 9 | 9 | ✅ Complete |
| 1.3 Equipment Master List | 13 | 13 | ✅ Complete |
| 1.4 Location Master List | 9 | 9 | ✅ Complete |
| 1.5 Core Audit Lists | 12 | 12 | ✅ Complete |
| 1.6 PowerApp Foundation | 6 | 0 | 📋 Guide Ready |

**Phase 1 Progress: 43/47 tasks (91%)**

**Implementation Guides Available:**
- Tasks 1.1.1-1.1.4: See `implementation_guides/phase1_1_sharepoint_site_setup.md`
- Tasks 1.6.1-1.6.6: See `implementation_guides/phase1_6_powerapp_foundation.md`

### Phases 2-4

All phases now have complete implementation guides ready. See the Implementation Guides section below for the full index of 18 guides covering all 165 tasks.

## SharePoint List Schemas

The `sharepoint_schemas/` directory contains JSON configuration files that define:

- **Column definitions** with types, validation rules, and default values
- **View configurations** for different use cases (filters, sorting, grouping)
- **Lookup relationships** between lists
- **Calculated columns** with SharePoint-compatible formulas

These schemas can be used with:
- SharePoint PnP PowerShell for automated provisioning
- Manual list creation as a reference
- Power Platform CLI for deployment

### Example: Creating a List with PnP PowerShell

```powershell
# Connect to SharePoint
Connect-PnPOnline -Url "https://yourtenant.sharepoint.com/sites/RBWHTrolleyAudit" -Interactive

# Read schema and create list
$schema = Get-Content "sharepoint_schemas/ServiceLine.json" | ConvertFrom-Json
New-PnPList -Title $schema.listName -Template GenericList

# Add columns based on schema
foreach ($col in $schema.columns) {
    # Add column based on type
    switch ($col.type) {
        "Text" { Add-PnPField -List $schema.listName -DisplayName $col.displayName ... }
        "Boolean" { Add-PnPField -List $schema.listName -DisplayName $col.displayName ... }
        # etc.
    }
}
```

## Seed Data

The `seed_data/` directory contains JSON files ready for import into SharePoint lists:

| File | Records | Description |
|------|---------|-------------|
| ServiceLine.json | 7 | RBWH service lines/directorates |
| EquipmentCategory.json | 8 | Trolley sections (Top, Drawers 1-4, etc.) |
| AuditPeriod.json | 1 | Initial January 2026 period |
| Equipment.json | 89 | All trolley equipment items |
| Location.json | 76 | All trolley locations across campus |

### Data Import Methods

1. **Power Automate**: Create a flow to read JSON and create SharePoint items
2. **PnP PowerShell**: Use `Add-PnPListItem` with JSON data
3. **Power Apps**: Import directly through canvas app data connections
4. **Manual**: Copy/paste into SharePoint list grid view

## Implementation Guides

Comprehensive step-by-step guides covering all 165 tasks across 4 phases. Each guide provides detailed instructions for manual implementation in SharePoint/PowerApps UI.

### Complete Guide Index

| Guide | Tasks Covered | Description |
|-------|---------------|-------------|
| **phase1_1_sharepoint_site_setup.md** | 1.1.1-1.1.4 | SharePoint site provisioning, permissions, navigation, branding |
| **phase1_6_powerapp_foundation.md** | 1.6.1-1.6.6 | Canvas app setup, data connections, theme, navigation, Home screen |
| **phase2_1_trolley_management_screens.md** | 2.1.1-2.1.18 | Trolley list, detail, add/edit screens with filters |
| **phase2_2_trolley_management_flows.md** | 2.2.1-2.2.8 | Power Automate flows for trolley CRUD operations |
| **phase2_3_audit_entry_screens.md** | 2.3.1-2.3.22 | Audit selection, documentation, condition, routine checks |
| **phase2_4_equipment_checklist.md** | 2.4.1-2.4.13 | Equipment checklist with scoring and validation |
| **phase2_5_audit_submission.md** | 2.5.1-2.5.15 | Review screen, compliance scoring, submission flows |
| **phase2_6_issue_management_lists.md** | 2.6.1-2.6.11 | Issue, CorrectiveAction, IssueComment list schemas |
| **phase2_7_issue_management_screens.md** | 2.7.1-2.7.20 | Issue list, detail, add screens with status workflow |
| **phase2_8_issue_workflow_flows.md** | 2.8.1-2.8.11 | Issue lifecycle flows: create, assign, resolve, escalate |
| **phase2_9_random_selection.md** | 2.9.1-2.9.17 | Weekly random audit selection algorithm and screens |
| **phase3_1_dashboard_kpis.md** | 3.1.1-3.1.9 | Dashboard KPI calculations and display |
| **phase3_2_power_bi_reports.md** | 3.2.1-3.2.16 | Power BI workspace, reports, embedding |
| **phase3_3_historical_data_migration.md** | 3.3.1-3.3.11 | 2023/2024 data migration scripts and validation |
| **phase4_1_notifications.md** | 4.1.1-4.1.10 | Email templates and notification flows |
| **phase4_2_advanced_features.md** | 4.2.1-4.2.8 | Offline mode, custom equipment, photo attachments |
| **phase4_3_testing.md** | 4.3.1-4.3.10 | Test plan, test cases, UAT, defect management |
| **phase4_4_deployment.md** | 4.4.1-4.4.8 | User guides, training, go-live checklist |

### Implementation Coverage Summary

- **Phase 1 (Foundation)**: 47 tasks - 2 guides covering site setup and app foundation
- **Phase 2 (Core Functionality)**: 106 tasks - 8 guides covering trolleys, audits, issues, workflows
- **Phase 3 (Reporting & Analytics)**: 36 tasks - 3 guides covering dashboards, Power BI, data migration
- **Phase 4 (Advanced Features & Launch)**: 36 tasks - 4 guides covering notifications, features, testing, deployment

**Total: 18 guides covering all 165 implementation tasks**

### Using the Guides

Each guide includes:
- Prerequisites and required permissions
- Detailed step-by-step instructions with UI navigation
- Configuration values ready to copy/paste
- Formula examples for calculated columns and Power Fx
- Validation checkpoints after each major section
- Troubleshooting tips for common issues
- Time estimates per task

## Next Steps

1. **Create SharePoint Site** (Task 1.1.1) - Follow `implementation_guides/phase1_1_sharepoint_site_setup.md`
2. **Provision Lists** - Use schemas to create SharePoint lists (Tasks 1.2-1.5 already complete)
3. **Import Seed Data** - Populate reference data lists (already complete)
4. **Begin PowerApp Development** (Phase 1.6) - Follow `implementation_guides/phase1_6_powerapp_foundation.md`

## Key Features

- **76 trolley locations** across RBWH campus
- **89 equipment items** with supplier and quantity tracking
- **7 service lines** for organizational grouping
- **Configurable audit periods** for compliance tracking
- **Equipment-level audit detail** replacing binary "all items stocked"
- **Calculated compliance scores** with weighted formulas
- **Location change audit trail** for governance

## Technical Notes

- All schemas use SharePoint-compatible column types
- Calculated column formulas use SharePoint syntax
- Lookup columns define cross-list relationships
- Views include filters for common scenarios

## Documentation

- `RBWH_Trolley_Audit_Program_Specification_v2 (1).md` - Full program specification
- `RBWH_Resuscitation_Trolley_Audit_Schema.md` - Data schema details
- `RBWH_Trolley_Audit_Task_List.md` - Complete task breakdown

---

*Version: 1.0 | January 2026*
