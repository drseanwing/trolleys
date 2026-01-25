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

Phases 2-4 tasks are pending. See `RBWH_Trolley_Audit_Task_List.md` for full details.

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

Detailed step-by-step guides are available for manual implementation tasks that must be performed in the SharePoint/PowerApps UI:

### Available Guides

1. **Phase 1.1: SharePoint Site Setup** (`implementation_guides/phase1_1_sharepoint_site_setup.md`)
   - Create SharePoint site with Communication template
   - Configure site permissions (Owners, Members, Visitors)
   - Set up site navigation structure
   - Apply RBWH branding and theme colors
   - Estimated time: 5 hours

2. **Phase 1.6: PowerApp Foundation** (`implementation_guides/phase1_6_powerapp_foundation.md`)
   - Create new Canvas PowerApp with tablet/phone layout
   - Configure data connections to all 11 SharePoint lists
   - Create RBWH color theme and reusable components
   - Build navigation header and Home screen
   - Add KPI placeholder cards
   - Estimated time: 11 hours

### Using the Guides

Each guide includes:
- Prerequisites and required permissions
- Detailed step-by-step instructions with screenshots descriptions
- Configuration values ready to copy/paste
- Validation checkpoints
- Troubleshooting tips

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
