# Phase 2.8 Issue Workflow Flows Implementation Guide

**REdI Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 2.8 implements the complete issue workflow automation through 11 Power Automate flows. These flows manage the entire issue lifecycle from creation through resolution, including status transitions, corrective action tracking, comments, escalation, and reopening. Each flow is designed to enforce business rules and maintain data integrity.

**Phase Scope:** Tasks 2.8.1 through 2.8.11
**Estimated Duration:** 15 hours
**Prerequisites:**
- Phase 2.6 complete (Issue, CorrectiveAction, IssueComment lists created)
- Phase 2.7 complete (Issue management screens and dialogs built)
- Access to Power Automate with edit permissions to create flows

**Dependency Graph:**
```
2.8.1 (Save New Issue) → 2.8.2 (Generate Issue Number)
                          │
                          ▼
              2.8.3 (Assign Issue)
              2.8.4 (Save Corrective Action) → 2.8.5 (Update Status on First Action)
              2.8.6 (Save Comment)
              2.8.7 (Mark Resolved)
              2.8.8 (Verify Resolution)
              2.8.9 (Close Issue)
              2.8.10 (Reopen Issue)
              2.8.11 (Escalate Issue)
```

---

## Issue Status Lifecycle Reference

Before implementing flows, understand the complete status transition model:

```
┌────────────────────────────────────────────────────────────┐
│                   ISSUE STATUS LIFECYCLE                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐    │
│  │  OPEN    │───▶│ ASSIGNED │───▶│  IN_PROGRESS     │    │
│  └──────────┘    └──────────┘    └──────────────────┘    │
│                                          │                 │
│                                          ▼                 │
│                                  ┌──────────────────┐    │
│                                  │PENDING_VERIFICATION│  │
│                                  └──────────────────┘    │
│                                          │                 │
│                                          ▼                 │
│                                   ┌──────────┐            │
│                                   │ RESOLVED │            │
│                                   └──────────┘            │
│                                          │                 │
│                                          ▼                 │
│                                   ┌──────────┐            │
│                                   │  CLOSED  │            │
│                                   └──────────┘            │
│                                          ▲                 │
│                   ┌────────────────────────┘              │
│                   │                                       │
│           (Can Reopen → IN_PROGRESS)                     │
│                                                            │
│  Escalation: Can occur from any status                   │
│  (Updates EscalationLevel +1, EscalatedTo = Manager)     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Status Definitions:**
- **Open:** Issue logged but not yet assigned
- **Assigned:** Issue has been assigned to a person
- **In_Progress:** Corrective action(s) have been started
- **Pending_Verification:** Issue marked as resolved, awaiting verification
- **Resolved:** Resolution verified and confirmed
- **Closed:** Issue fully resolved and closed
- **Reopened:** Issue was resolved but new evidence requires re-opening (status → In_Progress)

---

## Prerequisite: Issue List Schema Reference

All flows reference the following Issue list columns:

| Column | Type | Required | Purpose |
|--------|------|----------|---------|
| Title | Text | Yes | Issue ID (ISS-2026-0001 format) |
| IssueNumber | Calculated | Auto | Sequential number ISS-YYYY-NNNN |
| Location | Lookup | Yes | Trolley location reference |
| Audit | Lookup | No | Related audit (if from audit) |
| Equipment | Lookup | No | Related equipment item (if applicable) |
| Category | Choice | Yes | Equipment / Documentation / Trolley / Other |
| Severity | Choice | Yes | Critical / High / Medium / Low |
| Title_Issue | Text | Yes | Brief issue description |
| Description | Note | Yes | Detailed description |
| Status | Choice | Yes | See status lifecycle above |
| ReportedDate | DateTime | Auto | Date/time issue created |
| ReportedBy | User | Yes | Person who logged issue |
| AssignedTo | User | No | Person assigned to resolve |
| AssignedDate | DateTime | No | When assigned |
| ReopenCount | Number | Default: 0 | Times issue has been reopened |
| EscalationLevel | Number | Default: 0 | Escalation count (0, 1, 2, 3) |
| EscalatedTo | User | No | Manager escalated to |
| EscalatedDate | DateTime | No | When escalated |
| ResolvedDate | DateTime | No | When marked resolved |
| ClosedDate | DateTime | No | When closed |

**Related Lists:**
- **CorrectiveAction** - Child records linked via Lookup
- **IssueComment** - Child records linked via Lookup

---

## Task 2.8.1: Create Save New Issue Flow

### Objective

Create a Power Automate flow triggered from the "Add Issue" dialog in PowerApp that creates a new Issue record with all required fields populated.

### Prerequisites

- Power Automate environment access
- Issue list created (Task 2.6.1)
- PowerApp with "Add Issue" dialog (Task 2.7.13)
- Permission to create flows in the Power Automate environment

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** in the left navigation
3. Select **Cloud flows** → **Instant cloud flow** (Manually triggered)
4. Name the flow: `Save New Issue`
5. Click **Create**

#### Step 2: Configure Trigger

The flow will receive data from PowerApp. Add input parameters:

1. In the trigger section, click **Edit in advanced mode**
2. Replace the trigger JSON schema with:

```json
{
  "type": "object",
  "properties": {
    "issueCategory": {
      "type": "string",
      "title": "Issue Category",
      "description": "Equipment / Documentation / Trolley / Other"
    },
    "issueSeverity": {
      "type": "string",
      "title": "Issue Severity",
      "description": "Critical / High / Medium / Low"
    },
    "issueTitle": {
      "type": "string",
      "title": "Issue Title",
      "description": "Brief issue description (max 100 chars)"
    },
    "issueDescription": {
      "type": "string",
      "title": "Issue Description",
      "description": "Detailed issue description"
    },
    "locationId": {
      "type": "string",
      "title": "Location ID",
      "description": "GUID of Location record"
    },
    "auditId": {
      "type": "string",
      "title": "Audit ID",
      "description": "GUID of Audit (optional)"
    },
    "equipmentId": {
      "type": "string",
      "title": "Equipment ID",
      "description": "GUID of Equipment (optional)"
    },
    "reportedByEmail": {
      "type": "string",
      "title": "Reported By Email",
      "description": "Email of person logging issue"
    }
  },
  "required": ["issueCategory", "issueSeverity", "issueTitle", "issueDescription", "locationId", "reportedByEmail"]
}
```

#### Step 3: Add Create Issue Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Create item**
4. Configure:
   - **Site Address:** Select REdI Trolley Audit site
   - **List Name:** Issue

5. Click **Edit in advanced mode** to add all fields

#### Step 4: Configure Fields for New Issue

Add the following field mappings (click "Add dynamic content" for field values):

```
Title:
  Expression: concat('ISS-', year(utcNow()), '-', formatNumber(int(substring(utcNow(), 5, 2)), '0000'))

IssueNumber (if separate):
  Expression: Same as Title

Category:
  Dynamic Content: @triggerBody()['issueCategory']

Severity:
  Dynamic Content: @triggerBody()['issueSeverity']

Title_Issue:
  Dynamic Content: @triggerBody()['issueTitle']

Description:
  Dynamic Content: @triggerBody()['issueDescription']

Location:
  Dynamic Content: @triggerBody()['locationId']

Audit (if provided):
  Dynamic Content: @triggerBody()['auditId']

Equipment (if provided):
  Dynamic Content: @triggerBody()['equipmentId']

Status:
  Value: "Open"

ReportedDate:
  Dynamic Content: @utcNow()

ReportedBy:
  Dynamic Content: @triggerBody()['reportedByEmail']
  (SharePoint will resolve email to user ID)

ReopenCount:
  Value: 0

EscalationLevel:
  Value: 0
```

**Important:** Ensure all required fields are populated. Optional fields (Audit, Equipment) use conditional logic.

#### Step 5: Add Response Action

1. Click **+ New step** after the Create item action
2. Search for "Response"
3. Select **Response** action
4. Set Status code to: `200`
5. Set Body to:

```json
{
  "success": true,
  "issueId": @outputs('Create_item')?['body/ID'],
  "issueTitle": @triggerBody()['issueTitle'],
  "message": "Issue successfully created"
}
```

#### Step 6: Test the Flow

1. Click **Save**
2. Click **Test** → **Manually**
3. Provide sample input:
   - issueCategory: "Equipment"
   - issueSeverity: "High"
   - issueTitle: "BVM mask missing"
   - issueDescription: "Top of trolley BVM mask not present during audit"
   - locationId: (paste valid Location item GUID)
   - reportedByEmail: (your email)
4. Click **Run test**
5. Verify issue record created in SharePoint

### Flow Definition

**Trigger Type:** Manual (from PowerApp)

**Actions:**
1. Create item in Issue list
2. Return successful response with issue ID

**Data Flow Diagram:**
```
PowerApp Dialog
      │
      ├─ Issue Category
      ├─ Issue Severity
      ├─ Issue Title
      ├─ Issue Description
      ├─ Location ID
      ├─ Audit ID (optional)
      ├─ Equipment ID (optional)
      └─ Reported By Email
            │
            ▼
    Save New Issue Flow
            │
    ┌───────┴───────┐
    │               │
    ▼               ▼
