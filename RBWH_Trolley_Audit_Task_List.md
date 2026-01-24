# RBWH Resuscitation Trolley Audit System
## Build Task List

**Version:** 1.0  
**Date:** January 2026  
**Methodology:** Ralph Principle (atomic tasks - no "and" in scope description)

---

## Task List Overview

| Phase | Task Count | Estimated Duration |
|-------|------------|-------------------|
| Phase 1: Foundation | 47 tasks | Weeks 1-4 |
| Phase 2: Core Features | 58 tasks | Weeks 5-8 |
| Phase 3: Reporting | 32 tasks | Weeks 9-12 |
| Phase 4: Enhancement | 28 tasks | Weeks 13-16 |
| **Total** | **165 tasks** | **16 weeks** |

---

## Phase 1: Foundation (Weeks 1-4)

### 1.1 SharePoint Site Setup

| ID | Task | Description | Dependency | Est. Hours | Status |
|----|------|-------------|------------|------------|--------|
| 1.1.1 | Create SharePoint site | Provision new SharePoint site named "RBWH Trolley Audit" | None | 1 | Not Started |
| 1.1.2 | Configure site permissions | Set up Owners, Members, Visitors groups with appropriate access | 1.1.1 | 2 | Not Started |
| 1.1.3 | Create site navigation | Build navigation menu structure for lists | 1.1.1 | 1 | Not Started |
| 1.1.4 | Configure site branding | Apply RBWH branding elements to site | 1.1.1 | 1 | Not Started |

### 1.2 Reference Data Lists

| ID | Task | Description | Dependency | Est. Hours | Status |
|----|------|-------------|------------|------------|--------|
| 1.2.1 | Create ServiceLine list | Build SharePoint list with all ServiceLine columns | 1.1.1 | 1 | ✅ Complete |
| 1.2.2 | Configure ServiceLine validation | Add column validation rules for ServiceLine | 1.2.1 | 0.5 | ✅ Complete |
| 1.2.3 | Import ServiceLine seed data | Populate ServiceLine list with 7 service lines | 1.2.2 | 0.5 | ✅ Complete |
| 1.2.4 | Create EquipmentCategory list | Build SharePoint list with all EquipmentCategory columns | 1.1.1 | 1 | ✅ Complete |
| 1.2.5 | Configure EquipmentCategory validation | Add column validation rules for EquipmentCategory | 1.2.4 | 0.5 | ✅ Complete |
| 1.2.6 | Import EquipmentCategory seed data | Populate EquipmentCategory list with 8 categories | 1.2.5 | 0.5 | ✅ Complete |
| 1.2.7 | Create AuditPeriod list | Build SharePoint list with all AuditPeriod columns | 1.1.1 | 1 | ✅ Complete |
| 1.2.8 | Configure AuditPeriod validation | Add column validation rules for AuditPeriod | 1.2.7 | 0.5 | ✅ Complete |
| 1.2.9 | Create initial AuditPeriod record | Add current audit period configuration | 1.2.8 | 0.5 | ✅ Complete |

### 1.3 Equipment Master List

| ID | Task | Description | Dependency | Est. Hours | Status |
|----|------|-------------|------------|------------|--------|
| 1.3.1 | Create Equipment list schema | Build SharePoint list with all Equipment columns | 1.2.6 | 2 | ✅ Complete |
| 1.3.2 | Configure Equipment lookup to Category | Set up lookup column to EquipmentCategory | 1.3.1 | 0.5 | ✅ Complete |
| 1.3.3 | Add Equipment validation rules | Configure required fields validation | 1.3.2 | 1 | ✅ Complete |
| 1.3.4 | Add Equipment calculated columns | Create computed columns for display | 1.3.3 | 1 | ✅ Complete |
| 1.3.5 | Import Top of Trolley equipment | Populate equipment items for Top of Trolley category | 1.3.4 | 1 | ✅ Complete |
| 1.3.6 | Import Drawer 1 equipment | Populate equipment items for Drawer 1 category | 1.3.4 | 1 | ✅ Complete |
| 1.3.7 | Import Drawer 2 equipment | Populate equipment items for Drawer 2 category | 1.3.4 | 0.5 | ✅ Complete |
| 1.3.8 | Import Drawer 3 equipment | Populate equipment items for Drawer 3 category | 1.3.4 | 1 | ✅ Complete |
| 1.3.9 | Import Drawer 4 equipment | Populate equipment items for Drawer 4 category | 1.3.4 | 0.5 | ✅ Complete |
| 1.3.10 | Import Side of Trolley equipment | Populate equipment items for Side of Trolley category | 1.3.4 | 0.5 | ✅ Complete |
| 1.3.11 | Import Back of Trolley equipment | Populate equipment items for Back of Trolley category | 1.3.4 | 0.5 | ✅ Complete |
| 1.3.12 | Import Paediatric Box equipment | Populate equipment items for Paediatric Box category | 1.3.4 | 0.5 | ✅ Complete |
| 1.3.13 | Validate equipment import completeness | Verify all 89 equipment items imported correctly | 1.3.12 | 1 | ✅ Complete |

