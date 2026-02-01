# RBWH Resuscitation Trolley Audit System
## Data Schema and Application Logic Specification

**Version:** 1.0  
**Date:** January 2026  
**Purpose:** Define the data model and business logic for a PowerApps/Power Automate audit solution

---

## Part 1: Current State Analysis

### 1.1 Data Sources Reviewed

| Source | Description | Records |
|--------|-------------|---------|
| Standard Resuscitation Trolley Equipment List (Sept 2022) | Master equipment checklist for adult trolleys | ~60 items |
| Paediatric Resuscitation Equipment Box List (March 2022) | Supplementary paediatric equipment | 6 items |
| Trolley Locations - March 2022 | Master location register | 75 locations |
| Trolley Locations - Outpatient & Clinic | Updated location register | 76 locations |
| Audit 2023 | Microsoft Forms responses | 75 audits |
| Audit 2024 | Microsoft Forms responses | 76 audits |

### 1.2 Current Data Structure (Microsoft Forms Export)

**Audit Response Fields (2024 version):**

| Field | Type | Values/Format |
|-------|------|---------------|
| Id | Integer | Auto-generated |
| Start time | DateTime | Submission start |
| Completion time | DateTime | Submission complete |
| Email | String | "anonymous" |
| Auditor Name | String | Free text |
| Clinical Area | String | Free text (inconsistent naming) |
| Service Line/Directorate | Choice | 7 options |
| Other Directorate | String | Free text if "Other" |
| Check Record Present | Choice | Yes - current / Yes - old / No |
| Checking Guidelines Present | Choice | Yes - current / Yes - old / No |
| BLS Poster Present | Choice | Yes / No |
| Equipment List Present | Choice | Yes / No |
| All Items Stocked | Choice | Yes / No |
| Additional Items Found | Choice | Yes / No |
| Items Added/Missing (comments) | String | Free text |
| Outside Check Count | String | Numeric or "Not Available" |
| Inside Check Count | String | Numeric or "Not Available" |
| Rubber Bands Present | Choice | Yes / No |
| Trolley Clean | Choice | Yes / No |
| Trolley Working Order | Choice | Yes / No |
| Issue Details | String | Free text |
| O2 Tubing Correct | Choice | Yes / No |
| INHALO Cylinder OK | Choice | Yes / No |

### 1.3 Identified Data Quality Issues

1. **Inconsistent Clinical Area Naming**
   - "7A North" vs "7AN" vs "7A north"
   - "5c" vs "5C" vs "5C beds 1-18"
   - "Cath Lab 1" vs "Cath lab procedure room 1"

2. **No Foreign Key Relationship**
   - Audit responses don't link to master location register
   - Manual text entry causes matching failures

3. **Mixed Data Types**
   - Check counts: "31", "Not Available", "NUM off ward", "21/21"
   - No standardised numeric validation

4. **No Equipment-Level Tracking**
   - Binary "all items stocked" without granular detail
   - Free text for missing/extra items (difficult to analyse)

5. **No Audit Period Tracking**
   - Year-specific column names require annual form redesign
   - No standard audit period reference

6. **Limited Compliance Calculation**
   - 2023: Expected shifts vs actual (percentage)
   - 2024: Separate outside/inside counts without expected baseline

---

## Part 2: Proposed Data Schema

### 2.1 Entity Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   ServiceLine    │       │     Location     │       │   AuditPeriod    │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ ServiceLineId PK │◄──────│ ServiceLineId FK │       │ PeriodId PK      │
│ Name             │       │ LocationId PK    │       │ PeriodName       │
│ Abbreviation     │       │ DepartmentName   │       │ StartDate        │
│ IsActive         │       │ Building         │       │ EndDate          │
└──────────────────┘       │ Level            │       │ ExpectedOutside  │
                           │ SpecificLocation │       │ ExpectedInside   │
                           │ TrolleyType      │       │ IsActive         │
                           │ HasPaedBox       │       └──────────────────┘
                           │ DefibrillatorType│               │
                           │ IsActive         │               │
                           │ Notes            │               │
                           └──────────────────┘               │
                                    │                         │
                                    │                         │
                           ┌────────┴─────────────────────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │      Audit       │
                    ├──────────────────┤
                    │ AuditId PK       │
                    │ LocationId FK    │
                    │ PeriodId FK      │
                    │ AuditorName      │
                    │ AuditDateTime    │
                    │ SubmissionStatus │
                    └──────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ AuditDocuments   │ │ AuditEquipment   │ │ AuditCondition   │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ AuditDocId PK    │ │ AuditEquipId PK  │ │ AuditCondId PK   │