Generate      Create Issue Item
Issue Number  (Status: Open)
(ISS-YYYY-NNNN)    │
                   ▼
            Return Success Response
                   │
                   ▼
            PowerApp Updates UI
```

### Error Handling

**Scenario: Required field missing**
- **Detection:** Create item fails with "required field" error
- **Response:** Flow terminates with error message to PowerApp
- **Mitigation:** Validate all required fields in PowerApp before triggering flow

**Scenario: Location doesn't exist**
- **Detection:** LocationId parameter references non-existent record
- **Response:** Create item fails with lookup error
- **Mitigation:** PowerApp location dropdown only shows valid Location records

**Scenario: Duplicate issue number collision**
- **Detection:** Same-day issue with same sequence number (extremely rare)
- **Response:** SharePoint enforces unique constraint; create fails
- **Mitigation:** Add milliseconds to number: `formatNumber(int(substring(utcNow(), 5, 2)), '0000')` + hash of description

### Verification Checklist

- [ ] Flow created and named "Save New Issue"
- [ ] Manual trigger with proper input schema defined
- [ ] Issue list item creation action configured
- [ ] All required fields mapped correctly
- [ ] Issue status set to "Open"
- [ ] ReportedDate set to current date/time
- [ ] ReopenCount initialized to 0
- [ ] EscalationLevel initialized to 0
- [ ] Response action returns success message with Issue ID
- [ ] Flow tested with sample data
- [ ] New Issue record verified in SharePoint

---

## Task 2.8.2: Generate Issue Number in Flow

### Objective

Configure the issue numbering system to generate sequential issue numbers in the format ISS-YYYY-NNNN (e.g., ISS-2026-0001, ISS-2026-0002).

### Prerequisites

- Task 2.8.1 completed (Save New Issue flow created)
- Issue list has IssueNumber calculated column created (Task 2.6.6)
- Understanding of Power Automate expressions for date/number manipulation

### Step-by-Step Instructions

#### Step 1: Understand Current Year Issue Count

In SharePoint, we need to count existing issues from the current year to generate the next sequential number.

1. Open the "Save New Issue" flow created in Task 2.8.1
2. We'll modify the Title field to use a proper sequential number

#### Step 2: Add Filter Query Action (Before Create Item)

1. In the "Save New Issue" flow, click **+ New step** (before the Create item action)
2. Search for "SharePoint"
3. Select **Get items**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue

5. Click **Edit in advanced mode** to add OData filter

#### Step 3: Filter for Current Year Issues

In the Get items action, add OData filter query:

```
odata:
filterQuery=startswith(Title, concat('ISS-', year(utcNow())))
```

This retrieves all issues from the current year.

**PowerFx Expression:**
```
@concat('ISS-', string(year(utcNow())), '-*')
```

#### Step 4: Calculate Next Sequence Number

After retrieving current year issues, add a **Compose** action:

1. Click **+ New step**
2. Search for "Compose"
3. Select **Compose** action
4. In the Inputs field, add expression:

```
@concat('ISS-', string(year(utcNow())), '-', padLeft(string(add(length(outputs('Get_items')?['body/value']), 1)), 4, '0'))
```

**Expression Explanation:**
- `year(utcNow())` - Current year (2026)
- `length(outputs('Get_items')?['body/value'])` - Count of existing 2026 issues
- `add(..., 1)` - Add 1 to get next sequence number
- `padLeft(..., 4, '0')` - Left-pad with zeros to 4 digits (0001, 0002, etc.)
- `concat(...)` - Combine into format ISS-YYYY-NNNN

#### Step 5: Use Generated Number in Create Item

1. Find the Create item action in your flow
2. Modify the **Title** field to reference the composed number:

```
Dynamic Content: @outputs('Compose')?['body']
```

3. Also update the **IssueNumber** field (if it exists as a separate field) to the same value

#### Step 6: Test Sequential Generation

1. Save the flow
2. Test it multiple times in the same day
3. Verify each new issue gets an incremented sequence number:
   - First issue: ISS-2026-0001
   - Second issue: ISS-2026-0002
   - Third issue: ISS-2026-0003

4. Check that next day's issue starts at ISS-2026-0004 (continues sequence through year)

### Implementation Pattern: Complete Updated Flow

**Update Flow Structure:**

```
Trigger: Manual (PowerApp)
  ↓
Get items from Issue list (filter: current year)
  ↓
Compose: Calculate next issue number
  ISS-YYYY-NNNN format
  ↓
Create item in Issue list
  Title: [Composed number]
  Category: [From input]
  Severity: [From input]
  Status: "Open"
  ReportedDate: [Current date/time]
  ReportedBy: [From input]
  ↓
Response: Return success with Issue ID
```

### Performance Optimization

**For high-volume issue creation** (unlikely in this scenario, but good practice):

Add a **Scope** action to wrap the Get items action to make failures non-blocking:

```
If Get items fails:
  Generate number based on timestamp hash instead:
  @concat('ISS-', string(year(utcNow())), '-', substring(string(rand(1000, 9999)), 0, 4))
```

### Error Handling

**Scenario: Multiple issues created simultaneously**
- **Detection:** Race condition - two flows create issues before either increments counter
- **Response:** Sequential number collision (ISS-2026-0001 created twice)
- **Mitigation:** SharePoint enforces unique constraint on Title; second creation fails
  - Add retry logic with exponential backoff (3 retries, 1-3 second delay)

**Scenario: Get items query times out**
- **Detection:** Filter query returns timeout error
- **Response:** Flow fails without creating issue
- **Mitigation:** Use Scope action to catch timeout and generate fallback number
  ```
  Fallback: ISS-YYYY-[Timestamp]
  Example: ISS-2026-1672531200000
  ```

**Scenario: Year changes at midnight**
- **Detection:** Issue created at 23:59:59 on Dec 31 vs 00:00:00 on Jan 1
- **Response:** Year in number changes naturally
- **Expected:** ISS-2025-9999 → ISS-2026-0001 (correct behavior)

### Verification Checklist

- [ ] Get items action added to retrieve current year issues
- [ ] OData filter query correctly filters by current year
- [ ] Compose action creates correct ISS-YYYY-NNNN format
- [ ] Sequence number increments correctly (1, 2, 3...)
- [ ] Title field uses composed number in Create item action
- [ ] Flow tested multiple times in same day
- [ ] Issue numbers increment sequentially
- [ ] Year rollover tested (if applicable)
- [ ] Unique constraint prevents duplicates
- [ ] Error handling for Get items failures documented

---

## Task 2.8.3: Create Assign Issue Flow

### Objective

Create a Power Automate flow triggered from PowerApp that assigns an issue to a person, updates the AssignedTo and AssignedDate fields, and changes status to "Assigned".

### Prerequisites

- Task 2.8.1 completed (Issue list populated with new issues)
- Issue Detail screen with "Assign" action (Task 2.7.8)
- User lookup column available in Issue list

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Assign Issue`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. In the trigger section, click **Edit in advanced mode**
2. Replace trigger JSON schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of the issue to assign"
    },
    "assignedToEmail": {
      "type": "string",
      "title": "Assigned To Email",
      "description": "Email of person to assign issue to"
    }
  },
  "required": ["issueId", "assignedToEmail"]
}
```

#### Step 3: Add Update Issue Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Update item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

5. Click **Edit in advanced mode** to add field mappings

#### Step 4: Map Assignment Fields

Add the following field updates:

```
AssignedTo:
  Dynamic Content: @triggerBody()['assignedToEmail']
  (SharePoint resolves email to user ID)

AssignedDate:
  Dynamic Content: @utcNow()

Status:
  Value: "Assigned"
```

**Important:** Only update these three fields to prevent overwriting other data.

#### Step 5: Add Response Action

1. Click **+ New step**
2. Search for "Response"
3. Select **Response**
4. Set Status code: `200`
5. Set Body:

```json
{
  "success": true,
  "issueId": @triggerBody()['issueId'],
  "assignedToEmail": @triggerBody()['assignedToEmail'],
  "message": "Issue assigned successfully"
}
```

#### Step 6: Test the Flow

1. Save the flow
2. Click **Test** → **Manually**
3. Get an existing issue ID and valid user email
4. Provide input:
   - issueId: (paste issue ID from SharePoint)
   - assignedToEmail: (valid user email)
5. Click **Run test**
6. Verify in SharePoint that issue now shows:
   - Status: "Assigned"
   - AssignedTo: (selected user)
   - AssignedDate: (today's date)

### Flow Definition

**Trigger Type:** Manual (from PowerApp Issue Detail screen)

**Actions:**
1. Update Issue item with assignment details
2. Return success response

**Status Transition:**
```
Before: Status = "Open"
After:  Status = "Assigned"
        AssignedTo = [Selected User]
        AssignedDate = [Today]
