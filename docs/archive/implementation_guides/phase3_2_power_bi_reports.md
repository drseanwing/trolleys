# Phase 3.2: Power BI Reports Implementation Guide
## REdI Trolley Audit System

**Version:** 1.0
**Date:** January 2026
**Status:** Implementation Guide
**Scope:** Tasks 3.2.1-3.2.16 - Power BI Workspace, Data Model, DAX Measures, and Report Visualizations

---

## Table of Contents

1. [Overview](#overview)
2. [Phase 3.2 Task Breakdown](#phase-32-task-breakdown)
3. [Workspace Setup](#workspace-setup)
4. [Data Model & Relationships](#data-model--relationships)
5. [DAX Measures & Calculated Columns](#dax-measures--calculated-columns)
6. [Compliance Reports](#compliance-reports)
7. [Issue Reports](#issue-reports)
8. [Integration & Publishing](#integration--publishing)
9. [Verification Checklist](#verification-checklist)

---

## Overview

Phase 3.2 delivers enterprise-grade Power BI analytics for the REdI Trolley Audit system. This phase transforms SharePoint data into actionable dashboards enabling real-time compliance monitoring, trend analysis, and issue tracking across all trolley locations.

**Objectives:**
- Establish Power BI workspace and data connectivity
- Build dimensional data model from normalized SharePoint lists
- Create DAX measures for compliance calculations
- Deliver 8 report pages with 16 distinct visualizations
- Embed Power BI reports in PowerApps and SharePoint

**Deliverables:**
- Power BI workspace with configured data refresh
- Data model with 5 relationship chains
- 25+ DAX measures and calculated columns
- 8 report pages (4 compliance, 3 issue, 1 integration)
- Published to app workspace with Row-Level Security (RLS)

---

## Phase 3.2 Task Breakdown

### Tasks 3.2.1-3.2.3: Workspace Setup (15 days)

| Task | Description | Duration | Owner |
|------|-------------|----------|-------|
| 3.2.1 | Create Power BI workspace and enable premium capacity | 3 days | BI Administrator |
| 3.2.2 | Connect to SharePoint lists and configure refresh schedule | 5 days | Power BI Developer |
| 3.2.3 | Define data model relationships and validate data quality | 7 days | Data Architect |

**Deliverables:**
- Power BI workspace in app.powerbi.com
- Data model with all 5 relationship chains defined
- Automated daily refresh schedule
- Data quality validation report

---

### Tasks 3.2.4-3.2.8: Compliance Reports (20 days)

| Task | Chart Type | Description | Duration |
|------|-----------|-------------|----------|
| 3.2.4 | Line Chart | Compliance trend (monthly over 12 months) | 4 days |
| 3.2.5 | Clustered Bar Chart | Service line comparison with avg compliance | 3 days |
| 3.2.6 | Clustered Bar Chart | Building comparison with compliance variance | 3 days |
| 3.2.7 | Heatmap Calendar | Audit activity by date (last 90 days) | 5 days |
| 3.2.8 | Histogram | Days since audit distribution | 5 days |

**Deliverables:**
- 5 visual specifications
- Page 1: Compliance Trends dashboard
- Page 2: Location Performance dashboard

---

### Tasks 3.2.9-3.2.12: Issue Reports (18 days)

| Task | Chart Type | Description | Duration |
|------|-----------|-------------|----------|
| 3.2.9 | Pie Chart | Issues by category (Equipment/Doc/Condition/Compliance) | 3 days |
| 3.2.10 | Pie Chart | Issues by severity (Critical/High/Medium/Low) | 3 days |
| 3.2.11 | Stacked Bar Chart | Issue aging (0-7, 8-14, 15-30, 31-60, 60+ days) | 4 days |
| 3.2.12 | Matrix Table | Equipment deficiency (top 20 missing items) | 5 days |
| | KPI Cards | Issue metrics (open count, avg age, critical count) | 3 days |

**Deliverables:**
- 5 visual specifications
- Page 3: Issue Summary dashboard
- Page 4: Issue Aging & Details dashboard

---

### Tasks 3.2.13-3.2.16: Integration & Publishing (20 days)

| Task | Description | Duration | Owner |
|------|-------------|----------|-------|
| 3.2.13 | Create trolley detail page with full audit history | 5 days | Power BI Developer |
| 3.2.14 | Implement dynamic filters (service line, date range, building) | 4 days | Power BI Developer |
| 3.2.15 | Publish to workspace and configure Row-Level Security | 5 days | BI Administrator |
| 3.2.16 | Embed Power BI in PowerApp and create Power BI tile | 6 days | Power BI/PowerApps Developer |

**Deliverables:**
- Page 5: Trolley Detail page
- Shared dataset with RLS rules
- Power BI tiles embedded in PowerApp
- User acceptance testing complete

---

## Workspace Setup

### Task 3.2.1: Create Power BI Workspace

**Prerequisites:**
- Power BI Premium capacity or Pro licenses assigned to users
- Power BI Service access (app.powerbi.com)
- Service Principal configured for automated refresh (optional but recommended)

**Steps:**

1. **Create Workspace**
   ```
   Power BI Service > Workspaces > Create a workspace
   Name: "REdI Trolley Audit Reports"
   Description: "Enterprise dashboards for resuscitation trolley audits"
   License mode: Premium per user (or Premium capacity if available)
   ```

2. **Configure Workspace Roles**
   ```
   Members:
   - MERT Educators → Admin
   - BI Administrator → Admin
   - Service Line Managers → Contributor
   - Clinical Staff → Viewer
   - Leadership → Viewer
   ```

3. **Enable Features**
   - Enable "Workspace New Look" for modern interface
   - Configure workspace refresh schedule
   - Enable dataflow support for advanced transformations

4. **Security Groups Setup**
   ```
   Azure AD Security Groups (created in advance):
   - MERT.Educators@rbwh.health.qld.gov.au
   - ClinicianAuditors@rbwh.health.qld.gov.au
   - Leadership.Reporting@rbwh.health.qld.gov.au
   ```

5. **Capacity Planning**
   ```
   Estimated Load:
   - 76 active trolley locations
   - ~500 audits/year (annual comprehensive + weekly spot checks)
   - ~200 open issues at any time
   - 100+ concurrent viewers during peak hours

   Recommended: Premium capacity (P1) or minimum 10 Pro licenses
   ```

**Success Criteria:**
- Workspace created and accessible
- All users assigned to correct roles
- Workspace settings configured

---

### Task 3.2.2: Connect to SharePoint Lists

**Data Sources:**
1. Location (76 records)
2. Audit (500+ records)
3. AuditEquipment (50,000+ item records)
4. Equipment (200+ items)
5. ServiceLine (15+ records)
6. Issue (200+ records)
7. CorrectiveAction (300+ records)

**Connection Steps:**

1. **Create Power BI Desktop Project**
   ```
   File > New Report
   Name: "REdI Trolley Audit Analytics"
   Save to: Local workspace with version control
   ```

2. **Connect to SharePoint Site**
   ```
   Home > Get Data > SharePoint Online

   Site URL: https://rbwh.sharepoint.com/sites/TrolleyAuditSystem
   (Use your actual SharePoint site URL)

   Select tables:
   ✓ Location
   ✓ Audit
   ✓ AuditEquipment
   ✓ Equipment
   ✓ ServiceLine
   ✓ Issue
   ✓ CorrectiveAction
   ```

3. **Load Data in Power Query**
   ```
   For each table, configure:
   - Data type validation
   - Remove system columns (ID, ContentType, etc.)
   - Create helper columns for relationships
   - Date/Time timezone normalization

   Refresh strategy: Direct Query or Import (recommended: Import with 1-day refresh)
   ```

4. **Data Transformation Rules**

   **Location Table:**
   ```
   - Rename [Title] → LocationName
   - Create DaysSinceAudit = INT((TODAY() - [LastAuditDate])/86400)
   - Create ComplianceStatus = IF([LastAuditCompliance] >= 0.95, "Excellent",
                                   IF([LastAuditCompliance] >= 0.80, "Compliant",
                                   IF([LastAuditCompliance] >= 0.60, "At Risk", "Non-Compliant")))
   - Sort by ServiceLine, Building
   ```

   **Audit Table:**
   ```
   - Rename [Title] → AuditReference
   - Create CompliancePercentage = [OverallCompliance] * 100
   - Create AuditMonth = DATE(YEAR([CompletedDateTime]), MONTH([CompletedDateTime]), 1)
   - Create AuditQuarter = DATE(YEAR([CompletedDateTime]), INT((MONTH([CompletedDateTime])-1)/3)*3+1, 1)
   - Filter: SubmissionStatus = "Submitted" or "Verified"
   ```

   **AuditEquipment Table:**
   ```
   - Create ComplianceFlag = IF([IsCompliant] = true, 1, 0)
   - Create IssueSeverity = IF([QuantityVariance] < -3, "Critical",
                              IF([QuantityVariance] < -1, "High",
                              IF([QuantityVariance] < 0, "Medium", "None")))
   ```

   **Issue Table:**
   ```
   - Create IssueDaysOpen = INT((TODAY() - [ReportedDate])/86400)
   - Create AgeGroup = IF([IssueDaysOpen] <= 7, "0-7 days",
                          IF([IssueDaysOpen] <= 14, "8-14 days",
                          IF([IssueDaysOpen] <= 30, "15-30 days",
                          IF([IssueDaysOpen] <= 60, "31-60 days", "60+ days"))))
   - Create IsCritical = IF([Severity] = "Critical", 1, 0)
   - Filter: Status <> "Closed"
   ```

5. **Load to Power BI**
   ```
   Close and Apply
   (Data loads into data model)
   ```

6. **Configure Refresh Schedule**
   ```
   Power BI Service:
   Dataset > Schedule refresh

   Refresh frequency: Daily
   Refresh time: 02:00 AM (AEST) - off-peak hours
   Notification: Email on failure

   Alternative (if using Service Principal):
   Configure incremental refresh for AuditEquipment (>1M rows)
   ```

**Success Criteria:**
- All 7 tables loaded
- No data quality errors
- Refresh completes successfully daily
- Data updated within 24 hours

---

### Task 3.2.3: Define Data Model Relationships

**Current State Analysis:**
```
Disconnected tables from SharePoint will load as independent queries.
All foreign keys are text/GUID fields pointing to list titles.
Need to establish star schema with proper relationships.
```

**Relationship Configuration:**

#### Relationship 1: Location ↔ ServiceLine (Many-to-One)

```
From Table: Location
From Column: ServiceLine (Lookup field text)

To Table: ServiceLine
To Column: Title

Relationship Properties:
- Relationship Type: Single direction (many-to-one)
- Cross-filter direction: Single (filters FROM ServiceLine TO Location)
- Assume referential integrity: YES
- Active: YES
```

#### Relationship 2: Location → Audit (One-to-Many)

```
From Table: Location
From Column: LocationName

To Table: Audit
To Column: Location (Lookup field text)

Relationship Properties:
- Relationship Type: Single direction (one-to-many)
- Cross-filter direction: Single (filters FROM Location TO Audit)
- Assume referential integrity: YES
- Active: YES
```

#### Relationship 3: Audit → AuditEquipment (One-to-Many)

```
From Table: Audit
From Column: AuditReference

To Table: AuditEquipment
To Column: Audit (Lookup field)

Relationship Properties:
- Relationship Type: Single direction (one-to-many)
- Cross-filter direction: Single
- Assume referential integrity: YES
- Active: YES
```

#### Relationship 4: Equipment ↔ AuditEquipment (Many-to-One)

```
From Table: Equipment
From Column: ItemName

To Table: AuditEquipment
To Column: Equipment (Lookup field)

Relationship Properties:
- Relationship Type: Single direction (many-to-one)
- Cross-filter direction: Single
- Assume referential integrity: YES
- Active: YES
```

#### Relationship 5: Location ↔ Issue (One-to-Many)

```
From Table: Location
From Column: LocationName

To Table: Issue
To Column: Location (Lookup field)

Relationship Properties:
- Relationship Type: Single direction (one-to-many)
- Cross-filter direction: Single
- Assume referential integrity: YES
- Active: YES
```

#### Relationship 6: Issue → CorrectiveAction (One-to-Many)

```
From Table: Issue
From Column: IssueNumber

To Table: CorrectiveAction
To Column: IssueId (Lookup or text)

Relationship Properties:
- Relationship Type: Single direction (one-to-many)
- Cross-filter direction: Single
- Assume referential integrity: YES
- Active: YES
```

**Create Date Dimension Table (Best Practice)**

```M
// Power Query: Create Calendar Table
let
    MinDate = List.Min(#"Audit"[CompletedDateTime]),
    MaxDate = List.Max(#"Audit"[CompletedDateTime]),

    DateList = List.Dates(
        DateTime.Date(MinDate),
        Number.From(DateTime.Date(MaxDate) - DateTime.Date(MinDate)) + 1,
        #duration(1, 0, 0, 0)
    ),

    DateTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),

    AddYear = Table.AddColumn(DateTable, "Year", each Date.Year([Date])),
    AddMonth = Table.AddColumn(AddYear, "Month", each Date.Month([Date])),
    AddDay = Table.AddColumn(AddMonth, "Day", each Date.Day([Date])),
    AddQuarter = Table.AddColumn(AddDay, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date]))),
    AddMonthName = Table.AddColumn(AddQuarter, "MonthName", each Date.ToText([Date], "MMMM")),
    AddWeekday = Table.AddColumn(AddMonthName, "Weekday", each Date.DayOfWeekName([Date])),
    AddWeekNum = Table.AddColumn(AddWeekday, "WeekNumber", each Date.WeekOfYear([Date]))

in
    AddWeekNum
```

**Relationship: Audit → Date (One-to-Many)**

```
From Table: Date
From Column: Date

To Table: Audit
To Column: CompletedDateTime (converted to Date)

Relationship Properties:
- Active: YES (use for time series)
```

**Data Model Diagram (Final State)**

```
┌─────────────────────────────────────────────────────────────────┐
│                    POWER BI DATA MODEL                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│        ┌─────────────┐                                          │
│        │  ServiceLine│◄─────────────┐                           │
│        └─────────────┘              │ 1:M                       │
│                                     │                           │
│    ┌───────────────────────────────┴────────────────────────┐   │
│    │                                                        │   │
│    ▼                                                        ▼   │
│ ┌──────────┐                    ┌─────────────────┐     ┌──────┐
│ │Location  │───1:M─────────────►│     Audit       │◄────│ Date │
│ └──────────┘                    └─────────────────┘     └──────┘
│    │                                   │
│    │ 1:M                           1:M │
│    │                                   ▼
│    │                          ┌──────────────────┐
│    │                          │ AuditEquipment   │
│    │                          └──────────────────┘
│    │                                   │
│    │                               M:1 │
│    │                                   ▼
│    │                          ┌──────────────────┐
│    │                          │    Equipment     │
│    │                          └──────────────────┘
│    │
│    │ 1:M
│    └──────────────────┐
│                       ▼
│                   ┌───────────┐
│                   │   Issue   │
│                   └─────┬─────┘
│                         │ 1:M
│                         ▼
│                   ┌──────────────────┐
│                   │CorrectiveAction  │
│                   └──────────────────┘
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Data Quality Validation**

```DAX
// Create validation table (for Power BI service)
1. Check referential integrity:
   - Count(Audit.Location) = all locations exist in Location table
   - Count(AuditEquipment.Audit) = all audits exist in Audit table
   - Count(Issue.Location) = all locations exist in Location table

2. Completeness checks:
   - Location: 100% have ServiceLine (required)
   - Audit: 100% have Location, AuditType, Auditor
   - Issue: 100% have IssueCategory, Severity, ReportedDate

3. Range checks:
   - Audit.OverallCompliance: 0-100%
   - AuditEquipment.QuantityFound: >= 0
   - Issue.IssueDaysOpen: >= 0

4. Uniqueness checks:
   - Location.LocationName: All unique
   - Audit.AuditReference: All unique (format AUD-YYYY-NNNN)
```

**Success Criteria:**
- All 6 relationships established and active
- Date dimension created with calendar hierarchy
- Data quality validation passed 100%
- No orphaned records (Audit with missing Location, etc.)
- Star schema properly normalized

---

## Data Model & Relationships

### Dimensional Analysis

**Fact Tables:**
- Audit (500+ rows) - Central fact table
- AuditEquipment (50,000+ rows) - Detail fact table
- Issue (200+ rows) - Secondary fact table
- CorrectiveAction (300+ rows) - Action fact table

**Dimension Tables:**
- Location (76 rows) - Conformed dimension
- ServiceLine (15+ rows) - Conformed dimension
- Equipment (200+ rows) - Slowly changing dimension
- Date (1,825 rows) - Standard date dimension

**Grain of Facts:**
- **Audit:** One row per audit event (Location, DateTime, Scores)
- **AuditEquipment:** One row per equipment item per audit
- **Issue:** One row per issue (Location, Category, Severity)
- **CorrectiveAction:** One row per action taken on an issue

### Relationship Rules

| From | To | Type | Cardinality | Active | Filter Direction |
|------|----|----|------------|--------|------------------|
| ServiceLine | Location | M:1 | M-1 | Yes | Single |
| Location | Audit | 1:M | 1-* | Yes | Single |
| Audit | AuditEquipment | 1:M | 1-* | Yes | Single |
| Equipment | AuditEquipment | M:1 | *-1 | Yes | Single |
| Location | Issue | 1:M | 1-* | Yes | Single |
| Issue | CorrectiveAction | 1:M | 1-* | Yes | Single |
| Date | Audit | 1:M | 1-* | Yes | Single |

---

## DAX Measures & Calculated Columns

### Calculated Columns (Created in Power Query or DAX)

#### Location Table Additions

```DAX
// Column: Audit Priority Score (for random selection)
AuditPriorityScore =
CALCULATE(
    BLANK(),
    IF(Location[LastAuditDate] = BLANK(), 1000,
    IF(Location[DaysSinceLastAudit] > 365, 500 + Location[DaysSinceLastAudit],
    IF(Location[DaysSinceLastAudit] > 180, 200 + Location[DaysSinceLastAudit],
    IF(Location[DaysSinceLastAudit] > 90, 100 + Location[DaysSinceLastAudit],
    Location[DaysSinceLastAudit]))))
)

// Column: Compliance Trend Status
ComplianceStatus =
IF(Location[LastAuditCompliance] >= 0.95, "Excellent",
IF(Location[LastAuditCompliance] >= 0.80, "Compliant",
IF(Location[LastAuditCompliance] >= 0.60, "At Risk", "Non-Compliant")))

// Column: Audit Status
AuditStatus =
IF(Location[Status] = "Inactive", "Inactive",
IF(Location[LastAuditDate] = BLANK(), "Never Audited",
IF(Location[DaysSinceLastAudit] <= 30, "Recently Audited",
IF(Location[DaysSinceLastAudit] <= 90, "Upcoming Due",
IF(Location[DaysSinceLastAudit] <= 180, "Approaching Overdue", "Overdue")))))
```

#### Audit Table Additions

```DAX
// Column: Audit Month (for time series)
AuditMonth =
FORMAT(Audit[CompletedDateTime], "MMMM YYYY")

// Column: Audit Month Date (for sorting)
AuditMonthDate =
DATE(YEAR(Audit[CompletedDateTime]), MONTH(Audit[CompletedDateTime]), 1)

// Column: Audit Quarter
AuditQuarter =
"Q" & Text.From(QUARTER(Audit[CompletedDateTime])) & " " & Text.From(YEAR(Audit[CompletedDateTime]))

// Column: Days to Complete
DaysToComplete =
DATEDIF(Audit[StartedDateTime], Audit[CompletedDateTime], "D")

// Column: Compliance Bucket
ComplianceBucket =
IF(Audit[OverallCompliance] >= 0.95, "95-100%",
IF(Audit[OverallCompliance] >= 0.80, "80-94%",
IF(Audit[OverallCompliance] >= 0.60, "60-79%", "Below 60%")))

// Column: Requires Follow Up Flag
IsFollowUpRequired =
IF(Audit[OverallCompliance] < 0.80, 1, 0)
```

#### Issue Table Additions

```DAX
// Column: Issue Days Open
IssueDaysOpen =
IF(Issue[Status] = "Closed",
    DATEDIF(Issue[ReportedDate], Issue[ClosedDate], "D"),
    DATEDIF(Issue[ReportedDate], TODAY(), "D"))

// Column: Issue Age Group
IssueAgeGroup =
IF(Issue[IssueDaysOpen] <= 7, "0-7 days",
IF(Issue[IssueDaysOpen] <= 14, "8-14 days",
IF(Issue[IssueDaysOpen] <= 30, "15-30 days",
IF(Issue[IssueDaysOpen] <= 60, "31-60 days", "60+ days"))))

// Column: Is Overdue
IsOverdue =
IF(Issue[Status] <> "Closed" AND Issue[IssueDaysOpen] > 30, 1, 0)

// Column: Is Critical
IsCritical =
IF(Issue[Severity] = "Critical", 1, 0)

// Column: Escalation Flag
NeedsEscalation =
IF(Issue[IssueDaysOpen] > 7 AND Issue[Status] <> "Closed", 1, 0)
```

#### AuditEquipment Table Additions

```DAX
// Column: Is Equipment Compliant
IsEquipmentCompliant =
IF(AuditEquipment[QuantityFound] >= AuditEquipment[QuantityExpected], 1, 0)

// Column: Equipment Variance
EquipmentVariance =
AuditEquipment[QuantityFound] - AuditEquipment[QuantityExpected]

// Column: Shortage Severity
ShortageSeverity =
IF(AuditEquipment[EquipmentVariance] >= 0, "Compliant",
IF(AuditEquipment[EquipmentVariance] = -1, "Minor",
IF(AuditEquipment[EquipmentVariance] <= -3, "Critical", "Moderate")))
```

---

### DAX Measures (For Report Visualizations)

#### Compliance Measures

```DAX
// Measure: Average Compliance Score (Overall)
Average Compliance =
CALCULATE(
    AVERAGE(Audit[OverallCompliance]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Average Compliance This Month
Average Compliance (This Month) =
CALCULATE(
    [Average Compliance],
    MONTH(Audit[CompletedDateTime]) = MONTH(TODAY()),
    YEAR(Audit[CompletedDateTime]) = YEAR(TODAY())
)

// Measure: Average Compliance Previous Month
Average Compliance (Previous Month) =
CALCULATE(
    [Average Compliance],
    MONTH(Audit[CompletedDateTime]) = MONTH(TODAY()) - 1,
    YEAR(Audit[CompletedDateTime]) = YEAR(TODAY())
)

// Measure: Compliance Trend (Month over Month)
Compliance MoM Change =
[Average Compliance (This Month)] - [Average Compliance (Previous Month)]

// Measure: Locations Meeting Target (>80%)
Locations Meeting Target =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[LastAuditCompliance] >= 0.80
)

// Measure: Total Active Locations
Total Active Locations =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[Status] = "Active"
)

// Measure: Percentage Meeting Target
% Meeting Target =
IF([Total Active Locations] = 0, 0,
DIVIDE([Locations Meeting Target], [Total Active Locations]))

// Measure: Average Equipment Score
Average Equipment Score =
CALCULATE(
    AVERAGE(Audit[EquipmentScore]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Average Documentation Score
Average Documentation Score =
CALCULATE(
    AVERAGE(Audit[DocumentationScore]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Average Condition Score
Average Condition Score =
CALCULATE(
    AVERAGE(Audit[ConditionScore]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Average Checks Score
Average Checks Score =
CALCULATE(
    AVERAGE(Audit[ChecksScore]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)
```

#### Audit Activity Measures

```DAX
// Measure: Total Audits Completed
Total Audits =
CALCULATE(
    COUNTA(Audit[Title]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Audits This Year
Audits This Year =
CALCULATE(
    [Total Audits],
    YEAR(Audit[CompletedDateTime]) = YEAR(TODAY())
)

// Measure: Audits Last Year
Audits Last Year =
CALCULATE(
    [Total Audits],
    YEAR(Audit[CompletedDateTime]) = YEAR(TODAY()) - 1
)

// Measure: Audits This Month
Audits This Month =
CALCULATE(
    [Total Audits],
    MONTH(Audit[CompletedDateTime]) = MONTH(TODAY()),
    YEAR(Audit[CompletedDateTime]) = YEAR(TODAY())
)

// Measure: Audits Last 7 Days
Audits Last 7 Days =
CALCULATE(
    [Total Audits],
    Audit[CompletedDateTime] >= TODAY() - 7
)

// Measure: Audit Completion Rate (%)
Audit Completion Rate =
DIVIDE(
    CALCULATE([Total Audits], MONTH(Audit[CompletedDateTime]) = MONTH(TODAY())),
    CALCULATE(DISTINCTCOUNT(Location[LocationName]), Location[Status] = "Active")
) * 100

// Measure: Average Days to Complete Audit
Average Days to Complete =
CALCULATE(
    AVERAGE(Audit[DaysToComplete]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Comprehensive Audits Count
Comprehensive Audits =
CALCULATE(
    COUNTA(Audit[Title]),
    Audit[AuditType] = "Comprehensive",
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Spot Check Audits Count
Spot Check Audits =
CALCULATE(
    COUNTA(Audit[Title]),
    Audit[AuditType] = "SpotCheck",
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Follow Up Audits Count
Follow Up Audits =
CALCULATE(
    COUNTA(Audit[Title]),
    Audit[AuditType] = "FollowUp",
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Audits Requiring Follow Up
Audits Requiring Follow Up =
CALCULATE(
    COUNTA(Audit[Title]),
    Audit[RequiresFollowUp] = TRUE,
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)
```

#### Issue Measures

```DAX
// Measure: Total Open Issues
Total Open Issues =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[Status] <> "Closed"
)

// Measure: Critical Issues
Critical Issues =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[Severity] = "Critical",
    Issue[Status] <> "Closed"
)

// Measure: High Priority Issues
High Priority Issues =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[Severity] IN {"High", "Critical"},
    Issue[Status] <> "Closed"
)

// Measure: Overdue Issues
Overdue Issues =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueDaysOpen] > 30,
    Issue[Status] <> "Closed"
)

// Measure: Average Issue Age (Days)
Average Issue Age =
CALCULATE(
    AVERAGE(Issue[IssueDaysOpen]),
    Issue[Status] <> "Closed"
)

// Measure: Issues Resolved This Month
Issues Resolved This Month =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    MONTH(Issue[ClosedDate]) = MONTH(TODAY()),
    YEAR(Issue[ClosedDate]) = YEAR(TODAY()),
    Issue[Status] = "Closed"
)

// Measure: Issues by Category - Equipment
Issues Equipment =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueCategory] = "Equipment",
    Issue[Status] <> "Closed"
)

// Measure: Issues by Category - Documentation
Issues Documentation =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueCategory] = "Documentation",
    Issue[Status] <> "Closed"
)

// Measure: Issues by Category - Condition
Issues Condition =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueCategory] = "Condition",
    Issue[Status] <> "Closed"
)

// Measure: Issues by Category - Compliance
Issues Compliance =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueCategory] = "Compliance",
    Issue[Status] <> "Closed"
)

// Measure: Average Resolution Time (Days)
Average Resolution Time =
CALCULATE(
    AVERAGE(Issue[IssueDaysOpen]),
    Issue[Status] = "Closed"
)

// Measure: Issue Escalation Count
Escalated Issues =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[EscalationLevel] > 0,
    Issue[Status] <> "Closed"
)

// Measure: % Issues Resolved Within Target
Resolved Within Target % =
DIVIDE(
    CALCULATE([Issues Resolved This Month], Issue[IssueDaysOpen] <= 30),
    [Issues Resolved This Month]
)
```

#### Equipment Deficiency Measures

```DAX
// Measure: Total Equipment Items Checked
Total Equipment Checked =
COUNTA(AuditEquipment[Title])

// Measure: Total Compliant Equipment
Compliant Equipment =
CALCULATE(
    COUNTA(AuditEquipment[Title]),
    AuditEquipment[IsEquipmentCompliant] = 1
)

// Measure: Non-Compliant Equipment
Non-Compliant Equipment =
CALCULATE(
    COUNTA(AuditEquipment[Title]),
    AuditEquipment[IsEquipmentCompliant] = 0
)

// Measure: Equipment Compliance Rate (%)
Equipment Compliance Rate =
DIVIDE([Compliant Equipment], [Total Equipment Checked]) * 100

// Measure: Total Equipment Shortages
Total Equipment Shortages =
CALCULATE(
    SUM(AuditEquipment[EquipmentVariance]),
    AuditEquipment[EquipmentVariance] < 0
)

// Measure: Most Common Missing Item (Text)
Most Missing Item =
MAXX(
    TOPN(1, VALUES(AuditEquipment[Equipment]),
    CALCULATE(COUNT(AuditEquipment[EquipmentVariance]),
    AuditEquipment[EquipmentVariance] < 0), 1),
    AuditEquipment[Equipment]
)

// Measure: Count of Item Shortages
Count Item Shortages =
CALCULATE(
    COUNTA(AuditEquipment[Equipment]),
    AuditEquipment[EquipmentVariance] < 0
)

// Measure: Average Shortage Quantity
Average Shortage Amount =
CALCULATE(
    AVERAGE(AuditEquipment[EquipmentVariance]),
    AuditEquipment[EquipmentVariance] < 0
)
```

#### Service Line & Location Measures

```DAX
// Measure: Service Lines with Data
Total Service Lines =
DISTINCTCOUNT(ServiceLine[Title])

// Measure: Average Compliance by Service Line
Average Compliance by SL =
CALCULATE(
    AVERAGE(Location[LastAuditCompliance]),
    Location[Status] = "Active"
)

// Measure: Locations Per Service Line
Locations Per SL =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[Status] = "Active"
)

// Measure: Never Audited Count
Never Audited =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[LastAuditDate] = BLANK(),
    Location[Status] = "Active"
)

// Measure: Overdue Audit Count (>180 days)
Overdue Audit Count =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[DaysSinceLastAudit] > 180,
    Location[Status] = "Active"
)

// Measure: Days Since Last Audit (Max)
Max Days Without Audit =
MAXX(ALLSELECTED(Location), Location[DaysSinceLastAudit])

// Measure: Days Since Last Audit (Min)
Min Days Without Audit =
MINX(ALLSELECTED(Location), Location[DaysSinceLastAudit])

// Measure: Average Days Since Audit
Average Days Since Audit =
CALCULATE(
    AVERAGE(Location[DaysSinceLastAudit]),
    Location[Status] = "Active",
    Location[LastAuditDate] <> BLANK()
)
```

---

## Compliance Reports

### Task 3.2.4: Compliance Trend Line Chart (Page 1)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Line Chart with Area Fill |
| X-Axis (Category) | AuditMonthDate (from Audit table) |
| Y-Axis (Value) | Average Compliance measure |
| Legend | Audit Type (Comprehensive, SpotCheck, FollowUp) |
| Data Period | Last 12 months |
| Formatting | Green line (>85%), Amber line (70-85%), Red line (<70%) |

**DAX Measures Used:**
- Average Compliance
- Average Compliance (This Month)
- Average Compliance (Previous Month)
- Compliance MoM Change

**DAX Measure: Compliance Trend Calculation**

```DAX
// Supporting measure for trend line
Compliance Trend =
VAR CurrentMonth = MONTH(TODAY())
VAR CurrentYear = YEAR(TODAY())
VAR SelectionMonth = MONTH([AuditMonth])
VAR SelectionYear = YEAR([AuditMonth])
RETURN
CALCULATE(
    AVERAGE(Audit[OverallCompliance]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)
```

**Configuration Steps:**

1. **Add Line Chart to Report Canvas**
   ```
   Visualizations > Line Chart
   Size: 50% width, 400px height
   Position: Top-left of page
   ```

2. **Configure Axes**
   ```
   X-Axis (Category):
   - Field: Audit[CompletedDateTime]
   - Group by: Month/Year
   - Sort by: Audit Month Date (ascending)

   Y-Axis (Values):
   - Field: [Average Compliance]
   - Format: Percentage (0 decimal places)
   - Min: 0%, Max: 100%
   ```

3. **Configure Line Properties**
   ```
   Series:
   - Line 1 (Comprehensive): Solid green, 3px width
   - Line 2 (SpotCheck): Solid blue, 2px width
   - Line 3 (FollowUp): Dashed orange, 2px width

   Enable area fill: Yes (25% transparency)
   Show data points: Yes (6px circles)
   ```

4. **Add Trend Analysis**
   ```
   Secondary Y-Axis (Optional):
   - Field: [Audits This Month]
   - Format: Whole number
   - Show as: Bar chart (light gray)
   ```

5. **Add Interactive Elements**
   ```
   Tooltip (hover):
   - Average Compliance (%)
   - Audit Count
   - Audits This Month

   Data Labels:
   - Show on end only
   - Format: 0 decimal places
   - Position: Above line
   ```

**Success Criteria:**
- Chart displays 12 months of data
- Trend direction clearly visible
- Multiple audit types shown in legend
- MoM change calculated and displayable

---

### Task 3.2.5: Service Line Comparison Bar Chart (Page 1)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Clustered Bar Chart |
| Category Axis | ServiceLine[Title] |
| Value Axis | Average Compliance measure |
| Columns | [Average Compliance] and [Locations Meeting Target %] |
| Color Encoding | Gradient (Red < 70%, Yellow 70-85%, Green > 85%) |
| Sorting | By Average Compliance (descending) |

**Configuration Steps:**

1. **Add Clustered Bar Chart**
   ```
   Visualizations > Clustered Bar Chart
   Size: 50% width (right side), 400px height
   Position: Top-right of page
   ```

2. **Configure Fields**
   ```
   Axis (Category):
   - Field: ServiceLine[Title]
   - Sort: By Average Compliance (descending)

   Legend:
   - Field: N/A (single metric)

   Values:
   - Field: [Average Compliance by SL]
   - Secondary: [Locations Per SL] (as count label)
   ```

3. **Add Data Labels**
   ```
   Label Position: Inside end
   Data Labels Display:
   - Value: {Average Compliance:%}
   - Category: ServiceLine name
   - Secondary label: N locations
   ```

4. **Color Formatting**
   ```
   Conditional Formatting: Background Color
   - Lowest: Red (#d13438)
   - Neutral: Yellow (#ffd34c) at 80%
   - Highest: Green (#107c10)
   - Field: [Average Compliance by SL]
   ```

5. **Add Drill-Down (Optional)**
   ```
   - Click service line → drill to Location detail page
   - Show audit trend for selected service line
   ```

**Success Criteria:**
- All service lines visible and sortable
- Compliance averages calculated per service line
- Visual comparison makes best/worst performers obvious
- Color encoding helps quick assessment

---

### Task 3.2.6: Building Comparison Bar Chart (Page 2)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Stacked Bar Chart |
| Category Axis | Location[Building] |
| Value Axis | Count of Locations |
| Stacking | By ComplianceStatus (Excellent/Compliant/AtRisk/NonCompliant) |
| Color Scheme | Traffic light (Green/Yellow/Orange/Red) |
| Display | Percentage stacked |

**DAX Measures for Compliance Status Breakdown**

```DAX
// Measure: Locations - Excellent Compliance
Locations Excellent =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[LastAuditCompliance] >= 0.95,
    Location[Status] = "Active"
)

// Measure: Locations - Compliant
Locations Compliant =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[LastAuditCompliance] >= 0.80,
    Location[LastAuditCompliance] < 0.95,
    Location[Status] = "Active"
)

// Measure: Locations - At Risk
Locations At Risk =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[LastAuditCompliance] >= 0.60,
    Location[LastAuditCompliance] < 0.80,
    Location[Status] = "Active"
)

// Measure: Locations - Non-Compliant
Locations Non-Compliant =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[LastAuditCompliance] < 0.60,
    Location[Status] = "Active"
)
```

**Configuration Steps:**

1. **Add Stacked Bar Chart**
   ```
   Visualizations > Stacked Bar Chart
   Size: 100% width, 400px height
   Position: Page 2, top
   ```

2. **Configure Fields**
   ```
   Axis (Category):
   - Field: Location[Building]

   Values (Stacked):
   - [Locations Excellent]
   - [Locations Compliant]
   - [Locations At Risk]
   - [Locations Non-Compliant]

   Format: 100% stacked bar (shows proportions)
   ```

3. **Color Mapping**
   ```
   Excellent: Dark Green (#107c10)
   Compliant: Light Green (#8ec642)
   At Risk: Orange (#ffb900)
   Non-Compliant: Red (#d13438)
   ```

4. **Labels and Tooltips**
   ```
   Data Labels: Inside, show percentages
   Tooltip:
   - Building name
   - Status breakdown (counts)
   - Total locations in building
   ```

5. **Interactive Filters**
   ```
   Add filter: Date Range (Last Audit Date)
   Add filter: Service Line (optional cross-filter)
   ```

**Success Criteria:**
- Buildings ranked by compliance status distribution
- Stacked bar visually shows status breakdown
- Easy to identify buildings needing attention

---

### Task 3.2.7: Audit Activity Calendar Heatmap (Page 2)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Matrix (Heat Map) |
| Rows | Date[Weekday] + Date[WeekNumber] |
| Columns | Date[MonthName] |
| Values | Count of Audits |
| Conditional Formatting | Heat map (light = few audits, dark = many) |
| Time Range | Last 90 days |

**Alternative: Custom Calendar Visual (via Power BI Visuals Store)**

If matrix doesn't provide desired calendar layout, use:
- "Calendar by Harikesh" (Power BI Visuals)
- Configuration: Heatmap mode, color by audit count

**DAX Measures:**

```DAX
// Measure: Audit Count for Calendar
Audit Count =
COUNTA(Audit[Title])

// Measure: Audit Activity Score (0-10 scale)
Activity Score =
VAR AuditCount = [Audit Count]
RETURN
IF(AuditCount = 0, 0,
IF(AuditCount <= 2, 2,
IF(AuditCount <= 5, 4,
IF(AuditCount <= 10, 6,
IF(AuditCount <= 15, 8, 10)))))

// Measure: Days with Audits (Count)
Days With Audits =
CALCULATE(
    DISTINCTCOUNT(Date[Date]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)
```

**Configuration Steps:**

1. **Add Matrix Visual**
   ```
   Visualizations > Matrix
   Size: 100% width, 350px height
   Position: Page 2, middle
   ```

2. **Configure Matrix**
   ```
   Rows:
   - Date[WeekNumber]
   - Date[Weekday]

   Columns:
   - Date[MonthName]
   - Date[Week]

   Values:
   - [Audit Count]
   ```

3. **Apply Heatmap Formatting**
   ```
   Conditional Formatting:
   - Field: [Audit Count]
   - Format: Background color
   - Lowest: Light blue (#cfe8ff)
   - Highest: Dark blue (#003d99)
   - Type: Color scale
   ```

4. **Add Data Labels**
   ```
   Cell values: Show audit counts
   Font size: 10pt
   Bold headers: Yes
   ```

5. **Filter to Last 90 Days**
   ```
   Date[Date] >= TODAY() - 90
   ```

**Success Criteria:**
- Calendar clearly shows audit distribution over 90 days
- Dark areas show high activity periods
- Day of week and week number visible
- Easy to spot patterns/gaps

---

### Task 3.2.8: Days Since Audit Histogram (Page 2)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Histogram Chart |
| Numeric Field | Location[DaysSinceLastAudit] |
| Bins | 10-15 bins (auto-calculated) |
| Y-Axis | Count of Locations |
| Color | Blue bars with gray outline |
| Target Line | 180 days (overdue threshold) |

**DAX Supporting Measures:**

```DAX
// Measure: Locations Analyzed
Locations Analyzed =
CALCULATE(
    DISTINCTCOUNT(Location[LocationName]),
    Location[Status] = "Active",
    Location[LastAuditDate] <> BLANK()
)

// Measure: Median Days Since Audit
Median Days Since Audit =
MEDIAN(Location[DaysSinceLastAudit])

// Measure: 25th Percentile
Percentile 25 =
PERCENTILE.INC(ALLSELECTED(Location[DaysSinceLastAudit]), 0.25)

// Measure: 75th Percentile
Percentile 75 =
PERCENTILE.INC(ALLSELECTED(Location[DaysSinceLastAudit]), 0.75)
```

**Configuration Steps:**

1. **Add Histogram Visual**
   ```
   Visualizations > Histogram
   Size: 100% width, 300px height
   Position: Page 2, bottom
   ```

2. **Configure Histogram**
   ```
   Numeric Field: Location[DaysSinceLastAudit]

   Histogram Properties:
   - Bin count: 12 (automatic)
   - Bin size: ~30 days per bin
   ```

3. **Add Reference Line (Overdue Threshold)**
   ```
   Analytics Pane > Reference Line
   - Value: 180 (days)
   - Label: "Overdue Threshold (180 days)"
   - Color: Red
   - Style: Dashed
   ```

4. **Add Percentile Reference Lines**
   ```
   Analytics > Reference Line
   - Percentile 25: Blue dashed, label "Q1"
   - Percentile 75: Blue dashed, label "Q3"
   - Median: Green solid, label "Median"
   ```

5. **Data Labels**
   ```
   Show on bars: Count of locations
   Format: Whole number
   ```

**Statistical Annotations**

```
Card Visual (Statistics):
- Mean: [Average Days Since Audit]
- Median: [Median Days Since Audit]
- Max: [Max Days Without Audit]
- Min: [Min Days Without Audit]
- Std Dev: (calculated)
- Locations Overdue: [Overdue Audit Count]
```

**Success Criteria:**
- Histogram clearly shows distribution of audit recency
- 180-day threshold line identifies overdue locations
- Distribution shape visible (left-skewed = good/recent audits)
- Percentiles help identify quartiles

---

## Issue Reports

### Task 3.2.9: Issues by Category Pie Chart (Page 3)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Pie Chart |
| Category | Issue[IssueCategory] |
| Values | Count of Issues |
| Data | Open issues only (Status <> "Closed") |
| Color Scheme | Custom (Equipment=Blue, Doc=Green, Condition=Orange, Compliance=Red) |
| Display | Percentage labels on slices |

**Configuration Steps:**

1. **Add Pie Chart**
   ```
   Visualizations > Pie Chart
   Size: 50% width (left), 350px height
   Position: Page 3, top-left
   ```

2. **Configure Pie Chart**
   ```
   Legend:
   - Field: Issue[IssueCategory]

   Values:
   - Field: [Total Open Issues] filtered by category

   Data Labels:
   - Show category names: Yes
   - Show percentages: Yes
   - Show counts: Yes (in tooltip)
   ```

3. **Apply Category Colors**
   ```
   Conditional Formatting > Shape fill
   - Equipment: Blue (#0078d4)
   - Documentation: Green (#107c10)
   - Condition: Orange (#ffb900)
   - Compliance: Red (#d13438)
   - Other: Gray (#738496)
   ```

4. **Add Tooltip Detail**
   ```
   Tooltip Fields:
   - Category (dimension)
   - Issue Count (measure)
   - Percentage of total
   - Average resolution time for category
   ```

5. **Configuration Validation**
   ```
   DAX Check:
   SUM([Issues Equipment] + [Issues Documentation] +
       [Issues Condition] + [Issues Compliance])
   = [Total Open Issues]
   ```

**Success Criteria:**
- Pie chart adds to 100%
- All 5 categories represented
- Largest category clearly visible
- Color coding consistent across all reports

---

### Task 3.2.10: Issues by Severity Pie Chart (Page 3)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Pie Chart |
| Category | Issue[Severity] |
| Values | Count of Open Issues |
| Color Scheme | Traffic Light (Critical=Red, High=Orange, Medium=Yellow, Low=Green) |
| Data Label | Count + percentage |

**Configuration Steps:**

1. **Add Second Pie Chart**
   ```
   Visualizations > Pie Chart
   Size: 50% width (right), 350px height
   Position: Page 3, top-right (adjacent to category pie)
   ```

2. **Configure Pie Chart**
   ```
   Legend:
   - Field: Issue[Severity]
   - Order: Critical → High → Medium → Low

   Values:
   - Field: [Total Open Issues] (context-aware by severity)
   ```

3. **Apply Severity Colors**
   ```
   - Critical: Dark Red (#8b0000)
   - High: Orange (#ff8c00)
   - Medium: Gold (#ffd700)
   - Low: Green (#228b22)
   ```

4. **Add Emphasis to Critical**
   ```
   - Highlight critical slice: Slightly exploded
   - Bold label
   - Enhanced tooltip showing context
   ```

5. **KPI Cards Alongside**
   ```
   Card 1: [Critical Issues] count (large number, red background)
   Card 2: [High Priority Issues] count (orange background)
   Card 3: [Total Open Issues] count (gray background)
   Card 4: [Average Issue Age] in days
   ```

**Success Criteria:**
- Severity distribution clearly visible
- Critical issues highlighted
- Color scheme matches organizational standards
- Total open issues matches from other pages

---

### Task 3.2.11: Issue Aging Bar Chart (Page 4)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Stacked Column Chart (inverted to bar for readability) |
| Category | Issue[IssueAgeGroup] (0-7, 8-14, 15-30, 31-60, 60+ days) |
| Stacks | By Severity (Critical/High/Medium/Low) |
| Values | Count of Issues |
| Color | Severity-based stacking |
| Sort | By age group (oldest first) |

**DAX Measures for Age Groups:**

```DAX
// Measure: Issues 0-7 Days Old
Issues 0-7 Days =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueDaysOpen] <= 7,
    Issue[Status] <> "Closed"
)

// Measure: Issues 8-14 Days Old
Issues 8-14 Days =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueDaysOpen] >= 8,
    Issue[IssueDaysOpen] <= 14,
    Issue[Status] <> "Closed"
)

// Measure: Issues 15-30 Days Old
Issues 15-30 Days =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueDaysOpen] >= 15,
    Issue[IssueDaysOpen] <= 30,
    Issue[Status] <> "Closed"
)

// Measure: Issues 31-60 Days Old
Issues 31-60 Days =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueDaysOpen] >= 31,
    Issue[IssueDaysOpen] <= 60,
    Issue[Status] <> "Closed"
)

// Measure: Issues 60+ Days Old
Issues 60 Plus Days =
CALCULATE(
    COUNTA(Issue[IssueNumber]),
    Issue[IssueDaysOpen] > 60,
    Issue[Status] <> "Closed"
)
```

**Configuration Steps:**

1. **Add Stacked Bar Chart**
   ```
   Visualizations > Stacked Bar Chart
   Size: 100% width, 350px height
   Position: Page 4, top
   ```

2. **Configure Chart**
   ```
   Axis (Category):
   - Field: Issue[IssueAgeGroup]
   - Sort: Custom order (0-7, 8-14, 15-30, 31-60, 60+)

   Values (Stacked by Severity):
   - [Issues Critical] (red)
   - [Issues High] (orange)
   - [Issues Medium] (yellow)
   - [Issues Low] (green)
   ```

3. **Color by Severity**
   ```
   - Critical: Red (#d13438)
   - High: Orange (#ff8c00)
   - Medium: Yellow (#ffd34c)
   - Low: Green (#107c10)
   ```

4. **Data Labels**
   ```
   Show on bars: Total count per age group
   Position: End of bar
   Format: Whole number

   Tooltip: Severity breakdown for selected age group
   ```

5. **Add Target Line (Optional)**
   ```
   Analytics > Reference Line
   - Value: 30 days (target resolution time)
   - Label: "Target Resolution"
   - Color: Blue dashed
   ```

**Success Criteria:**
- Age groups progress from newest to oldest
- Red sections (critical) visually prominent
- Easy to see issue aging pattern
- Escalation threshold (30 days) clearly marked

---

### Task 3.2.12: Equipment Deficiency Matrix Table (Page 4)

**Visual Specification:**

| Property | Value |
|----------|-------|
| Visual Type | Matrix Table (Top-N Visual) |
| Rows | Equipment[ItemName] (Top 20 by deficiency) |
| Column 1 | Shortage Count |
| Column 2 | Total Occurrences |
| Column 3 | Deficiency Rate (%) |
| Column 4 | Average Shortage Qty |
| Column 5 | Last Audit Date (item not found) |
| Sort | By deficiency count (descending) |

**DAX Measures for Equipment Deficiency:**

```DAX
// Measure: Equipment Deficiency Count
Equipment Deficiency Count =
CALCULATE(
    COUNTA(AuditEquipment[Equipment]),
    AuditEquipment[IsEquipmentCompliant] = 0
)

// Measure: Equipment Total Count
Equipment Total Count =
COUNTA(AuditEquipment[Equipment])

// Measure: Equipment Deficiency Rate (%)
Equipment Deficiency Rate =
DIVIDE([Equipment Deficiency Count], [Equipment Total Count]) * 100

// Measure: Equipment Average Shortage
Equipment Average Shortage =
CALCULATE(
    AVERAGE(AuditEquipment[EquipmentVariance]),
    AuditEquipment[IsEquipmentCompliant] = 0
)

// Measure: Equipment Criticality
Equipment Critical Count =
CALCULATE(
    COUNTA(AuditEquipment[Equipment]),
    AuditEquipment[IsEquipmentCompliant] = 0,
    Equipment[CriticalItem] = TRUE
)
```

**Configuration Steps:**

1. **Add Matrix Visual**
   ```
   Visualizations > Matrix
   Size: 100% width, 450px height
   Position: Page 4, bottom
   ```

2. **Configure Matrix Rows and Columns**
   ```
   Rows:
   - Equipment[ItemName] (TOPN: 20)
   - Sort by: [Equipment Deficiency Count] (descending)

   Values (Columns):
   - [Equipment Deficiency Count]
   - [Equipment Total Count]
   - [Equipment Deficiency Rate]
   - [Equipment Average Shortage]
   - Last audit date (min)
   ```

3. **Apply Conditional Formatting**
   ```
   Background Color on Deficiency Rate:
   - Red (0-10%): No color
   - Yellow (10-25%): Light yellow
   - Orange (25-50%): Orange
   - Red (50%+): Dark red

   Font Color on Critical Items:
   - If Equipment[CriticalItem] = TRUE: Bold red
   ```

4. **Add Data Bars**
   ```
   Column: [Equipment Deficiency Rate]
   - Add data bar: Orange gradient
   - Show values: Yes
   ```

5. **Row Totals**
   ```
   Show row totals: Top
   Row total label: "Most Deficient Items"
   ```

6. **Interactive Elements**
   ```
   Allow expansion: Yes (drill down by audit if needed)
   Tooltip: Equipment name, deficiency summary, supplier, category
   ```

**Success Criteria:**
- Top 20 deficient items ranked
- Deficiency rate clearly visible
- Critical items highlighted
- Trend visible (increasing/decreasing deficiencies)

---

## Integration & Publishing

### Task 3.2.13: Trolley Detail Report Page

**Visual Specification:**

**Page 5: Trolley Detail Dashboard**

**Layout:**
- Header section (trolley info cards)
- Audit history timeline
- Equipment checklist status
- Issues timeline
- Corrective actions log

**Card Section (Top)**

```
┌─────────────────────────────────────────────────────────────────┐
│ Trolley Detail: 7A North                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │Building: │  │Service:  │  │Status:   │  │Last Audit│        │
│  │James     │  │ICU       │  │Active    │  │45 days  │        │
│  │Mayne     │  │Services  │  │          │  │ago      │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Audit History Table**

```DAX
// Measure: Trolley Audit Count
Trolley Audit Count =
CALCULATE(
    COUNTA(Audit[Title]),
    Audit[SubmissionStatus] IN {"Submitted", "Verified"}
)

// Measure: Trolley Average Compliance (Last Audit)
Trolley Latest Compliance =
MAXX(
    TOPN(1, VALUES(Audit[CompletedDateTime]),
    Audit[CompletedDateTime], 0),
    Audit[OverallCompliance]
)

// Measure: Trolley Audit Trend (Last 3 Audits)
Trolley Trend =
IF(
    [Trolley Audit Count] < 2,
    "Insufficient data",
    "See audit history"
)
```

**Configuration Steps:**

1. **Create Trolley Selection Slicer**
   ```
   Visualizations > Slicer
   Field: Location[LocationName]
   Style: List with search
   Size: 20% of page width
   Position: Left sidebar
   ```

2. **Add Trolley Info Cards**
   ```
   Card 1: Department Name
   - Field: Location[DepartmentName]

   Card 2: Building
   - Field: Location[Building]

   Card 3: Last Compliance Score
   - Field: Location[LastAuditCompliance]
   - Format: Percentage
   - Color: Green if >80%, Red if <80%

   Card 4: Days Since Last Audit
   - Field: Location[DaysSinceLastAudit]
   - Format: Integer
   - Suffix: "days ago"

   Card 5: Total Audits
   - Field: [Trolley Audit Count]

   Card 6: Open Issues
   - Field: (Count of issues for this trolley)
   - Color: Red if >0
   ```

3. **Add Audit History Table**
   ```
   Visualizations > Table

   Columns:
   - Audit Date (CompletedDateTime)
   - Auditor Name
   - Audit Type (Comprehensive/SpotCheck/FollowUp)
   - Overall Compliance (%)
   - Equipment Score (%)
   - Documentation Score (%)
   - Issues Found

   Sorting: By date (descending - newest first)
   Conditional formatting: Compliance colors (green/yellow/red)
   ```

4. **Add Audit Trend Line Chart**
   ```
   Visualizations > Line Chart

   X-Axis: Audit Date (most recent 12 audits)
   Y-Axis: Overall Compliance (%)
   Display: Line with data points
   Target Line: 80% (green dashed line)

   Size: 50% width, 300px height
   ```

5. **Add Equipment Status**
   ```
   Visualizations > KPI or Gauge

   Current Value: [Equipment Compliance Rate] (this trolley)
   Target: 95%
   Color: Green if on target, red if below

   Size: 25% width x 2
   ```

6. **Add Issues Timeline**
   ```
   Visualizations > Table (Issues for this trolley)

   Columns:
   - Issue # (linked to detail)
   - Category
   - Severity (color-coded)
   - Days Open
   - Status
   - Assigned To

   Filter: Status <> "Closed"
   Conditional formatting: Severity colors
   ```

**Success Criteria:**
- Single trolley selection filters all visuals
- Complete audit history visible
- Trend clearly shows compliance pattern
- Open issues for trolley highlighted
- Cross-filter to specific equipment possible

---

### Task 3.2.14: Dynamic Filters Implementation

**Filter 1: Service Line Slicer (Multi-select)**

```
Visualizations > Slicer
Field: ServiceLine[Title]
Style: List (with Search)
Behaviors:
- Multi-select: Enabled
- All items search: Enabled
- Default: All service lines
- Position: Top-left of all pages
```

**Filter 2: Date Range Slicer**

```
Visualizations > Slicer
Field: Audit[CompletedDateTime]
Type: Between date picker
Behaviors:
- Default range: Last 12 months
- Allow custom dates: Yes
- Format: DD/MM/YYYY
- Position: Top-center

DAX Measure for Date Filter:
Date Filter Status =
"Showing data from " &
FORMAT(MIN(Audit[CompletedDateTime]), "DD MMM YYYY") &
" to " &
FORMAT(MAX(Audit[CompletedDateTime]), "DD MMM YYYY")
```

**Filter 3: Building Filter (Dropdown)**

```
Visualizations > Slicer
Field: Location[Building]
Style: Dropdown
Behaviors:
- All option: Yes
- Multi-select: Yes
- Position: Top-right
```

**Filter 4: Location Status Filter (Buttons)**

```
Visualizations > Buttons (Custom)
Options:
- Button 1: Active locations
- Button 2: Inactive locations
- Button 3: All locations

DAX Measure:
Location Status Filter =
VALUES(Location[Status])

Action: Bookmarks
- Active button → Bookmark 1 (filters to Active)
- Inactive button → Bookmark 2 (filters to Inactive)
- All button → Bookmark 3 (no filter)
```

**Sync Slicers Across Pages**

```
For each slicer on each page:
- Format > General
- Edit interactions
- Set slicers to sync across all pages
- Service Line slicer affects:
  ✓ All location visuals
  ✓ All compliance charts
  ✓ All issue charts

- Date slicer affects:
  ✓ Audit history
  ✓ Compliance trends
  ✓ Issue aging charts

- Building slicer affects:
  ✓ Location performance
  ✓ Compliance breakdown
```

**Filter Combinations (Cross-Filtering Logic)**

```
Service Line → Location (filters to locations in service line)
Service Line → Audit (filters to audits of that service line)
Location → Audit (shows only audits for that location)
Location → Issue (shows only issues for that location)
Building → Location (filters to locations in building)
Date Range → Audit (filters to audits within date range)
Date Range → Issue (filters to issues opened within date range)
```

**Success Criteria:**
- All slicers sync across pages
- Cross-filtering works correctly
- No circular dependencies
- Default filter state sensible
- Filter reset option available

---

### Task 3.2.15: Publish to Workspace & Row-Level Security

**Publishing Steps:**

1. **Publish from Power BI Desktop**
   ```
   File > Publish
   Select workspace: "REdI Trolley Audit Reports"
   Publish dataset as: "Trolley Audit Analytics"

   Dataset publishing options:
   ✓ Include data model
   ✓ Include measures
   ✓ Include relationships
   ```

2. **Verify Publication**
   ```
   Power BI Service > Workspace > Datasets
   - Dataset name: "Trolley Audit Analytics"
   - Status: Healthy (green checkmark)
   - Last refresh: Today
   - Endorsement: Certified (set by admin)
   ```

3. **Configure Refresh Schedule**
   ```
   Dataset settings > Scheduled refresh

   Frequency: Daily
   Time: 02:00 AM AEST
   Time zone: Brisbane Time
   Notification:
   - Email on failure: admin@rbwh.health.qld.gov.au
   - Retry on failure: Yes (retry after 1 hour)
   ```

4. **Enable Gateway Refresh (if applicable)**
   ```
   If using on-premises SharePoint:
   - Configure Power BI Gateway
   - Set data source credentials
   - Test refresh
   ```

**Row-Level Security (RLS) Implementation**

RLS restricts users to see only data for their service line or location.

**RLS Roles Definition:**

```DAX
// Role 1: Clinical Staff (Location Manager)
// Sees only: Their assigned location(s)
[Role Name]: Clinical Staff
[DAX Filter]:
USERPRINCIPALNAME() IN {
    VALUES(Location[LocationAssignedTo])
}

// Role 2: Service Line Manager
// Sees only: Locations in their service line
[Role Name]: Service Line Manager
[DAX Filter]:
ServiceLine[Title] =
    LOOKUPVALUE(
        User[ServiceLine],
        User[Email],
        USERPRINCIPALNAME()
    )

// Role 3: MERT Educator
// Sees all: Full data access
[Role Name]: MERT Educator
[DAX Filter]:
BLANK() (no filter - see all)

// Role 4: Viewer / Leadership
// Sees: Aggregated only (no identifiable locations)
[Role Name]: Executive Viewer
[DAX Filter]:
BLANK() (no filter - see all aggregated data)
```

**Implementing RLS in Power BI Service:**

1. **Go to Dataset Settings**
   ```
   Power BI Service > Datasets > Trolley Audit Analytics
   Settings > Row-Level Security
   ```

2. **Define RLS Rules (in Power Query or DAX)**
   ```
   Rule 1 - For "Clinical Staff" role:
   Add Filter to Location table:
   Location[LocationAssignedTo] = USERNAME()

   Rule 2 - For "Service Line Manager" role:
   Add Filter to Location table:
   Location[ServiceLine] = [ServiceLineForUser]
   ```

3. **Test RLS**
   ```
   Analytics > View as roles
   Select role: "Clinical Staff"
   Select user: John Doe (user in that role)

   Verify: Only John's locations visible
   ```

4. **Publish RLS Config**
   ```
   Apply changes
   Sync with Azure AD groups
   Test with real users
   ```

**Security Group Mapping (Azure AD)**

```
Azure AD Security Groups → Power BI Roles:

1. MERT.Educators@rbwh.health.qld.gov.au
   → Power BI Role: Admin (in workspace)
   → RLS: No filter (see all)

2. ClinicianAuditors@rbwh.health.qld.gov.au
   → Power BI Role: Contributor
   → RLS: Own location only

3. Leadership.Reporting@rbwh.health.qld.gov.au
   → Power BI Role: Viewer
   → RLS: Aggregated views only

4. Pharmacy.Staff@rbwh.health.qld.gov.au
   → Power BI Role: Viewer
   → RLS: Equipment/issue summary only
```

**Verifying RLS**

```
Testing Checklist:
- [ ] MERT educator sees all locations
- [ ] Service line manager sees own service line only
- [ ] Clinical staff sees own location only
- [ ] Executive viewer sees aggregated data
- [ ] No data leakage between roles
- [ ] Performance acceptable with RLS
- [ ] Drill-through respects RLS
```

**Success Criteria:**
- Dataset published and refreshing daily
- RLS roles defined and tested
- Users access appropriate data only
- No data leakage
- Performance meets SLA

---

### Task 3.2.16: Embed in PowerApp & Create Power BI Tile

**Embedding Power BI Report in PowerApp:**

1. **Copy Power BI Report Embed Link**
   ```
   Power BI Service > Report > File > Embed report

   Select option: "Customer owns data"
   (for end-user sharing without Pro license)

   OR

   "Your organization owns data" (for internal app)

   Copy: Embed URL and Access Token
   ```

2. **Add Power BI Visual to PowerApp**
   ```
   PowerApp Canvas > Insert > Power BI visual

   Report: Select "Trolley Audit Analytics"
   Page: Select "Compliance Trends" (or other)

   Size: 90% width, 600px height
   Position: Main content area
   ```

3. **Configure Interactivity**
   ```
   Data passing:
   - Trolley slicer in PowerApp → Power BI visual
   - Service line filter → Power BI service line slicer

   DAX Measure for parameter passing:
   Location Filter =
   SELECTEDVALUE(Location[LocationName],
   PowerApp.SelectedLocation)
   ```

4. **Add Navigation Buttons**
   ```
   Button 1: "View Compliance Trends"
   → Navigate to Power BI page (Compliance Trends)

   Button 2: "View Issues"
   → Navigate to Power BI page (Issue Summary)

   Button 3: "View Full Report"
   → Launch Power BI in new window

   PowerFx Formula:
   Launch("https://app.powerbi.com/groups/workspace-id/reports/report-id")
   ```

**Creating Power BI Tiles for Dashboard:**

1. **Create Dashboard in Power BI**
   ```
   Power BI Service > Create > Dashboard
   Name: "REdI Trolley Audit Executive Dashboard"
   Description: "Real-time compliance monitoring"
   ```

2. **Pin Report Visuals to Dashboard**
   ```
   From Report > Click visual > Pin to dashboard

   Tiles to pin:
   - Average Compliance KPI (top)
   - Total Open Issues KPI (top)
   - Critical Issues KPI (top)
   - Compliance trend line chart
   - Service line comparison
   - Issue aging chart
   - Most recent audits table
   ```

3. **Add Q&A Tile (Natural Language Query)**
   ```
   Dashboard > Edit > Q&A tile
   Question: "Average compliance by service line"
   Display: Bar chart with service lines
   ```

4. **Configure Tile Settings**
   ```
   For each tile:
   - Title: Clear description
   - Subtitle: Last updated timestamp
   - Click behavior:
     * Drill-through to detail report
     * Link to PowerApp
     * Open full report page
   ```

5. **Pin Dashboard to PowerApp**
   ```
   Method 1: Embed dashboard in PowerApp
   Insert > Power BI visual > Dashboard

   Method 2: Link from PowerApp
   Button > Action:
   "Open Power BI dashboard"

   Link:
   https://app.powerbi.com/groups/workspace-id/dashboards/dashboard-id
   ```

**PowerApp Integration Workflow:**

```
User Flow:
1. User opens Trolley Audit PowerApp
2. Navigates to "Reports" tab
3. Sees embedded Power BI tiles (KPIs, compliance)
4. Clicks "View Full Report"
5. Launches Power BI in modal window
6. Filters by service line (synced from PowerApp)
7. Drills down to specific trolley
8. Views 12-month audit history
9. Clicks issue to see details
10. Returns to PowerApp
```

**Performance Optimization:**

```DAX
// Measure for dashboard performance
Dashboard Load Time =
VAR RefreshTime = DATEDIFF(TODAY(), TODAY()-1, "S")
RETURN
IF(RefreshTime < 300, "Good",
IF(RefreshTime < 600, "Acceptable", "Slow"))
```

**Mobile Optimization:**

```
Power BI Mobile Report:
- Vertical layout for phone display
- Single visual per screen
- Touch-friendly filters
- Swipe to navigate between pages

PowerApp Mobile:
- Responsive design
- Full Power BI tile view
- Embedded report readable on mobile
- Touch interactions work correctly
```

**Success Criteria:**
- Power BI report embeds in PowerApp
- Tiles display with real-time data
- Filters sync between PowerApp and Power BI
- Navigation to detailed reports works
- Mobile view is usable
- No performance degradation
- Security and RLS respected in embedded view

---

## Verification Checklist

### Data Quality Verification

- [ ] All 7 SharePoint lists connected
- [ ] 0 null values in required fields
- [ ] Referential integrity: 100% match rate
- [ ] Date fields consistent timezone
- [ ] Numeric fields in correct ranges
- [ ] No duplicate records in Audit or Issue tables
- [ ] ServiceLine lookup resolution rate: 100%
- [ ] Location lookup resolution rate: 100%

### Data Model Verification

- [ ] 6 active relationships established
- [ ] Date dimension table created with 1,825 rows
- [ ] Star schema pattern properly normalized
- [ ] No circular relationships
- [ ] Cross-filter directions set correctly
- [ ] Relationship cardinality (1:*, *:1) correct
- [ ] Referential integrity enabled where applicable

### DAX Measures Verification

- [ ] 25+ measures created and tested
- [ ] All measures use correct context/filters
- [ ] No circular measure dependencies
- [ ] Aggregate functions handling blanks correctly
- [ ] Conditional logic working as designed
- [ ] Performance acceptable (<1s calculation)
- [ ] Measure results align with source data

### Report Visualization Verification

**Compliance Reports (Tasks 3.2.4-3.2.8):**
- [ ] 3.2.4: Line chart shows 12-month trend, multiple audit types
- [ ] 3.2.5: Bar chart sorts by compliance, shows all service lines
- [ ] 3.2.6: Stacked bar shows status distribution by building
- [ ] 3.2.7: Calendar heatmap displays 90-day activity pattern
- [ ] 3.2.8: Histogram shows days-since-audit distribution, 180-day line visible

**Issue Reports (Tasks 3.2.9-3.2.12):**
- [ ] 3.2.9: Pie chart shows all 5 categories, adds to 100%
- [ ] 3.2.10: Pie chart severity distribution, critical highlighted
- [ ] 3.2.11: Stacked bar shows age groups, severity breakdown
- [ ] 3.2.12: Matrix table top 20 deficient items, sorted correctly
- [ ] All issue counts reconcile with dashboard totals

**Interactive Elements:**
- [ ] 3.2.13: Trolley slicer filters all visuals correctly
- [ ] 3.2.14: Service line, date, building filters working
- [ ] Cross-filtering between pages functions correctly
- [ ] No broken/missing relationships in drill-through

**Publishing & Integration (Tasks 3.2.15-3.2.16):**
- [ ] Dataset published to workspace
- [ ] Auto-refresh working (daily at 2 AM)
- [ ] Row-Level Security roles defined and tested
- [ ] Users see only appropriate data
- [ ] Power BI embedded in PowerApp
- [ ] Tiles displaying on dashboard
- [ ] No performance degradation
- [ ] Mobile view responsive

### User Acceptance Testing

- [ ] MERT educators can access full data
- [ ] Service line managers see filtered data correctly
- [ ] Clinical staff see single location view
- [ ] Leadership sees aggregated views
- [ ] Filter combinations work intuitively
- [ ] Report load times < 5 seconds
- [ ] Drill-through drill-back functions work
- [ ] Print/export functionality available

### Security Verification

- [ ] RLS preventing unauthorized data access
- [ ] Service principals not exposed in reports
- [ ] Dataset credentials not visible
- [ ] Embedded reports respect app's permissions
- [ ] No data leakage in cross-filters
- [ ] Audit trail logs available for admin review

### Documentation Verification

- [ ] Data model diagram created and documented
- [ ] DAX measure documentation complete
- [ ] User guide for report navigation completed
- [ ] Filter usage documented
- [ ] Refresh schedule documented
- [ ] RLS role matrix documented
- [ ] Troubleshooting guide created

---

## Summary of Deliverables

### Phase 3.2 Completion Checklist

**Workspace Setup (3.2.1-3.2.3):**
- ✓ Power BI workspace created
- ✓ All 7 SharePoint lists connected
- ✓ Data refresh schedule configured
- ✓ Data model with 6 relationships established
- ✓ Date dimension created

**Compliance Reports (3.2.4-3.2.8):**
- ✓ Compliance Trends dashboard (line chart)
- ✓ Service Line Comparison (bar chart)
- ✓ Building Comparison (stacked bar)
- ✓ Audit Activity Heatmap (calendar)
- ✓ Days Since Audit Histogram

**Issue Reports (3.2.9-3.2.12):**
- ✓ Issues by Category pie chart
- ✓ Issues by Severity pie chart
- ✓ Issue Aging stacked bar chart
- ✓ Equipment Deficiency matrix table
- ✓ Issue KPI cards

**Integration & Publishing (3.2.13-3.2.16):**
- ✓ Trolley Detail report page
- ✓ Dynamic filters implemented
- ✓ Published to workspace with RLS
- ✓ Embedded in PowerApp
- ✓ Power BI tiles created

**Supporting Artifacts:**
- ✓ 25+ DAX measures
- ✓ Data quality validation report
- ✓ User documentation
- ✓ RLS role matrix
- ✓ Refresh schedule configuration

---

## Next Steps (Phase 4)

1. **User Training** - Conduct workshops on report navigation
2. **Performance Tuning** - Monitor refresh times, optimize if needed
3. **Feedback Collection** - Gather user feedback after 2 weeks
4. **Enhancements** - Add additional drill-throughs based on feedback
5. **Maintenance Plan** - Establish support and update schedule

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Documentation Team | Initial implementation guide |

**End of Phase 3.2 Implementation Guide**