### 1.4 Location Master List

| ID | Task | Description | Dependency | Est. Hours | Status |
|----|------|-------------|------------|------------|--------|
| 1.4.1 | Create Location list schema | Build SharePoint list with all Location columns | 1.2.3 | 3 | ✅ Complete |
| 1.4.2 | Configure Location lookup to ServiceLine | Set up lookup column to ServiceLine | 1.4.1 | 0.5 | ✅ Complete |
| 1.4.3 | Add Location choice columns | Configure choice fields for TrolleyType, DefibrillatorType, OperatingHours, Status | 1.4.2 | 1 | ✅ Complete |
| 1.4.4 | Add Location validation rules | Configure required fields validation | 1.4.3 | 1 | ✅ Complete |
| 1.4.5 | Create Location calculated columns | Add DaysSinceLastAudit computed column | 1.4.4 | 2 | ✅ Complete |
| 1.4.6 | Import Location data from CSV | Populate Location list with 76 trolley locations | 1.4.5 | 2 | ✅ Complete |
| 1.4.7 | Validate Location import completeness | Verify all locations imported with correct service line mapping | 1.4.6 | 1 | ✅ Complete |
| 1.4.8 | Create LocationChangeLog list | Build SharePoint list for location audit trail | 1.4.1 | 1 | ✅ Complete |
| 1.4.9 | Configure LocationChangeLog columns | Set up all columns for change tracking | 1.4.8 | 1 | ✅ Complete |

### 1.5 Core Audit Lists

| ID | Task | Description | Dependency | Est. Hours | Status |
|----|------|-------------|------------|------------|--------|
| 1.5.1 | Create Audit list schema | Build SharePoint list with all Audit columns | 1.4.1 | 2 | ✅ Complete |
| 1.5.2 | Configure Audit lookup to Location | Set up lookup column to Location | 1.5.1 | 0.5 | ✅ Complete |
| 1.5.3 | Configure Audit lookup to AuditPeriod | Set up lookup column to AuditPeriod | 1.5.1 | 0.5 | ✅ Complete |
| 1.5.4 | Add Audit choice columns | Configure choice fields for AuditType, SubmissionStatus | 1.5.3 | 1 | ✅ Complete |
| 1.5.5 | Add Audit validation rules | Configure required fields validation | 1.5.4 | 1 | ✅ Complete |
| 1.5.6 | Create AuditDocuments list | Build SharePoint list for documentation checks | 1.5.1 | 1 | ✅ Complete |
| 1.5.7 | Configure AuditDocuments lookup to Audit | Set up lookup column to parent Audit | 1.5.6 | 0.5 | ✅ Complete |
| 1.5.8 | Add AuditDocuments choice columns | Configure choice fields for status values | 1.5.7 | 1 | ✅ Complete |
| 1.5.9 | Create AuditCondition list | Build SharePoint list for condition checks | 1.5.1 | 1 | ✅ Complete |
| 1.5.10 | Configure AuditCondition lookup to Audit | Set up lookup column to parent Audit | 1.5.9 | 0.5 | ✅ Complete |
| 1.5.11 | Create AuditChecks list | Build SharePoint list for routine check counts | 1.5.1 | 1 | ✅ Complete |
| 1.5.12 | Configure AuditChecks lookup to Audit | Set up lookup column to parent Audit | 1.5.11 | 0.5 | ✅ Complete |

### 1.6 PowerApp Foundation