```

### Error Handling

**Scenario: Invalid issue ID**
- **Detection:** Update item action fails with "Item not found"
- **Response:** Flow terminates with 404 error
- **Mitigation:** PowerApp only shows valid issue IDs from Issue list

**Scenario: Invalid email address**
- **Detection:** SharePoint user lookup fails to resolve email
- **Response:** Update item fails; AssignedTo field remains empty
- **Mitigation:** PowerApp user picker only shows valid organizational users

**Scenario: Issue already assigned**
- **Detection:** (Expected scenario) Updating already-assigned issue
- **Response:** Previous assignee is replaced with new assignee (correct behavior)
- **Mitigation:** PowerApp shows warning: "This issue was previously assigned to [name]. Continue?"

**Scenario: Status is already "In_Progress"**
- **Detection:** (Expected scenario) User tries to assign issue already being worked
- **Response:** Status stays "In_Progress" (assignment happens, status doesn't change)
- **Fix:** Add condition to only update status if current status is "Open"

```
Condition: If current Status = "Open" THEN set Status = "Assigned"
          Else do not change Status
```

### Implementation with Status Check

Improved flow structure:

```
Trigger: Manual (issueId, assignedToEmail)
  ↓
Get item from Issue list (retrieve current status)
  ↓
Condition: If Status = "Open"?
  ├─ YES: Update item with Status = "Assigned"
  │         AssignedTo = email
  │         AssignedDate = now()
  │
  └─ NO: Update item with AssignedTo = email
         AssignedDate = now()
         (keep existing status)
  ↓
Response: Return success
```

### Verification Checklist

- [ ] Flow created and named "Assign Issue"
- [ ] Manual trigger with issueId and assignedToEmail schema defined
- [ ] Get item action retrieves current issue status
- [ ] Condition checks if status is "Open"
- [ ] Update item action maps all three fields correctly
- [ ] AssignedTo uses user email resolution
- [ ] AssignedDate set to current date/time
- [ ] Status updated to "Assigned" (only if was "Open")
- [ ] Response returns success message
- [ ] Flow tested with valid issue ID and user email
- [ ] Assignment verified in SharePoint

---

## Task 2.8.4: Create Save Corrective Action Flow

### Objective

Create a Power Automate flow that saves a corrective action record linked to an issue when the user submits the "Add Action" dialog.

### Prerequisites

- Task 2.8.1 completed (Issues exist)
- CorrectiveAction list created (Task 2.6.7)
- CorrectiveAction lookup to Issue configured (Task 2.6.8)
- "Add Action" dialog in PowerApp (Task 2.7.19)

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Save Corrective Action`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of parent issue"
    },
    "actionType": {
      "type": "string",
      "title": "Action Type",
      "description": "Repair / Replace / Document / Investigate / Other"
    },
    "actionDescription": {
      "type": "string",
      "title": "Action Description",
      "description": "Detailed description of corrective action"
    },
    "assignedToEmail": {
      "type": "string",
      "title": "Assigned To Email",
      "description": "Email of person assigned to this action"
    }
  },
  "required": ["issueId", "actionType", "actionDescription", "assignedToEmail"]
}
```

#### Step 3: Add Create CorrectiveAction Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Create item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** CorrectiveAction

5. Click **Edit in advanced mode** for all fields

#### Step 4: Map CorrectiveAction Fields

Add field mappings:

```
Title:
  Expression: @concat('ACT-', triggerBody()['issueId'], '-', utcNow())

Issue (Lookup):
  Dynamic Content: @triggerBody()['issueId']

ActionType:
  Dynamic Content: @triggerBody()['actionType']

ActionDescription:
  Dynamic Content: @triggerBody()['actionDescription']

AssignedTo:
  Dynamic Content: @triggerBody()['assignedToEmail']

Status:
  Value: "Open"

CreatedDate:
  Dynamic Content: @utcNow()

CreatedBy:
  Dynamic Content: User executing the flow (or from context)

DueDate:
  Value: Empty (user can set later)
```

#### Step 5: Add Response Action

1. Click **+ New step**
2. Select **Response**
3. Status code: `200`
4. Body:

```json
{
  "success": true,
  "actionId": @outputs('Create_item')?['body/ID'],
  "issueId": @triggerBody()['issueId'],
  "message": "Corrective action created successfully"
}
```

#### Step 6: Test the Flow

1. Save the flow
2. Get a valid Issue ID from SharePoint
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (valid ID from Issue list)
   - actionType: "Repair"
   - actionDescription: "Replace missing BVM mask with new sterile unit"
   - assignedToEmail: (valid user email)
5. Click **Run test**
6. Verify in SharePoint:
   - New CorrectiveAction record created
   - Linked to correct Issue
   - All fields populated correctly

### Flow Definition

**Trigger Type:** Manual (from PowerApp "Add Action" dialog)

**Actions:**
1. Create CorrectiveAction item
2. Return success response

**Note:** Task 2.8.5 will add the status update logic to change Issue status to "In_Progress" when first action is created.

### Error Handling

**Scenario: Invalid issue ID**
- **Detection:** Lookup to non-existent issue
- **Response:** Create item fails with lookup error
- **Mitigation:** PowerApp issue picker only shows valid issues

**Scenario: Missing required fields**
- **Detection:** Create item fails with "required field" error
- **Response:** Flow fails without creating action
- **Mitigation:** PowerApp validates all fields before triggering flow

**Scenario: User has no permission to create**
- **Detection:** SharePoint returns 403 Forbidden
- **Response:** Flow fails with permission error
- **Mitigation:** Ensure app creator has Contributor+ role on site

### Verification Checklist

- [ ] Flow created and named "Save Corrective Action"
- [ ] Manual trigger with proper input schema
- [ ] Create item action configured for CorrectiveAction list
- [ ] All fields mapped correctly
- [ ] Issue lookup references parent issue
- [ ] ActionType populated from input
- [ ] ActionDescription populated from input
- [ ] AssignedTo uses email resolution
- [ ] Status set to "Open"
- [ ] CreatedDate set to current date/time
- [ ] Response returns success with Action ID
- [ ] Flow tested with valid issue ID
- [ ] CorrectiveAction record verified in SharePoint

---

## Task 2.8.5: Update Issue Status on First Action

### Objective

Modify the "Save Corrective Action" flow to detect if this is the first corrective action for an issue and, if so, update the issue status from "Assigned" to "In_Progress".

### Prerequisites

- Task 2.8.4 completed (Save Corrective Action flow created)
- Ability to query and count CorrectiveAction records

### Step-by-Step Instructions

#### Step 1: Add Get Items Action to Check for Existing Actions

1. Open the "Save Corrective Action" flow
2. Add a new step **before** the Create item action
3. Click **+ New step**
4. Search for "SharePoint"
5. Select **Get items**
6. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** CorrectiveAction
   - **Filter Query:** `Issue/ID eq @{triggerBody()['issueId']}`

This retrieves all existing actions for this issue.

#### Step 2: Add Create Item Action (as before)

The Create item action for CorrectiveAction should already exist from Task 2.8.4. Keep it in place.

#### Step 3: Add Condition to Check if First Action

1. Add a new step **after** the Create item action
2. Click **+ New step**
3. Search for "Condition"
4. Select **Condition**
5. Configure the condition:

```
Condition: length(outputs('Get_items')?['body/value']) equals 0
```

**Explanation:**
- `outputs('Get_items')` - Results from Get items action
- `['body/value']` - Array of items returned
- `length(...)` - Count of items
- `equals 0` - True if no existing actions (this is the first)

#### Step 4: Add Update Issue Item in YES Path

1. In the **True** (YES) branch of the condition:
2. Click **Add an action**
3. Search for "SharePoint"
4. Select **Update item**
5. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']
   - **Status:** "In_Progress"

This changes the issue status only on first action.

#### Step 5: Leave FALSE Path Empty (No Action)

If there are already existing actions, do nothing (issue is already "In_Progress").

The FALSE path automatically skips (no action needed).

#### Step 6: Updated Response

Modify the Response action to include action count:

```json
{
  "success": true,
  "actionId": @outputs('Create_item')?['body/ID'],
  "issueId": @triggerBody()['issueId'],
  "isFirstAction": @equals(length(outputs('Get_items')?['body/value']), 0),
  "statusUpdated": @equals(length(outputs('Get_items')?['body/value']), 0),
  "message": "Corrective action created"
}
```

#### Step 7: Test the Flow

1. Find an issue with Status = "Assigned" (no actions yet)
2. Run the flow with this issue ID
3. Verify:
   - CorrectiveAction created
   - Issue status changed to "In_Progress"
   - Response shows isFirstAction: true

4. Run the flow again with same issue ID
5. Verify:
   - New CorrectiveAction created
   - Issue status remains "In_Progress"
   - Response shows isFirstAction: false

### Updated Flow Definition

**Trigger Type:** Manual (from PowerApp)

**Actions:**
1. Get items from CorrectiveAction list (filter by issue)
2. Create new CorrectiveAction item
3. Condition: If action count was 0?
   - YES: Update Issue status to "In_Progress"
   - NO: No action needed
4. Return response

**Status Transition Logic:**
```
Issue Status Flow:
Open → Assigned → (First Action Added) → In_Progress → Pending_Verification → Resolved → Closed