│ AuditId FK       │ │ AuditId FK       │ │ AuditId FK       │
│ CheckRecord      │ │ EquipmentId FK   │ │ IsClean          │
│ CheckGuidelines  │ │ IsPresent        │ │ IsWorkingOrder   │
│ BLSPoster        │ │ Quantity         │ │ IssueDescription │
│ EquipmentList    │ │ ExpiryOK         │ │ RubberBandsUsed  │
└──────────────────┘ │ Notes            │ │ O2TubingCorrect  │
                     └──────────────────┘ │ InhaloCylinderOK │
                                          └──────────────────┘
          │
          ▼
┌──────────────────┐       ┌──────────────────┐
│  AuditChecks     │       │    Equipment     │
├──────────────────┤       ├──────────────────┤
│ AuditCheckId PK  │       │ EquipmentId PK   │
│ AuditId FK       │       │ CategoryId FK    │
│ OutsideCount     │       │ ItemName         │
│ InsideCount      │       │ S4HANACode       │
│ CountNA          │       │ Supplier         │
│ CountNotes       │       │ StandardQty      │
└──────────────────┘       │ TrolleySection   │
                           │ IsPaediatric     │
                           │ IsActive         │
                           └──────────────────┘
                                    │
                                    │
                           ┌──────────────────┐
                           │EquipmentCategory │
                           ├──────────────────┤
                           │ CategoryId PK    │
                           │ CategoryName     │
                           │ SortOrder        │
                           └──────────────────┘