| ID | Task | Description | Dependency | Est. Hours | Status |
|----|------|-------------|------------|------------|--------|
| 1.6.1 | Create new Canvas PowerApp | Initialise new app with tablet/phone layout | 1.5.5 | 1 | Not Started |
| 1.6.2 | Configure app data connections | Connect app to all SharePoint lists | 1.6.1 | 2 | Not Started |
| 1.6.3 | Create app colour theme | Define colour variables matching RBWH branding | 1.6.2 | 1 | Not Started |
| 1.6.4 | Create app navigation component | Build reusable header with navigation menu | 1.6.3 | 3 | Not Started |
| 1.6.5 | Create Home screen layout | Build dashboard screen structure | 1.6.4 | 2 | Not Started |
| 1.6.6 | Add Home screen KPI placeholders | Create placeholder cards for KPI values | 1.6.5 | 2 | Not Started |

---

## Phase 2: Core Features (Weeks 5-8)

### 2.1 Trolley Management Screens

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.1.1 | Create Trolley List screen | Build screen showing all trolley locations | 1.6.4 | 3 |
| 2.1.2 | Add Trolley List filter by ServiceLine | Implement dropdown filter for service line | 2.1.1 | 1 |
| 2.1.3 | Add Trolley List filter by Building | Implement dropdown filter for building | 2.1.1 | 1 |
| 2.1.4 | Add Trolley List filter by Status | Implement dropdown filter for active/inactive | 2.1.1 | 1 |
| 2.1.5 | Add Trolley List search box | Implement text search for department name | 2.1.1 | 1 |
| 2.1.6 | Add Trolley List sort functionality | Enable column header sorting | 2.1.1 | 2 |
| 2.1.7 | Add Trolley List colour coding | Colour code rows by days since last audit | 2.1.1 | 2 |
| 2.1.8 | Create Trolley Detail screen | Build screen showing single trolley details | 2.1.1 | 3 |
| 2.1.9 | Add Trolley Detail view mode | Display all trolley attributes read-only | 2.1.8 | 2 |
| 2.1.10 | Add Trolley Detail edit mode | Enable editing of trolley attributes | 2.1.9 | 3 |
| 2.1.11 | Add Trolley Detail optional equipment toggles | Build toggle controls for HasPaediatricBox etc. | 2.1.10 | 2 |
| 2.1.12 | Create Add New Trolley screen | Build form for creating new trolley location | 2.1.10 | 3 |
| 2.1.13 | Add form validation for new trolley | Implement required field validation | 2.1.12 | 2 |
| 2.1.14 | Add duplicate department name check | Validate uniqueness before save | 2.1.13 | 1 |
| 2.1.15 | Create Deactivate Trolley dialog | Build confirmation dialog with reason field | 2.1.10 | 2 |
| 2.1.16 | Create Reactivate Trolley dialog | Build confirmation dialog for reactivation | 2.1.10 | 1 |
| 2.1.17 | Create Trolley History tab | Build tab showing all audits for trolley | 2.1.8 | 3 |
| 2.1.18 | Add Trolley History compliance trend chart | Display compliance scores over time | 2.1.17 | 3 |

### 2.2 Trolley Management Flows

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.2.1 | Create Save New Trolley flow | Build Power Automate flow to create Location record | 2.1.14 | 2 |
| 2.2.2 | Create Log New Trolley change flow | Log creation to LocationChangeLog | 2.2.1 | 1 |
| 2.2.3 | Create Update Trolley flow | Build Power Automate flow to update Location record | 2.1.10 | 2 |
| 2.2.4 | Create Log Trolley Update flow | Log modification to LocationChangeLog | 2.2.3 | 2 |
| 2.2.5 | Create Deactivate Trolley flow | Update status to Inactive with reason | 2.1.15 | 2 |
| 2.2.6 | Create Log Deactivation flow | Log status change to LocationChangeLog | 2.2.5 | 1 |
| 2.2.7 | Create Reactivate Trolley flow | Update status to Active | 2.1.16 | 1 |
| 2.2.8 | Create Log Reactivation flow | Log status change to LocationChangeLog | 2.2.7 | 1 |