First Corrective Action Trigger:
  Current Status: "Assigned"
  After first action: "In_Progress"
  (Subsequent actions: Status remains "In_Progress")
```

### Error Handling

**Scenario: Get items times out**
- **Detection:** Get items action exceeds timeout
- **Response:** Flow fails; issue not updated
- **Mitigation:** Add timeout handling with Try/Catch using Scope actions

**Scenario: No action type selected**
- **Detection:** actionType parameter is empty string
- **Response:** Create item fails with validation error
- **Mitigation:** PowerApp dropdown validates action type selected

**Scenario: Concurrent actions created for same issue**
- **Detection:** Race condition - two actions created before first status update
- **Response:** Both actions created; status updated to "In_Progress" (correct)
- **Mitigation:** Status update is idempotent (updating to "In_Progress" twice = same result)

### Verification Checklist

- [ ] Get items action added to retrieve existing actions
- [ ] Filter query correctly filters by issue ID
- [ ] Create item action preserved from Task 2.8.4
- [ ] Condition checks if existing actions count = 0
- [ ] Update issue action in TRUE path updates to "In_Progress"
- [ ] FALSE path left empty (no unnecessary updates)
- [ ] Response includes isFirstAction boolean
- [ ] Flow tested with issue in "Assigned" status
- [ ] First action triggers status update to "In_Progress"
- [ ] Second action does NOT trigger status update
- [ ] Issue status verified in SharePoint

---

## Task 2.8.6: Create Save Comment Flow

### Objective

Create a Power Automate flow that saves a comment to an issue when submitted from the "Add Comment" dialog in PowerApp.

### Prerequisites

- Task 2.8.1 completed (Issues exist)
- IssueComment list created (Task 2.6.10)
- IssueComment lookup to Issue configured (Task 2.6.11)
- "Add Comment" dialog in PowerApp (Task 2.7.20)

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Save Comment`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of parent issue"
    },
    "commentText": {
      "type": "string",
      "title": "Comment Text",
      "description": "Comment content"
    },
    "commentedByEmail": {
      "type": "string",
      "title": "Commented By Email",
      "description": "Email of person adding comment"
    }
  },
  "required": ["issueId", "commentText", "commentedByEmail"]
}
```

#### Step 3: Add Create IssueComment Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Create item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** IssueComment

5. Click **Edit in advanced mode** for field mappings

#### Step 4: Map IssueComment Fields

Add field mappings:

```
Title:
  Expression: @concat('Comment-', triggerBody()['issueId'], '-', formatDateTime(utcNow(), 'yyyyMMddHHmmss'))

Issue (Lookup):
  Dynamic Content: @triggerBody()['issueId']

CommentText:
  Dynamic Content: @triggerBody()['commentText']

CommentedBy:
  Dynamic Content: @triggerBody()['commentedByEmail']
  (SharePoint resolves to user)

CommentedDate:
  Dynamic Content: @utcNow()
```

#### Step 5: Add Response Action

1. Click **+ New step**
2. Select **Response**
3. Status code: `200`
4. Body:

```json
{
  "success": true,
  "commentId": @outputs('Create_item')?['body/ID'],
  "issueId": @triggerBody()['issueId'],
  "commentedDate": @utcNow(),
  "message": "Comment added successfully"
}
```

#### Step 6: Test the Flow

1. Save the flow
2. Get a valid Issue ID
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (valid ID from Issue list)
   - commentText: "Waiting for BVM replacement unit from CELS"
   - commentedByEmail: (valid user email)
5. Click **Run test**
6. Verify in SharePoint:
   - New IssueComment record created
   - Linked to correct Issue
   - CommentText populated
   - CommentedDate set to today

### Flow Definition

**Trigger Type:** Manual (from PowerApp "Add Comment" dialog)

**Actions:**
1. Create IssueComment item linked to issue
2. Return success response

**Data Model:**
```
Issue
  ├─ Title: ISS-2026-0001
  ├─ Status: In_Progress
  └─ Comments (lookup):
      ├─ Comment 1: "Starting repair process"
      │  ├─ CommentedBy: John Smith
      │  └─ CommentedDate: 2026-01-20 09:00
      │
      ├─ Comment 2: "Waiting for replacement part"
      │  ├─ CommentedBy: Jane Doe
      │  └─ CommentedDate: 2026-01-20 14:30
      │
      └─ Comment 3: "Part arrived, installation in progress"
         ├─ CommentedBy: John Smith
         └─ CommentedDate: 2026-01-21 10:15
```

### Error Handling

**Scenario: Empty comment text**
- **Detection:** commentText parameter is empty string
- **Response:** Create item may still create record with empty text
- **Mitigation:** PowerApp validates comment length >= 1 character before flow trigger

**Scenario: Issue ID doesn't exist**
- **Detection:** Lookup to non-existent issue
- **Response:** Create item fails with lookup error
- **Mitigation:** PowerApp issue picker only shows valid issues

**Scenario: Invalid user email**
- **Detection:** SharePoint lookup fails to resolve email
- **Response:** Create item fails; CommentedBy lookup fails
- **Mitigation:** PowerApp uses user picker control (ensures valid users only)

### Verification Checklist

- [ ] Flow created and named "Save Comment"
- [ ] Manual trigger with proper input schema
- [ ] Create item action configured for IssueComment list
- [ ] Title field uses comment ID format
- [ ] Issue lookup references parent issue
- [ ] CommentText populated from input
- [ ] CommentedBy uses email resolution
- [ ] CommentedDate set to current date/time
- [ ] Response returns success with Comment ID
- [ ] Flow tested with valid issue ID
- [ ] IssueComment record verified in SharePoint
- [ ] Comment displays chronologically in Issue Detail

---

## Task 2.8.7: Create Mark Resolved Flow

### Objective

Create a Power Automate flow that updates an issue status from "In_Progress" to "Pending_Verification" when marked as resolved from the Issue Detail screen.

### Prerequisites

- Task 2.8.1 completed (Issues exist)
- Issue Detail screen with "Mark Resolved" action (Task 2.7.8)
- Understanding of issue status lifecycle

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Mark Issue Resolved`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of issue to mark resolved"
    },
    "resolutionNotes": {
      "type": "string",
      "title": "Resolution Notes",
      "description": "Optional notes about resolution"
    }
  },
  "required": ["issueId"]
}
```

#### Step 3: Add Update Issue Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Update item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

5. Click **Edit in advanced mode** for field updates

#### Step 4: Map Fields for Status Update

Add field updates:

```
Status:
  Value: "Pending_Verification"

ResolutionNotes (if field exists):
  Dynamic Content: @triggerBody()['resolutionNotes']
```

**Important:** Only update Status and ResolutionNotes. Do not modify other fields.

#### Step 5: Add Validation Condition (Optional but Recommended)

Before updating, verify current status is "In_Progress" or "Assigned":

1. Add a step **before** Update item
2. Click **+ New step**
3. Search for "SharePoint"
4. Select **Get item**
5. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

6. Add Condition:
   - Condition: `outputs('Get_item')?['body/Status'] not equals "Resolved"`
   - If True: Proceed with Update item
   - If False: Skip update (already resolved)

#### Step 6: Add Response Action

1. Click **+ New step**
2. Select **Response**
3. Status code: `200`
4. Body:

```json
{
  "success": true,
  "issueId": @triggerBody()['issueId'],
  "newStatus": "Pending_Verification",
  "message": "Issue marked as pending verification"
}
```

#### Step 7: Test the Flow

1. Save the flow
2. Find an issue with Status = "In_Progress"
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (valid In_Progress issue ID)
   - resolutionNotes: "BVM replacement installed and verified"
5. Click **Run test**
6. Verify in SharePoint:
   - Issue Status changed to "Pending_Verification"
   - ResolutionNotes populated

### Flow Definition

**Trigger Type:** Manual (from PowerApp Issue Detail screen)

**Actions:**
1. Get issue item (current state)
2. Condition: Status not = "Resolved"?
3. If True: Update status to "Pending_Verification"
4. Return success response

**Status Transition:**
```
BEFORE: Status = "In_Progress"
AFTER:  Status = "Pending_Verification"

This allows verification before full closure.
Reviewer can then:
  - Verify and move to "Resolved" (Task 2.8.8)
  - Reopen if issues found (Task 2.8.10)