```

### 2.2 Table Definitions

#### 2.2.1 ServiceLine (Reference Data)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ServiceLineId | GUID | PK | Unique identifier |
| Name | String(100) | Required | Full name |
| Abbreviation | String(10) | Required | Short code (IMS, S&P, etc.) |
| IsActive | Boolean | Default: true | Soft delete flag |

**Seed Data:**
- Internal Medicine Services (IMS)
- Surgical & Perioperative Services (S&P)
- Cancer Care Services (CCS)
- Women's & Newborn Services (WNBS)
- Critical Care & Clinical Support Services (CC&CSS)
- Mental Health (MH)
- Allied Health (AH)

#### 2.2.2 Location (Master Trolley Register)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| LocationId | GUID | PK | Unique identifier |
| ServiceLineId | GUID | FK, Required | Link to service line |
| DepartmentName | String(100) | Required, Unique | Official department name |
| DisplayName | String(50) | Required | Short display name |
| Building | String(50) | Required | James Mayne, Ned Hanlon, etc. |
| Level | String(20) | Required | Ground, L3, Level 5, etc. |
| SpecificLocation | String(100) | Optional | Room/bay details |
| TrolleyType | Choice | Required | Standard / Emergency / Other |
| HasPaedBox | Boolean | Default: false | Requires paediatric equipment |
| DefibrillatorType | Choice | Required | LIFEPAK_1000_AED / LIFEPAK_20_20e |
| OperatingHours | Choice | Required | 24_7 / Weekday_Business / Weekday_Extended |
| ExpectedDailyChecks | Integer | Computed | Based on operating hours |
| IsActive | Boolean | Default: true | Currently in service |
| DecommissionedDate | Date | Optional | When taken out of service |
| Notes | String(500) | Optional | Special requirements |
| CreatedDate | DateTime | Auto | Record creation |
| ModifiedDate | DateTime | Auto | Last modification |

**Operating Hours Mapping:**
- 24_7: 3 shifts/day × 7 days = 21 outside checks/week, 93 checks/month
- Weekday_Business: 1 shift/day × 5 days = 5 outside checks/week
- Weekday_Extended: 2 shifts/day × 5 days = 10 outside checks/week

#### 2.2.3 AuditPeriod

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| PeriodId | GUID | PK | Unique identifier |
| PeriodName | String(50) | Required | "March 2024", "April 2024" |
| Year | Integer | Required | Calendar year |
| Month | Integer | Required | 1-12 |
| StartDate | Date | Required | Period start |
| EndDate | Date | Required | Period end |
| WorkingDays | Integer | Computed | Business days in period |
| TotalDays | Integer | Computed | Calendar days |
| AuditDeadline | Date | Required | Submission deadline |
| IsActive | Boolean | Default: true | Current audit period |
| CreatedBy | String | Required | Admin who created |

#### 2.2.4 EquipmentCategory

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CategoryId | GUID | PK | Unique identifier |
| CategoryName | String(50) | Required | Top of Trolley, Drawer 1, etc. |
| SortOrder | Integer | Required | Display order |
| Description | String(200) | Optional | Category notes |

**Seed Data:**
1. Top of Trolley
2. Side of Trolley
3. Back of Trolley
4. Drawer 1 - IV Equipment
5. Drawer 2 - Medication & IV Fluids
6. Drawer 3 - Airway Equipment
7. Drawer 4 - PPE & Extra Equipment
8. Paediatric Box

#### 2.2.5 Equipment (Master Equipment List)

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
| IsPaediatric | Boolean | Default: false | Paed box only |
| RequiresExpiryCheck | Boolean | Default: false | Has expiration date |
| SizeVariants | String(100) | Optional | Size options (e.g., "3,4,5") |
| IsActive | Boolean | Default: true | Currently required |
| EffectiveDate | Date | Required | When added to list |
| RetiredDate | Date | Optional | When removed |
| Notes | String(500) | Optional | Special instructions |

#### 2.2.6 Audit (Main Audit Record)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AuditId | GUID | PK | Unique identifier |
| LocationId | GUID | FK, Required | Trolley being audited |
| PeriodId | GUID | FK, Required | Audit period |
| AuditorName | String(100) | Required | Person conducting audit |
| AuditorEmail | String(100) | Optional | Contact email |
| StartedDateTime | DateTime | Required | When audit began |
| CompletedDateTime | DateTime | Optional | When submitted |
| SubmissionStatus | Choice | Required | Draft / Submitted / Verified |
| OverallCompliance | Decimal | Computed | Percentage score |
| RequiresFollowUp | Boolean | Computed | Based on issues |
| FollowUpNotes | String(1000) | Optional | Actions required |
| VerifiedBy | String(100) | Optional | Reviewer name |
| VerifiedDateTime | DateTime | Optional | When reviewed |

#### 2.2.7 AuditDocuments (Documentation Checks)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AuditDocId | GUID | PK | Unique identifier |
| AuditId | GUID | FK, Required | Parent audit |
| CheckRecordStatus | Choice | Required | Current / Old / None |
| CheckGuidelinesStatus | Choice | Required | Current / Old / None |
| BLSPosterPresent | Boolean | Required | Yes/No |
| EquipmentListStatus | Choice | Required | Current / Old / None |
| DocumentNotes | String(500) | Optional | Additional comments |

#### 2.2.8 AuditEquipment (Item-Level Checks)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AuditEquipId | GUID | PK | Unique identifier |
| AuditId | GUID | FK, Required | Parent audit |
| EquipmentId | GUID | FK, Required | Item being checked |
| IsPresent | Boolean | Required | Item found |
| QuantityFound | Integer | Optional | Actual count |
| QuantityExpected | Integer | Computed | From Equipment.StandardQuantity |
| ExpiryChecked | Boolean | Optional | If applicable |
| ExpiryOK | Boolean | Optional | Within date |
| SizeChecked | String(50) | Optional | Which sizes found |
| ItemNotes | String(200) | Optional | Issues/comments |

#### 2.2.9 AuditCondition (Physical Trolley Checks)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AuditCondId | GUID | PK | Unique identifier |
| AuditId | GUID | FK, Required | Parent audit |
| IsClean | Boolean | Required | Clean and dust free |
| IsWorkingOrder | Boolean | Required | Mechanically sound |
| IssueType | Choice | Optional | Wheels / Handle / Other |
| IssueDescription | String(500) | Optional | Details of issues |
| RubberBandsUsed | Boolean | Required | Inappropriate practice |
| O2TubingCorrect | Boolean | Required | Green tubing on BVM |
| InhaloCylinderOK | Boolean | Required | Pressure adequate |
| ConditionNotes | String(500) | Optional | Additional observations |

#### 2.2.10 AuditChecks (Routine Check Compliance)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AuditCheckId | GUID | PK | Unique identifier |
| AuditId | GUID | FK, Required | Parent audit |
| OutsideCheckCount | Integer | Optional | Daily checks completed |
| InsideCheckCount | Integer | Optional | Weekly checks completed |
| ExpectedOutside | Integer | Computed | From Location + Period |
| ExpectedInside | Integer | Computed | Weeks in period |
| CountNotAvailable | Boolean | Default: false | Unable to determine |
| NotAvailableReason | String(200) | Optional | Why unavailable |
| CheckNotes | String(500) | Optional | Additional context |
| OutsideCompliance | Decimal | Computed | Percentage |
| InsideCompliance | Decimal | Computed | Percentage |

---

## Part 3: Enhancements and Extensions

### 3.1 Immediate Improvements

#### 3.1.1 Standardised Location Lookup
- **Problem:** Free text clinical area entry causes inconsistent naming
- **Solution:** Dropdown selection from Location table with search/filter
- **Benefit:** 100% match rate between audits and master register

#### 3.1.2 Granular Equipment Tracking
- **Problem:** Binary "all items stocked" loses detail
- **Solution:** Equipment checklist with item-level presence/quantity
- **Benefit:** Trend analysis, targeted restocking, supplier reporting

#### 3.1.3 Computed Compliance Scores
- **Problem:** Manual percentage calculations in Excel
- **Solution:** Automatic calculation from check counts vs. expected
- **Benefit:** Real-time dashboards, automatic flagging

#### 3.1.4 Audit Period Configuration
- **Problem:** Year-specific questions require annual form redesign
- **Solution:** Dynamic period reference from AuditPeriod table
- **Benefit:** Zero maintenance for annual rollover

### 3.2 Future Extensions

#### 3.2.1 Photo Evidence
```
┌──────────────────┐
│   AuditPhoto     │
├──────────────────┤
│ PhotoId PK       │
│ AuditId FK       │
│ PhotoType        │  (Trolley / Issue / Equipment)
│ BlobURL          │
│ ThumbnailURL     │
│ CapturedDateTime │
│ Notes            │
└──────────────────┘
```
- Capture trolley condition
- Document issues for maintenance
- Before/after evidence

#### 3.2.2 Maintenance Tracking
```
┌──────────────────┐
│ MaintenanceLog   │
├──────────────────┤
│ LogId PK         │
│ LocationId FK    │
│ AuditId FK       │  (Optional - if triggered by audit)
│ IssueType        │
│ Description      │
│ ReportedDate     │
│ ReportedBy       │
│ AssignedTo       │
│ Status           │  (Open / InProgress / Resolved)
│ ResolvedDate     │
│ ResolutionNotes  │
└──────────────────┘
```
- Track issues to resolution
- Link to originating audit
- Accountability trail

#### 3.2.3 Expiry Tracking
```
┌──────────────────┐
│  ExpiryRecord    │
├──────────────────┤
│ ExpiryId PK      │
│ LocationId FK    │
│ EquipmentId FK   │
│ BatchNumber      │
│ ExpiryDate       │
│ CheckedDate      │
│ CheckedBy        │
│ ReplacedDate     │
└──────────────────┘
```
- Proactive expiry alerts
- Batch tracking for medications
- Automatic reorder triggers

#### 3.2.4 Staff Training Integration
```
┌──────────────────┐
│   StaffTraining  │
├──────────────────┤
│ TrainingId PK    │
│ StaffName        │
│ StaffEmail       │
│ ServiceLineId FK │
│ TrainingType     │  (AuditProcedure / BLS / Equipment)
│ CompletedDate    │
│ ExpiryDate       │
│ CertificateURL   │
└──────────────────┘
```
- Track auditor competency
- Prevent untrained staff auditing
- Integration with Moodle LMS

#### 3.2.5 Supplier Integration
- Automatic reorder notifications to CELS, Pharmacy
- Stock level alerts based on audit findings
- S/4HANA integration for procurement

---

## Part 4: Application Logic

### 4.1 Audit Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AUDIT WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │  START   │───▶│  SELECT  │───▶│ DOCUMENTS│───▶│EQUIPMENT │     │
│  │  AUDIT   │    │ LOCATION │    │  CHECK   │    │  CHECK   │     │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│                                                         │          │
│                                                         ▼          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │  EMAIL   │◀───│  REVIEW  │◀───│ ROUTINE  │◀───│CONDITION │     │
│  │ SUMMARY  │    │ & SUBMIT │    │  CHECKS  │    │  CHECK   │     │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│                        │                                           │
│                        ▼                                           │
│                 ┌──────────────┐                                   │
│                 │ FOLLOW-UP    │                                   │
│                 │ WORKFLOW?    │                                   │
│                 └──────────────┘                                   │
│                        │                                           │
│              ┌─────────┴─────────┐                                 │
│              ▼                   ▼                                 │
│       ┌──────────┐        ┌──────────┐                            │
│       │   YES    │        │    NO    │                            │
│       │Create    │        │  END     │                            │
│       │Issue     │        └──────────┘                            │
│       └──────────┘                                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Business Rules

#### 4.2.1 Audit Initiation
```
RULE: Audit_Start_Validation
WHEN: User starts new audit
THEN:
  - Check active AuditPeriod exists
  - Verify Location is active
  - Check no existing audit for Location + Period (or allow override with reason)
  - Auto-populate: AuditorName from logged-in user
  - Auto-populate: Expected check counts from Location.OperatingHours + Period
  - Create draft Audit record