### 2.3 Audit Entry Screens

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.3.1 | Create Audit Selection screen | Build screen to select trolley for audit | 1.6.4 | 2 |
| 2.3.2 | Add trolley dropdown with search | Implement searchable dropdown for location selection | 2.3.1 | 2 |
| 2.3.3 | Display last audit info on selection | Show last audit date when trolley selected | 2.3.2 | 1 |
| 2.3.4 | Add audit type selection | Radio buttons for Comprehensive vs Spot Check | 2.3.3 | 1 |
| 2.3.5 | Create Documentation Check screen | Build screen for documentation questions | 2.3.4 | 3 |
| 2.3.6 | Add Check Record status radio group | Three-option radio for Current/Old/None | 2.3.5 | 1 |
| 2.3.7 | Add Guidelines status radio group | Three-option radio for Current/Old/None | 2.3.5 | 1 |
| 2.3.8 | Add BLS Poster toggle | Yes/No toggle for poster presence | 2.3.5 | 0.5 |
| 2.3.9 | Add Equipment List status radio group | Three-option radio for Current/Old/None | 2.3.5 | 1 |
| 2.3.10 | Create Condition Check screen | Build screen for trolley condition questions | 2.3.9 | 3 |
| 2.3.11 | Add cleanliness toggle | Yes/No toggle for clean status | 2.3.10 | 0.5 |
| 2.3.12 | Add working order toggle | Yes/No toggle for working order | 2.3.10 | 0.5 |
| 2.3.13 | Add issue description field | Conditional text field when not working | 2.3.12 | 1 |
| 2.3.14 | Add rubber bands toggle | Yes/No toggle for rubber bands | 2.3.10 | 0.5 |
| 2.3.15 | Add O2 tubing toggle | Yes/No toggle for correct tubing | 2.3.10 | 0.5 |
| 2.3.16 | Add INHALO cylinder toggle | Yes/No toggle for cylinder pressure | 2.3.10 | 0.5 |
| 2.3.17 | Create Routine Checks screen | Build screen for check count entry | 2.3.16 | 2 |
| 2.3.18 | Add outside check count field | Numeric input for daily checks | 2.3.17 | 1 |
| 2.3.19 | Add inside check count field | Numeric input for weekly checks | 2.3.17 | 1 |
| 2.3.20 | Add not available toggle | Toggle when counts unavailable | 2.3.19 | 1 |
| 2.3.21 | Add not available reason field | Conditional text field for reason | 2.3.20 | 1 |
| 2.3.22 | Display expected check counts | Show calculated expected values | 2.3.21 | 2 |

### 2.4 Equipment Checklist

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.4.1 | Create AuditEquipment list | Build SharePoint list for equipment check results | 1.3.13 | 2 |
| 2.4.2 | Configure AuditEquipment lookups | Set up lookups to Audit, Equipment | 2.4.1 | 1 |
| 2.4.3 | Create Equipment Check screen | Build screen for equipment checklist | 2.3.22 | 4 |
| 2.4.4 | Build category accordion component | Create expandable sections by category | 2.4.3 | 4 |
| 2.4.5 | Build equipment item row component | Create reusable row with quantity input | 2.4.4 | 3 |
| 2.4.6 | Filter equipment by trolley config | Show only applicable items based on toggles | 2.4.5 | 3 |
| 2.4.7 | Filter equipment by defibrillator type | Show correct defib pads based on type | 2.4.6 | 2 |
| 2.4.8 | Add quantity found input | Numeric input defaulting to expected | 2.4.7 | 2 |
| 2.4.9 | Add item notes field | Optional text field per item | 2.4.8 | 1 |
| 2.4.10 | Calculate equipment subscore | Real-time calculation of items OK vs total | 2.4.9 | 2 |
| 2.4.11 | Display equipment subscore | Show percentage on screen | 2.4.10 | 1 |
| 2.4.12 | Highlight short items | Visual indicator for quantity below expected | 2.4.11 | 2 |
| 2.4.13 | Highlight critical missing items | Prominent warning for critical equipment | 2.4.12 | 2 |

### 2.5 Audit Submission

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.5.1 | Create Review screen | Build screen showing audit summary | 2.4.13 | 3 |
| 2.5.2 | Display all responses summary | Show all answers across sections | 2.5.1 | 3 |
| 2.5.3 | Calculate overall compliance score | Implement weighted scoring formula | 2.5.2 | 4 |
| 2.5.4 | Display compliance score breakdown | Show subscores by category | 2.5.3 | 2 |
| 2.5.5 | Add edit buttons per section | Allow return to previous screens | 2.5.4 | 2 |
| 2.5.6 | Add submit button | Final submission control | 2.5.5 | 1 |
| 2.5.7 | Add save draft button | Save incomplete audit | 2.5.6 | 1 |
| 2.5.8 | Create Submit Audit flow | Build Power Automate flow for submission | 2.5.6 | 4 |
| 2.5.9 | Save Audit record | Create main audit record | 2.5.8 | 1 |
| 2.5.10 | Save AuditDocuments record | Create documentation child record | 2.5.9 | 1 |
| 2.5.11 | Save AuditCondition record | Create condition child record | 2.5.9 | 1 |
| 2.5.12 | Save AuditChecks record | Create routine checks child record | 2.5.9 | 1 |
| 2.5.13 | Save AuditEquipment records | Create equipment check records | 2.5.9 | 2 |
| 2.5.14 | Update Location last audit fields | Set LastAuditDate, LastAuditCompliance | 2.5.13 | 2 |
| 2.5.15 | Create Save Draft flow | Save incomplete audit as draft | 2.5.7 | 3 |