```

### Error Handling

**Scenario: Invalid issue ID**
- **Detection:** Get item returns 404 error
- **Response:** Flow terminates without updating
- **Mitigation:** PowerApp only passes valid issue IDs

**Scenario: Issue already "Resolved" or "Closed"**
- **Detection:** Condition check fails (Status = "Resolved")
- **Response:** Update action skipped (already resolved)
- **Mitigation:** This is expected behavior - no double-status-change

**Scenario: Another user changed status simultaneously**
- **Detection:** (Race condition) Get item shows "In_Progress", but Update fails
- **Response:** Update may fail with conflict error
- **Mitigation:** Add retry logic or accept failure (user refresh to see current state)

### Verification Checklist

- [ ] Flow created and named "Mark Issue Resolved"
- [ ] Manual trigger with issueId and optional resolutionNotes
- [ ] Get item action retrieves current issue status
- [ ] Condition checks if Status not = "Resolved"
- [ ] Update item action only in TRUE path
- [ ] Status field set to "Pending_Verification"
- [ ] ResolutionNotes field populated if provided
- [ ] Response returns success message
- [ ] Flow tested with In_Progress issue
- [ ] Status changed to "Pending_Verification" in SharePoint
- [ ] Re-running flow does not double-update (idempotent)

---

## Task 2.8.8: Create Verify Resolution Flow

### Objective

Create a Power Automate flow that updates an issue status from "Pending_Verification" to "Resolved" when a verifier confirms the resolution, and sets the ResolvedDate field.

### Prerequisites

- Task 2.8.7 completed (Issues can be marked as pending verification)
- Issue Detail screen with "Verify Resolution" action available to managers/verifiers only

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Verify Resolution`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of issue to verify"
    },
    "verificationNotes": {
      "type": "string",
      "title": "Verification Notes",
      "description": "Notes from verification reviewer"
    },
    "verifiedByEmail": {
      "type": "string",
      "title": "Verified By Email",
      "description": "Email of person verifying resolution"
    }
  },
  "required": ["issueId", "verifiedByEmail"]
}
```

#### Step 3: Add Get Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Get item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

This retrieves current issue status for validation.

#### Step 4: Add Condition to Validate Status

1. Click **+ New step**
2. Search for "Condition"
3. Select **Condition**
4. Configure:

```
Condition: outputs('Get_item')?['body/Status'] equals "Pending_Verification"
```

This ensures only issues awaiting verification are updated.

#### Step 5: Add Update Issue Item (in TRUE path)

1. In the **True** branch:
2. Click **Add an action**
3. Search for "SharePoint"
4. Select **Update item**
5. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

6. Click **Edit in advanced mode** for field mappings

#### Step 6: Map Verification Fields

Add field updates:

```
Status:
  Value: "Resolved"

ResolvedDate:
  Dynamic Content: @utcNow()

VerificationNotes (if field exists):
  Dynamic Content: @triggerBody()['verificationNotes']

VerifiedBy (if field exists):
  Dynamic Content: @triggerBody()['verifiedByEmail']
  (SharePoint resolves to user)
```

#### Step 7: Add False Path Response (Status not Pending)

1. In the **False** branch:
2. Click **Add an action**
3. Select **Response**
4. Status code: `400`
5. Body:

```json
{
  "success": false,
  "issueId": @triggerBody()['issueId'],
  "currentStatus": @outputs('Get_item')?['body/Status'],
  "message": "Issue cannot be verified - not in Pending_Verification status",
  "error": "INVALID_STATUS_FOR_VERIFICATION"
}
```

This prevents verifying issues not awaiting verification.

#### Step 8: Add True Path Response

1. Still in **True** branch, after Update item
2. Click **Add an action**
3. Select **Response**
4. Status code: `200`
5. Body:

```json
{
  "success": true,
  "issueId": @triggerBody()['issueId'],
  "newStatus": "Resolved",
  "resolvedDate": @utcNow(),
  "message": "Issue resolution verified successfully"
}
```

#### Step 9: Test the Flow

1. Save the flow
2. Find an issue with Status = "Pending_Verification"
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (Pending_Verification issue ID)
   - verificationNotes: "BVM replacement verified and functional"
   - verifiedByEmail: (manager/verifier email)
5. Click **Run test**
6. Verify in SharePoint:
   - Issue Status = "Resolved"
   - ResolvedDate set to today
   - VerificationNotes populated

### Flow Definition

**Trigger Type:** Manual (from PowerApp - Verifier role only)

**Actions:**
1. Get issue item (validate current state)
2. Condition: Status = "Pending_Verification"?
   - TRUE path: Update to "Resolved", set ResolvedDate
   - FALSE path: Return error

**Status Transition:**
```
BEFORE: Status = "Pending_Verification"
AFTER:  Status = "Resolved"
        ResolvedDate = [Today]
        VerifiedBy = [Manager Name]

If Status is not "Pending_Verification":
  Error: INVALID_STATUS_FOR_VERIFICATION
  (Cannot verify non-pending issues)
```

### Error Handling

**Scenario: Issue not in Pending_Verification status**
- **Detection:** Condition check fails
- **Response:** FALSE path returns 400 error
- **Mitigation:** PowerApp disables "Verify" button for non-pending issues

**Scenario: Invalid issue ID**
- **Detection:** Get item returns 404
- **Response:** Flow terminates; no update
- **Mitigation:** PowerApp validates issue ID exists

**Scenario: Verifier lacks permissions**
- **Detection:** Update item fails with 403 Forbidden
- **Response:** Flow fails with permission error
- **Mitigation:** Flow uses app identity (has write permissions)

**Scenario: Multiple concurrent verifications**
- **Detection:** (Race condition) Two verifiers try to verify same issue
- **Response:** First succeeds; second fails (status already "Resolved")
- **Mitigation:** Expected behavior - only first verification counts

### Verification Checklist

- [ ] Flow created and named "Verify Resolution"
- [ ] Manual trigger with issueId, verificationNotes, verifiedByEmail
- [ ] Get item action retrieves current issue
- [ ] Condition checks if Status = "Pending_Verification"
- [ ] Update item action only in TRUE path
- [ ] Status set to "Resolved"
- [ ] ResolvedDate set to current date/time
- [ ] VerificationNotes populated from input
- [ ] VerifiedBy set to verifier email
- [ ] FALSE path returns 400 error with reason
- [ ] Response includes resolved date
- [ ] Flow tested with Pending_Verification issue
- [ ] Status successfully updated to "Resolved"

---

## Task 2.8.9: Create Close Issue Flow

### Objective

Create a Power Automate flow that closes a resolved issue by updating status to "Closed" and setting the ClosedDate field.

### Prerequisites

- Task 2.8.8 completed (Issues can be verified/resolved)
- Issue Detail screen with "Close Issue" action

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Close Issue`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of issue to close"
    },
    "closureNotes": {
      "type": "string",
      "title": "Closure Notes",
      "description": "Optional final notes before closing"
    }
  },
  "required": ["issueId"]
}
```

#### Step 3: Add Update Issue Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Update item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

5. Click **Edit in advanced mode** for field mappings

#### Step 4: Map Closure Fields

Add field updates:

```
Status:
  Value: "Closed"

ClosedDate:
  Dynamic Content: @utcNow()

ClosureNotes (if field exists):
  Dynamic Content: @triggerBody()['closureNotes']
```

#### Step 5: Add Response Action

1. Click **+ New step**
2. Select **Response**
3. Status code: `200`
4. Body:

```json
{
  "success": true,
  "issueId": @triggerBody()['issueId'],
  "newStatus": "Closed",
  "closedDate": @utcNow(),
  "message": "Issue closed successfully"
}
```

#### Step 6: Test the Flow

1. Save the flow
2. Find an issue with Status = "Resolved"
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (Resolved issue ID)
   - closureNotes: "BVM replacement complete and verified. Ready for next audit."
5. Click **Run test**
6. Verify in SharePoint:
   - Issue Status = "Closed"
   - ClosedDate set to today

### Flow Definition

**Trigger Type:** Manual (from PowerApp Issue Detail screen)

**Actions:**
1. Update Issue status to "Closed"
2. Set ClosedDate to current date/time
3. Optionally populate closure notes
4. Return success response

**Status Transition:**
```
BEFORE: Status = "Resolved"
AFTER:  Status = "Closed"
        ClosedDate = [Today]

(Note: Issues typically close after being Resolved,
 but closing logic does not enforce this prerequisite.
 This allows closing by manager override if needed.)
