# RBWH Resuscitation Trolley Audit System
## Program Specification Document

**Version:** 2.0  
**Date:** January 2026  
**Status:** Draft for Review  
**Author:** Medical Education & Simulation  

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | - | Initial schema and logic |
| 2.0 | Jan 2026 | - | Added: Random audit selection, historical tracking, trolley management, issue/corrective action workflow |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Requirements](#2-business-requirements)
3. [Functional Requirements](#3-functional-requirements)
4. [Data Schema](#4-data-schema)
5. [User Interface Specifications](#5-user-interface-specifications)
6. [Business Logic & Workflows](#6-business-logic--workflows)
7. [Reporting & Analytics](#7-reporting--analytics)
8. [Security & Permissions](#8-security--permissions)
9. [Integration Requirements](#9-integration-requirements)
10. [Implementation Plan](#10-implementation-plan)
11. [Appendices](#11-appendices)

---

## 1. Executive Summary

### 1.1 Purpose

This document specifies the requirements for a PowerApps/Power Automate solution to manage the annual audit process for resuscitation trolleys across the RBWH campus. The system will replace the current Microsoft Forms-based process with a comprehensive solution that provides:

- Standardised audit data collection with equipment-level tracking
- Random weekly audit selection based on historical audit dates
- Complete trolley lifecycle management (add/edit/deactivate)
- Issue logging with corrective action tracking through to resolution
- Historical trend analysis per trolley location
- Automated compliance scoring and notifications

### 1.2 Scope

**In Scope:**
- All RBWH campus resuscitation trolleys (~76 locations)
- Offsite satellite locations (dialysis units, cancer care)
- Standard adult trolleys and paediatric equipment boxes
- Annual comprehensive audits and random spot checks
- Issue management and corrective actions
- Historical data and trend reporting

**Out of Scope (Future Phases):**
- Integration with S/4HANA procurement
- Automated expiry date tracking with barcode scanning
- Staff training/competency integration with Moodle
- Real-time stock level monitoring

### 1.3 Key Stakeholders

| Role | Responsibilities |
|------|------------------|
| MERT Nurse Educators | System owners, audit oversight, reporting |
| Nurse Unit Managers | Ensure audits completed, action corrective items |
| Clinical Staff (Auditors) | Conduct trolley audits |
| Service Line Managers | Monitor compliance within service line |
| CELS / Pharmacy | Receive restocking notifications |

---

## 2. Business Requirements

### 2.1 Core Business Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| BR-01 | Track the last audit date for every trolley location | Must Have |
| BR-02 | Generate weekly list of 10 random trolleys for spot-check audits, prioritising those not audited in 6+ months | Must Have |
| BR-03 | Maintain complete audit history per trolley for trend analysis | Must Have |
| BR-04 | Allow authorised users to add, edit, and deactivate trolley locations | Must Have |
| BR-05 | Support configurable optional equipment checks (e.g., paediatric box) per trolley | Must Have |
| BR-06 | Log issues discovered during audits with severity classification | Must Have |
| BR-07 | Track corrective actions from identification through resolution | Must Have |
| BR-08 | Calculate compliance scores automatically | Must Have |
| BR-09 | Send notifications for overdue audits and open issues | Should Have |
| BR-10 | Provide dashboards for compliance monitoring | Should Have |
| BR-11 | Support offline audit capability for areas with poor connectivity | Could Have |
| BR-12 | Capture photographic evidence of issues | Could Have |

### 2.2 Business Rules

| ID | Rule |
|----|------|
| BRU-01 | All active trolleys must be audited at least once per calendar year (comprehensive audit) |
| BRU-02 | Trolleys not audited in 6+ months should be prioritised for random selection |
| BRU-03 | Critical issues (missing adrenaline, defib pads, BVM) must trigger immediate notification |
| BRU-04 | Issues must not remain open longer than 30 days without escalation |
| BRU-05 | Only MERT Educators can add/edit/deactivate trolley locations |
| BRU-06 | Deactivated trolleys are retained for historical reporting but excluded from active audit lists |
| BRU-07 | Compliance score below 80% triggers mandatory follow-up within 7 days |

---

## 3. Functional Requirements

### 3.1 Trolley Management (FR-100 Series)

| ID | Function | Description | User |
|----|----------|-------------|------|
| FR-101 | View Trolley List | Display all trolleys with filter/sort by service line, building, status, last audit date | All |
| FR-102 | Add New Trolley | Create new trolley location with all required attributes | MERT Educator |
| FR-103 | Edit Trolley | Modify trolley attributes including optional equipment toggles | MERT Educator |
| FR-104 | Deactivate Trolley | Soft-delete with reason and date; retain history | MERT Educator |
| FR-105 | Reactivate Trolley | Restore previously deactivated trolley | MERT Educator |
| FR-106 | View Trolley History | Display all audits, issues, and changes for a specific trolley | All |
| FR-107 | Configure Optional Equipment | Toggle paediatric box, specific defib type, other optional items | MERT Educator |
| FR-108 | Bulk Import Trolleys | Import trolley data from CSV/Excel | MERT Educator |

### 3.2 Audit Management (FR-200 Series)

| ID | Function | Description | User |
|----|----------|-------------|------|
| FR-201 | Generate Random Audit List | Create weekly list of 10 trolleys prioritised by days since last audit | System/MERT |
| FR-202 | View Audit Schedule | Display trolleys due for audit with priority indicators | All |
| FR-203 | Start New Audit | Begin audit for selected trolley; validate no duplicate in progress | Auditor |
| FR-204 | Complete Audit Checklist | Step through documentation, equipment, condition checks | Auditor |
| FR-205 | Save Draft Audit | Save incomplete audit for later completion | Auditor |
| FR-206 | Submit Audit | Finalise and lock audit; trigger compliance calculation | Auditor |
| FR-207 | View Audit Details | Display completed audit with all responses | All |
| FR-208 | Export Audit Report | Generate PDF/Excel of single audit or batch | MERT/Manager |
| FR-209 | Distinguish Audit Types | Tag audits as "Annual Comprehensive" or "Random Spot Check" | System |

### 3.3 Issue & Corrective Action Management (FR-300 Series)

| ID | Function | Description | User |
|----|----------|-------------|------|
| FR-301 | Log Issue | Create issue record from within audit; classify severity | Auditor |
| FR-302 | View Open Issues | List all open issues with filters by location, severity, age | All |
| FR-303 | Assign Issue | Assign issue to responsible person/role | MERT/Manager |
| FR-304 | Add Corrective Action | Record action taken with date, person, description | Assignee |
| FR-305 | Request Verification | Mark action complete; request verification | Assignee |
| FR-306 | Verify Resolution | Confirm issue resolved; close issue | MERT/Manager |
| FR-307 | Reopen Issue | Reopen issue if verification fails | MERT/Manager |
| FR-308 | Escalate Issue | Escalate overdue issues to next level | System/MERT |
| FR-309 | View Issue History | Display full timeline of issue including all actions | All |
| FR-310 | Link Issue to Follow-up Audit | Connect resolution verification to subsequent audit | System |

### 3.4 Reporting & Analytics (FR-400 Series)

| ID | Function | Description | User |
|----|----------|-------------|------|
| FR-401 | Compliance Dashboard | Real-time overview of audit status, scores, issues | All |
| FR-402 | Trolley Trend Report | Historical compliance trend for single trolley | All |
| FR-403 | Service Line Report | Aggregate compliance by service line | Manager |
| FR-404 | Overdue Audit Report | List trolleys past due for audit | MERT |
| FR-405 | Open Issues Report | Summary of open issues by age, severity, location | MERT |
| FR-406 | Equipment Deficiency Report | Most commonly missing/short items | MERT |
| FR-407 | Year-over-Year Comparison | Compare same period across multiple years | MERT |
| FR-408 | Export to Excel/PDF | Export any report | All |

---

## 4. Data Schema

### 4.1 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIPS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐        │
│  │ ServiceLine  │◄────────│   Location   │────────►│ AuditPeriod  │        │
│  └──────────────┘    1:M  └──────────────┘  M:1    └──────────────┘        │
│                                  │                                          │
│                                  │ 1:M                                      │
│                     ┌────────────┼────────────┐                             │
│                     │            │            │                             │
│                     ▼            ▼            ▼                             │
│              ┌──────────┐ ┌──────────┐ ┌──────────────┐                    │
│              │  Audit   │ │  Issue   │ │LocationChange│                    │
│              └──────────┘ └──────────┘ └──────────────┘                    │
│                    │            │                                           │
│          ┌─────────┼─────────┐  │ 1:M                                      │
│          │         │         │  ▼                                          │
│          ▼         ▼         ▼  ┌──────────────┐                           │
│   ┌──────────┐┌────────┐┌──────┐│CorrectiveAct │                           │
│   │AuditDocs ││AuditEq ││AuditC│└──────────────┘                           │
│   └──────────┘└────────┘└──────┘                                           │
│                    │                                                        │
│                    │ M:1                                                    │
│                    ▼                                                        │
│  ┌──────────────┐  ┌──────────────┐                                        │
│  │  Equipment   │◄─│EquipCategory │                                        │
│  └──────────────┘  └──────────────┘                                        │
│         │                                                                   │
│         │ M:M (via LocationEquipment)                                      │
│         ▼                                                                   │
│  ┌──────────────────┐                                                      │
│  │LocationEquipment │  (Optional equipment config per location)            │
│  └──────────────────┘                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Table Definitions

#### 4.2.1 ServiceLine (Reference Data)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ServiceLineId | GUID | PK | Unique identifier |
| Name | String(100) | Required, Unique | Full name |
| Abbreviation | String(10) | Required, Unique | Short code |
| ContactEmail | String(100) | Optional | Service line contact |
| IsActive | Boolean | Default: true | Soft delete flag |
| CreatedDate | DateTime | Auto | Record creation |
| ModifiedDate | DateTime | Auto | Last modification |

---

#### 4.2.2 Location (Master Trolley Register) - UPDATED

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| LocationId | GUID | PK | Unique identifier |
| ServiceLineId | GUID | FK, Required | Link to service line |
| DepartmentName | String(100) | Required, Unique | Official department name |
| DisplayName | String(50) | Required | Short display name for lists |
| Building | String(50) | Required | James Mayne, Ned Hanlon, etc. |
| Level | String(20) | Required | Ground, L3, Level 5, etc. |
| SpecificLocation | String(100) | Optional | Room/bay details |
| TrolleyType | Choice | Required | Standard / Emergency / Specialty |
| DefibrillatorType | Choice | Required | LIFEPAK_1000_AED / LIFEPAK_20_20e |
| OperatingHours | Choice | Required | 24_7 / Weekday_Business / Weekday_Extended |
| ExpectedDailyChecks | Integer | Computed | Based on operating hours |
| **HasPaediatricBox** | Boolean | Default: false | **Requires paediatric equipment** |
| **HasAlteredAirway** | Boolean | Default: false | **Requires altered airway equipment** |
| **HasSpecialtyMeds** | Boolean | Default: false | **Has department-specific medications** |
| **SpecialtyMedsNotes** | String(500) | Optional | **Details of specialty medications** |
| **LastAuditDate** | DateTime | Nullable | **Date of most recent completed audit** |
| **LastAuditId** | GUID | FK, Nullable | **Reference to most recent audit** |
| **LastAuditCompliance** | Decimal | Nullable | **Compliance score from last audit** |
| **DaysSinceLastAudit** | Integer | Computed | **Calculated from LastAuditDate** |
| **AuditPriorityScore** | Integer | Computed | **For random selection weighting** |
| Status | Choice | Required | Active / Inactive / Decommissioned |
| StatusChangeDate | DateTime | Nullable | When status last changed |
| StatusChangeReason | String(500) | Optional | Why status changed |
| StatusChangedBy | String(100) | Optional | Who changed status |
| Notes | String(500) | Optional | Special requirements |
| CreatedDate | DateTime | Auto | Record creation |
| CreatedBy | String(100) | Required | Who created |
| ModifiedDate | DateTime | Auto | Last modification |
| ModifiedBy | String(100) | Required | Who modified |

**Computed Fields:**
```
DaysSinceLastAudit = DATEDIFF(day, LastAuditDate, TODAY())
                    -- Returns NULL if LastAuditDate is NULL

AuditPriorityScore = CASE
    WHEN LastAuditDate IS NULL THEN 1000  -- Never audited = highest priority
    WHEN DaysSinceLastAudit > 365 THEN 500 + DaysSinceLastAudit
    WHEN DaysSinceLastAudit > 180 THEN 200 + DaysSinceLastAudit
    WHEN DaysSinceLastAudit > 90 THEN 100 + DaysSinceLastAudit
    ELSE DaysSinceLastAudit
END
```

---

#### 4.2.3 LocationEquipment (Optional Equipment Configuration) - NEW

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| LocationEquipmentId | GUID | PK | Unique identifier |
| LocationId | GUID | FK, Required | Link to location |
| EquipmentId | GUID | FK, Required | Link to equipment item |
| IsRequired | Boolean | Default: true | Must be present at this location |
| CustomQuantity | Integer | Optional | Override standard quantity |
| Notes | String(200) | Optional | Location-specific notes |
| CreatedDate | DateTime | Auto | Record creation |
| ModifiedDate | DateTime | Auto | Last modification |

*This table allows per-location customisation of the equipment checklist.*

---

#### 4.2.4 LocationChangeLog (Audit Trail) - NEW

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ChangeLogId | GUID | PK | Unique identifier |
| LocationId | GUID | FK, Required | Link to location |
| ChangeType | Choice | Required | Created / Modified / StatusChange / Deactivated / Reactivated |
| FieldChanged | String(50) | Optional | Which field changed |
| OldValue | String(500) | Optional | Previous value |
| NewValue | String(500) | Optional | New value |
| ChangeReason | String(500) | Optional | Why change was made |
| ChangedBy | String(100) | Required | Who made change |
| ChangedDate | DateTime | Auto | When change occurred |

---

#### 4.2.5 AuditPeriod (Reference Data)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| PeriodId | GUID | PK | Unique identifier |
| PeriodName | String(50) | Required | "March 2024", "Q1 2024" |
| PeriodType | Choice | Required | Monthly / Quarterly / Annual |
| Year | Integer | Required | Calendar year |
| Month | Integer | Optional | 1-12 for monthly |
| Quarter | Integer | Optional | 1-4 for quarterly |
| StartDate | Date | Required | Period start |
| EndDate | Date | Required | Period end |
| WorkingDays | Integer | Computed | Business days in period |
| TotalDays | Integer | Computed | Calendar days |
| AuditDeadline | Date | Required | Submission deadline |
| IsActive | Boolean | Default: false | Current audit period |
| CreatedBy | String(100) | Required | Admin who created |
| CreatedDate | DateTime | Auto | Record creation |

---

#### 4.2.6 Audit (Main Audit Record) - UPDATED

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AuditId | GUID | PK | Unique identifier |
| LocationId | GUID | FK, Required | Trolley being audited |
| PeriodId | GUID | FK, Optional | Audit period (for annual) |
| **AuditType** | Choice | Required | **Annual_Comprehensive / Random_Spot_Check / Follow_Up** |
| **TriggeredByIssueId** | GUID | FK, Optional | **If follow-up, which issue triggered it** |
| AuditorName | String(100) | Required | Person conducting audit |
| AuditorEmail | String(100) | Optional | Contact email |
| StartedDateTime | DateTime | Required | When audit began |
| CompletedDateTime | DateTime | Optional | When submitted |
| SubmissionStatus | Choice | Required | Draft / Submitted / Verified / Rejected |
| OverallCompliance | Decimal | Computed | Percentage score |
| DocumentScore | Decimal | Computed | Documentation subscore |
| EquipmentScore | Decimal | Computed | Equipment subscore |
| ConditionScore | Decimal | Computed | Condition subscore |
| CheckScore | Decimal | Computed | Routine checks subscore |
| RequiresFollowUp | Boolean | Computed | Based on issues found |
| FollowUpDueDate | Date | Computed | If follow-up required |
| FollowUpNotes | String(1000) | Optional | Actions required |
| VerifiedBy | String(100) | Optional | Reviewer name |
| VerifiedDateTime | DateTime | Optional | When reviewed |
| RejectionReason | String(500) | Optional | If rejected |
| CreatedDate | DateTime | Auto | Record creation |
| ModifiedDate | DateTime | Auto | Last modification |

---

#### 4.2.7 Issue (Issue Tracking) - NEW/EXPANDED

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| IssueId | GUID | PK | Unique identifier |
| LocationId | GUID | FK, Required | Trolley with issue |
| AuditId | GUID | FK, Optional | Audit where discovered (null if reported independently) |
| IssueNumber | String(20) | Auto, Unique | Human-readable ID (e.g., "ISS-2024-0001") |
| **IssueCategory** | Choice | Required | **Equipment / Documentation / Condition / Compliance / Other** |
| **Severity** | Choice | Required | **Critical / High / Medium / Low** |
| Title | String(200) | Required | Brief issue description |
| Description | String(2000) | Required | Detailed description |
| **EquipmentId** | GUID | FK, Optional | **Specific equipment item if applicable** |
| **ImpactDescription** | String(500) | Optional | **Clinical/safety impact** |
| ReportedBy | String(100) | Required | Who identified issue |
| ReportedDate | DateTime | Required | When identified |
| **AssignedTo** | String(100) | Optional | **Person responsible for resolution** |
| **AssignedDate** | DateTime | Optional | **When assigned** |
| **AssignedBy** | String(100) | Optional | **Who made assignment** |
| **TargetResolutionDate** | Date | Optional | **Expected resolution date** |
| **Status** | Choice | Required | **Open / Assigned / In_Progress / Pending_Verification / Resolved / Closed / Escalated** |
| **StatusChangedDate** | DateTime | Auto | **When status last changed** |
| **StatusChangedBy** | String(100) | Optional | **Who changed status** |
| **ResolutionSummary** | String(1000) | Optional | **How issue was resolved** |
| **ResolvedDate** | DateTime | Optional | **When marked resolved** |
| **ResolvedBy** | String(100) | Optional | **Who resolved** |
| **VerifiedBy** | String(100) | Optional | **Who verified resolution** |
| **VerifiedDate** | DateTime | Optional | **When verified** |
| **ClosedDate** | DateTime | Optional | **When closed** |
| **ClosedBy** | String(100) | Optional | **Who closed** |
| **ReopenCount** | Integer | Default: 0 | **Times issue was reopened** |
| **EscalationLevel** | Integer | Default: 0 | **Current escalation level** |
| **EscalatedTo** | String(100) | Optional | **Who issue escalated to** |
| **EscalatedDate** | DateTime | Optional | **When escalated** |
| **LinkedFollowUpAuditId** | GUID | FK, Optional | **Audit that verified resolution** |
| CreatedDate | DateTime | Auto | Record creation |
| ModifiedDate | DateTime | Auto | Last modification |

**Severity Definitions:**
- **Critical**: Immediate patient safety risk (missing adrenaline, no defib pads, no BVM)
- **High**: Significant gap requiring urgent attention within 48 hours
- **Medium**: Issue requiring attention within 7 days
- **Low**: Minor issue, address within 30 days

**Status Workflow:**
```
Open → Assigned → In_Progress → Pending_Verification → Resolved → Closed
                       ↓                    ↓
                  Escalated            (Reopen) → In_Progress
```

---

#### 4.2.8 CorrectiveAction (Action Tracking) - NEW

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ActionId | GUID | PK | Unique identifier |
| IssueId | GUID | FK, Required | Parent issue |
| ActionNumber | Integer | Auto | Sequence within issue (1, 2, 3...) |
| ActionType | Choice | Required | Immediate_Fix / Replacement / Repair / Process_Change / Training / Escalation / Other |
| Description | String(1000) | Required | What action was taken |
| ActionTakenBy | String(100) | Required | Who performed action |
| ActionDate | DateTime | Required | When action performed |
| OutcomeDescription | String(500) | Optional | Result of action |
| OutcomeSuccessful | Boolean | Optional | Did action resolve issue? |
| EvidenceAttached | Boolean | Default: false | Photo/document attached |
| EvidenceURL | String(500) | Optional | Link to evidence |
| Notes | String(500) | Optional | Additional notes |
| CreatedDate | DateTime | Auto | Record creation |
| CreatedBy | String(100) | Required | Who logged action |

---

#### 4.2.9 IssueComment (Communication Thread) - NEW

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CommentId | GUID | PK | Unique identifier |
| IssueId | GUID | FK, Required | Parent issue |
| CommentText | String(2000) | Required | Comment content |
| CommentBy | String(100) | Required | Who commented |
| CommentDate | DateTime | Auto | When commented |
| IsInternal | Boolean | Default: false | Internal note vs visible comment |
| MentionedUsers | String(500) | Optional | @mentioned users |

---

#### 4.2.10 RandomAuditSelection (Weekly Selection) - NEW

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| SelectionId | GUID | PK | Unique identifier |
| WeekStartDate | Date | Required | Monday of selection week |
| WeekEndDate | Date | Required | Sunday of selection week |
| GeneratedDate | DateTime | Auto | When list generated |
| GeneratedBy | String(100) | Required | Who generated (or "System") |
| SelectionCriteria | String(500) | Optional | Algorithm parameters used |
| IsActive | Boolean | Default: true | Current week's selection |
| CreatedDate | DateTime | Auto | Record creation |

---

#### 4.2.11 RandomAuditSelectionItem (Selected Trolleys) - NEW

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| SelectionItemId | GUID | PK | Unique identifier |
| SelectionId | GUID | FK, Required | Parent selection |
| LocationId | GUID | FK, Required | Selected trolley |
| SelectionRank | Integer | Required | Order in selection (1-10) |
| PriorityScore | Integer | Required | Score at time of selection |
| DaysSinceAudit | Integer | Required | Days since last audit at selection |
| AuditStatus | Choice | Default: Pending | Pending / Completed / Skipped / Rescheduled |
| AuditId | GUID | FK, Optional | Link to completed audit |
| SkipReason | String(200) | Optional | If skipped, why |
| Notes | String(500) | Optional | Additional notes |

---

#### 4.2.12 Equipment (Master Equipment List) - UPDATED

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| EquipmentId | GUID | PK | Unique identifier |
| CategoryId | GUID | FK, Required | Link to category |
| ItemName | String(150) | Required | Full item description |
| ShortName | String(50) | Required | Abbreviated name |
| S4HANACode | String(20) | Optional | Ordering code |
| Supplier | String(50) | Optional | CELS, PHARMACY, etc. |
| StandardQuantity | Integer | Required | Expected count |
| UnitOfMeasure | String(20) | Default: "each" | Box, pack, roll, etc. |
| **IsStandardItem** | Boolean | Default: true | **Included on all trolleys** |
| **IsPaediatricItem** | Boolean | Default: false | **Paediatric box only** |
| **IsAlteredAirwayItem** | Boolean | Default: false | **Altered airway kit** |
| **RequiredForDefibType** | Choice | Optional | **LIFEPAK_1000_AED / LIFEPAK_20_20e / Both / None** |
| RequiresExpiryCheck | Boolean | Default: false | Has expiration date |
| SizeVariants | String(100) | Optional | Size options |
| CriticalItem | Boolean | Default: false | Missing = critical issue |
| IsActive | Boolean | Default: true | Currently required |
| EffectiveDate | Date | Required | When added to list |
| RetiredDate | Date | Optional | When removed |
| Notes | String(500) | Optional | Special instructions |
| CreatedDate | DateTime | Auto | Record creation |
| ModifiedDate | DateTime | Auto | Last modification |

---

#### 4.2.13 AuditDocuments (No changes from v1)

#### 4.2.14 AuditCondition (No changes from v1)

#### 4.2.15 AuditChecks (No changes from v1)

#### 4.2.16 AuditEquipment (No changes from v1)

#### 4.2.17 EquipmentCategory (No changes from v1)

---

### 4.3 Schema Changes Summary

| Entity | Change Type | Description |
|--------|-------------|-------------|
| Location | Modified | Added: LastAuditDate, LastAuditId, LastAuditCompliance, DaysSinceLastAudit, AuditPriorityScore, HasPaediatricBox, HasAlteredAirway, HasSpecialtyMeds, Status fields |
| LocationEquipment | New | Per-location equipment configuration |
| LocationChangeLog | New | Audit trail for trolley changes |
| Audit | Modified | Added: AuditType, TriggeredByIssueId, subscore fields |
| Issue | New/Expanded | Complete issue tracking with workflow |
| CorrectiveAction | New | Action tracking linked to issues |
| IssueComment | New | Communication thread on issues |
| RandomAuditSelection | New | Weekly random selection header |
| RandomAuditSelectionItem | New | Individual trolleys in selection |
| Equipment | Modified | Added: IsStandardItem, IsPaediatricItem, IsAlteredAirwayItem, RequiredForDefibType, CriticalItem |

---

## 5. User Interface Specifications

### 5.1 Application Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    RBWH TROLLEY AUDIT APP                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │    HOME     │ │  TROLLEYS   │ │   AUDITS    │ │  ISSUES   │ │
│  │  Dashboard  │ │  Management │ │  & Checks   │ │  Tracker  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│         │               │               │               │       │
│         ▼               ▼               ▼               ▼       │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐ │
│  │ KPIs      │   │ List View │   │ This Week │   │ Open List │ │
│  │ Charts    │   │ Add New   │   │ Start New │   │ My Issues │ │
│  │ Alerts    │   │ Edit      │   │ Drafts    │   │ Add New   │ │
│  │ Reports   │   │ History   │   │ History   │   │ Reports   │ │
│  └───────────┘   └───────────┘   └───────────┘   └───────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      ADMIN SECTION                          ││
│  │  (MERT Educators Only)                                      ││
│  │  - Generate Random Selection                                ││
│  │  - Manage Reference Data                                    ││
│  │  - User Permissions                                         ││
│  │  - System Settings                                          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Screen Specifications

#### 5.2.1 Home Dashboard (SCR-001)

**Purpose:** At-a-glance system status and navigation

**Components:**
| Component | Description |
|-----------|-------------|
| KPI Cards | Audit completion %, Open issues count, Overdue audits, Avg compliance |
| This Week's Audits | List of 10 random selections with status |
| Recent Activity | Latest audits completed, issues raised |
| Alerts Panel | Critical issues, overdue items, system notifications |
| Quick Actions | Start Audit, Log Issue, View Reports |

**Wireframe:**
```
┌────────────────────────────────────────────────────────────────────┐
│ RBWH Trolley Audit                              [User] [Settings]  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │ 85%      │ │ 12       │ │ 3        │ │ 92%      │              │
│  │ Audits   │ │ Open     │ │ Overdue  │ │ Avg      │              │
│  │ Complete │ │ Issues   │ │ Audits   │ │ Complian │              │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │
│                                                                    │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐ │
│  │ THIS WEEK'S AUDITS (5/10)   │  │ ALERTS                      │ │
│  │ ────────────────────────────│  │ ────────────────────────────│ │
│  │ ✓ 7A North - Completed      │  │ ⚠ CRITICAL: 8BN missing     │ │
│  │ ✓ CCU Pod 1 - Completed     │  │   adrenaline                │ │
│  │ ○ Hyperbaric - Pending      │  │ ⚠ 5 audits overdue >7 days  │ │
│  │ ○ Birth Suite - Pending     │  │ ℹ Weekly selection ready    │ │
│  │ ...                         │  │                             │ │
│  │ [View All] [Generate New]   │  │ [View All Alerts]           │ │
│  └─────────────────────────────┘  └─────────────────────────────┘ │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ COMPLIANCE TREND (Last 12 Months)                           │  │
│  │ [═══════════════════════════════════════════════════════]   │  │
│  │  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  [ START NEW AUDIT ]  [ LOG ISSUE ]  [ VIEW REPORTS ]             │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

#### 5.2.2 Trolley List (SCR-010)

**Purpose:** View and manage all trolley locations

**Components:**
| Component | Description |
|-----------|-------------|
| Filter Bar | Service Line, Building, Status, Days Since Audit |
| Search | Search by name/department |
| Trolley List | Sortable table with key fields |
| Action Buttons | Add New, Export, Bulk Actions (MERT only) |

**List Columns:**
1. Department Name
2. Building / Level
3. Service Line
4. Status (Active/Inactive)
5. Last Audit Date
6. Days Since Audit (colour coded: green <90, amber 90-180, red >180)
7. Last Compliance Score
8. Open Issues Count
9. Actions (View, Edit, Audit, History)

---

#### 5.2.3 Trolley Detail/Edit (SCR-011)

**Purpose:** View and edit trolley configuration

**Tabs:**
1. **Details** - Core attributes, status
2. **Equipment Config** - Optional equipment toggles
3. **Audit History** - All audits for this trolley with trends
4. **Issues** - All issues for this trolley
5. **Change Log** - Audit trail of modifications

**Equipment Config Section:**
```
┌─────────────────────────────────────────────────────────────────┐
│ OPTIONAL EQUIPMENT CONFIGURATION                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Standard Equipment               Always included               │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  [✓] Paediatric Resuscitation Box                              │
│      Include paediatric BVM, masks, defibrillator pads         │
│                                                                 │
│  [ ] Altered Airway Equipment                                   │
│      Include catheter mount, swivel connector                   │
│                                                                 │
│  [ ] Specialty Medications                                      │
│      Department-specific medications beyond standard list       │
│      Notes: [________________________________]                  │
│                                                                 │
│  Defibrillator Type: [LIFEPAK 20/20e ▼]                        │
│      Determines which defibrillator pads required              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 5.2.4 Audit Entry (SCR-020)

**Purpose:** Multi-step audit data collection

**Steps:**
1. **Select Trolley** - Dropdown with search, shows last audit info
2. **Documentation** - Check record, guidelines, BLS poster, equipment list
3. **Equipment Check** - Dynamic checklist based on trolley config
4. **Condition Check** - Cleanliness, working order, O2 tubing, INHALO
5. **Routine Checks** - Outside/inside check counts
6. **Issues** - Log any issues found (inline issue creation)
7. **Review & Submit** - Summary with calculated compliance score

**Equipment Check Screen:**
```
┌─────────────────────────────────────────────────────────────────┐
│ AUDIT: 7A North                          Step 3 of 7: Equipment │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ▼ TOP OF TROLLEY                                    [Expand]   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Item                          │ Exp │ Found │ OK │ Notes │  │
│  │─────────────────────────────────────────────────────────────│  │
│  │ BVM Resuscitator w/mask       │  1  │ [1 ]  │ ✓  │ [   ] │  │
│  │ Box of gloves (medium)        │  1  │ [1 ]  │ ✓  │ [   ] │  │
│  │ Razor                         │  1  │ [1 ]  │ ✓  │ [   ] │  │
│  │ Quick-Combo defib pads (att)  │  1  │ [1 ]  │ ✓  │ [   ] │  │
│  │ Quick-Combo defib pads (spare)│  1  │ [0 ]  │ ⚠  │ [   ] │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ▶ DRAWER 1 - IV EQUIPMENT (28 items)                          │
│  ▶ DRAWER 2 - MEDICATION & IV FLUIDS (5 items)                 │
│  ▶ DRAWER 3 - AIRWAY EQUIPMENT (24 items)                      │
│  ▶ DRAWER 4 - PPE & EXTRA EQUIPMENT (9 items)                  │
│  ▼ PAEDIATRIC BOX                                    [Expand]   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Paed BVM w/Toddler mask       │  1  │ [1 ]  │ ✓  │ [   ] │  │
│  │ ...                           │     │       │    │       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Equipment Score: 94% (83/88 items OK)                          │
│                                                                 │
│  [◀ Back]                          [Log Issue]     [Next ▶]     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 5.2.5 Issue List (SCR-030)

**Purpose:** View and manage all issues

**Filters:**
- Status (Open, Assigned, In Progress, Pending Verification, Resolved, Closed)
- Severity (Critical, High, Medium, Low)
- Category (Equipment, Documentation, Condition, Compliance)
- Location / Service Line
- Assigned To (Me, Unassigned, All)
- Age (Overdue, Due This Week, All)

**List Columns:**
1. Issue # (linked to detail)
2. Title
3. Location
4. Severity (colour coded)
5. Status
6. Age (days open)
7. Assigned To
8. Target Date
9. Actions

---

#### 5.2.6 Issue Detail (SCR-031)

**Purpose:** View and manage single issue with full history

**Sections:**
```
┌─────────────────────────────────────────────────────────────────┐
│ ISSUE: ISS-2024-0042                                    [Edit]  │
│ Missing Adrenaline - 8B North                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Status: [In Progress ▼]          Severity: ● CRITICAL         │
│  Assigned: John Smith             Target: 25 Jan 2024          │
│  Reported: Jane Doe, 22 Jan 2024  Age: 3 days                  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  DESCRIPTION                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  During routine audit, found only 4 of 6 required adrenaline   │
│  ampoules. 2 ampoules had expired (exp date Dec 2023).         │
│                                                                 │
│  Linked Audit: AUD-2024-0198 (View)                            │
│  Equipment: Adrenaline 1mg in 10mL                             │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  CORRECTIVE ACTIONS                              [+ Add Action] │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  #1 - Immediate Fix - 22 Jan 2024 - Jane Doe                   │
│     Replaced 2 expired ampoules from ward stock.               │
│     Outcome: Partial - only 5 ampoules now present             │
│                                                                 │
│  #2 - Replacement - 23 Jan 2024 - John Smith                   │
│     Ordered additional adrenaline from Pharmacy.               │
│     Order #PH-2024-1234. Expected delivery: 24 Jan             │
│     Outcome: Pending                                           │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  COMMENTS                                        [+ Add Comment]│
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Jane Doe - 22 Jan 10:30                                       │
│  Notified NUM and MERT educator of critical shortage.          │
│                                                                 │
│  John Smith - 23 Jan 08:15                                     │
│  Pharmacy confirmed stock available. Will deliver today.       │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  [Mark Resolved]  [Escalate]  [Close]  [Reopen]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 5.2.7 Random Selection Generator (SCR-040) - MERT Only

**Purpose:** Generate weekly random audit list

**Process:**
1. Display current week's selection (if exists)
2. Button to generate new selection
3. Algorithm configuration (usually defaults)
4. Preview before confirming
5. Notify relevant staff

**Screen:**
```
┌─────────────────────────────────────────────────────────────────┐
│ WEEKLY RANDOM AUDIT SELECTION                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Week: 20-26 January 2024                                       │
│  Generated: 20 Jan 2024 08:00 by System                        │
│                                                                 │
│  Selection Criteria:                                            │
│  - Prioritise trolleys not audited in 6+ months                │
│  - Ensure spread across service lines                          │
│  - Exclude trolleys audited in last 30 days                    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ #  │ Location          │ Days Since │ Priority │ Status  │  │
│  │────│───────────────────│────────────│──────────│─────────│  │
│  │ 1  │ Hyperbaric        │ 245        │ High     │ Pending │  │
│  │ 2  │ Nuclear Med Stress│ 198        │ High     │ Pending │  │
│  │ 3  │ HIRF Clinic       │ 187        │ High     │ Completed│  │
│  │ 4  │ Birth Suite       │ 156        │ Medium   │ Pending │  │
│  │ 5  │ 9A South          │ 134        │ Medium   │ Pending │  │
│  │ 6  │ Cath Lab 2        │ 122        │ Medium   │ Pending │  │
│  │ 7  │ ENT OPD           │ 98         │ Low      │ Pending │  │
│  │ 8  │ 7BW               │ 95         │ Low      │ Pending │  │
│  │ 9  │ MH G Floor        │ 91         │ Low      │ Pending │  │
│  │ 10 │ Private Practice  │ 88         │ Low      │ Pending │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Progress: 1/10 completed (10%)                                 │
│                                                                 │
│  [Regenerate Selection]  [Export List]  [Send Reminders]        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Business Logic & Workflows

### 6.1 Random Audit Selection Algorithm

```
FUNCTION GenerateWeeklyRandomSelection(weekStartDate)

INPUT:
  - weekStartDate: Monday of target week
  - selectionCount: 10 (configurable)
  - minDaysSinceAudit: 30 (exclude recently audited)
  - priorityThreshold: 180 (days for high priority)

PROCESS:
  1. Get all active trolleys
     WHERE Status = 'Active'
     AND (LastAuditDate IS NULL OR DaysSinceLastAudit >= minDaysSinceAudit)

  2. Calculate priority score for each:
     IF LastAuditDate IS NULL THEN score = 1000
     ELSE IF DaysSinceLastAudit > 365 THEN score = 500 + DaysSinceLastAudit
     ELSE IF DaysSinceLastAudit > priorityThreshold THEN score = 200 + DaysSinceLastAudit
     ELSE score = DaysSinceLastAudit

  3. Group by ServiceLine to ensure distribution

  4. Select trolleys:
     a. First, select all with DaysSinceLastAudit > priorityThreshold (up to selectionCount)
     b. If more than selectionCount qualify, randomly select from this pool
        ensuring at least 1 per ServiceLine where possible
     c. If fewer than selectionCount, fill remaining slots randomly
        from lower priority trolleys, weighted by score

  5. Rank selected trolleys by priority score (highest first)

  6. Create RandomAuditSelection record
  7. Create RandomAuditSelectionItem for each selected trolley

OUTPUT:
  - SelectionId
  - List of 10 LocationIds with ranks and scores

TRIGGER:
  - Automatic: Every Monday at 06:00
  - Manual: MERT Educator via admin screen
```

### 6.2 Compliance Score Calculation

```
FUNCTION CalculateComplianceScore(auditId)

INPUT: Completed audit with all related records

PROCESS:
  // 1. Document Score (25% weight)
  docPoints = 0
  docMax = 4
  
  IF CheckRecordStatus = 'Current' THEN docPoints += 1
  ELSE IF CheckRecordStatus = 'Old' THEN docPoints += 0.5
  
  IF CheckGuidelinesStatus = 'Current' THEN docPoints += 1
  ELSE IF CheckGuidelinesStatus = 'Old' THEN docPoints += 0.5
  
  IF BLSPosterPresent THEN docPoints += 1
  
  IF EquipmentListStatus = 'Current' THEN docPoints += 1
  ELSE IF EquipmentListStatus = 'Old' THEN docPoints += 0.5
  
  DocumentScore = docPoints / docMax

  // 2. Equipment Score (40% weight)
  equipOK = COUNT(AuditEquipment WHERE IsPresent = true AND QuantityFound >= QuantityExpected)
  equipTotal = COUNT(AuditEquipment)
  EquipmentScore = equipOK / equipTotal

  // 3. Condition Score (15% weight)
  condPoints = 0
  condMax = 5
  
  IF IsClean THEN condPoints += 1
  IF IsWorkingOrder THEN condPoints += 1
  IF RubberBandsUsed = false THEN condPoints += 1
  IF O2TubingCorrect THEN condPoints += 1
  IF InhaloCylinderOK THEN condPoints += 1
  
  ConditionScore = condPoints / condMax

  // 4. Check Score (20% weight)
  outsideRate = MIN(OutsideCheckCount / ExpectedOutside, 1.0)
  insideRate = MIN(InsideCheckCount / ExpectedInside, 1.0)
  
  IF CountNotAvailable THEN
    CheckScore = NULL  // Exclude from calculation
    checkWeight = 0
  ELSE
    CheckScore = (outsideRate + insideRate) / 2
    checkWeight = 0.20
  
  // 5. Overall Score
  IF CheckScore IS NULL THEN
    // Redistribute weight
    OverallCompliance = (DocumentScore * 0.30) + (EquipmentScore * 0.50) + (ConditionScore * 0.20)
  ELSE
    OverallCompliance = (DocumentScore * 0.25) + (EquipmentScore * 0.40) + 
                        (ConditionScore * 0.15) + (CheckScore * 0.20)

OUTPUT:
  - DocumentScore, EquipmentScore, ConditionScore, CheckScore
  - OverallCompliance (0.00 to 1.00)
```

### 6.3 Issue Workflow State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ISSUE STATUS WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              ┌──────────┐                                   │
│                              │  OPEN    │                                   │
│                              └────┬─────┘                                   │
│                                   │                                         │
│                          Assign to person                                   │
│                                   │                                         │
│                                   ▼                                         │
│                             ┌──────────┐                                    │
│                             │ ASSIGNED │                                    │
│                             └────┬─────┘                                    │
│                                  │                                          │
│                         Begin work on fix                                   │
│                                  │                                          │
│                                  ▼                                          │
│   Escalate             ┌─────────────────┐                                  │
│  ┌──────────────────── │  IN_PROGRESS    │ ────────────────────┐            │
│  │                     └────────┬────────┘                     │            │
│  │                              │                              │            │
│  │                    Mark as fixed                    Auto-escalate        │
│  │                    (needs verification)             (if overdue)         │
│  │                              │                              │            │
│  │                              ▼                              │            │
│  │                    ┌───────────────────┐                    │            │
│  │                    │PENDING_VERIFICATION│                   │            │
│  │                    └─────────┬─────────┘                    │            │
│  │                       │             │                       │            │
│  │              Verified OK      Verification failed           │            │
│  │                    │                │                       │            │
│  │                    ▼                │                       ▼            │
│  │              ┌──────────┐           │               ┌───────────┐        │
│  │              │ RESOLVED │           │               │ ESCALATED │        │
│  │              └────┬─────┘           │               └─────┬─────┘        │
│  │                   │                 │                     │              │
│  │           Admin closes              │              Work continues        │
│  │                   │                 │                     │              │
│  │                   ▼                 └──────────────────────┘              │
│  │              ┌──────────┐                     │                          │
│  └─────────────►│  CLOSED  │◄────────────────────┘                          │
│                 └────┬─────┘                                                │
│                      │                                                      │
│              Issue recurs?                                                  │
│                      │                                                      │
│                      ▼                                                      │
│                 ┌──────────┐                                                │
│                 │ REOPENED │ ──────────► (returns to IN_PROGRESS)           │
│                 └──────────┘                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

TRANSITIONS:
  Open → Assigned: AssignedTo set, AssignedDate set
  Assigned → In_Progress: First CorrectiveAction logged
  In_Progress → Pending_Verification: User marks ready for verification
  Pending_Verification → Resolved: Verifier confirms fix
  Pending_Verification → In_Progress: Verification fails (ReopenCount++)
  Resolved → Closed: Admin review complete
  Closed → In_Progress: Issue reopened (ReopenCount++)
  Any → Escalated: Manual escalation or auto-escalate rule triggers

AUTO-ESCALATE RULES:
  - Critical issues: Not resolved within 48 hours
  - High issues: Not resolved within 7 days
  - Medium issues: Not resolved within 14 days
  - Low issues: Not resolved within 30 days
  - Any issue: Target date passed by 3 days
```

### 6.4 Location Update After Audit

```
TRIGGER: On Audit.SubmissionStatus changed to 'Submitted'

ACTIONS:
  1. Update Location record:
     - LastAuditDate = Audit.CompletedDateTime
     - LastAuditId = Audit.AuditId
     - LastAuditCompliance = Audit.OverallCompliance
  
  2. IF OverallCompliance < 0.80 THEN:
     - Set Audit.RequiresFollowUp = true
     - Set Audit.FollowUpDueDate = CompletedDateTime + 7 days
     - Send notification to NUM and MERT
  
  3. IF any critical equipment missing:
     - Auto-create Issue with Severity = 'Critical'
     - Send immediate notification to NUM, MERT, and Service Line Manager
  
  4. Update RandomAuditSelectionItem (if exists):
     - Set AuditStatus = 'Completed'
     - Set AuditId = Audit.AuditId
  
  5. Log activity for dashboard
```

### 6.5 Trolley Change Logging

```
TRIGGER: On Location record Created, Modified, or Status changed

ACTIONS:
  1. Create LocationChangeLog record:
     - ChangeType based on operation
     - Capture old and new values for changed fields
     - Record user and timestamp
  
  2. IF Status changed to 'Inactive' or 'Decommissioned':
     - Remove from any active RandomAuditSelection
     - Close any pending audits as 'Cancelled'
     - Note: Do NOT close open Issues (may need resolution)
  
  3. IF Status changed to 'Active' (reactivation):
     - Set LastAuditDate = NULL (force re-audit)
     - Add note requiring audit before trolley returns to service
```

---

## 7. Reporting & Analytics

### 7.1 Standard Reports

| Report | Description | Frequency | Audience |
|--------|-------------|-----------|----------|
| Weekly Audit Status | Progress on random selection, completed vs pending | Weekly | MERT, Managers |
| Monthly Compliance Summary | Aggregate scores by service line, building | Monthly | All |
| Quarterly Trend Analysis | Compliance trends, issue patterns | Quarterly | MERT, Leadership |
| Annual Comprehensive Report | Full year analysis, year-over-year comparison | Annual | Leadership |
| Overdue Audits | Trolleys past audit deadline | On-demand | MERT |
| Open Issues Aging | Issues by age bucket, severity | On-demand | MERT, Managers |
| Equipment Deficiency | Most common missing/short items | Monthly | MERT, CELS |
| Trolley History | Complete history for single trolley | On-demand | All |

### 7.2 Dashboard KPIs

| KPI | Target | Calculation | Alert Threshold |
|-----|--------|-------------|-----------------|
| Audit Completion Rate | 100% | Audits completed / Audits due | <90% |
| Average Compliance Score | >90% | Mean of all compliance scores | <85% |
| Critical Issues Open | 0 | Count where Severity = Critical and Status not Closed | >0 |
| Overdue Issues | 0 | Count where Status not Closed and Age > TargetDays | >5 |
| Trolleys >6 Months Since Audit | 0 | Count where DaysSinceLastAudit > 180 | >5 |
| Random Selection Completion | 100% | Weekly selections completed / 10 | <80% |

### 7.3 Trend Visualisations

1. **Compliance Over Time** - Line chart showing monthly average compliance
2. **Issues by Category** - Pie chart of issue categories
3. **Audit Activity Heatmap** - Calendar view of audit completions
4. **Service Line Comparison** - Bar chart comparing service line compliance
5. **Days Since Audit Distribution** - Histogram of trolley audit recency

---

## 8. Security & Permissions

### 8.1 Role Definitions

| Role | Description | Users |
|------|-------------|-------|
| System Admin | Full system access, user management | IT Support |
| MERT Educator | Trolley management, all audits, all issues, reports | MERT Nurse Educators |
| Service Line Manager | View/edit within service line, approve issues | NUMs, SL Managers |
| Auditor | Conduct audits, log issues, view own work | Clinical Staff |
| Viewer | Read-only access to dashboards and reports | Leadership |

### 8.2 Permission Matrix

| Function | Admin | MERT | SL Manager | Auditor | Viewer |
|----------|-------|------|------------|---------|--------|
| View Dashboard | ✓ | ✓ | ✓ (own SL) | ✓ (limited) | ✓ |
| View Trolley List | ✓ | ✓ | ✓ (own SL) | ✓ | ✓ |
| Add/Edit Trolley | ✓ | ✓ | - | - | - |
| Deactivate Trolley | ✓ | ✓ | - | - | - |
| Generate Random Selection | ✓ | ✓ | - | - | - |
| Start Audit | ✓ | ✓ | ✓ | ✓ | - |
| Submit Audit | ✓ | ✓ | ✓ | ✓ | - |
| Verify Audit | ✓ | ✓ | ✓ (own SL) | - | - |
| Log Issue | ✓ | ✓ | ✓ | ✓ | - |
| Assign Issue | ✓ | ✓ | ✓ (own SL) | - | - |
| Close Issue | ✓ | ✓ | ✓ (own SL) | - | - |
| View All Reports | ✓ | ✓ | ✓ (own SL) | - | ✓ |
| Export Data | ✓ | ✓ | ✓ (own SL) | - | - |
| Manage Users | ✓ | - | - | - | - |

---

## 9. Integration Requirements

### 9.1 Current Integrations (Phase 1)

| System | Integration Type | Purpose |
|--------|------------------|---------|
| Microsoft 365 | Native | User authentication, email notifications |
| SharePoint Online | Native | Data storage (lists) |
| Power Automate | Native | Workflow automation |
| Power BI | Native | Reporting dashboards |

### 9.2 Future Integrations (Phase 2+)

| System | Integration Type | Purpose |
|--------|------------------|---------|
| S/4HANA | API | Automated procurement for restocking |
| Moodle LMS | API | Staff training verification |
| Asset Management | API | Trolley asset tracking |
| Clinical Systems | TBD | Incident reporting alignment |

---

## 10. Implementation Plan

### 10.1 Phase Overview

| Phase | Duration | Focus | Deliverables |
|-------|----------|-------|--------------|
| Phase 1 | Weeks 1-4 | Foundation | SharePoint lists, basic PowerApp, core flows |
| Phase 2 | Weeks 5-8 | Core Features | Equipment checklist, issue tracking, random selection |
| Phase 3 | Weeks 9-12 | Reporting | Power BI dashboards, historical data migration |
| Phase 4 | Weeks 13-16 | Enhancement | Offline support, photos, advanced workflows |

### 10.2 Phase 1: Foundation (Weeks 1-4)

**Week 1-2: Data Layer**
- Create SharePoint site and lists
- Import reference data (ServiceLine, EquipmentCategory, Equipment)
- Import Location data from cleaned CSV
- Configure list permissions

**Week 3-4: Basic App**
- PowerApp: Home screen, trolley list, trolley detail view
- PowerApp: Basic audit entry (documentation, condition screens)
- Power Automate: Audit submission flow with compliance calculation
- Testing with sample data

### 10.3 Phase 2: Core Features (Weeks 5-8)

**Week 5-6: Equipment & Issues**
- PowerApp: Dynamic equipment checklist
- PowerApp: Issue logging within audit
- PowerApp: Issue list and detail screens
- Power Automate: Issue notifications

**Week 7-8: Random Selection & Trolley Management**
- PowerApp: Trolley add/edit screens (MERT only)
- PowerApp: Random selection generator
- Power Automate: Weekly auto-generation
- Power Automate: Location update after audit

### 10.4 Phase 3: Reporting (Weeks 9-12)

**Week 9-10: Dashboards**
- Power BI: Compliance dashboard
- Power BI: Issue tracking dashboard
- Power BI: Trolley history report
- Embed in PowerApp/SharePoint

**Week 11-12: Data Migration & Refinement**
- Import 2023-2024 historical audit data
- Map to new schema
- Validate trends and reports
- User acceptance testing

### 10.5 Phase 4: Enhancement (Weeks 13-16)

- Offline capability for PowerApp
- Photo capture integration
- Advanced notification rules
- Performance optimisation
- User training and documentation
- Go-live preparation

---

## 11. Appendices

### Appendix A: Equipment Master List

*See equipment_master_list.json*

### Appendix B: Location Master List

*See locations_master_cleaned.csv*

### Appendix C: Glossary

| Term | Definition |
|------|------------|
| BLS | Basic Life Support |
| BVM | Bag-Valve-Mask resuscitator |
| CELS | Central Equipment Library Service |
| Comprehensive Audit | Full annual audit of all trolley components |
| MERT | Medical Emergency Response Team |
| NUM | Nurse Unit Manager |
| Random Spot Check | Weekly selected audit for quality assurance |
| S/4HANA | SAP enterprise resource planning system |

### Appendix D: Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | | | |
| MERT Educator | | | |
| IT Representative | | | |
| Clinical Representative | | | |

---

*End of Document*