### 2.6 Issue Management Lists

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.6.1 | Create Issue list schema | Build SharePoint list with all Issue columns | 1.4.1 | 3 |
| 2.6.2 | Configure Issue lookup to Location | Set up lookup column to Location | 2.6.1 | 0.5 |
| 2.6.3 | Configure Issue lookup to Audit | Set up lookup column to Audit | 2.6.1 | 0.5 |
| 2.6.4 | Configure Issue lookup to Equipment | Set up optional lookup to Equipment | 2.6.1 | 0.5 |
| 2.6.5 | Add Issue choice columns | Configure choices for Category, Severity, Status | 2.6.4 | 2 |
| 2.6.6 | Add Issue number auto-generation | Configure calculated column for ISS-YYYY-NNNN | 2.6.5 | 2 |
| 2.6.7 | Create CorrectiveAction list | Build SharePoint list for actions | 2.6.1 | 2 |
| 2.6.8 | Configure CorrectiveAction lookup to Issue | Set up lookup column to parent Issue | 2.6.7 | 0.5 |
| 2.6.9 | Add CorrectiveAction choice columns | Configure choices for ActionType | 2.6.8 | 1 |
| 2.6.10 | Create IssueComment list | Build SharePoint list for comments | 2.6.1 | 1 |
| 2.6.11 | Configure IssueComment lookup to Issue | Set up lookup column to parent Issue | 2.6.10 | 0.5 |

### 2.7 Issue Management Screens

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.7.1 | Create Issue List screen | Build screen showing all issues | 2.6.6 | 3 |
| 2.7.2 | Add Issue List filter by Status | Implement multi-select filter for status | 2.7.1 | 1 |
| 2.7.3 | Add Issue List filter by Severity | Implement multi-select filter for severity | 2.7.1 | 1 |
| 2.7.4 | Add Issue List filter by Location | Implement dropdown filter for location | 2.7.1 | 1 |
| 2.7.5 | Add Issue List filter by Assigned To | Implement filter including "My Issues" | 2.7.1 | 2 |
| 2.7.6 | Add Issue List severity colour coding | Colour code rows by severity level | 2.7.1 | 1 |
| 2.7.7 | Add Issue List age column | Calculate days since reported | 2.7.1 | 1 |
| 2.7.8 | Create Issue Detail screen | Build screen showing single issue | 2.7.1 | 4 |
| 2.7.9 | Display issue header information | Show issue number, title, status, severity | 2.7.8 | 2 |
| 2.7.10 | Display issue description section | Show full description text | 2.7.9 | 1 |
| 2.7.11 | Display corrective actions list | Show all actions for issue | 2.7.10 | 3 |
| 2.7.12 | Display comments thread | Show all comments in chronological order | 2.7.11 | 2 |
| 2.7.13 | Create Add Issue screen | Build form for logging new issue | 2.7.8 | 3 |
| 2.7.14 | Add issue category dropdown | Dropdown for Equipment/Documentation/etc. | 2.7.13 | 1 |
| 2.7.15 | Add issue severity dropdown | Dropdown for Critical/High/Medium/Low | 2.7.13 | 1 |
| 2.7.16 | Add issue title field | Text input for brief description | 2.7.13 | 0.5 |
| 2.7.17 | Add issue description field | Multi-line text for details | 2.7.13 | 0.5 |
| 2.7.18 | Add equipment item dropdown | Optional dropdown for related equipment | 2.7.13 | 2 |
| 2.7.19 | Create Add Action dialog | Build dialog for adding corrective action | 2.7.11 | 3 |
| 2.7.20 | Create Add Comment dialog | Build dialog for adding comment | 2.7.12 | 2 |