```

### Error Handling

**Scenario: Invalid issue ID**
- **Detection:** Update item fails with 404
- **Response:** Flow terminates without closing
- **Mitigation:** PowerApp only passes valid issue IDs

**Scenario: Issue already "Closed"**
- **Detection:** (Expected scenario) Attempting to close already-closed issue
- **Response:** Update succeeds (idempotent - setting same values)
- **Mitigation:** This is acceptable behavior

**Scenario: Issue in "Open" or "In_Progress" status**
- **Detection:** (Possible but not recommended) User tries to close without resolving
- **Response:** Update succeeds (no validation on this flow)
- **Mitigation:** PowerApp UI disables "Close" button for non-resolved issues

### Verification Checklist

- [ ] Flow created and named "Close Issue"
- [ ] Manual trigger with issueId and optional closureNotes
- [ ] Update item action configured for Issue list
- [ ] Status set to "Closed"
- [ ] ClosedDate set to current date/time
- [ ] ClosureNotes populated from input if provided
- [ ] Response returns success message
- [ ] Flow tested with Resolved issue
- [ ] Status successfully updated to "Closed" in SharePoint
- [ ] ClosedDate timestamp verified

---

## Task 2.8.10: Create Reopen Issue Flow

### Objective

Create a Power Automate flow that reopens a closed issue by updating status back to "In_Progress", incrementing ReopenCount, and resetting resolved dates for further investigation.

### Prerequisites

- Task 2.8.9 completed (Issues can be closed)
- Issue Detail screen with "Reopen Issue" action (available to managers/verifiers)

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Reopen Issue`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of issue to reopen"
    },
    "reopenReason": {
      "type": "string",
      "title": "Reopen Reason",
      "description": "Reason for reopening the issue"
    }
  },
  "required": ["issueId", "reopenReason"]
}
```

#### Step 3: Add Get Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Get item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

This retrieves current ReopenCount to increment it.

#### Step 4: Add Update Issue Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Update item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

5. Click **Edit in advanced mode** for field mappings

#### Step 5: Map Reopen Fields

Add field updates:

```
Status:
  Value: "In_Progress"

ReopenCount:
  Expression: @add(int(outputs('Get_item')?['body/ReopenCount']), 1)
  (Increments current count by 1)

ResolvedDate:
  Value: Null or empty string
  (Clear the resolved date)

ClosedDate:
  Value: Null or empty string
  (Clear the closed date)

ReopenReason (if field exists):
  Dynamic Content: @triggerBody()['reopenReason']

ReopenedDate (if field exists):
  Dynamic Content: @utcNow()
```

#### Step 6: Add Add Comment for Audit Trail

After updating, automatically add a comment documenting the reopen:

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Create item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** IssueComment

5. Map fields:

```
Title:
  Expression: @concat('Reopen-', triggerBody()['issueId'], '-', formatDateTime(utcNow(), 'yyyyMMdd'))

Issue (Lookup):
  Dynamic Content: @triggerBody()['issueId']

CommentText:
  Expression: @concat('SYSTEM: Issue reopened. Reason: ', triggerBody()['reopenReason'])

CommentedBy:
  Value: System user or current user

CommentedDate:
  Dynamic Content: @utcNow()
```

#### Step 7: Add Response Action

1. Click **+ New step**
2. Select **Response**
3. Status code: `200`
4. Body:

```json
{
  "success": true,
  "issueId": @triggerBody()['issueId'],
  "newStatus": "In_Progress",
  "reopenCount": @add(int(outputs('Get_item')?['body/ReopenCount']), 1),
  "reopenReason": @triggerBody()['reopenReason'],
  "message": "Issue reopened for further investigation"
}
```

#### Step 8: Test the Flow

1. Save the flow
2. Find an issue with Status = "Closed"
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (Closed issue ID)
   - reopenReason: "BVM replacement found to be defective during follow-up audit"
5. Click **Run test**
6. Verify in SharePoint:
   - Issue Status = "In_Progress"
   - ReopenCount incremented (e.g., 0 → 1)
   - ResolvedDate cleared
   - ClosedDate cleared
   - System comment created with reopen reason

### Flow Definition

**Trigger Type:** Manual (from PowerApp - Manager role only)

**Actions:**
1. Get issue item (retrieve current ReopenCount)
2. Update issue fields:
   - Status → "In_Progress"
   - ReopenCount + 1
   - Clear ResolvedDate and ClosedDate
3. Create audit trail comment
4. Return success response

**Status Transition:**
```
BEFORE: Status = "Closed"
        ReopenCount = 0
        ResolvedDate = [date]
        ClosedDate = [date]

AFTER:  Status = "In_Progress"
        ReopenCount = 1
        ResolvedDate = [cleared]
        ClosedDate = [cleared]

System Comment: "Issue reopened. Reason: [provided reason]"

Reopen allows issue to cycle back through:
In_Progress → Pending_Verification → Resolved → Closed
```

### Error Handling

**Scenario: Invalid issue ID**
- **Detection:** Get item returns 404
- **Response:** Flow terminates without reopening
- **Mitigation:** PowerApp validates issue ID

**Scenario: Issue never had ReopenCount field set**
- **Detection:** Get item returns null for ReopenCount
- **Response:** Expression fails or treats as 0
- **Mitigation:** Ensure Issue list initializes ReopenCount to 0 for all items

**Scenario: Issue in "Open" or "Assigned" status**
- **Detection:** (Possible scenario) Reopening issue that never closed
- **Response:** Update succeeds (status becomes "In_Progress" anyway)
- **Mitigation:** PowerApp UI only enables "Reopen" for Closed issues

**Scenario: Multiple reopens**
- **Detection:** (Expected) ReopenCount increments multiple times
- **Response:** ReopenCount = 0, 1, 2, 3, etc. (tracks reopen history)
- **Mitigation:** Expected behavior - tracks issue stability

### Verification Checklist

- [ ] Flow created and named "Reopen Issue"
- [ ] Manual trigger with issueId and reopenReason
- [ ] Get item action retrieves current issue
- [ ] Update item action maps all reopen fields
- [ ] Status set to "In_Progress"
- [ ] ReopenCount incremented correctly
- [ ] ResolvedDate and ClosedDate cleared
- [ ] ReopenReason stored in IssueComment
- [ ] System audit comment created automatically
- [ ] Response includes new ReopenCount
- [ ] Flow tested with Closed issue
- [ ] Status changed to "In_Progress"
- [ ] ReopenCount incremented in SharePoint
- [ ] Dates cleared as expected

---

## Task 2.8.11: Create Escalate Issue Flow

### Objective

Create a Power Automate flow that escalates an issue by incrementing EscalationLevel and assigning to the appropriate manager level based on escalation count.

### Prerequisites

- All previous tasks completed (issues exist and can transition through statuses)
- Issue Detail screen with "Escalate Issue" action
- Manager/Escalation matrix defined (which managers handle which escalation levels)

### Step-by-Step Instructions

#### Step 1: Create New Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flows** → **Instant cloud flow**
3. Name the flow: `Escalate Issue`
4. Click **Create**

#### Step 2: Configure Trigger with Input Schema

1. Click **Edit in advanced mode** on trigger
2. Replace schema with:

```json
{
  "type": "object",
  "properties": {
    "issueId": {
      "type": "string",
      "title": "Issue ID",
      "description": "SharePoint ID of issue to escalate"
    },
    "escalationReason": {
      "type": "string",
      "title": "Escalation Reason",
      "description": "Reason for escalation"
    },
    "escalatedByEmail": {
      "type": "string",
      "title": "Escalated By Email",
      "description": "Email of person escalating issue"
    }
  },
  "required": ["issueId", "escalationReason"]
}
```

#### Step 3: Add Get Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Get item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

This retrieves current escalation level.

#### Step 4: Add Compose for Escalation Assignment

Escalation level determines which manager handles it:
- Level 0: Team Lead / Departmental Manager
- Level 1: Nurse Unit Manager / Department Head
- Level 2: Directorate Manager / Clinical Director
- Level 3: Executive / Chief Medical Officer

1. Click **+ New step**
2. Search for "Compose"
3. Select **Compose** action
4. Name: "Calculate Next Escalation Manager"
5. In the Inputs field, add expression for manager email based on level:

```
@if(equals(add(int(outputs('Get_item')?['body/EscalationLevel']), 1), 1),
  'team-lead@rbwh.health.qld.gov.au',
  if(equals(add(int(outputs('Get_item')?['body/EscalationLevel']), 1), 2),
    'num@rbwh.health.qld.gov.au',
    if(equals(add(int(outputs('Get_item')?['body/EscalationLevel']), 1), 3),
      'director@rbwh.health.qld.gov.au',
      'cmo@rbwh.health.qld.gov.au'
    )
  )
)
```

**Note:** Customize email addresses to match your Metro North Health escalation hierarchy.

#### Step 5: Add Update Issue Item Action

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Update item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** Issue
   - **ID:** @triggerBody()['issueId']

5. Click **Edit in advanced mode** for field mappings

#### Step 6: Map Escalation Fields

Add field updates:

```
EscalationLevel:
  Expression: @add(int(outputs('Get_item')?['body/EscalationLevel']), 1)
  (Increments current level by 1)

EscalatedTo:
  Dynamic Content: @outputs('Calculate_Next_Escalation_Manager')
  (Manager email for next level)

EscalatedDate:
  Dynamic Content: @utcNow()

EscalationReason (if field exists):
  Dynamic Content: @triggerBody()['escalationReason']
