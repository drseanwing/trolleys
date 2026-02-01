# REdI Trolley Audit System
## Phase 2.6 Issue Management Lists Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 2.6.1 - 2.6.11

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Prerequisites](#prerequisites)
3. [Overview](#overview)
4. [Task 2.6.1-2.6.6: Issue List](#task-262.6-issue-list)
5. [Task 2.6.7-2.6.9: CorrectiveAction List](#task-267-269-correctiveaction-list)
6. [Task 2.6.10-2.6.11: IssueComment List](#task-26102611-issuecomment-list)
7. [List Relationships & Dependencies](#list-relationships--dependencies)
8. [Validation Rules](#validation-rules)
9. [Calculated Columns](#calculated-columns)
10. [Views Configuration](#views-configuration)
11. [Testing Verification](#testing-verification)

---

## Executive Summary

Phase 2.6 establishes the three linked SharePoint lists that comprise the Issue Management system. These lists track problems identified during audits or discovered during trolley operation, manage corrective actions, and maintain an audit trail of comments.

### What You'll Complete

| Task | Objective | Time | Dependency |
|------|-----------|------|-----------|
| 2.6.1 | Create Issue list schema | 3 hours | 1.4.1 (Location list) |
| 2.6.2 | Configure Location lookup | 0.5 hours | 2.6.1 |
| 2.6.3 | Configure Audit lookup | 0.5 hours | 2.6.1 |
| 2.6.4 | Configure Equipment lookup | 0.5 hours | 2.6.1 |
| 2.6.5 | Add choice columns | 2 hours | 2.6.4 |
| 2.6.6 | Add issue number auto-generation | 2 hours | 2.6.5 |
| 2.6.7 | Create CorrectiveAction list | 2 hours | 2.6.1 |
| 2.6.8 | Configure Issue lookup | 0.5 hours | 2.6.7 |
| 2.6.9 | Add ActionType choices | 1 hour | 2.6.8 |
| 2.6.10 | Create IssueComment list | 1 hour | 2.6.1 |
| 2.6.11 | Configure Issue lookup | 0.5 hours | 2.6.10 |

**Total Duration:** Approximately 13.5 hours of implementation work

### Lists Created

By the end of Phase 2.6, you will have:

1. **Issue List** - Central issue tracking with 18 columns
2. **CorrectiveAction List** - Actions taken to resolve issues (7 columns)
3. **IssueComment List** - Comment/audit trail (4 columns)

### Dependencies

Phase 2.6 depends on:
- **Location list** (Phase 1.4) - For location lookups
- **Audit list** (Phase 1.5) - For audit lookups
- **Equipment list** (Phase 1.3) - For optional equipment lookups

---

## Prerequisites

### Required Access & Permissions

- **SharePoint Admin** or **Site Owner** access to REdI Trolley Audit site
- Ability to create lists and configure columns
- Power Automate access for calculated columns (if using flows)

### Required Information

Before starting, ensure you have:

1. **Existing Lists Verified**
   - Location list created and populated (76 locations)
   - Audit list created and available
   - Equipment list created and available
   - All lists accessible and functioning

2. **Schema Files**
   - Issue.json (provided in sharepoint_schemas/)
   - CorrectiveAction.json (provided in sharepoint_schemas/)
   - IssueComment.json (provided in sharepoint_schemas/)

3. **Business Context**
   - Understanding of issue categories for trolley management
   - Approval of severity levels (Critical/High/Medium/Low)
   - Clarity on issue workflow states

### Pre-Implementation Checklist

- [ ] Location list exists with at least 1 record
- [ ] Audit list exists and is linked to Location
- [ ] Equipment list exists and populated
- [ ] All related lists accessible via SharePoint
- [ ] Current user has Site Owner or Admin permissions
- [ ] JSON schema files downloaded or accessible

---

## Overview

### Issue Management System Architecture

```
┌─────────────────────────────────────────────────────┐
│          Issue Management System                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Issue List (Parent)                          │  │
│  │ - Issue tracking                             │  │
│  │ - Status management                          │  │
│  │ - Severity classification                    │  │
│  │ - Assignment & escalation                    │  │
│  └──────────────────────────────────────────────┘  │
│            ▲              ▲                         │
│            │              │                         │
│   ┌────────┴──┐    ┌─────┴────────┐               │
│   │            │    │              │                │
│   ▼            ▼    ▼              ▼                │
│  ┌──────┐  ┌────────────┐  ┌──────────────┐      │
│  │Correc│  │Issue       │  │Related       │      │
│  │tive  │  │Comment     │  │Location,Audit│     │
│  │Action│  │            │  │Equipment     │      │
│  └──────┘  └────────────┘  └──────────────┘      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Data Flow

```
Issue Created → Categorized & Severity Set → Assigned
    ↓              ↓                           ↓
Location        Category:               AssignedTo set
Audit (optional) Equipment/Doc/        AssignedDate set
Equipment (opt)  Condition/Process

    ↓ (work begins)
    ├── CorrectiveAction added
    │   └→ Status changes: Open → Assigned → In_Progress
    ├── IssueComment added for notes
    │   └→ Audit trail of all updates
    │
    ↓ (resolution process)
    ├── CorrectiveAction completed
    └→ Status: Pending_Verification → Resolved → Closed
```

### Column Organization

**Issue List Structure:**

```
Identifiers         References          Management
─────────────────   ──────────────────  ──────────────
IssueNumber         LocationId          Status
(auto-generated)    AuditId             Severity
Title               EquipmentId         Category
                                        AssignedTo

Lifecycle           Context             Escalation
─────────────────   ──────────────────  ──────────────
ReportedDate        Description         EscalationLevel
ReportedBy          ReopenCount         EscalatedTo
AssignedDate        (implicit parent-
ResolvedDate        child links to
ClosedDate          actions & comments)
```

---

## Task 2.6.1-2.6.6: Issue List

### Objective

Create the Issue list that serves as the central hub for issue tracking. This list captures all problems identified during audits or trolley operation, tracks their status through resolution, and manages assignments and escalations.

### Column Definitions

The Issue list contains 18 columns organized into 5 categories:

#### Category 1: Identification

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| Issue Number | IssueNumber | Text | Yes | Auto-generated: ISS-YYYY-NNNN format |
| Title | Title | Text | Yes | Brief description of issue (200 chars max) |
| Description | Description | Note | Yes | Detailed explanation of the issue |

#### Category 2: Classification

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| Category | Category | Choice | Yes | Equipment / Documentation / Condition / Process |
| Severity | Severity | Choice | Yes | Critical / High / Medium / Low |
| Status | Status | Choice | Yes | Open / Assigned / In_Progress / Pending_Verification / Resolved / Closed |

#### Category 3: References

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| LocationId | LocationId | Lookup | Yes | Link to Location (trolley) |
| AuditId | AuditId | Lookup | No | Link to Audit that identified issue |
| EquipmentId | EquipmentId | Lookup | No | Link to Equipment item (if applicable) |

#### Category 4: Lifecycle

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| ReportedBy | ReportedBy | Text | Yes | Name of person reporting |
| ReportedDate | ReportedDate | DateTime | Yes | When issue was first reported |
| AssignedTo | AssignedTo | User | No | Person responsible for resolution |
| AssignedDate | AssignedDate | DateTime | No | When issue was assigned |
| ResolvedDate | ResolvedDate | DateTime | No | When issue was marked resolved |
| ClosedDate | ClosedDate | DateTime | No | When issue was closed |

#### Category 5: Escalation & Tracking

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| EscalationLevel | EscalationLevel | Choice | No | None / Level1 / Level2 / Level3 |
| EscalatedTo | EscalatedTo | User | No | Person responsible if escalated |
| ReopenCount | ReopenCount | Number | No | Number of times reopened (default: 0) |

### Step-by-Step Instructions

#### Step 1: Navigate to Create New List

**Action:** Access SharePoint and initiate list creation

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Click "+ New" in the top left
3. Select "List"
4. Choose "Create from template" → "Blank list"
   OR "Create your own" → proceed with manual configuration
```

**Expected Result:** List creation interface appears

---

#### Step 2: Name and Configure List Settings

**Action:** Set up basic list properties

**Form Fields:**

| Field | Value | Notes |
|-------|-------|-------|
| **List Name** | Issue | Exact name for lookups |
| **Description** | Issue tracking list for audit findings and trolley problems | Displayed in list gallery |
| **More options** | Click if available | Access advanced settings |
| **Show in navigation** | Yes | Makes list visible in menu |
| **Allow attachments** | Yes | For supporting documentation |
| **Enable versioning** | Yes | Track column changes over time |

**Steps:**

```
1. Enter list name: "Issue"
2. Enter description
3. Click "Create"
4. Wait for list creation to complete (1-2 minutes)
5. You should land on the empty list page
```

**Expected Result:** Empty Issue list created with default Title column

---

#### Step 3: Rename Title Column

**Action:** Change the default "Title" column to more meaningful name

```
1. From the list, click on "Title" column header
2. Select "Edit column"
3. Change Display Name to: "Issue Title"
4. Keep Internal Name as: "Title"
5. Click "Save"
```

**Note:** Keeping Internal Name as "Title" maintains SharePoint compatibility

---

#### Step 4: Add Issue Number Column

**Action:** Create auto-generated issue number column

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Text |
| **Display Name** | Issue Number |
| **Internal Name** | IssueNumber |
| **Required** | No (will be auto-filled) |
| **Maximum Length** | 20 |
| **Default Value** | (leave blank - use formula) |

**Steps:**

```
1. From list settings, click "+ Add column"
2. Select "Text"
3. Enter Display Name: "Issue Number"
4. Keep Internal Name: "IssueNumber"
5. Set Maximum Length: 20
6. Click "Save"
```

**Note:** Issue number auto-generation will be configured in Task 2.6.6 using calculated columns or Power Automate.

---

#### Step 5: Add Description Column

**Action:** Add multi-line notes field for detailed issue description

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Multiple lines of text |
| **Display Name** | Description |
| **Internal Name** | Description |
| **Required** | Yes |
| **Number of Lines** | 4 |
| **Enhanced Rich Text** | Yes (for formatting) |

**Steps:**

```
1. Click "+ Add column"
2. Select "Multiple lines of text"
3. Display Name: "Description"
4. Set Number of Lines: 4
5. Enable "Rich text (formatted)"
6. Click "Save"
```

---

#### Step 6: Add Classification Columns (Category, Severity, Status)

**Action:** Add choice columns for issue classification

**6a. Add Category Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Choice |
| **Display Name** | Category |
| **Internal Name** | Category |
| **Required** | Yes |
| **Choices** | Equipment, Documentation, Condition, Process |
| **Display as** | Dropdown |
| **Default Value** | Equipment |

**Steps:**

```
1. Click "+ Add column"
2. Select "Choice"
3. Display Name: "Category"
4. Enter choices (one per line):
   Equipment
   Documentation
   Condition
   Process
5. Set default: Equipment
6. Click "Save"
```

**6b. Add Severity Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Choice |
| **Display Name** | Severity |
| **Internal Name** | Severity |
| **Required** | Yes |
| **Choices** | Critical, High, Medium, Low |
| **Display as** | Dropdown |
| **Default Value** | Medium |

**Steps:**

```
1. Click "+ Add column"
2. Select "Choice"
3. Display Name: "Severity"
4. Enter choices:
   Critical
   High
   Medium
   Low
5. Set default: Medium
6. Click "Save"
```

**6c. Add Status Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Choice |
| **Display Name** | Status |
| **Internal Name** | Status |
| **Required** | Yes |
| **Choices** | Open, Assigned, In_Progress, Pending_Verification, Resolved, Closed |
| **Display as** | Dropdown |
| **Default Value** | Open |

**Steps:**

```
1. Click "+ Add column"
2. Select "Choice"
3. Display Name: "Status"
4. Enter choices:
   Open
   Assigned
   In_Progress
   Pending_Verification
   Resolved
   Closed
5. Set default: Open
6. Click "Save"
```

---

#### Step 7: Add Lookup Columns to Related Lists

**Action:** Create lookup connections to Location, Audit, and Equipment lists

**7a. Add LocationId Lookup Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Lookup |
| **Display Name** | LocationId |
| **Internal Name** | LocationId |
| **Get information from** | Location |
| **In this column** | Title |
| **Required** | Yes |
| **Allow multiple values** | No |

**Steps:**

```
1. Click "+ Add column"
2. Select "Lookup"
3. Display Name: "LocationId"
4. Get information from: "Location" (dropdown)
5. In this column: "Title"
6. Required: Yes
7. Click "Save"
```

**Verification:** After saving, you should see a dropdown listing all locations.

**7b. Add AuditId Lookup Column (Optional)**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Lookup |
| **Display Name** | AuditId |
| **Internal Name** | AuditId |
| **Get information from** | Audit |
| **In this column** | Title |
| **Required** | No |
| **Allow multiple values** | No |

**Steps:**

```
1. Click "+ Add column"
2. Select "Lookup"
3. Display Name: "AuditId"
4. Get information from: "Audit"
5. In this column: "Title"
6. Required: No (optional)
7. Click "Save"
```

**7c. Add EquipmentId Lookup Column (Optional)**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Lookup |
| **Display Name** | EquipmentId |
| **Internal Name** | EquipmentId |
| **Get information from** | Equipment |
| **In this column** | Title |
| **Required** | No |
| **Allow multiple values** | No |

**Steps:**

```
1. Click "+ Add column"
2. Select "Lookup"
3. Display Name: "EquipmentId"
4. Get information from: "Equipment"
5. In this column: "Title"
6. Required: No (optional)
7. Click "Save"
```

---

#### Step 8: Add People Columns for Assignment

**Action:** Create columns for assigning responsibility

**8a. Add ReportedBy Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Single line of text |
| **Display Name** | ReportedBy |
| **Internal Name** | ReportedBy |
| **Required** | Yes |
| **Maximum Length** | 100 |

**Steps:**

```
1. Click "+ Add column"
2. Select "Single line of text"
3. Display Name: "ReportedBy"
4. Required: Yes
5. Maximum Length: 100
6. Click "Save"
```

**Note:** Using Text instead of User column for flexibility (can be name or email)

**8b. Add AssignedTo Column (User Type)**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Person or Group |
| **Display Name** | AssignedTo |
| **Internal Name** | AssignedTo |
| **Required** | No |
| **Allow multiple values** | No |
| **Show field** | Name |

**Steps:**

```
1. Click "+ Add column"
2. Select "Person or Group"
3. Display Name: "AssignedTo"
4. Allow multiple: No
5. Show field: Name
6. Click "Save"
```

**8c. Add EscalatedTo Column (User Type)**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Person or Group |
| **Display Name** | EscalatedTo |
| **Internal Name** | EscalatedTo |
| **Required** | No |
| **Allow multiple values** | No |
| **Show field** | Name |

**Steps:**

```
1. Click "+ Add column"
2. Select "Person or Group"
3. Display Name: "EscalatedTo"
4. Allow multiple: No
5. Click "Save"
```

---

#### Step 9: Add Date Columns for Lifecycle Tracking

**Action:** Add date/time columns for tracking issue progression

**9a. Add ReportedDate Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Date and Time |
| **Display Name** | ReportedDate |
| **Internal Name** | ReportedDate |
| **Required** | Yes |
| **Format** | Date and Time |
| **Default Value** | Today's date |

**Steps:**

```
1. Click "+ Add column"
2. Select "Date and Time"
3. Display Name: "ReportedDate"
4. Format: Date and Time
5. Default: [Today] (auto-select)
6. Click "Save"
```

**9b. Add AssignedDate Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Date and Time |
| **Display Name** | AssignedDate |
| **Internal Name** | AssignedDate |
| **Required** | No |
| **Format** | Date and Time |

**Steps:**

```
1. Click "+ Add column"
2. Select "Date and Time"
3. Display Name: "AssignedDate"
4. Format: Date and Time
5. Click "Save"
```

**9c. Add ResolvedDate Column**

**Configuration:**

```
Same as AssignedDate:
- Column Type: Date and Time
- Display Name: ResolvedDate
- Format: Date and Time
- Required: No
```

**9d. Add ClosedDate Column**

**Configuration:**

```
Same as ResolvedDate:
- Column Type: Date and Time
- Display Name: ClosedDate
- Format: Date and Time
- Required: No
```

---

#### Step 10: Add Escalation and Tracking Columns

**Action:** Add columns for escalation management

**10a. Add EscalationLevel Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Choice |
| **Display Name** | EscalationLevel |
| **Internal Name** | EscalationLevel |
| **Required** | No |
| **Choices** | None, Level1, Level2, Level3 |
| **Default Value** | None |

**Steps:**

```
1. Click "+ Add column"
2. Select "Choice"
3. Display Name: "EscalationLevel"
4. Choices:
   None
   Level1
   Level2
   Level3
5. Default: None
6. Click "Save"
```

**10b. Add ReopenCount Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Number |
| **Display Name** | ReopenCount |
| **Internal Name** | ReopenCount |
| **Required** | No |
| **Decimal places** | 0 |
| **Default Value** | 0 |
| **Minimum** | 0 |

**Steps:**

```
1. Click "+ Add column"
2. Select "Number"
3. Display Name: "ReopenCount"
4. Decimal places: 0
5. Default value: 0
6. Minimum: 0
7. Click "Save"
```

---

#### Step 11: Verify All Columns Created

**Action:** Confirm all 18 columns are present

**Verification Checklist:**

From the Issue list view, verify these columns exist:

**Identification:**
- [ ] IssueNumber
- [ ] Issue Title
- [ ] Description

**Classification:**
- [ ] Category
- [ ] Severity
- [ ] Status

**References:**
- [ ] LocationId
- [ ] AuditId
- [ ] EquipmentId

**Lifecycle:**
- [ ] ReportedBy
- [ ] ReportedDate
- [ ] AssignedTo
- [ ] AssignedDate
- [ ] ResolvedDate
- [ ] ClosedDate

**Escalation:**
- [ ] EscalationLevel
- [ ] EscalatedTo
- [ ] ReopenCount

**Steps:**

```
1. From Issue list, click on column headers area
2. Click "Display columns" or view settings
3. Verify all columns listed above are present
4. Adjust column order if desired (optional):
   - Drag columns to reorder
   - Move frequently used columns to left
5. Click "Save"
```

---

### Configuration Summary for Tasks 2.6.1-2.6.5

| Item | Status | Notes |
|------|--------|-------|
| Issue list created | ✓ | Named exactly "Issue" |
| 18 columns added | ✓ | All column types configured |
| Lookups configured | ✓ | Location (required), Audit & Equipment (optional) |
| Choice columns set | ✓ | Category, Severity, Status values defined |
| Date columns added | ✓ | Lifecycle tracking columns in place |
| User columns added | ✓ | AssignedTo, EscalatedTo configured |

---

### Task 2.6.6: Issue Number Auto-Generation

**Objective:** Implement ISS-YYYY-NNNN format auto-generation for issue tracking

#### Option A: Using Calculated Column (Recommended)

This approach uses a SharePoint calculated column with a formula to generate issue numbers.

**Formula Logic:**

```
Format: ISS-YYYY-NNNN
Example: ISS-2026-0001, ISS-2026-0002, etc.

Where:
- ISS = Literal prefix
- YYYY = Current year from ReportedDate
- NNNN = Sequential 4-digit number padded with zeros
```

**Steps:**

```
1. From Issue list, click "+ Add column"
2. Select "Calculated column"
3. Display Name: IssueNumber (note: should exist as Text already)
4. Internal Name: IssueNumberCalc (or create new if needed)
5. Formula: (see below based on your approach)
6. Data type returned: Text
7. Click "Save"
```

**Formula Options:**

**Option A1: Using Created Field (Simpler)**

```
="ISS-"&YEAR([Created])&"-"&TEXT([ID],"0000")
```

This formula:
- Gets year from Created timestamp
- Pads item ID with leading zeros to 4 digits
- Creates format like ISS-2026-0005

**Implementation Steps:**

```
1. In calculated column formula field, paste:
   ="ISS-"&YEAR([Created])&"-"&TEXT([ID],"0000")
2. Set Data type returned: Text
3. Click "OK"
4. Verify on first test item
```

**Option A2: Using ReportedDate (More Control)**

If you want to use the ReportedDate instead of Created:

```
="ISS-"&YEAR([ReportedDate])&"-"&TEXT([ID],"0000")
```

**Implementation:**

```
1. Paste formula using ReportedDate field
2. Ensure ReportedDate is populated before creating formula
3. Click "OK"
```

**Limitations of Calculated Columns:**

- Cannot update list items after creation
- Only works with built-in fields (Created, ID)
- Recalculates when any field changes (could cause different numbers)

---

#### Option B: Using Power Automate Flow (Recommended for Full Control)

This approach uses a flow to generate issue numbers with proper sequencing.

**Setup Steps:**

```
1. Create new automated cloud flow
2. Trigger: When an item is created in Issue list
3. Actions:
   a. Get all items from Issue list for current year
   b. Count items (this becomes sequence number)
   c. Format: "ISS-" + YEAR(now()) + "-" + sequence number
   d. Update item with generated issue number
```

**Flow Configuration:**

**Trigger:**

```
Trigger type: "When an item is created"
List: "Issue"
```

**Actions:**

```
Action 1 - Get Items
- List: "Issue"
- Filter Query: Add filter for current year
  YEAR([ReportedDate]) = YEAR(now())

Action 2 - Count Items
- Input: @length(body('Get_items')?['value'])

Action 3 - Compose (format number)
- Inputs: @concat('ISS-', string(year(now())), '-', padLeft(string(add(outputs('Count_Items'), 1)), 4, '0'))

Action 4 - Update Item
- List: "Issue"
- Item ID: triggerOutputs()['body/ID']
- IssueNumber: @outputs('Compose')
```

**Workflow:**

```
Issue Created
    ↓
Flow Triggers
    ↓
Count existing items for current year
    ↓
Add 1 to count for new sequence
    ↓
Format: ISS-2026-0001
    ↓
Update IssueNumber field
    ↓
Complete
```

---

#### Option C: Using Column Formula with ID Offset (Simple Alternative)

If calculated columns only:

```
Formula: ="ISS-"&TEXT(YEAR(NOW()),​"0000")&"-"&TEXT([ID],"0000")
```

This generates: ISS-2026-0001 where 0001 is the Item ID

**Advantages:**
- Simple, no flow needed
- Number is unique and sequential
- Different year if created next year

**Disadvantages:**
- ID numbers can have gaps if items deleted
- May not start at 0001 if list already has items

---

### Recommended Implementation

**Recommendation: Option B (Power Automate Flow)**

Reasons:
1. Proper sequential numbering (1, 2, 3, not item IDs)
2. Can handle year rollover correctly
3. Can add additional logic if needed
4. Most professional and scalable

**Implementation Time: 30 minutes**

For now, configure the IssueNumber field as a Text column and leave it empty. We will implement the auto-generation in Phase 2.8 Task 2.8.2 when creating the flow.

---

## Task 2.6.7-2.6.9: CorrectiveAction List

### Objective

Create the CorrectiveAction list that tracks actions taken to resolve issues. Each corrective action links to an issue and records what was done, when, and by whom.

### Column Definitions

The CorrectiveAction list contains 7 columns:

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| Action Title | Title | Text | Yes | Brief description of action taken |
| IssueId | IssueId | Lookup | Yes | Link to parent Issue |
| ActionType | ActionType | Choice | Yes | Replacement / Repair / Restock / Training / Process Change / Other |
| Description | Description | Note | No | Detailed description of action |
| ActionDate | ActionDate | DateTime | Yes | When action was taken |
| ActionBy | ActionBy | Text | Yes | Who performed the action (name or email) |
| CompletedDate | CompletedDate | DateTime | No | When action was completed |

### Step-by-Step Instructions

#### Step 1: Create CorrectiveAction List

**Action:** Navigate to create new list

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Click "+ New"
3. Select "List"
4. Select "Create your own" or "Blank list"
5. Enter list name: "CorrectiveAction"
6. Click "Create"
```

---

#### Step 2: Configure Basic Settings

**Action:** Set up list properties

| Setting | Value |
|---------|-------|
| **List Name** | CorrectiveAction |
| **Description** | Actions taken to resolve issues |
| **Show in navigation** | Yes |
| **Allow attachments** | Yes |
| **Enable versioning** | Yes |

---

#### Step 3: Rename Title Column

**Action:** Update default Title column

```
1. Click "Title" column header
2. Select "Edit column"
3. Change to Display Name: "Action Title"
4. Keep Internal Name: "Title"
5. Save
```

---

#### Step 4: Add IssueId Lookup Column

**Action:** Link to parent Issue list

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Lookup |
| **Display Name** | IssueId |
| **Internal Name** | IssueId |
| **Get information from** | Issue |
| **In this column** | IssueNumber |
| **Required** | Yes |

**Steps:**

```
1. Click "+ Add column"
2. Select "Lookup"
3. Display Name: "IssueId"
4. Get information from: "Issue"
5. In this column: "IssueNumber"
6. Required: Yes
7. Click "Save"
```

---

#### Step 5: Add ActionType Choice Column

**Action:** Define types of corrective actions

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Choice |
| **Display Name** | ActionType |
| **Internal Name** | ActionType |
| **Required** | Yes |
| **Choices** | Replacement, Repair, Restock, Training, Process Change, Other |
| **Display as** | Dropdown |
| **Default Value** | Other |

**Steps:**

```
1. Click "+ Add column"
2. Select "Choice"
3. Display Name: "ActionType"
4. Choices (one per line):
   Replacement
   Repair
   Restock
   Training
   Process Change
   Other
5. Default: Other
6. Click "Save"
```

---

#### Step 6: Add Description Column

**Action:** Add detailed notes about action

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Multiple lines of text |
| **Display Name** | Description |
| **Internal Name** | Description |
| **Required** | No |
| **Number of Lines** | 3 |
| **Enhanced Rich Text** | Yes |

**Steps:**

```
1. Click "+ Add column"
2. Select "Multiple lines of text"
3. Display Name: "Description"
4. Number of Lines: 3
5. Enable "Rich text (formatted)"
6. Click "Save"
```

---

#### Step 7: Add Date Columns

**Action:** Track action timing

**7a. Add ActionDate Column**

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Date and Time |
| **Display Name** | ActionDate |
| **Internal Name** | ActionDate |
| **Required** | Yes |
| **Format** | Date and Time |
| **Default Value** | Today |

**Steps:**

```
1. Click "+ Add column"
2. Select "Date and Time"
3. Display Name: "ActionDate"
4. Format: Date and Time
5. Default: [Today]
6. Click "Save"
```

**7b. Add CompletedDate Column**

**Configuration:**

```
- Column Type: Date and Time
- Display Name: CompletedDate
- Format: Date and Time
- Required: No
```

---

#### Step 8: Add ActionBy Column

**Action:** Track who performed action

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Single line of text |
| **Display Name** | ActionBy |
| **Internal Name** | ActionBy |
| **Required** | Yes |
| **Maximum Length** | 100 |

**Steps:**

```
1. Click "+ Add column"
2. Select "Single line of text"
3. Display Name: "ActionBy"
4. Required: Yes
5. Maximum Length: 100
6. Click "Save"
```

---

#### Step 9: Verify CorrectiveAction List Structure

**Verification Checklist:**

- [ ] List named "CorrectiveAction"
- [ ] 7 columns present:
  - [ ] Title (renamed to "Action Title")
  - [ ] IssueId (Lookup to Issue)
  - [ ] ActionType (Choice)
  - [ ] Description (Note)
  - [ ] ActionDate (DateTime)
  - [ ] ActionBy (Text)
  - [ ] CompletedDate (DateTime)

---

### Configuration Summary for Tasks 2.6.7-2.6.9

| Item | Status | Notes |
|------|--------|-------|
| CorrectiveAction list created | ✓ | Named exactly "CorrectiveAction" |
| 7 columns added | ✓ | All column types configured |
| Issue lookup configured | ✓ | Links to Issue.IssueNumber |
| ActionType choices added | ✓ | 6 action types defined |
| Date tracking columns | ✓ | ActionDate and CompletedDate |

---

## Task 2.6.10-2.6.11: IssueComment List

### Objective

Create the IssueComment list for maintaining an audit trail of comments, updates, and discussions related to issues.

### Column Definitions

The IssueComment list contains 4 columns:

| Column | Internal Name | Type | Required | Notes |
|--------|---------------|------|----------|-------|
| Comment Text | Title | Note | Yes | The comment content |
| IssueId | IssueId | Lookup | Yes | Link to parent Issue |
| CommentBy | CommentBy | Text | Yes | Who added the comment |
| CommentDate | CommentDate | DateTime | Yes | When comment was added |

### Step-by-Step Instructions

#### Step 1: Create IssueComment List

**Action:** Create new list

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Click "+ New" → "List"
3. Select "Blank list"
4. Enter name: "IssueComment"
5. Click "Create"
```

---

#### Step 2: Configure Title Column

**Action:** Rename Title to CommentText

```
1. Click "Title" header
2. Select "Edit column"
3. Change Display Name to: "Comment Text"
4. Keep Internal Name: "Title"
5. Set column type to: "Multiple lines of text"
6. Number of Lines: 3
7. Enable Rich text
8. Click "Save"
```

---

#### Step 3: Add IssueId Lookup Column

**Action:** Link to parent Issue

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Lookup |
| **Display Name** | IssueId |
| **Get information from** | Issue |
| **In this column** | IssueNumber |
| **Required** | Yes |

**Steps:**

```
1. Click "+ Add column"
2. Select "Lookup"
3. Display Name: "IssueId"
4. Get information from: "Issue"
5. In this column: "IssueNumber"
6. Required: Yes
7. Click "Save"
```

---

#### Step 4: Add CommentBy Column

**Action:** Track who added comment

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Single line of text |
| **Display Name** | CommentBy |
| **Internal Name** | CommentBy |
| **Required** | Yes |
| **Maximum Length** | 100 |

**Steps:**

```
1. Click "+ Add column"
2. Select "Single line of text"
3. Display Name: "CommentBy"
4. Required: Yes
5. Maximum Length: 100
6. Click "Save"
```

---

#### Step 5: Add CommentDate Column

**Action:** Track when comment was added

**Configuration:**

| Setting | Value |
|---------|-------|
| **Column Type** | Date and Time |
| **Display Name** | CommentDate |
| **Internal Name** | CommentDate |
| **Required** | Yes |
| **Format** | Date and Time |
| **Default Value** | Today |

**Steps:**

```
1. Click "+ Add column"
2. Select "Date and Time"
3. Display Name: "CommentDate"
4. Format: Date and Time
5. Default: [Today]
6. Click "Save"
```

---

#### Step 6: Verify IssueComment List Structure

**Verification Checklist:**

- [ ] List named "IssueComment"
- [ ] 4 columns present:
  - [ ] Comment Text (Note/Multiple lines)
  - [ ] IssueId (Lookup to Issue)
  - [ ] CommentBy (Text)
  - [ ] CommentDate (DateTime)

---

### Configuration Summary for Tasks 2.6.10-2.6.11

| Item | Status | Notes |
|------|--------|-------|
| IssueComment list created | ✓ | Named exactly "IssueComment" |
| 4 columns added | ✓ | All types configured |
| Issue lookup configured | ✓ | Links to Issue.IssueNumber |
| Audit trail columns | ✓ | CommentBy and CommentDate |

---

## List Relationships & Dependencies

### Relationship Diagram

```
┌────────────────────┐
│   Location List    │
│   (76 items)       │
└────────┬───────────┘
         │ Referenced by
         │
         ▼
┌────────────────────┐
│   Issue List       │
│  (new, empty)      │
└────────┬───────────┘
         │ Parent of
         ├──────────────────────────┬─────────────────────┐
         │                          │                     │
         ▼                          ▼                     ▼
  ┌─────────────────┐      ┌──────────────────┐  ┌──────────────────┐
  │ CorrectiveAction│      │ IssueComment     │  │ Audit (optional) │
  │    List         │      │    List          │  │    Reference     │
  │ (new, empty)    │      │  (new, empty)    │  │                  │
  └─────────────────┘      └──────────────────┘  └──────────────────┘
```

### Lookup Field Relationships

#### Issue List References

| Column | References | Notes |
|--------|-----------|-------|
| LocationId | Location.Title | Required - must select a trolley |
| AuditId | Audit.Title | Optional - link to audit that found issue |
| EquipmentId | Equipment.Title | Optional - specific equipment item |

#### CorrectiveAction References

| Column | References | Notes |
|--------|-----------|-------|
| IssueId | Issue.IssueNumber | Required - parent relationship |

#### IssueComment References

| Column | References | Notes |
|--------|-----------|-------|
| IssueId | Issue.IssueNumber | Required - parent relationship |

### Data Flow & Cascading

**Creation Sequence:**

```
1. Issue record created in Issue list
   └─ LocationId set (required)
   └─ Category/Severity/Status set
   └─ ReportedDate auto-set

2. CorrectiveAction records created (zero to many)
   └─ IssueId set to parent Issue
   └─ ActionType selected
   └─ ActionDate and ActionBy recorded

3. IssueComment records created (zero to many)
   └─ IssueId set to parent Issue
   └─ Comment author and date tracked

4. Deletion Behavior
   └─ Deleting Issue → leaves CorrectiveAction & Comments orphaned
      (Consider Power Automate flow to cascade delete)
```

**Recommendation:** Create Power Automate flows to cascade delete comments/actions when issue deleted (optional, Phase 2.8).

---

## Validation Rules

### Issue List Validation

#### Required Field Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| Title | Not empty | "Issue title is required" |
| Description | Not empty | "Please provide issue description" |
| Category | Not empty | "Select issue category" |
| Severity | Not empty | "Select severity level" |
| Status | Not empty | "Status required" |
| LocationId | Not empty | "Must select trolley location" |
| ReportedBy | Not empty | "Who reported this issue?" |
| ReportedDate | Not empty | "Report date required" |

#### Business Logic Validation

| Scenario | Rule | Implementation |
|----------|------|-----------------|
| Status transitions | Only valid state changes | Power Automate validation |
| Critical issues | Auto-escalate to Level1 | Power Automate action |
| Expiry of open issues | Alert if > 30 days old | Power Automate scheduled |
| ReopenCount max | Limit to 3 reopens, then escalate | Power Automate check |

### CorrectiveAction List Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| Title | Not empty | "Action description required" |
| IssueId | Must reference existing Issue | "Must select valid issue" |
| ActionType | Not empty | "Select action type" |
| ActionDate | Valid date | "Must be valid date" |
| ActionBy | Not empty | "Who performed this action?" |

### IssueComment List Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| Title (Comment) | Not empty | "Comment cannot be empty" |
| IssueId | Must reference existing Issue | "Must select valid issue" |
| CommentBy | Not empty | "Who added this comment?" |
| CommentDate | Valid date/time | "Must be valid date/time" |

---

## Calculated Columns

### Issue List Calculated Columns

While not implemented in the initial schema, consider these calculated columns for Phase 2.8:

#### 1. DaysSinceReported

**Purpose:** Show how long issue has been open

**Formula:**
```
=INT(TODAY()-[ReportedDate])
```

**Display:** Used in views to highlight aging issues

**Implementation:**
```
1. Add calculated column
2. Display Name: Days Since Reported
3. Formula: =INT(TODAY()-[ReportedDate])
4. Data type returned: Number
5. Add to "Aging Issues" view
```

#### 2. IsOverdue

**Purpose:** Flag issues not resolved within SLA

**Formula (30-day SLA):**
```
=IF(AND([Status]<>"Closed",[Status]<>"Resolved",INT(TODAY()-[ReportedDate])>30),"Yes","No")
```

**Display:** Color-coded conditional formatting

#### 3. ActionCount

**Purpose:** Show number of corrective actions

**Note:** This requires Power Automate as SharePoint formulas cannot count related items. Use a flow to set a counter field.

### Recommendation

For now, skip calculated columns. Implement them in Phase 2.8 when adding views and formatting.

---

## Views Configuration

### Issue List Views

After lists are created, configure these views:

#### View 1: All Issues (Default)

| Setting | Value |
|---------|-------|
| **View Name** | All Issues |
| **Default** | Yes |
| **Columns Shown** | IssueNumber, Title, Severity, Status, LocationId, AssignedTo |
| **Sort** | ReportedDate (Descending) |
| **Filter** | None |
| **Group by** | None |

#### View 2: Open Issues

**Purpose:** Show unresolved issues

| Setting | Value |
|---------|-------|
| **Filter** | Status ≠ Closed AND Status ≠ Resolved |
| **Sort** | Severity (Critical first), ReportedDate (newest) |
| **Columns** | IssueNumber, Title, Severity, LocationId, AssignedTo, Days overdue |

#### View 3: By Status

**Purpose:** Grouped by workflow state

| Setting | Value |
|---------|-------|
| **Group by** | Status |
| **Sort** | Severity (Descending) within each group |
| **Columns** | IssueNumber, Title, Severity, LocationId |

#### View 4: My Issues

**Purpose:** Filter to current user's assignments

| Setting | Value |
|---------|-------|
| **Filter** | AssignedTo = [Me] AND Status ≠ Closed |
| **Sort** | Severity (Critical first) |
| **Columns** | IssueNumber, Title, Severity, LocationId, ResolvedDate |

#### View 5: Critical Issues

**Purpose:** High-priority items requiring attention

| Setting | Value |
|---------|-------|
| **Filter** | Severity = Critical |
| **Sort** | ReportedDate (newest) |
| **Columns** | IssueNumber, Title, LocationId, AssignedTo, AssignedDate |

### CorrectiveAction List Views

#### View 1: All Actions (Default)

| Setting | Value |
|---------|-------|
| **Columns** | Title, IssueId, ActionType, ActionDate, ActionBy |
| **Sort** | ActionDate (Descending) |

#### View 2: By Issue

| Setting | Value |
|---------|-------|
| **Group by** | IssueId |
| **Sort** | ActionDate (Ascending within group) |

#### View 3: Pending Completion

| Setting | Value |
|---------|-------|
| **Filter** | CompletedDate is empty |
| **Sort** | ActionDate (Ascending) |

### IssueComment List Views

#### View 1: All Comments (Default)

| Setting | Value |
|---------|-------|
| **Columns** | Title, IssueId, CommentBy, CommentDate |
| **Sort** | CommentDate (Ascending - oldest first) |

#### View 2: By Issue

| Setting | Value |
|---------|-------|
| **Group by** | IssueId |
| **Sort** | CommentDate (Ascending within group) |

---

## Testing Verification

### Phase 2.6 Completion Verification

Use this checklist to verify all Phase 2.6 tasks are complete and functioning correctly.

### Test 1: Issue List Structure

**Objective:** Verify Issue list has all required columns and settings

**Steps:**

```
1. Navigate to Issue list
2. Verify list name: "Issue" (exact spelling)
3. Count columns - should have 18 total
4. Verify each column:
   - Column name
   - Column type
   - Required/optional status
   - Default values (if applicable)
```

**Verification Checklist:**

**Columns:**
- [ ] IssueNumber (Text) - Required: No
- [ ] Issue Title (Text) - Required: Yes
- [ ] Description (Note) - Required: Yes
- [ ] Category (Choice) - Required: Yes, Options: Equipment/Documentation/Condition/Process
- [ ] Severity (Choice) - Required: Yes, Options: Critical/High/Medium/Low
- [ ] Status (Choice) - Required: Yes, Options: Open/Assigned/In_Progress/Pending_Verification/Resolved/Closed
- [ ] LocationId (Lookup) - Required: Yes
- [ ] AuditId (Lookup) - Required: No
- [ ] EquipmentId (Lookup) - Required: No
- [ ] ReportedBy (Text) - Required: Yes
- [ ] ReportedDate (DateTime) - Required: Yes
- [ ] AssignedTo (User) - Required: No
- [ ] AssignedDate (DateTime) - Required: No
- [ ] ResolvedDate (DateTime) - Required: No
- [ ] ClosedDate (DateTime) - Required: No
- [ ] EscalationLevel (Choice) - Required: No, Options: None/Level1/Level2/Level3
- [ ] EscalatedTo (User) - Required: No
- [ ] ReopenCount (Number) - Required: No

**Result:** ✓ PASS / ✗ FAIL

---

### Test 2: CorrectiveAction List Structure

**Objective:** Verify CorrectiveAction list configuration

**Steps:**

```
1. Navigate to CorrectiveAction list
2. Verify list name: "CorrectiveAction"
3. Verify 7 columns present
4. Check each column type and settings
```

**Verification Checklist:**

- [ ] Action Title (Text) - Required: Yes
- [ ] IssueId (Lookup to Issue) - Required: Yes
- [ ] ActionType (Choice) - Required: Yes, Options: Replacement/Repair/Restock/Training/Process Change/Other
- [ ] Description (Note) - Required: No
- [ ] ActionDate (DateTime) - Required: Yes
- [ ] ActionBy (Text) - Required: Yes
- [ ] CompletedDate (DateTime) - Required: No

**Result:** ✓ PASS / ✗ FAIL

---

### Test 3: IssueComment List Structure

**Objective:** Verify IssueComment list configuration

**Steps:**

```
1. Navigate to IssueComment list
2. Verify list name: "IssueComment"
3. Verify 4 columns present
```

**Verification Checklist:**

- [ ] Comment Text (Note) - Required: Yes
- [ ] IssueId (Lookup to Issue) - Required: Yes
- [ ] CommentBy (Text) - Required: Yes
- [ ] CommentDate (DateTime) - Required: Yes, Default: Today

**Result:** ✓ PASS / ✗ FAIL

---

### Test 4: Lookups Functioning

**Objective:** Verify lookup fields work correctly

**Steps:**

```
1. From Issue list, add new item
2. Click LocationId field
3. Verify dropdown shows all locations from Location list
4. Select one location
5. Click AuditId field (if test audits exist)
6. Verify dropdown shows audit records
7. Save item
```

**Verification Checklist:**

- [ ] LocationId dropdown populated with locations
- [ ] Can select location successfully
- [ ] AuditId dropdown populated (if Audit records exist)
- [ ] Item saves with lookup selected

**Result:** ✓ PASS / ✗ FAIL

---

### Test 5: Choice Fields Functioning

**Objective:** Verify choice column dropdowns work

**Steps:**

```
1. Create test issue record
2. Click Category dropdown
3. Verify shows: Equipment, Documentation, Condition, Process
4. Select one
5. Click Severity dropdown
6. Verify shows: Critical, High, Medium, Low
7. Select one
8. Click Status dropdown
9. Verify shows: Open, Assigned, In_Progress, etc.
10. Save item
```

**Verification Checklist:**

- [ ] Category shows 4 options
- [ ] Severity shows 4 options
- [ ] Status shows 6 options
- [ ] Can select and save choices
- [ ] Default values apply (Category: Equipment, Severity: Medium, Status: Open)

**Result:** ✓ PASS / ✗ FAIL

---

### Test 6: Date Fields

**Objective:** Verify date columns work correctly

**Steps:**

```
1. Create test issue
2. Verify ReportedDate auto-populated with today's date
3. Manually enter AssignedDate
4. Verify DateTime format (includes time)
5. Leave ResolvedDate and ClosedDate empty
6. Save item
```

**Verification Checklist:**

- [ ] ReportedDate auto-populated with today
- [ ] Can manually set dates
- [ ] Optional dates can be left blank
- [ ] Dates display correctly (format: MM/DD/YYYY HH:MM)

**Result:** ✓ PASS / ✗ FAIL

---

### Test 7: Cross-List Relationships

**Objective:** Verify child lists link to Issue correctly

**Steps - CorrectiveAction:**

```
1. Go to CorrectiveAction list
2. Create new item
3. Click IssueId lookup
4. Verify dropdown shows Issue records
5. Select the test issue created above
6. Enter action details
7. Save
8. Go back to Issue list
9. Navigate to the issue item
10. Verify we can see related actions (via Power Automate later)
```

**Steps - IssueComment:**

```
1. Go to IssueComment list
2. Create new comment
3. Click IssueId lookup
4. Select same test issue
5. Enter comment text
6. Save
```

**Verification Checklist:**

- [ ] CorrectiveAction IssueId lookup shows Issue records
- [ ] Can select Issue from dropdown
- [ ] IssueComment IssueId lookup shows Issue records
- [ ] Can select Issue from dropdown
- [ ] Records save successfully with lookups

**Result:** ✓ PASS / ✗ FAIL

---

### Test 8: List Navigation

**Objective:** Verify lists appear in site navigation

**Steps:**

```
1. Go to site home
2. Check left navigation menu
3. Look for Issue list (should appear)
4. Look for CorrectiveAction list (should appear)
5. Look for IssueComment list (should appear)
6. Click each to verify they navigate correctly
```

**Verification Checklist:**

- [ ] Issue list appears in navigation
- [ ] CorrectiveAction list appears in navigation
- [ ] IssueComment list appears in navigation
- [ ] All lists accessible via navigation

**Result:** ✓ PASS / ✗ FAIL

---

### Test 9: List Settings

**Objective:** Verify list-level settings are correct

**Steps:**

```
1. For each list (Issue, CorrectiveAction, IssueComment):
   a. Go to list settings
   b. Verify "Allow attachments": Yes
   c. Verify "Enable versioning": Yes
   d. Verify "Require checkout": No (or your preference)
```

**Verification Checklist:**

- [ ] Issue: Attachments enabled
- [ ] Issue: Versioning enabled
- [ ] CorrectiveAction: Attachments enabled
- [ ] CorrectiveAction: Versioning enabled
- [ ] IssueComment: Attachments enabled
- [ ] IssueComment: Versioning enabled

**Result:** ✓ PASS / ✗ FAIL

---

### Test 10: Data Entry Test

**Objective:** Complete end-to-end data entry workflow

**Steps:**

```
1. Create complete Issue record:
   - Title: "Test Issue"
   - Description: "Test description"
   - Category: Equipment
   - Severity: High
   - Status: Open
   - LocationId: Select any location
   - ReportedBy: Your name
   - Leave other fields empty

2. Save record

3. Create CorrectiveAction:
   - IssueId: Select the issue just created
   - Title: "Test Action"
   - ActionType: Repair
   - ActionDate: Today
   - ActionBy: Your name

4. Save record

5. Create IssueComment:
   - IssueId: Select same issue
   - Comment Text: "This is a test comment"
   - CommentBy: Your name
   - CommentDate: Auto-populated

6. Save record

7. Return to Issue and verify all three records created
```

**Verification Checklist:**

- [ ] Issue created successfully
- [ ] Can save with only required fields
- [ ] CorrectiveAction created and linked
- [ ] IssueComment created and linked
- [ ] All records accessible from list view

**Result:** ✓ PASS / ✗ FAIL

---

### Test 11: JSON Schema Validation

**Objective:** Verify schema files are valid JSON

**Steps:**

```
1. Open SharePoint_schemas folder
2. Locate Issue.json, CorrectiveAction.json, IssueComment.json
3. Validate each file:
   a. Open in text editor or JSON validator
   b. Check for syntax errors
   c. Verify all required fields present
```

**Verification Checklist:**

- [ ] Issue.json is valid JSON
- [ ] CorrectiveAction.json is valid JSON
- [ ] IssueComment.json is valid JSON
- [ ] All schema files present in folder

**Result:** ✓ PASS / ✗ FAIL

---

### Test 12: Performance Check

**Objective:** Verify lists respond quickly

**Steps:**

```
1. Add 10 test records to Issue list
2. Add 20 test records to CorrectiveAction list
3. Add 30 test records to IssueComment list
4. Navigate to each list
5. Verify list loads within 3 seconds
6. Filter/sort each list
7. Verify filter responds within 2 seconds
```

**Verification Checklist:**

- [ ] Issue list loads quickly (< 3 seconds)
- [ ] CorrectiveAction list loads quickly
- [ ] IssueComment list loads quickly
- [ ] Filtering responds quickly (< 2 seconds)
- [ ] Sorting works without delay

**Result:** ✓ PASS / ✗ FAIL

---

### Overall Phase 2.6 Sign-Off

| Test | Pass | Status |
|------|------|--------|
| Issue list structure | ✓/✗ | PASS / FAIL |
| CorrectiveAction list structure | ✓/✗ | PASS / FAIL |
| IssueComment list structure | ✓/✗ | PASS / FAIL |
| Lookups functioning | ✓/✗ | PASS / FAIL |
| Choice fields functioning | ✓/✗ | PASS / FAIL |
| Date fields functioning | ✓/✗ | PASS / FAIL |
| Cross-list relationships | ✓/✗ | PASS / FAIL |
| List navigation | ✓/✗ | PASS / FAIL |
| List settings | ✓/✗ | PASS / FAIL |
| Data entry workflow | ✓/✗ | PASS / FAIL |
| JSON schemas valid | ✓/✗ | PASS / FAIL |
| Performance acceptable | ✓/✗ | PASS / FAIL |

**Phase 2.6 Status:**

- [ ] All tests PASS - Ready for Phase 2.7
- [ ] Some tests FAIL - Review and retest
- [ ] Unable to proceed - Contact support

---

## Summary

You have successfully completed Phase 2.6 - Issue Management Lists for the REdI Trolley Audit system.

### What Was Accomplished

✓ **Task 2.6.1** - Created Issue list schema with 18 columns
✓ **Task 2.6.2** - Configured LocationId lookup (required)
✓ **Task 2.6.3** - Configured AuditId lookup (optional)
✓ **Task 2.6.4** - Configured EquipmentId lookup (optional)
✓ **Task 2.6.5** - Added Category, Severity, Status choice columns
✓ **Task 2.6.6** - Prepared IssueNumber column for auto-generation (Phase 2.8)
✓ **Task 2.6.7** - Created CorrectiveAction list with 7 columns
✓ **Task 2.6.8** - Configured IssueId lookup to Issue
✓ **Task 2.6.9** - Added ActionType choice column
✓ **Task 2.6.10** - Created IssueComment list with 4 columns
✓ **Task 2.6.11** - Configured IssueId lookup to Issue

### Key Artefacts Created

1. **Issue List** (REdI Trolley Audit / Issue)
   - Central issue tracking repository
   - 18 columns for comprehensive issue management
   - Links to Location, Audit, Equipment
   - Status workflow tracking
   - Escalation management

2. **CorrectiveAction List** (REdI Trolley Audit / CorrectiveAction)
   - Child list tracking actions to resolve issues
   - 7 columns with action classification
   - Links to parent Issue

3. **IssueComment List** (REdI Trolley Audit / IssueComment)
   - Audit trail of comments and updates
   - 4 columns for minimal tracking
   - Links to parent Issue

### Phase 2.6 Dependency Graph

```
Phase 2.6 Complete
       ↓
Phase 2.7 Ready: Issue Management Screens
  (Create UI components for issue tracking)
       ↓
Phase 2.8 Ready: Issue Workflow Flows
  (Add automation for status transitions, escalation)
```

### Next Steps

**Immediate (Phase 2.7):**
- Create Issue List screen in PowerApp
- Create Issue Detail screen
- Add Issue filtering and sorting

**Soon (Phase 2.8):**
- Implement issue number auto-generation
- Create workflow flows for status transitions
- Add escalation automation

**Later (Phase 2.9):**
- Integrate with audit submission process
- Auto-create issues from audit findings
- Link to random selection if needed

---

**Document Version:** 1.0
**Last Updated:** January 2026
**Status:** APPROVED FOR IMPLEMENTATION

For questions or updates, contact the MERT Coordination Team.

---

*End of Phase 2.6 Implementation Guide*