### 2.8 Issue Workflow Flows

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.8.1 | Create Save New Issue flow | Build flow to create Issue record | 2.7.18 | 2 |
| 2.8.2 | Generate issue number in flow | Create sequential issue number | 2.8.1 | 2 |
| 2.8.3 | Create Assign Issue flow | Update AssignedTo, AssignedDate | 2.7.8 | 2 |
| 2.8.4 | Create Save Corrective Action flow | Create CorrectiveAction record | 2.7.19 | 2 |
| 2.8.5 | Update issue status on first action | Change status from Assigned to In_Progress | 2.8.4 | 1 |
| 2.8.6 | Create Save Comment flow | Create IssueComment record | 2.7.20 | 1 |
| 2.8.7 | Create Mark Resolved flow | Update status to Pending_Verification | 2.7.8 | 2 |
| 2.8.8 | Create Verify Resolution flow | Update status to Resolved | 2.7.8 | 2 |
| 2.8.9 | Create Close Issue flow | Update status to Closed | 2.7.8 | 1 |
| 2.8.10 | Create Reopen Issue flow | Update status to In_Progress, increment ReopenCount | 2.7.8 | 2 |
| 2.8.11 | Create Escalate Issue flow | Update EscalationLevel, EscalatedTo | 2.7.8 | 2 |

### 2.9 Random Selection

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 2.9.1 | Create RandomAuditSelection list | Build SharePoint list for weekly selection header | 1.4.1 | 1 |
| 2.9.2 | Create RandomAuditSelectionItem list | Build SharePoint list for selected trolleys | 2.9.1 | 2 |
| 2.9.3 | Configure SelectionItem lookup to Selection | Set up lookup to parent selection | 2.9.2 | 0.5 |
| 2.9.4 | Configure SelectionItem lookup to Location | Set up lookup to selected location | 2.9.2 | 0.5 |
| 2.9.5 | Configure SelectionItem lookup to Audit | Set up lookup to completed audit | 2.9.2 | 0.5 |
| 2.9.6 | Create Random Selection Admin screen | Build screen for MERT to generate selection | 2.9.5 | 3 |
| 2.9.7 | Display current week selection | Show existing selection if present | 2.9.6 | 2 |
| 2.9.8 | Display selection progress | Show completed vs pending count | 2.9.7 | 1 |
| 2.9.9 | Add Generate New Selection button | Trigger generation flow | 2.9.8 | 1 |
| 2.9.10 | Create Generate Selection flow | Build Power Automate flow for algorithm | 2.9.9 | 6 |
| 2.9.11 | Calculate priority scores in flow | Implement scoring algorithm | 2.9.10 | 4 |
| 2.9.12 | Select top 10 trolleys in flow | Apply selection logic with distribution | 2.9.11 | 4 |
| 2.9.13 | Create selection records in flow | Save RandomAuditSelection header | 2.9.12 | 1 |
| 2.9.14 | Create selection item records in flow | Save 10 RandomAuditSelectionItem records | 2.9.13 | 2 |
| 2.9.15 | Create Scheduled Generation flow | Weekly trigger for auto-generation | 2.9.14 | 2 |
| 2.9.16 | Display This Week's Audits on Home | Show selection list on dashboard | 2.9.7 | 3 |
| 2.9.17 | Link selection to audit completion | Update SelectionItem when audit submitted | 2.5.14 | 2 |

---

## Phase 3: Reporting (Weeks 9-12)

### 3.1 Dashboard KPIs

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 3.1.1 | Calculate audit completion rate KPI | Count completed vs due audits | 2.5.14 | 2 |
| 3.1.2 | Display audit completion rate card | Show KPI on Home screen | 3.1.1 | 1 |
| 3.1.3 | Calculate open issues count KPI | Count issues where Status not Closed | 2.8.1 | 1 |
| 3.1.4 | Display open issues count card | Show KPI on Home screen | 3.1.3 | 1 |
| 3.1.5 | Calculate overdue audits KPI | Count trolleys past due date | 2.5.14 | 2 |
| 3.1.6 | Display overdue audits card | Show KPI on Home screen | 3.1.5 | 1 |
| 3.1.7 | Calculate average compliance KPI | Mean of recent compliance scores | 2.5.14 | 2 |
| 3.1.8 | Display average compliance card | Show KPI on Home screen | 3.1.7 | 1 |
| 3.1.9 | Add KPI drill-down navigation | Click KPI to see details | 3.1.8 | 3 |