```

**Important:** Do NOT change the issue status. Escalation can happen at any status level.

#### Step 7: Add Comment for Escalation Trail

1. Click **+ New step**
2. Search for "SharePoint"
3. Select **Create item**
4. Configure:
   - **Site Address:** REdI Trolley Audit site
   - **List Name:** IssueComment

5. Map fields:

```
Title:
  Expression: @concat('Escalation-', triggerBody()['issueId'], '-L', outputs('Compose')?['body'])

Issue (Lookup):
  Dynamic Content: @triggerBody()['issueId']

CommentText:
  Expression: @concat('ESCALATION: Issue escalated to Level ',
                      add(int(outputs('Get_item')?['body/EscalationLevel']), 1),
                      '. Reason: ', triggerBody()['escalationReason'])

CommentedBy:
  Dynamic Content: @triggerBody()['escalatedByEmail']

CommentedDate:
  Dynamic Content: @utcNow()
```

#### Step 8: Add Response Action

1. Click **+ New step**
2. Select **Response**
3. Status code: `200`
4. Body:

```json
{
  "success": true,
  "issueId": @triggerBody()['issueId'],
  "newEscalationLevel": @add(int(outputs('Get_item')?['body/EscalationLevel']), 1),
  "escalatedToEmail": @outputs('Calculate_Next_Escalation_Manager'),
  "escalationReason": @triggerBody()['escalationReason'],
  "message": "Issue escalated successfully"
}
```

#### Step 9: Test the Flow

1. Save the flow
2. Find any issue (at any status)
3. Click **Test** → **Manually**
4. Provide input:
   - issueId: (any issue ID)
   - escalationReason: "SLA breach - issue unresolved for 30 days"
   - escalatedByEmail: (your email)
5. Click **Run test**
6. Verify in SharePoint:
   - EscalationLevel incremented (e.g., 0 → 1)
   - EscalatedTo set to appropriate manager email
   - EscalatedDate set to today
   - System comment created with escalation reason

### Flow Definition

**Trigger Type:** Manual (from PowerApp Issue Detail screen)

**Actions:**
1. Get issue item (retrieve current escalation level)
2. Compose: Determine manager for next escalation level
3. Update issue:
   - EscalationLevel + 1
   - EscalatedTo = new manager email
   - EscalatedDate = now
4. Create audit trail comment
5. Return success response

**Escalation Matrix:**
```
Level 0 (None)     → No escalation
Level 1 (Manager)  → Team Lead
Level 2 (Director) → Nurse Unit Manager
Level 3 (Executive)→ Directorate Manager
Level 4 (C-Level)  → Chief Medical Officer