```

#### 4.2.2 Location Selection
```
RULE: Location_Filtering
WHEN: User selects location
THEN:
  - Filter by user's Service Line (if enforced)
  - Show only IsActive = true locations
  - Indicate existing audit status for current period
  - Highlight overdue locations (no audit in current period)
```

#### 4.2.3 Equipment Check Logic
```
RULE: Equipment_List_Generation
WHEN: Audit reaches equipment check screen
THEN:
  - Load all Equipment where IsActive = true AND IsPaediatric = false
  - IF Location.HasPaedBox = true THEN also load IsPaediatric = true items
  - IF Location.DefibrillatorType = LIFEPAK_20_20e THEN include cardiac monitoring items
  - Group by CategoryId, order by Category.SortOrder
  - Pre-populate QuantityExpected from Equipment.StandardQuantity
```

#### 4.2.4 Compliance Calculation
```
RULE: Calculate_Compliance
WHEN: Audit submitted
THEN:
  // Document compliance (25% weight)
  DocScore = (
    (CheckRecord = Current ? 1 : CheckRecord = Old ? 0.5 : 0) +
    (Guidelines = Current ? 1 : Guidelines = Old ? 0.5 : 0) +
    (BLSPoster = Yes ? 1 : 0) +
    (EquipmentList = Current ? 1 : EquipmentList = Old ? 0.5 : 0)
  ) / 4
  
  // Equipment compliance (40% weight)
  EquipScore = COUNT(IsPresent = true AND QuantityFound >= QuantityExpected) 
               / COUNT(all equipment items)
  
  // Condition compliance (15% weight)
  CondScore = (
    (IsClean ? 1 : 0) +
    (IsWorkingOrder ? 1 : 0) +
    (RubberBandsUsed = false ? 1 : 0) +
    (O2TubingCorrect ? 1 : 0) +
    (InhaloCylinderOK ? 1 : 0)
  ) / 5
  
  // Routine checks compliance (20% weight)
  CheckScore = (
    (OutsideCheckCount / ExpectedOutside) +
    (InsideCheckCount / ExpectedInside)
  ) / 2
  // Cap at 1.0 (100%)
  
  OverallCompliance = (DocScore * 0.25) + (EquipScore * 0.40) + 
                      (CondScore * 0.15) + (CheckScore * 0.20)