### 3.2 Power BI Reports

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 3.2.1 | Create Power BI workspace | Set up workspace for audit reports | 1.1.1 | 1 |
| 3.2.2 | Connect Power BI to SharePoint lists | Configure data source connections | 3.2.1 | 2 |
| 3.2.3 | Create data model relationships | Define relationships between tables | 3.2.2 | 3 |
| 3.2.4 | Create compliance trend line chart | Monthly compliance over time | 3.2.3 | 3 |
| 3.2.5 | Create service line comparison bar chart | Compliance by service line | 3.2.3 | 2 |
| 3.2.6 | Create building comparison bar chart | Compliance by building | 3.2.3 | 2 |
| 3.2.7 | Create audit activity calendar heatmap | Audits completed by date | 3.2.3 | 4 |
| 3.2.8 | Create days since audit histogram | Distribution of audit recency | 3.2.3 | 3 |
| 3.2.9 | Create issues by category pie chart | Issue distribution by category | 3.2.3 | 2 |
| 3.2.10 | Create issues by severity pie chart | Issue distribution by severity | 3.2.3 | 2 |
| 3.2.11 | Create issue aging bar chart | Open issues by age bucket | 3.2.3 | 3 |
| 3.2.12 | Create equipment deficiency table | Most common missing items | 3.2.3 | 3 |
| 3.2.13 | Create trolley detail report page | Single trolley history view | 3.2.3 | 4 |
| 3.2.14 | Add report filters | Service line, date range, building slicers | 3.2.13 | 3 |
| 3.2.15 | Publish reports to workspace | Deploy reports for access | 3.2.14 | 1 |
| 3.2.16 | Embed Power BI in PowerApp | Add report component to app | 3.2.15 | 3 |

### 3.3 Historical Data Migration

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 3.3.1 | Analyse 2023 data structure | Map existing columns to new schema | 3.2.3 | 2 |
| 3.3.2 | Create 2023 data mapping document | Document field mappings | 3.3.1 | 2 |
| 3.3.3 | Build 2023 data transformation script | Power Query to transform data | 3.3.2 | 4 |
| 3.3.4 | Import 2023 audit records | Load historical audits | 3.3.3 | 2 |
| 3.3.5 | Validate 2023 import | Verify record counts match | 3.3.4 | 2 |
| 3.3.6 | Analyse 2024 data structure | Map existing columns to new schema | 3.3.5 | 2 |
| 3.3.7 | Create 2024 data mapping document | Document field mappings | 3.3.6 | 2 |
| 3.3.8 | Build 2024 data transformation script | Power Query to transform data | 3.3.7 | 4 |
| 3.3.9 | Import 2024 audit records | Load historical audits | 3.3.8 | 2 |
| 3.3.10 | Validate 2024 import | Verify record counts match | 3.3.9 | 2 |
| 3.3.11 | Update Location last audit dates | Set LastAuditDate from imported data | 3.3.10 | 2 |

---

## Phase 4: Enhancement (Weeks 13-16)

### 4.1 Notifications

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 4.1.1 | Create audit submission email template | Design email for audit confirmation | 2.5.8 | 2 |
| 4.1.2 | Add submission confirmation email to flow | Send email on audit submit | 4.1.1 | 1 |
| 4.1.3 | Create critical issue email template | Design email for critical issues | 2.8.1 | 2 |
| 4.1.4 | Add critical issue notification to flow | Send email when critical issue logged | 4.1.3 | 2 |
| 4.1.5 | Create issue assignment email template | Design email for newly assigned issues | 2.8.3 | 2 |
| 4.1.6 | Add assignment notification to flow | Send email when issue assigned | 4.1.5 | 1 |
| 4.1.7 | Create weekly selection email template | Design email for random selection list | 2.9.15 | 2 |
| 4.1.8 | Add selection notification to flow | Send email when selection generated | 4.1.7 | 1 |
| 4.1.9 | Create overdue audit reminder flow | Scheduled flow for overdue reminders | 3.1.5 | 3 |
| 4.1.10 | Create overdue issue escalation flow | Scheduled flow for issue escalation | 2.8.11 | 4 |