Each escalation increments level and reassigns to appropriate authority.
```

**Escalation Example Timeline:**
```
Time    Status          Level  Escalated To          Event
────────────────────────────────────────────────────────────
Day 1   Open           0      [None]                Issue created
Day 8   In_Progress    0      [None]                Work begins
Day 15  Pending_Ver    1      Team Lead             Escalation 1 - SLA warning
Day 22  In_Progress    2      NUM                   Escalation 2 - Delayed resolution
Day 29  Resolved       3      Director              Escalation 3 - Executive review required
```

### Error Handling

**Scenario: Invalid issue ID**
- **Detection:** Get item returns 404
- **Response:** Flow terminates without escalating
- **Mitigation:** PowerApp validates issue ID

**Scenario: Escalation level exceeds 4**
- **Detection:** EscalationLevel + 1 = 5 (beyond defined hierarchy)
- **Response:** Manager defaults to C-Level (cmo@rbwh.health.qld.gov.au)
- **Mitigation:** Adjust escalation matrix or cap at level 4

**Scenario: Manager email invalid**
- **Detection:** Compose returns malformed email
- **Response:** Update item fails; issue not escalated
- **Mitigation:** Validate manager email addresses in compose expression

**Scenario: Multiple escalations on same day**
- **Detection:** (Expected) Issue escalated multiple times
- **Response:** EscalationLevel increases: 0 → 1 → 2 (tracks escalation history)
- **Mitigation:** System comment trail documents each escalation

### Verification Checklist

- [ ] Flow created and named "Escalate Issue"
- [ ] Manual trigger with issueId, escalationReason, escalatedByEmail
- [ ] Get item action retrieves current issue
- [ ] Compose action calculates next escalation manager
- [ ] Manager matrix matches Metro North Health organizational structure
- [ ] Update item action maps all escalation fields
- [ ] EscalationLevel incremented correctly
- [ ] EscalatedTo set to appropriate manager email
- [ ] EscalatedDate set to current date/time
- [ ] EscalationReason stored in comment
- [ ] System audit comment created automatically
- [ ] Response includes new escalation level and manager
- [ ] Flow tested with issue at each level (0, 1, 2, 3)
- [ ] Escalation level increments correctly
- [ ] Issue status remains unchanged during escalation

---

## Summary: Phase 2.8 Implementation Checklist

### All Tasks Complete

Use this checklist to verify all 11 flows are complete and functioning:

#### Task 2.8.1: Save New Issue Flow
- [ ] Flow created and deployed
- [ ] Trigger accepts issue details from PowerApp
- [ ] Issue record created with Status = "Open"
- [ ] All required fields populated
- [ ] Flow tested and verified

#### Task 2.8.2: Generate Issue Number
- [ ] Get items action filters for current year
- [ ] Compose action generates ISS-YYYY-NNNN format
- [ ] Sequential numbering increments correctly
- [ ] Number persists in SharePoint as Title field
- [ ] Numbers tested for sequential integrity

#### Task 2.8.3: Assign Issue Flow
- [ ] Flow updates AssignedTo field
- [ ] AssignedDate set to current date/time
- [ ] Status changed to "Assigned"
- [ ] Flow tested with valid user email
- [ ] Status transition verified

#### Task 2.8.4: Save Corrective Action Flow
- [ ] CorrectiveAction record created
- [ ] Linked to parent Issue via lookup
- [ ] All action fields populated
- [ ] Flow tested and records verified

#### Task 2.8.5: Update Status on First Action
- [ ] Get items action counts existing actions
- [ ] Condition checks if count = 0
- [ ] Issue status updated to "In_Progress" on first action only
- [ ] Subsequent actions do not re-update status
- [ ] Tested for multiple action creation

#### Task 2.8.6: Save Comment Flow
- [ ] IssueComment record created
- [ ] Linked to parent Issue
- [ ] CommentedBy and CommentedDate populated
- [ ] Comments appear chronologically in Issue detail
- [ ] Flow tested with valid input

#### Task 2.8.7: Mark Resolved Flow
- [ ] Updates Issue status to "Pending_Verification"
- [ ] ResolutionNotes populated if provided
- [ ] Only updates Pending_Verification status
- [ ] Flow idempotent (safe to run multiple times)
- [ ] Tested with In_Progress issue

#### Task 2.8.8: Verify Resolution Flow
- [ ] Get item validates current status
- [ ] Condition checks if Status = "Pending_Verification"
- [ ] Update changes status to "Resolved"
- [ ] ResolvedDate set to current date/time
- [ ] FALSE path returns 400 error
- [ ] Tested with Pending_Verification issue

#### Task 2.8.9: Close Issue Flow
- [ ] Updates Issue status to "Closed"
- [ ] ClosedDate set to current date/time
- [ ] ClosureNotes populated if provided
- [ ] Flow tested with Resolved issue
- [ ] Status updated in SharePoint

#### Task 2.8.10: Reopen Issue Flow
- [ ] Status changed to "In_Progress"
- [ ] ReopenCount incremented (+1)
- [ ] ResolvedDate and ClosedDate cleared
- [ ] ReopenReason documented in comment
- [ ] System audit comment created
- [ ] Tested with Closed issue
- [ ] Multiple reopens increment counter correctly

#### Task 2.8.11: Escalate Issue Flow
- [ ] EscalationLevel incremented
- [ ] EscalatedTo set to appropriate manager
- [ ] EscalatedDate set to current date/time
- [ ] Escalation can occur at any status
- [ ] System audit comment created
- [ ] Tested at escalation levels 0-3
- [ ] Manager assignments match organizational hierarchy

### Flow Testing Summary

| Flow | Test Scenario | Expected Result | Status |
|------|---|---|---|
| 2.8.1 | Create new issue | ISS-2026-NNNN generated, Status=Open | [ ] |
| 2.8.2 | Day 1: 3 issues created | ISS-2026-0001, 0002, 0003 | [ ] |
| 2.8.3 | Assign issue to user | Status=Assigned, AssignedTo populated | [ ] |
| 2.8.4 | Add corrective action | Action linked to issue | [ ] |
| 2.8.5 | Add first action to Assigned issue | Status→In_Progress | [ ] |
| 2.8.5 | Add second action | Status stays In_Progress | [ ] |
| 2.8.6 | Add comment to issue | Comment appears in detail | [ ] |
| 2.8.7 | Mark In_Progress as resolved | Status→Pending_Verification | [ ] |
| 2.8.8 | Verify Pending_Verification issue | Status→Resolved, ResolvedDate set | [ ] |
| 2.8.9 | Close Resolved issue | Status→Closed, ClosedDate set | [ ] |
| 2.8.10 | Reopen Closed issue | Status→In_Progress, ReopenCount=1 | [ ] |
| 2.8.11 | Escalate at Level 0 | Level→1, EscalatedTo=Team Lead | [ ] |
| 2.8.11 | Escalate at Level 1 | Level→2, EscalatedTo=NUM | [ ] |

### Integration Points

Verify all flows integrate properly with PowerApp screens:

- [ ] Task 2.7.13 "Add Issue" dialog → 2.8.1 flow triggers correctly
- [ ] Task 2.7.8 "Assign" button → 2.8.3 flow triggers correctly
- [ ] Task 2.7.19 "Add Action" dialog → 2.8.4 & 2.8.5 flows trigger
- [ ] Task 2.7.20 "Add Comment" dialog → 2.8.6 flow triggers
- [ ] Task 2.7.8 "Mark Resolved" button → 2.8.7 flow triggers
- [ ] Task 2.7.8 "Verify" button → 2.8.8 flow triggers
- [ ] Task 2.7.8 "Close" button → 2.8.9 flow triggers
- [ ] Task 2.7.8 "Reopen" button → 2.8.10 flow triggers
- [ ] Task 2.7.8 "Escalate" button → 2.8.11 flow triggers

### Dependencies Validation

Ensure all prerequisite tasks completed before 2.8:

- [ ] 2.6.1 - Issue list created
- [ ] 2.6.2-2.6.4 - Issue lookups configured
- [ ] 2.6.5 - Issue choice columns (Category, Severity, Status)
- [ ] 2.6.7 - CorrectiveAction list created
- [ ] 2.6.8-2.6.9 - CorrectiveAction lookups and choices
- [ ] 2.6.10-2.6.11 - IssueComment list created
- [ ] 2.7.1-2.7.8 - Issue management screens built
- [ ] 2.7.13-2.7.20 - Add Issue/Action/Comment dialogs built

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Action Type" field validation error

**Symptom:** When creating corrective action, flow fails with validation error on ActionType

**Root Cause:** Action type choices not defined in CorrectiveAction list

**Solution:**
1. Verify CorrectiveAction list has ActionType choice column (Task 2.6.9)
2. Check that choices are defined: Repair, Replace, Document, Investigate, Other
3. Ensure flow only submits valid choice values

#### Issue: User lookup fails in AssignedTo field

**Symptom:** "Assign Issue" flow creates issue but AssignedTo remains empty

**Root Cause:** Email format incorrect or user not in organizational directory

**Solution:**
1. Verify email format is valid (user@rbwh.health.qld.gov.au)
2. Ensure user exists in Azure AD
3. In PowerApp, use user picker control instead of text input
4. Test with known valid user email

#### Issue: Sequential issue numbers skip or duplicate

**Symptom:** Issue numbers show gaps (ISS-2026-0001, ISS-2026-0003) or duplicates

**Root Cause:** Race condition in simultaneous creates, or filter query returning stale results

**Solution:**
1. Add retry logic with exponential backoff (3 retries, 1-3 second delay)
2. Use Lock action (premium feature) to ensure sequential creation
3. Verify Get items OData filter is correct
4. Check SharePoint list doesn't have duplicate filtering

#### Issue: Status transition stuck in previous status

**Symptom:** After running flow, issue status doesn't change in SharePoint

**Root Cause:** Update item action not saving to correct field, or cache not refreshing

**Solution:**
1. Verify "Status" field name in Update item action is exactly "Status"
2. Check field type is Choice (not Text)
3. Verify choice values match exactly (case-sensitive)
4. Refresh SharePoint list view (F5 or close/reopen)
5. Check user has edit permissions on list

#### Issue: Escalation manager email not found

**Symptom:** Escalate flow fails or escalates to wrong manager

**Root Cause:** Manager email hardcoded in flow doesn't match organizational structure

**Solution:**
1. Update Compose expression in 2.8.11 with correct manager emails
2. Validate against Metro North Health organizational chart
3. Test each escalation level separately (0→1, 1→2, 2→3)
4. Verify manager email format is correct

#### Issue: Comments appear out of order

**Symptom:** Comments in Issue detail screen show wrong chronological order

**Root Cause:** CommentedDate not set correctly, or comments retrieved with wrong sort

**Solution:**
1. Verify 2.8.6 flow sets CommentedDate to @utcNow()
2. Check IssueComment list view sorts by CommentedDate descending
3. Ensure PowerApp sorts comment gallery by CommentedDate
4. Clear browser cache if dates appear cached

### Testing Procedures

#### Flow Execution Test

For each flow:
1. Navigate to https://make.powerautomate.com
2. Find the flow in your environment
3. Click **Edit**
4. Click **Test** → **Manually**
5. Provide valid test inputs
6. Click **Run test**
7. Verify success response
8. Check SharePoint list item created/updated correctly

#### End-to-End Issue Lifecycle Test

Complete full issue workflow:
1. Use PowerApp "Add Issue" to create new issue
2. Use "Assign" action to assign to team lead
3. Use "Add Action" to create corrective action
4. Verify status changed to "In_Progress"
5. Use "Add Comment" multiple times
6. Use "Mark Resolved" to move to verification
7. Use "Verify Resolution" to confirm resolution
8. Use "Close Issue" to close
9. Use "Reopen" to reopen issue
10. Use "Escalate" to escalate twice
11. Verify all status transitions and fields in SharePoint

#### Performance Test

Test flow performance under load:
1. Create 10 issues rapidly (within 1 minute)
2. Verify all generate unique sequential issue numbers
3. No duplicates or skipped numbers
4. All issues created successfully

---

## Deployment Checklist

Before deploying Phase 2.8 to production:

### Pre-Deployment
- [ ] All 11 flows created and tested in development environment
- [ ] Flow names follow naming convention (past tense: Save, Mark, Verify, etc.)
- [ ] All flows documented with input/output schemas
- [ ] Error handling implemented for all flows
- [ ] Response messages are user-friendly
- [ ] Flows tested with realistic data volumes

### SharePoint List Preparation
- [ ] Issue list has all required columns
- [ ] CorrectiveAction list created and linked
- [ ] IssueComment list created and linked
- [ ] All choice columns have correct values
- [ ] User lookup columns configured
- [ ] DateTime fields set to auto-populate (if using calculated columns)

### PowerApp Integration
- [ ] All dialog screens (Add Issue, Add Action, Add Comment) built
- [ ] Dialog actions configured to trigger correct flows
- [ ] Error messages from flows displayed to user
- [ ] Response values used to update UI (e.g., new issue ID)
- [ ] Loading indicators shown during flow execution

### Security & Permissions
- [ ] Flows run with app identity (not user identity) where appropriate
- [ ] Flows have minimum necessary permissions
- [ ] Escalation matrix uses valid Metro North Health manager email addresses
- [ ] User pickers in PowerApp restrict to organizational users only
- [ ] Admin access to flow monitoring and error logs

### Documentation
- [ ] Phase 2.8 implementation guide completed (this document)
- [ ] Flow diagrams documented
- [ ] Status transition rules documented
- [ ] Error codes and messages documented
- [ ] Troubleshooting guide created

### Training
- [ ] End users trained on issue workflow
- [ ] Managers trained on escalation process
- [ ] Support team trained on flow troubleshooting
- [ ] Documentation provided to users

### Monitoring
- [ ] Flow run history reviewed for errors
- [ ] Performance metrics baseline established
- [ ] Alert thresholds set for failure rates
- [ ] Support contact established for flow issues

---

## Related Documentation

- **Phase 2.6:** Issue Management Lists (Task List reference)
- **Phase 2.7:** Issue Management Screens (UI that triggers these flows)
- **Phase 2.5:** Audit Submission (can trigger issue creation)
- **Phase 3.1:** Dashboard KPIs (can display issue metrics from these flows)
- **Phase 4.1:** Notifications (can send alerts based on these flows)

---

## Conclusion

Phase 2.8 implements the complete issue workflow automation for the REdI Trolley Audit system. The 11 flows manage the full lifecycle of issues from creation through resolution, with comprehensive status tracking, escalation, and audit trails.

Key accomplishments:
- Automated issue numbering (ISS-YYYY-NNNN format)
- Enforced status lifecycle (Open → Assigned → In_Progress → Pending_Verification → Resolved → Closed)
- Corrective action tracking with automatic status updates
- Escalation matrix for management hierarchies
- Complete audit trail through system comments
- Error handling and validation at each step

All flows integrate with PowerApp dialogs to provide users with a complete issue management experience while maintaining data integrity through automated business logic.

**Estimated Total Duration:** 15 hours
**Complexity Level:** High (complex status logic, multiple interdependent flows)
**Risk Level:** Medium (lots of status transitions, but well-isolated flows)

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Technical Writer | Initial implementation guide |

**Status:** Ready for Implementation

*End of Phase 2.8 Implementation Guide*