```

#### 4.2.5 Follow-Up Triggers
```
RULE: Trigger_FollowUp
WHEN: Audit submitted
THEN:
  RequiresFollowUp = true IF ANY:
    - OverallCompliance < 0.80
    - CheckRecord = None
    - IsWorkingOrder = false
    - Any medication expired
    - OutsideCheckCount / ExpectedOutside < 0.50
    - Critical equipment missing (Adrenaline, BVM, Defib pads)
  
  IF RequiresFollowUp THEN:
    - Create MaintenanceLog record (if trolley issue)
    - Send notification to Nurse Unit Manager
    - Send notification to MERT Educator
    - Add to follow-up dashboard
```

#### 4.2.6 Audit Completion Validation
```
RULE: Submission_Validation
WHEN: User attempts to submit audit
THEN:
  BLOCK submission IF:
    - Any required field is empty
    - Check counts exceed possible maximum (OutsideCount > TotalDays * 3)
    - No equipment items checked
  
  WARN (allow override with reason) IF:
    - Completion time < 5 minutes (too fast for thorough audit)
    - All items marked present with no comments (rubber stamp risk)
    - CountNotAvailable = true without NotAvailableReason
```

### 4.3 Notification Rules

```
NOTIFICATION: Audit_Reminder
TRIGGER: AuditPeriod.AuditDeadline - 7 days
TO: Service Line managers
CONTENT: "X locations have not been audited for [PeriodName]"