### 4.2 Advanced Features

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 4.2.1 | Enable PowerApp offline mode | Configure offline sync settings | 2.5.6 | 4 |
| 4.2.2 | Test offline data capture | Verify offline audit entry works | 4.2.1 | 2 |
| 4.2.3 | Create LocationEquipment list | Build SharePoint list for custom equipment | 1.3.13 | 2 |
| 4.2.4 | Build equipment customisation screen | Allow per-location equipment config | 4.2.3 | 4 |
| 4.2.5 | Update equipment checklist for custom items | Filter based on LocationEquipment | 4.2.4 | 3 |
| 4.2.6 | Create follow-up audit workflow | Link issue resolution to verification audit | 2.8.8 | 4 |
| 4.2.7 | Add photo attachment capability | Enable camera capture in audit | 2.4.13 | 4 |
| 4.2.8 | Store photos in SharePoint library | Configure document library for images | 4.2.7 | 2 |

### 4.3 Testing

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 4.3.1 | Create test plan document | Document test cases for all functions | 4.2.6 | 4 |
| 4.3.2 | Execute trolley management test cases | Test add/edit/deactivate functions | 4.3.1 | 4 |
| 4.3.3 | Execute audit entry test cases | Test full audit workflow | 4.3.1 | 4 |
| 4.3.4 | Execute issue management test cases | Test issue lifecycle | 4.3.1 | 4 |
| 4.3.5 | Execute random selection test cases | Test generation algorithm | 4.3.1 | 2 |
| 4.3.6 | Execute reporting test cases | Verify dashboard accuracy | 4.3.1 | 3 |
| 4.3.7 | Conduct user acceptance testing | Testing with MERT educators | 4.3.6 | 8 |
| 4.3.8 | Document defects found | Log issues from testing | 4.3.7 | 2 |
| 4.3.9 | Fix critical defects | Resolve blocking issues | 4.3.8 | 8 |
| 4.3.10 | Retest fixed defects | Verify defect resolution | 4.3.9 | 4 |

### 4.4 Deployment

| ID | Task | Description | Dependency | Est. Hours |
|----|------|-------------|------------|------------|
| 4.4.1 | Create user guide document | Write end-user documentation | 4.3.10 | 8 |
| 4.4.2 | Create admin guide document | Write administrator documentation | 4.3.10 | 4 |
| 4.4.3 | Record training video for auditors | Screen recording of audit process | 4.4.1 | 4 |
| 4.4.4 | Record training video for managers | Screen recording of issue management | 4.4.1 | 3 |
| 4.4.5 | Conduct auditor training session | Live training for audit staff | 4.4.3 | 4 |
| 4.4.6 | Conduct manager training session | Live training for NUM/managers | 4.4.4 | 3 |
| 4.4.7 | Configure production permissions | Set final permission levels | 4.4.6 | 2 |
| 4.4.8 | Go-live deployment | Release app to production users | 4.4.7 | 2 |

---

## Task Summary by Type

| Type | Count | Total Hours |
|------|-------|-------------|
| SharePoint List Creation | 18 | 32 |
| SharePoint Configuration | 24 | 26 |
| Data Import | 14 | 15 |
| PowerApp Screen | 28 | 92 |
| PowerApp Component | 16 | 42 |
| Power Automate Flow | 32 | 74 |
| Power BI Report | 16 | 40 |
| Testing | 10 | 43 |
| Documentation | 6 | 26 |
| **Total** | **165** | **390** |

---

## Critical Path

The following tasks are on the critical path:

```
1.1.1 → 1.2.1 → 1.4.1 → 1.5.1 → 1.6.1 → 2.3.1 → 2.4.3 → 2.5.1 → 2.5.8 → 2.9.10 → 3.2.3 → 4.3.7 → 4.4.8
  │                                                                                          │
  └── Site Setup                                                                    Go-Live ──┘
```

**Critical Path Duration:** Approximately 14 weeks with parallel work

---

## Risk Items

| Risk | Mitigation | Impact |
|------|------------|--------|
| SharePoint list column limits | Design efficient schema, use lookups | Medium |
| Power Automate flow complexity | Break into smaller child flows | Medium |
| Historical data quality issues | Extensive validation during migration | High |
| User adoption resistance | Early involvement, comprehensive training | High |
| Offline sync conflicts | Clear conflict resolution rules | Low |

---

## Approval

| Role | Name | Date |
|------|------|------|
| Project Sponsor | | |
| Technical Lead | | |
| MERT Educator | | |

---

*End of Task List*