NOTIFICATION: Audit_Overdue
TRIGGER: AuditPeriod.AuditDeadline + 1 day
TO: MERT Educator, Service Line managers
CONTENT: "Overdue audits for [PeriodName]: [Location list]"

NOTIFICATION: Critical_Issue
TRIGGER: On audit submission where RequiresFollowUp = true
TO: Nurse Unit Manager, MERT Educator
CONTENT: "[LocationName] requires immediate attention: [Issue summary]"

NOTIFICATION: Weekly_Summary
TRIGGER: Every Monday 8am
TO: MERT Educator
CONTENT: Dashboard summary of audit status, compliance scores, open issues
```

### 4.4 Reporting Requirements

#### 4.4.1 Standard Reports
1. **Audit Completion Status** - Locations audited vs outstanding by period
2. **Compliance Summary** - Overall scores by service line, trending over periods
3. **Equipment Deficiency** - Most frequently missing/low items
4. **Routine Check Compliance** - Outside/inside check rates by location
5. **Issue Tracker** - Open maintenance items, age, status
6. **Year-over-Year Comparison** - Same period across multiple years

#### 4.4.2 Dashboard KPIs
- Audit completion rate (target: 100%)
- Average compliance score (target: >90%)
- Locations with <80% compliance (target: 0)
- Open maintenance issues (target: <5)
- Routine check compliance (target: >80%)

---

## Part 5: Implementation Recommendations

### 5.1 Phase 1: Foundation (Weeks 1-4)

1. **Create SharePoint Lists**
   - ServiceLine (reference data)
   - Location (migrate from Excel)
   - AuditPeriod (configure current + next period)
   - Equipment (migrate from PDF lists)
   - EquipmentCategory (reference data)

2. **Build Core PowerApp**
   - Location selection screen with search
   - Document checks screen
   - Condition checks screen
   - Routine checks screen
   - Review and submit screen

3. **Basic Power Automate Flows**
   - On submission: create audit record, send confirmation
   - Calculated compliance score (initially in Power Automate)

### 5.2 Phase 2: Equipment Detail (Weeks 5-8)

1. **Equipment Checklist**
   - Dynamic equipment list based on location type
   - Item-level presence/quantity entry
   - Grouped by category with collapsible sections

2. **Enhanced Compliance Calculation**
   - Weighted scoring formula
   - Automatic follow-up flagging

3. **Notification Flows**
   - Reminder emails
   - Overdue alerts
   - Critical issue notifications

### 5.3 Phase 3: Reporting & Analytics (Weeks 9-12)

1. **Power BI Dashboard**
   - Real-time compliance visualisation
   - Trend analysis
   - Drill-down by service line/location

2. **Historical Data Migration**
   - Import 2023-2024 audit data
   - Map to new schema where possible
   - Flag incomplete records

3. **User Training**
   - Auditor training materials
   - Manager dashboard training
   - Process documentation

### 5.4 Future Phases

- Photo capture integration
- Maintenance workflow
- Expiry tracking and alerts
- Moodle LMS integration
- Supplier notification automation

---

## Part 6: Technical Specifications

### 6.1 Platform Components

| Component | Purpose | Notes |
|-----------|---------|-------|
| SharePoint Online | Data storage | Lists for all entities |
| PowerApps | Audit entry UI | Canvas app, mobile-optimised |
| Power Automate | Business logic | Flows for notifications, calculations |
| Power BI | Reporting | Embedded in SharePoint or standalone |

### 6.2 SharePoint List Structure

All lists should be created in a dedicated SharePoint site (e.g., "RBWH Resuscitation Audit") with appropriate permissions:

- **Owners:** MERT Educators, System Administrators
- **Members:** Service Line Managers (edit own service line data)
- **Visitors:** Auditors (contribute to Audit list only)

### 6.3 PowerApps Design Principles

1. **Offline Capability** - Enable offline mode for areas with poor connectivity
2. **Mobile First** - Primary use case is tablet/phone in clinical areas
3. **Progressive Disclosure** - Show sections as needed, not all at once
4. **Validation at Entry** - Prevent invalid data before submission
5. **Save Draft** - Allow partial completion and return later

### 6.4 Data Retention

- **Audit Records:** Retain indefinitely (regulatory requirement)
- **Draft Audits:** Auto-delete after 30 days if not submitted
- **Photos:** Retain for 2 years, then archive/delete
- **Maintenance Logs:** Retain for 5 years after resolution

---

## Appendix A: Equipment Master List

### A.1 Standard Trolley - Top

| Item | S4HANA Code | Qty | Supplier |
|------|-------------|-----|----------|
| Bag-Valve-Mask Resuscitator with medium face mask | CELS | 1 | CELS |
| Box of gloves (medium) | 10019022 | 1 | Ward Stock |
| Razor | 10015626 | 1 | Ward Stock |
| Alcohol foam antiseptic handrub | PHARMACY | 1 | Pharmacy |

*[Continue for all items from equipment list PDF]*

### A.2 Paediatric Box

| Item | S4HANA Code | Qty | Notes |
|------|-------------|-----|-------|
| Paediatric Bag-Valve-Mask Resuscitator with Toddler face mask | 10054728 | 1 | |
| Disposable face mask (Infant 0) | 000252952 | 1 | |
| Paediatric Non-Rebreather mask | 10060733 | 1 | |
| Y suction catheter size 8FG | 10032481 | 1 | |
| Infant Bag-Valve-Mask with Neonate face mask | 10054100 | 1 | Depts seeing neonates only |
| Infant/Child 0-25kg defibrillator pads (Bright Pink) | CELS | 1 | LIFEPAK 1000 AED |
| Quick-Combo RTS 0-15kg defibrillator pads (Salmon Pink) | CELS | 1 | LIFEPAK 20/20e - Hyperbaric only |

---

## Appendix B: Service Line Reference

| Abbreviation | Full Name | Contact |
|--------------|-----------|---------|
| IMS | Internal Medicine Services | |
| S&P | Surgical & Perioperative Services | |
| CCS | Cancer Care Services | |
| WNBS | Women's & Newborn Services | |
| CC&CSS | Critical Care & Clinical Support Services | |
| MH | Mental Health | |
| AH | Allied Health | |

---

## Appendix C: Document Version Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | [To be completed] | Initial specification |

---

**Document prepared for:** RBWH Medical Emergency Response Team  
**Contact:** MERT Nurse Educator #70106 or #70108
