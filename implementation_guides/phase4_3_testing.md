# Phase 4.3 Testing Implementation Guide

**RBWH Resuscitation Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Comprehensive Testing Framework & Implementation Guide

---

## Overview

Phase 4.3 implements comprehensive testing and quality assurance for the RBWH Trolley Audit system before go-live. This phase covers test planning, functional testing across all modules, defect tracking and resolution, and formal sign-off procedures.

**Phase Scope:** Tasks 4.3.1 through 4.3.10
**Estimated Duration:** 4-6 weeks
**Prerequisites:** All Phases 1-4.2 complete and deployed to test environment

**Testing Strategy:**
```
Test Planning (4.3.1)
        ↓
Functional Testing (4.3.2-4.3.6)
  ├─ Trolley Management (4.3.2)
  ├─ Audit Entry (4.3.3)
  ├─ Issue Management (4.3.4)
  ├─ Random Selection (4.3.5)
  └─ Reporting (4.3.6)
        ↓
UAT & Defect Management (4.3.7-4.3.10)
  ├─ UAT Schedule (4.3.7)
  ├─ Defect Tracking (4.3.8)
  ├─ Defect Resolution (4.3.9)
  └─ Sign-off (4.3.10)
```

---

## Executive Summary

This guide provides:
1. **Test Plan Template** with scope, objectives, and entry/exit criteria
2. **70+ Test Cases** covering all functional areas with step-by-step instructions
3. **Defect Tracking Process** with severity classifications and SLA management
4. **UAT Framework** with participant roles and schedules
5. **Sign-off Checklist** for production readiness validation

All test cases follow the same structure: Objective, Prerequisites, Steps, Expected Result, and Pass/Fail Criteria.

---

## Part 1: Test Plan Template

### Task 4.3.1: Create Test Plan Document

#### 1.1 Test Plan Header

```
PROJECT: RBWH Resuscitation Trolley Audit System
TEST PLAN VERSION: 1.0
TEST ENVIRONMENT: SharePoint/Power Apps test site
TESTING PERIOD: [Start Date] to [End Date]
TEST LEAD: [Name/Title]
APPROVAL DATE: [Date]

Key Stakeholders:
- Test Lead: QA Manager
- Test Coordinator: [Name]
- Developer Representative: [Name]
- Business Representative: [Name]
```

#### 1.2 Test Scope and Objectives

**In Scope:**
- All PowerApp screens and navigation
- All SharePoint list operations (CRUD)
- Business logic and calculations (compliance scores, random selection)
- Power Automate workflows (audit submission, notifications)
- Power BI dashboard functionality
- Data validation and error handling
- Performance under expected load
- Security and permissions

**Out of Scope:**
- Load testing above 100 concurrent users
- Barcode scanning integration (Phase 5)
- S/4HANA integration (Phase 5)
- Mobile app native features (Phase 5)
- Staff training materials

**Testing Objectives:**
1. Validate all functional requirements are implemented correctly
2. Verify data integrity across SharePoint lists and calculations
3. Ensure error handling and edge cases are managed
4. Confirm user workflows match business process requirements
5. Validate security and role-based access controls
6. Verify performance meets acceptable standards
7. Identify and document all defects before go-live

#### 1.3 Test Environment Requirements

**System Configuration:**
| Component | Requirement | Status |
|-----------|------------|--------|
| SharePoint Site | Test tenant with 11 lists configured | ✓ Required |
| PowerApp | Canvas app published to test environment | ✓ Required |
| Power Automate | All flows activated in test tenant | ✓ Required |
| Power BI | Datasets connected to test SharePoint | ✓ Required |
| Test Data | Sample data matching production schemas | ✓ Required |
| User Accounts | Test accounts with various roles | ✓ Required |

**Required Test Data:**
- 76 Location records (trolley master data)
- 89 Equipment records (equipment master list)
- 8 EquipmentCategory records
- 7 ServiceLine records
- 1 AuditPeriod record (active)
- 50-100 sample Audit records (various statuses)
- 20-30 sample Issue records (various states)
- 10-15 sample RandomAuditSelection records

**User Accounts (Minimum):**
```
1. MERT_Educator (Full access)
2. NUM_Manager (Service line management)
3. Auditor_User (Audit entry, issue logging)
4. Clinical_Staff (View/audit capability)
5. Leadership_Viewer (Read-only access)
6. Anonymous (No access - security test)
```

#### 1.4 Entry and Exit Criteria

**Entry Criteria (Before Testing Begins):**
- [ ] All code from Phases 1-4.2 merged to test branch
- [ ] Test environment fully provisioned with all lists
- [ ] Test data imported and verified
- [ ] Test user accounts created with correct permissions
- [ ] All Power Automate flows deployed and activated
- [ ] PowerApp published to test environment
- [ ] Test plan approved by project stakeholders
- [ ] All testers trained on system and test procedures
- [ ] Defect tracking system configured and accessible

**Exit Criteria (Before Sign-off):**
- [ ] All test cases executed at least once
- [ ] No critical or high-severity defects remaining open
- [ ] All medium-severity defects addressed or accepted as deferred
- [ ] All test cases documented with pass/fail results
- [ ] Performance benchmarks met or documented as acceptable
- [ ] Security and access control tests passed
- [ ] UAT sign-off received from MERT Educators and NUM representatives
- [ ] Production deployment checklist completed
- [ ] Post-go-live support plan activated

#### 1.5 Test Case Format and Standards

**Standard Test Case Template:**

```
ID: [Test Case ID, e.g., TC-TM-001]
Title: [Concise description of what is being tested]
Module: [Trolley Management / Audit Entry / Issue Management / Random Selection / Reporting]
Priority: [Critical / High / Medium / Low]
Created By: [Name]
Date Created: [Date]
Last Updated: [Date]
Status: [Not Started / In Progress / Passed / Failed]

OBJECTIVE:
[What behavior or requirement is being validated?]

PREREQUISITES:
[System state required before test begins]
- User must be logged in as [Role]
- Data must include [specific records]
- [Other preconditions]

TEST STEPS:
1. [Action] - Example: "Click 'Add New Trolley' button"
2. [Action/Verification] - Example: "Enter 'ICU' in Department Name field"
3. [Action/Verification] - Example: "Verify form displays all required fields"
4. [Final action] - Example: "Click 'Save' button"

EXPECTED RESULT:
[What should happen if the system works correctly]
- Record is created successfully
- Confirmation message displays: "[specific message]"
- [User is navigated to appropriate screen]
- [Verification of data in SharePoint]

PASS/FAIL CRITERIA:
[ ] Record saved to Location list
[ ] All required fields have values
[ ] Audit trail entry created in LocationChangeLog
[ ] No error messages displayed
[ ] [Any other acceptance criteria]

ACTUAL RESULT:
[To be filled during testing]

NOTES:
[Any relevant observations, environment issues, or dependencies]
```

#### 1.6 Test Schedule and Milestones

```
WEEK 1: Test Planning & Preparation
├─ 4.3.1: Complete test plan document (3 days)
├─ Setup test environment (2 days)
└─ Import test data and verify (2 days)

WEEK 2-3: Functional Testing
├─ Trolley Management (4.3.2): 2 days
├─ Audit Entry (4.3.3): 3 days
├─ Issue Management (4.3.4): 2.5 days
├─ Random Selection (4.3.5): 1.5 days
└─ Reporting (4.3.6): 2 days

WEEK 3-4: Defect Resolution
├─ Defect triage and prioritization (1 day)
├─ Bug fix sprints (5 days)
└─ Regression testing (2 days)

WEEK 4-5: UAT Phase
├─ UAT kickoff meeting (0.5 days)
├─ UAT testing by business users (4 days)
├─ UAT findings review (1 day)
└─ Final fixes and verification (2 days)

WEEK 6: Sign-off
├─ Final testing verification (1 day)
├─ Sign-off meeting with stakeholders (0.5 days)
└─ Production deployment prep (1 day)
```

#### 1.7 Roles and Responsibilities

| Role | Responsibility | Effort |
|------|----------------|--------|
| **Test Lead** | Plan testing, coordinate activities, manage defects, sign-off | 30% |
| **Test Coordinator** | Prepare test environment, import data, manage test execution | 50% |
| **Automation QA** | Create test scripts, execute functional tests | 40% |
| **Manual QA** | Execute exploratory tests, UAT support | 30% |
| **Developer** | Reproduce defects, implement fixes, support testing | 20% |
| **Business Owner** | Define acceptance criteria, participate in UAT, approve sign-off | 15% |
| **UAT Participants** | Execute UAT test cases, provide business validation | 20% (external) |

#### 1.8 Risk Assessment and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Data inconsistencies in test environment | Medium | High | Automate data validation scripts, verify import completeness |
| Performance issues under load | Medium | High | Establish performance baselines early, document acceptable thresholds |
| Delays in defect resolution | Low | High | Allocate adequate developer resources, prioritize critical fixes |
| UAT stakeholder unavailability | Medium | Medium | Schedule UAT early, coordinate calendars in advance |
| Security access issues | Low | Critical | Test permissions thoroughly, involve IT security early |
| Power BI data refresh delays | Low | Medium | Monitor refresh schedules, document acceptable latency |

---

## Part 2: Functional Test Cases

### Task 4.3.2: Trolley Management Test Cases (15+ cases)

Trolley management includes operations to create, read, update, and manage trolley locations. These tests validate the full lifecycle of trolley records.

#### TC-TM-001: Add New Trolley - Basic Information

```
ID: TC-TM-001
Title: Add New Trolley with All Required Information
Module: Trolley Management
Priority: Critical
Created By: QA Lead
Date Created: January 2026

OBJECTIVE:
Verify that a MERT Educator can successfully create a new trolley location record with all required fields.

PREREQUISITES:
- User is logged in as MERT_Educator role
- On "Trolley Management" screen
- Test environment is running

TEST STEPS:
1. Click "Add New Trolley" button
2. Verify "Add New Trolley" form appears with all required fields
3. Enter Department Name: "ICU Pod 2"
4. Select Service Line: "Critical Care"
5. Enter Building: "James Mayne"
6. Enter Level: "L3"
7. Enter Specific Location: "Pod 2 Entrance"
8. Select Trolley Type: "Standard"
9. Select Defibrillator Type: "LIFEPAK 20/20e"
10. Select Operating Hours: "24_7"
11. Leave optional fields blank (paediatric, specialty meds)
12. Click "Save" button

EXPECTED RESULT:
- Form closes successfully
- Trolley list updates to show new record
- Department name "ICU Pod 2" appears in list with correct details
- Last Audit Date shows as empty/null
- CreatedBy shows logged-in user
- CreatedDate shows current date/time
- SharePoint Location list contains new record
- LocationChangeLog entry created with ChangeType: "Created"

PASS/FAIL CRITERIA:
[ ] Form submitted without validation errors
[ ] New record appears in trolley list immediately
[ ] Department name and all entered fields display correctly
[ ] SharePoint list updated within 2 minutes
[ ] Audit trail entry created
[ ] No error messages or notifications displayed
```

#### TC-TM-002: Add New Trolley - With Optional Equipment

```
ID: TC-TM-002
Title: Add New Trolley with Optional Equipment Configuration
Module: Trolley Management
Priority: High
Created By: QA Lead

OBJECTIVE:
Verify that optional equipment toggles (paediatric box, altered airway, specialty meds) are correctly saved when creating a trolley.

PREREQUISITES:
- User is logged in as MERT_Educator
- On "Add New Trolley" form
- Test environment running

TEST STEPS:
1. Enter all required fields (see TC-TM-001)
2. Toggle "Has Paediatric Box" to enabled (true)
3. Toggle "Has Altered Airway Equipment" to enabled (true)
4. Toggle "Has Specialty Medications" to enabled (true)
5. Enter specialty medication notes: "Requires cardiology drugs per protocol"
6. Click "Save" button
7. Navigate back to trolley list
8. Click on newly created trolley to view details

EXPECTED RESULT:
- All toggles show as enabled in detail view
- Specialty medication notes display correctly
- Equipment checklist will include:
  - Standard items
  - Paediatric items
  - Altered airway items
  - Specialty medication items (as noted)
- LocationEquipment records created with appropriate links
- Equipment filter shows paediatric flag = true

PASS/FAIL CRITERIA:
[ ] Optional equipment flags saved correctly
[ ] Specialty medication notes persisted
[ ] LocationEquipment detail records created (3 items)
[ ] Future audits will include optional equipment in checklist
[ ] Settings persistent after navigation and reopening
```

#### TC-TM-003: Edit Trolley - Update Basic Information

```
ID: TC-TM-003
Title: Edit Trolley Location - Change Basic Attributes
Module: Trolley Management
Priority: High

OBJECTIVE:
Verify that MERT Educator can edit existing trolley records and changes are persisted.

PREREQUISITES:
- User is logged in as MERT_Educator
- At least one trolley record exists in system
- On trolley list view

TEST STEPS:
1. Click on existing trolley record to open detail view
2. Click "Edit" button
3. Change Level from "L3" to "L5"
4. Change Specific Location from "Pod 2 Entrance" to "Pod 2 Main Area"
5. Select Trolley Type from "Standard" to "Specialty"
6. Click "Save" button
7. Verify return to detail view
8. Open same trolley record again to confirm changes

EXPECTED RESULT:
- Edit form displays all current values
- Changes saved without validation errors
- Detail view shows updated values
- Reopening record confirms changes persisted
- LocationChangeLog entry created with:
  - ChangeType: "Modified"
  - FieldChanged: "Level", "SpecificLocation", "TrolleyType"
  - OldValue: "L3", etc.
  - NewValue: "L5", etc.
- ModifiedDate updated to current time
- ModifiedBy shows logged-in user

PASS/FAIL CRITERIA:
[ ] All fields edited successfully
[ ] Changes displayed in detail view
[ ] Changes persisted after closing and reopening
[ ] Audit trail captures all field changes
[ ] Modification timestamp updated
[ ] User attribution correct
```

#### TC-TM-004: Edit Trolley - Deactivate with Reason

```
ID: TC-TM-004
Title: Deactivate Trolley with Reason and Date
Module: Trolley Management
Priority: High

OBJECTIVE:
Verify that trolleys can be deactivated with appropriate audit trail and removed from active audit lists.

PREREQUISITES:
- User is logged in as MERT_Educator
- Trolley is currently Active status
- On trolley detail view

TEST STEPS:
1. Click "Edit" button
2. Change Status to "Inactive"
3. Enter Status Change Date: [today's date]
4. Enter Status Change Reason: "Unit relocated to Ned Hanlon building"
5. Click "Save" button
6. Verify trolley detail shows inactive status
7. Navigate to trolley list
8. Verify trolley appears in list but marked as Inactive
9. Check random selection list (if applicable)

EXPECTED RESULT:
- Status changed to Inactive successfully
- StatusChangeDate and StatusChangeReason fields populated
- Trolley still visible in list (soft delete, not hard delete)
- Trolley excluded from active audit filters
- Trolley removed from any pending RandomAuditSelection records
- LocationChangeLog entry created:
  - ChangeType: "Deactivated"
  - OldValue: "Active"
  - NewValue: "Inactive"
  - ChangeReason: entered reason
- Any pending audits for this trolley cancelled with note
- Historical audit data retained for reporting

PASS/FAIL CRITERIA:
[ ] Status changed to Inactive
[ ] Deactivation reason recorded
[ ] Trolley excluded from "Add Audit" dropdown
[ ] Trolley excluded from random selection algorithm
[ ] Historical data retained (visible in trolley history)
[ ] Audit trail entry created with reason
[ ] Trolley can be reactivated if needed
```

#### TC-TM-005: Reactivate Deactivated Trolley

```
ID: TC-TM-005
Title: Reactivate Previously Deactivated Trolley
Module: Trolley Management
Priority: Medium

OBJECTIVE:
Verify that deactivated trolleys can be reactivated and returned to active audit status.

PREREQUISITES:
- User is logged in as MERT_Educator
- Trolley has Status = "Inactive"
- On trolley detail view

TEST STEPS:
1. Click "Edit" button
2. Verify Current Status shows "Inactive"
3. Change Status to "Active"
4. Verify status fields update (or clear for reactivation)
5. Click "Save" button
6. Verify trolley returns to Active status in list view
7. Navigate to "Start New Audit" and verify trolley appears in dropdown
8. Check that LastAuditDate is reset/cleared

EXPECTED RESULT:
- Status changed back to Active
- LastAuditDate reset to NULL (requires fresh audit before re-entering service)
- Trolley appears in active filters and dropdowns
- Trolley eligible for random selection
- LocationChangeLog entry created:
  - ChangeType: "Reactivated"
  - FieldChanged: "Status"
  - OldValue: "Inactive"
  - NewValue: "Active"
- Timestamp and user attribution correct

PASS/FAIL CRITERIA:
[ ] Status successfully changed to Active
[ ] Trolley appears in active audit list
[ ] LastAuditDate reset properly
[ ] Audit trail captures reactivation
[ ] No error messages displayed
[ ] Can immediately start audit for reactivated trolley
```

#### TC-TM-006: Filter Trolley List by Service Line

```
ID: TC-TM-006
Title: Filter Trolley List by Service Line
Module: Trolley Management
Priority: High

OBJECTIVE:
Verify that trolley list filtering by service line works correctly and displays only matching records.

PREREQUISITES:
- User is logged in as any role
- On trolley list view
- System contains trolleys from multiple service lines

TEST STEPS:
1. Verify trolley list shows all trolleys initially
2. Click "Filter" button or filter dropdown
3. Select "Service Line" filter
4. Select "Critical Care" from list
5. Verify list updates to show only Critical Care trolleys
6. Count displayed trolleys
7. Deselect filter to show all trolleys again
8. Apply multiple filters: Service Line = "Critical Care" AND Building = "James Mayne"

EXPECTED RESULT:
- Filter dropdown appears with service line options
- List updates immediately to show filtered results
- Count matches expected Critical Care trolleys
- All displayed trolleys show Service Line = "Critical Care"
- Multiple filter combinations work correctly
- List shows no results if no trolleys match filter
- Filter persists if user navigates and returns to list

PASS/FAIL CRITERIA:
[ ] Filter dropdown appears and is accessible
[ ] Single filter works correctly
[ ] Multiple filters work together (AND logic)
[ ] Result count accurate
[ ] All displayed records match filter criteria
[ ] Performance acceptable (list updates within 2 seconds)
[ ] Clear filter button works to reset
```

#### TC-TM-007: Search Trolley by Department Name

```
ID: TC-TM-007
Title: Search Trolley List by Department Name
Module: Trolley Management
Priority: High

OBJECTIVE:
Verify that the search function finds trolleys by partial department name matching.

PREREQUISITES:
- User is logged in as any role
- On trolley list view
- Multiple trolleys exist with searchable names

TEST STEPS:
1. Locate search box at top of trolley list
2. Enter "ICU" in search box
3. Verify list updates to show only trolleys containing "ICU"
4. Clear search and enter "7A" to search for specific floor
5. Verify search is case-insensitive by entering "7a" (lowercase)
6. Search for partial match: enter "Pod" to find "ICU Pod 1", "ICU Pod 2", etc.
7. Search for non-existent trolley: enter "XYZ999"
8. Verify no results message appears

EXPECTED RESULT:
- Search box accepts text input
- List filters in real-time as text is entered
- All results contain search term (case-insensitive)
- Partial matches included (e.g., "7A" matches "7A North", "7A South")
- Empty results show friendly message "No trolleys found"
- Search is context-aware (searches DepartmentName, Building, Level)
- Performance acceptable for lists with 100+ trolleys

PASS/FAIL CRITERIA:
[ ] Search box functional and visible
[ ] Real-time filtering works
[ ] Case-insensitive matching works
[ ] Partial matches included
[ ] Empty results handled gracefully
[ ] Search clears with X button
[ ] Results accurate
```

#### TC-TM-008: View Trolley Audit History

```
ID: TC-TM-008
Title: View Complete Audit History for Trolley
Module: Trolley Management
Priority: Medium

OBJECTIVE:
Verify that users can view all historical audits for a specific trolley with key details.

PREREQUISITES:
- User is logged in as any role with view access
- Trolley record exists with multiple completed audits
- On trolley detail view

TEST STEPS:
1. Click on trolley to open detail view
2. Click "Audit History" tab
3. Verify list of all audits appears in reverse chronological order (newest first)
4. Verify each audit shows:
   - Audit date
   - Auditor name
   - Audit type (Comprehensive / Spot Check)
   - Compliance score
   - Status (Submitted/Verified)
5. Click on individual audit to view full audit details
6. Verify graph/trend showing compliance over time
7. Return to trolley list

EXPECTED RESULT:
- Audit History tab displays all submitted audits
- Audits sorted by date descending
- Each row shows all key audit information
- Clicking audit navigates to audit detail view
- Trend chart shows compliance scores over time (visual or table)
- Performance acceptable (loads within 3 seconds for 50+ audits)
- Audits from deleted/deactivated trolleys not shown

PASS/FAIL CRITERIA:
[ ] All audits displayed (no missing records)
[ ] Audits sorted correctly (newest first)
[ ] All required fields visible
[ ] Audit drill-down works
[ ] Trend data accurate
[ ] Performance acceptable
[ ] No error messages
```

#### TC-TM-009: View Trolley Issues

```
ID: TC-TM-009
Title: View All Issues Associated with Trolley
Module: Trolley Management
Priority: Medium

OBJECTIVE:
Verify that users can view all issues linked to a specific trolley.

PREREQUISITES:
- User is logged in as any role with view access
- Trolley has multiple issues (open and closed)
- On trolley detail view

TEST STEPS:
1. Click on trolley to open detail view
2. Click "Issues" tab
3. Verify list of all issues displays
4. Verify each issue shows:
   - Issue ID
   - Title
   - Severity (color-coded)
   - Status
   - Assigned to
   - Days open
5. Apply filters: Status = "Open" to see only open issues
6. Apply filters: Severity = "Critical" to see critical issues
7. Click on issue to view full issue detail

EXPECTED RESULT:
- Issues tab displays all issues for trolley
- All required fields visible
- Issues can be filtered by status and severity
- Open issues highlighted or emphasized
- Clicking issue navigates to issue detail
- Closed issues still visible but marked as closed
- Count of open vs closed issues displayed

PASS/FAIL CRITERIA:
[ ] All issues displayed
[ ] Filters work correctly
[ ] Issue detail accessible
[ ] Severity color coding applied
[ ] Days open calculated correctly
[ ] Count totals accurate
```

#### TC-TM-010: View Trolley Change Log

```
ID: TC-TM-010
Title: View Audit Trail of Trolley Modifications
Module: Trolley Management
Priority: Medium

OBJECTIVE:
Verify that change log shows all modifications to trolley record with who, when, and why.

PREREQUISITES:
- User is logged in as MERT_Educator or higher
- Trolley has been modified multiple times
- On trolley detail view

TEST STEPS:
1. Click on trolley to open detail view
2. Click "Change Log" tab
3. Verify list displays in reverse chronological order (newest first)
4. For each entry, verify displays:
   - Date and time of change
   - Changed by (user name)
   - Change type (Created, Modified, Deactivated, Reactivated)
   - Field name changed (if modification)
   - Old value
   - New value
   - Reason for change (if deactivation)
5. Verify change log is read-only (no editing)

EXPECTED RESULT:
- Change log displays all modifications in order
- Each entry shows complete audit information
- Data is accurate and matches modifications made
- Timestamps reflect actual change times
- User attribution correct
- Change log is append-only (no deletions or edits)
- Performance acceptable (list loads quickly)

PASS/FAIL CRITERIA:
[ ] Change log displays all modifications
[ ] Chronological order correct
[ ] Field-level changes tracked
[ ] Old/new values accurate
[ ] User attribution correct
[ ] Timestamps accurate
[ ] Read-only enforcement
[ ] No missing entries
```

#### TC-TM-011: Bulk Import Trolleys from CSV

```
ID: TC-TM-011
Title: Bulk Import Multiple Trolleys from CSV File
Module: Trolley Management
Priority: Medium
Created By: QA Lead

OBJECTIVE:
Verify that MERT Educator can bulk import trolley data from properly formatted CSV file.

PREREQUISITES:
- User is logged in as MERT_Educator
- CSV file prepared with trolley data
- On Trolley Management screen
- CSV format matches schema requirements

TEST STEPS:
1. Navigate to "Trolley Management" screen
2. Click "Bulk Import Trolleys" button
3. Verify import dialog appears
4. Click "Choose File" to select CSV
5. Select test file with 10 trolleys
6. Verify preview shows data to be imported:
   - Columns mapped correctly
   - Row count correct
   - Data looks reasonable
7. Click "Validate" button
8. Verify validation results show any issues:
   - Missing required fields
   - Invalid choices
   - Duplicate department names
9. If valid, click "Import" button
10. Verify import completion message
11. Check trolley list for new records

EXPECTED RESULT:
- CSV file accepted and parsed
- Preview shows all rows to be imported
- Validation identifies data quality issues
- Import creates SharePoint records for all valid rows
- Invalid rows rejected with specific error messages
- LocationChangeLog entries created for each imported trolley
- Import report generated showing:
  - Total rows in file
  - Rows imported successfully
  - Rows rejected with reason
- Timestamps and CreatedBy set to current user/date

PASS/FAIL CRITERIA:
[ ] File upload works
[ ] Data preview accurate
[ ] Validation identifies issues
[ ] Valid rows imported successfully
[ ] Invalid rows reported with specific errors
[ ] Records appear in trolley list
[ ] Audit trail entries created
[ ] Import report accessible
```

#### TC-TM-012: Validate Required Fields on Add/Edit

```
ID: TC-TM-012
Title: Validate Required Fields Prevent Incomplete Records
Module: Trolley Management
Priority: Critical

OBJECTIVE:
Verify that required field validation prevents incomplete trolley records from being saved.

PREREQUISITES:
- User is logged in as MERT_Educator
- On "Add New Trolley" or "Edit Trolley" form

TEST STEPS:
1. Click "Add New Trolley" button
2. Leave Department Name blank
3. Leave Service Line blank
4. Leave Building blank
5. Click "Save" button
6. Verify error messages appear for each required field
7. Enter Department Name: "Test Trolley"
8. Leave other required fields blank
9. Click "Save" again
10. Verify error messages appear for remaining fields
11. Populate all required fields
12. Click "Save" button
13. Verify record saves successfully

EXPECTED RESULT:
- Save button disabled until required fields populated (or error shown on click)
- Error messages display clearly above each required field
- Error message text indicates which fields are required
- User prevented from saving incomplete record
- After all required fields filled, save succeeds
- No partial records created in SharePoint

PASS/FAIL CRITERIA:
[ ] Required field validation active
[ ] Error messages specific and helpful
[ ] Save prevented when fields missing
[ ] Save succeeds when complete
[ ] No orphaned/incomplete records created
```

#### TC-TM-013: Validate Choice Field Values

```
ID: TC-TM-013
Title: Validate Choice Fields Accept Only Allowed Values
Module: Trolley Management
Priority: High

OBJECTIVE:
Verify that choice fields (dropdowns) enforce allowed values and prevent invalid entries.

PREREQUISITES:
- User is logged in as MERT_Educator
- On "Add New Trolley" form

TEST STEPS:
1. Click Service Line dropdown
2. Verify only valid service lines appear:
   - Critical Care
   - Emergency Medicine
   - Paediatrics
   - Surgery
   - [Other valid options]
3. Select "Critical Care"
4. Click Trolley Type dropdown
5. Verify only Standard / Emergency / Specialty appear
6. Select "Standard"
7. Click Defibrillator Type dropdown
8. Verify only LIFEPAK_1000_AED / LIFEPAK_20_20e appear
9. Select "LIFEPAK 20/20e"
10. Click "Save" and verify record created with correct choice values

EXPECTED RESULT:
- Dropdowns show only allowed values
- User cannot manually type invalid values
- Selected values persist and save correctly to SharePoint
- Choice fields prevent data inconsistency
- Invalid values rejected if attempted (no direct SQL injection)

PASS/FAIL CRITERIA:
[ ] Service Line dropdown shows correct values
[ ] Trolley Type dropdown shows correct values
[ ] Defibrillator Type dropdown shows correct values
[ ] Invalid values cannot be selected
[ ] Selected values save correctly
[ ] SharePoint record shows selected choice values
```

#### TC-TM-014: Duplicate Department Name Validation

```
ID: TC-TM-014
Title: Prevent Duplicate Department Names
Module: Trolley Management
Priority: High

OBJECTIVE:
Verify that system prevents creation of duplicate trolley locations with same department name.

PREREQUISITES:
- User is logged in as MERT_Educator
- Trolley with Department Name "ICU Pod 1" already exists
- On "Add New Trolley" form

TEST STEPS:
1. Click "Add New Trolley" button
2. Enter Department Name: "ICU Pod 1" (exact match of existing trolley)
3. Fill other required fields
4. Click "Save" button
5. Verify error message appears: "A trolley with this department name already exists"
6. Change Department Name to "ICU Pod 1 - Room 2" (similar but different)
7. Click "Save" button
8. Verify record saves successfully

EXPECTED RESULT:
- Exact duplicate names rejected with clear error
- Similar names allowed (only enforces uniqueness)
- Error message appears before record creation
- No duplicate records created
- Error message suggests reviewing existing trolleys

PASS/FAIL CRITERIA:
[ ] Duplicate names rejected
[ ] Similar names allowed
[ ] Error message clear and helpful
[ ] No duplicate records in SharePoint
[ ] Existing trolley not modified
```

#### TC-TM-015: Verify Trolley Permissions - MERT Only Operations

```
ID: TC-TM-015
Title: Verify Only MERT Educators Can Add/Edit/Deactivate Trolleys
Module: Trolley Management
Priority: Critical

OBJECTIVE:
Verify that security controls enforce trolley management permissions (MERT Educator only).

PREREQUISITES:
- Test user accounts with various roles exist
- Users logged in with appropriate permissions

TEST STEPS:
1. Log in as Auditor_User role
2. Navigate to Trolley Management screen
3. Verify "Add New Trolley" button is not visible or disabled
4. Verify trolley list shows records but no "Edit" button on each row
5. Attempt to edit URL directly to add new trolley (if possible)
6. Verify access denied message appears
7. Log out and log in as MERT_Educator
8. Verify "Add New Trolley" button is visible and enabled
9. Verify "Edit" buttons appear on each trolley row
10. Verify ability to perform trolley operations

EXPECTED RESULT:
- Non-MERT users cannot see management buttons
- Non-MERT users cannot access add/edit/delete operations
- MERT Educators have full trolley management access
- Security enforced at both UI and backend (SharePoint permissions)
- Attempt to bypass via URL results in error
- Audit trail shows who made changes

PASS/FAIL CRITERIA:
[ ] Auditor cannot see Add/Edit buttons
[ ] Auditor cannot save trolley changes
[ ] Non-MERT role cannot access admin operations
[ ] MERT Educator has full access
[ ] URL-based bypass prevented
[ ] SharePoint list permissions enforce security
```

---

### Task 4.3.3: Audit Entry Test Cases (20+ cases)

Audit entry encompasses the full workflow for conducting audits: selecting trolleys, documenting findings, checking equipment, and submitting results. These tests are critical to the core business process.

#### TC-AE-001: Start New Audit - Location Selection

```
ID: TC-AE-001
Title: Start New Audit and Select Trolley Location
Module: Audit Entry
Priority: Critical

OBJECTIVE:
Verify that auditors can initiate a new audit by selecting a trolley location from the available list.

PREREQUISITES:
- User is logged in as Auditor role
- Multiple trolley locations exist in system
- On "Audit Entry" or "Start New Audit" screen

TEST STEPS:
1. Click "Start New Audit" button
2. Verify "Audit Selection" screen appears
3. Verify trolley list dropdown shows:
   - Department Name (prominent)
   - Building and Level (supporting info)
   - Last audit date if available
4. Click dropdown to open trolley selection
5. Search for "ICU" and verify filtered results appear
6. Select "ICU Pod 1" from dropdown
7. Verify form updates to show:
   - Last Audit Date: [date or "No previous audits"]
   - Days Since Last Audit: [number]
   - Last Compliance Score: [percentage or "-"]

EXPECTED RESULT:
- Trolley dropdown is searchable and filterable
- Selected location populates all related fields
- Historical audit information displays correctly
- Inactive/deactivated trolleys excluded from list
- Only active trolleys available for audit selection
- Last audit info accurately reflects Location record

PASS/FAIL CRITERIA:
[ ] Dropdown functional and searchable
[ ] All active trolleys available
[ ] Inactive trolleys excluded
[ ] Last audit info displayed correctly
[ ] Date formatting correct
[ ] No error messages
[ ] Performance acceptable (search < 1 sec)
```

#### TC-AE-002: Audit Type Selection - Comprehensive vs Spot Check

```
ID: TC-AE-002
Title: Select Audit Type - Comprehensive or Spot Check
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that auditors can select and confirm audit type (Comprehensive or Spot Check).

PREREQUISITES:
- User is logged in as Auditor
- Trolley location selected in previous step
- On Audit Selection screen

TEST STEPS:
1. Verify audit type radio buttons displayed with options:
   - Comprehensive: "Detailed check of all trolley items"
   - Spot Check: "Focused review of key items"
2. Verify Comprehensive is selected by default
3. Click Spot Check radio button
4. Verify Spot Check is now selected
5. Click Comprehensive radio button
6. Verify Comprehensive is selected again
7. Click "Continue" button with Comprehensive selected

EXPECTED RESULT:
- Both audit type options available and selectable
- Comprehensive defaults as pre-selected
- Selection updates immediately when clicked
- Selected option persists through form navigation
- Continue button navigates to Documentation Check screen
- Audit type stored in context for later processing

PASS/FAIL CRITERIA:
[ ] Both options visible and functional
[ ] Default to Comprehensive works
[ ] Selection updates correctly
[ ] Selection persists
[ ] Continue button works
```

#### TC-AE-003: Documentation Check - All Fields Present

```
ID: TC-AE-003
Title: Complete Documentation Check Screen with All Fields
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that auditors can complete documentation check section recording status of four document types.

PREREQUISITES:
- User has selected trolley and audit type
- On Documentation Check screen
- Step indicator shows "Step 1 of 4"

TEST STEPS:
1. Verify four documentation sections visible:
   - Check Record Present (Current / Old / None)
   - Checking Guidelines Present (Current / Old / None)
   - BLS Poster Present (Yes / No)
   - Equipment List Present (Current / Old / None)
2. Select "Current" for Check Record
3. Select "Old" for Checking Guidelines
4. Toggle BLS Poster to "Yes"
5. Select "None" for Equipment List
6. Verify all selections persist
7. Click "Continue to Condition Check" button

EXPECTED RESULT:
- All four document sections displayed correctly
- Radio buttons and toggles functional
- Selections saved in AuditData context
- Form navigates to Condition Check screen
- Selected location name persists in header
- Progress indicator shows Step 2 of 4 on next screen

PASS/FAIL CRITERIA:
[ ] All documentation fields visible
[ ] Selections functional and persistent
[ ] Continue button works
[ ] Navigation to next screen successful
[ ] Context data preserved
[ ] No validation errors
```

#### TC-AE-004: Condition Check - Cleanliness and Working Order

```
ID: TC-AE-004
Title: Complete Condition Check - Trolley Condition Assessment
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that auditors can assess physical condition of trolley including cleanliness and working order.

PREREQUISITES:
- Previous audit screens completed
- On Condition Check screen
- Step indicator shows "Step 2 of 4"

TEST STEPS:
1. Verify all condition check questions visible:
   - Is trolley clean? (Yes/No toggle)
   - Is trolley in working order? (Yes/No toggle)
   - Are rubber bands present and in use? (Yes/No)
   - Is O2 tubing correct type/condition? (Yes/No)
   - INHALO cylinder has correct pressure? (Yes/No)
2. Toggle "Clean" to "Yes"
3. Toggle "Working Order" to "Yes"
4. Verify issue description field does NOT appear
5. Click "Working Order" to toggle to "No"
6. Verify issue description field appears
7. Enter issue description: "Drawer 3 stuck, difficult to open"
8. Toggle "Clean" to "No"
9. Continue with other condition checks:
   - Rubber Bands: "No"
   - O2 Tubing: "Yes"
   - INHALO: "Yes"
10. Click "Continue to Routine Checks"

EXPECTED RESULT:
- All condition questions displayed with toggles
- Issue description field conditionally appears/hides based on working order
- All selections persist and update AuditData
- Form navigates to Routine Checks screen
- Issue description stored for later reference

PASS/FAIL CRITERIA:
[ ] All condition fields visible
[ ] Toggle functionality works
[ ] Issue field appears/hides correctly
[ ] Selections persist
[ ] Form validates
[ ] Navigation successful
```

#### TC-AE-005: Routine Checks - Check Count Entry

```
ID: TC-AE-005
Title: Enter Routine Check Counts for Audited Period
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that auditors can enter outside and inside check counts with proper validation.

PREREQUISITES:
- Previous screens completed
- On Routine Checks screen
- Step indicator shows "Step 3 of 4"

TEST STEPS:
1. Verify expected check counts display:
   - Expected Outside (Daily) Checks: [value from Location]
   - Expected Inside (Weekly) Checks: [value from Location]
2. Toggle "Check records available?" to "Yes"
3. Verify count entry fields appear
4. Enter Outside Check Count: "28"
5. Enter Inside Check Count: "5"
6. Verify helper text shows ratios: "28 / Expected: 30"
7. Click "Continue to Equipment Check"

EXPECTED RESULT:
- Expected counts displayed from Location master data
- Count entry fields functional
- Numeric validation prevents non-numeric entry
- Counts stored in AuditData
- Form navigates to Equipment Check screen
- Context preserved

PASS/FAIL CRITERIA:
[ ] Expected counts accurate
[ ] Count fields visible and functional
[ ] Numeric input only accepted
[ ] Counts stored
[ ] Navigation works
[ ] No validation errors
```

#### TC-AE-006: Routine Checks - Records Not Available

```
ID: TC-AE-006
Title: Handle Case When Check Records Not Available
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that auditors can indicate when routine check records are unavailable and provide reason.

PREREQUISITES:
- On Routine Checks screen

TEST STEPS:
1. Toggle "Check records available?" to "No"
2. Verify count entry fields disappear
3. Verify reason text field appears with label "Reason records not available:"
4. Enter reason: "Check book archived, ward unable to locate records"
5. Click "Continue to Equipment Check"

EXPECTED RESULT:
- Count entry fields hidden when toggle set to No
- Reason field displayed and required
- Reason saved in AuditData
- CheckCountNotAvailable flag set to true
- Count fields will be excluded from compliance calculation
- Form navigates successfully

PASS/FAIL CRITERIA:
[ ] Count fields hide correctly
[ ] Reason field appears
[ ] Reason required (cannot continue without it)
[ ] Reason saved
[ ] Navigation works
```

#### TC-AE-007: Equipment Check - Dynamic Checklist

```
ID: TC-AE-007
Title: View Equipment Checklist - Correct Items Based on Trolley Config
Module: Audit Entry
Priority: Critical

OBJECTIVE:
Verify that equipment checklist displays correct items based on trolley configuration (paediatric, altered airway, specialty meds).

PREREQUISITES:
- Previous screens completed
- Selected trolley configured with optional equipment
- On Equipment Check screen

TEST STEPS:
1. Verify equipment displayed in categories:
   - TOP OF TROLLEY
   - DRAWER 1 - IV EQUIPMENT
   - DRAWER 2 - MEDICATION & IV FLUIDS
   - DRAWER 3 - AIRWAY EQUIPMENT
   - DRAWER 4 - PPE & EXTRA EQUIPMENT
2. If trolley has paediatric box enabled, verify PAEDIATRIC BOX section present
3. If trolley has altered airway enabled, verify altered airway items included in appropriate drawers
4. If trolley has specialty meds enabled, verify specialty medication items in Drawer 2
5. For each item, verify columns:
   - Item name
   - Expected quantity
   - Found quantity (input field)
   - OK/Not OK indicator
   - Notes field
6. Enter quantities for 5 items:
   - BVM: 1 found (Expected: 1) → OK
   - Gloves: 0 found (Expected: 1) → Not OK (missing)
   - Adrenaline: 4 found (Expected: 6) → Not OK (short)
   - Suction: 1 found (Expected: 1) → OK
   - O2 mask: 1 found (Expected: 1) → OK

EXPECTED RESULT:
- Correct items appear based on trolley configuration
- Standard items always appear
- Optional items appear only if enabled for trolley
- All equipment fields editable
- OK/Not OK status calculated automatically
- Equipment score updates as items entered

PASS/FAIL CRITERIA:
[ ] Correct items displayed for trolley config
[ ] Optional items included/excluded appropriately
[ ] All item fields visible
[ ] Quantity input functional
[ ] Status updates correctly
[ ] Equipment score calculates
```

#### TC-AE-008: Equipment Check - Quantity Validation

```
ID: TC-AE-008
Title: Validate Equipment Quantity Entry - Numeric and Range
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that equipment quantity fields accept only valid numeric values.

PREREQUISITES:
- On Equipment Check screen
- Quantity entry fields visible

TEST STEPS:
1. Click on quantity field for first item
2. Type "abc" and try to move to next field
3. Verify text is rejected or cleared
4. Type "5" (numeric) in quantity field
5. Verify numeric value accepted
6. Try typing "-3" (negative number)
7. Verify negative rejected with message
8. Type "999" (unreasonably high number)
9. Verify value accepted (no upper limit enforcement needed)
10. Leave quantity field blank
11. Try to continue to next screen
12. Verify form validation requires all quantities filled

EXPECTED RESULT:
- Numeric input only accepted
- Non-numeric characters rejected
- Negative numbers rejected
- Empty fields trigger validation error on form submit
- Error message appears: "Please enter quantities for all equipment items"
- User cannot proceed until all fields populated

PASS/FAIL CRITERIA:
[ ] Non-numeric rejected
[ ] Negative numbers rejected
[ ] Numeric values accepted
[ ] Empty fields validated
[ ] Error messages clear
```

#### TC-AE-009: Equipment Check - Missing Critical Items

```
ID: TC-AE-009
Title: Equipment Check - Identify Critical Missing Items
Module: Audit Entry
Priority: Critical

OBJECTIVE:
Verify that system identifies and flags critical items as missing (safety-critical equipment).

PREREQUISITES:
- On Equipment Check screen
- Equipment with CriticalItem flag = true exists in data

TEST STEPS:
1. For critical items (adrenaline, defib pads, BVM), enter quantity "0"
2. Verify item shows as critical (highlighted in red or marked "CRITICAL")
3. Verify compliance score immediately drops
4. Note items flagged as critical:
   - Adrenaline 1mg (6 ampoules)
   - Quick-Combo defib pads
   - BVM resuscitator with mask
5. Continue to review screen without fixing critical items
6. Verify warning message appears on Review screen

EXPECTED RESULT:
- Critical items flagged clearly (red background, exclamation mark)
- Compliance score shows significant penalty
- Warning displayed when critical items missing
- System allows submission but flags for review
- Audit can be flagged for escalation

PASS/FAIL CRITERIA:
[ ] Critical items identified visually
[ ] Compliance score penalized
[ ] Warning shown on review
[ ] System allows submission
[ ] Audit flagged appropriately
```

#### TC-AE-010: Audit Review and Compliance Score Calculation

```
ID: TC-AE-010
Title: Review Audit Summary and Verify Compliance Score
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that audit review screen displays complete summary with calculated compliance scores.

PREREQUISITES:
- All audit entry screens completed
- On Audit Review screen

TEST STEPS:
1. Verify review screen displays summary of all entered data:
   - Selected location
   - Audit type
   - Auditor name
   - All documentation check results
   - All condition check results
   - Routine check counts
   - Equipment findings (summary)
2. Verify compliance scores displayed:
   - Documentation Score: [percentage]
   - Equipment Score: [percentage]
   - Condition Score: [percentage]
   - Check Score: [percentage]
   - Overall Compliance: [percentage]
3. Verify score calculation breakdown is accurate (weights shown)
4. If compliance < 80%, verify "Requires Follow-up" flag set
5. Verify follow-up due date calculated (7 days from today)

EXPECTED RESULT:
- All audit data summarized correctly
- Compliance scores calculated per business logic
- Scores displayed as percentages
- Weights and formulas accurate
- Follow-up flag set when compliance < 80%
- Follow-up date calculated correctly
- Edit button to return to previous screens available

PASS/FAIL CRITERIA:
[ ] All audit data displayed correctly
[ ] Compliance scores calculated accurately
[ ] Scores match business logic weights
[ ] Follow-up flag set appropriately
[ ] Follow-up due date correct
[ ] Edit buttons functional
```

#### TC-AE-011: Submit Audit - Save to SharePoint

```
ID: TC-AE-011
Title: Submit Audit and Save to SharePoint Lists
Module: Audit Entry
Priority: Critical

OBJECTIVE:
Verify that audit submission creates records in all appropriate SharePoint lists.

PREREQUISITES:
- All audit entry screens completed
- On Audit Review screen
- Ready to submit

TEST STEPS:
1. Verify all data is correct on review screen
2. Click "Submit Audit" button
3. Verify confirmation message appears
4. Wait for form processing (2-5 seconds)
5. Verify audit submitted message displays
6. Check SharePoint Audit list for new record:
   - AuditId generated
   - LocationId populated
   - AuditType set correctly
   - SubmissionStatus = "Submitted"
   - StartedDateTime = when audit began
   - CompletedDateTime = when submitted
   - Compliance scores populated
7. Verify AuditEquipment records created for each equipment item
8. Verify Location record updated with LastAuditDate and LastAuditCompliance
9. Check if any issues created for critical items

EXPECTED RESULT:
- Audit record created successfully in Audit list
- AuditEquipment detail records created (one per item)
- Location record updated with latest audit info
- All timestamp fields populated
- Compliance scores calculated and stored
- SubmissionStatus = "Submitted"
- If critical issues, Issue records created
- User notification confirms successful submission
- Form navigates to next action (issue review or home)

PASS/FAIL CRITERIA:
[ ] Audit record created in SharePoint
[ ] All required fields populated
[ ] AuditEquipment records created
[ ] Location record updated
[ ] Timestamps correct
[ ] Compliance scores stored
[ ] Issues created if applicable
[ ] Confirmation message clear
```

#### TC-AE-012: Draft Audit - Save and Resume Later

```
ID: TC-AE-012
Title: Save Audit as Draft and Resume Later
Module: Audit Entry
Priority: Medium

OBJECTIVE:
Verify that auditors can save incomplete audits and resume them later without losing data.

PREREQUISITES:
- Audit entry in progress
- Partway through Equipment Check screen

TEST STEPS:
1. Enter data through Equipment Check screen
2. Click "Save as Draft" button
3. Verify confirmation: "Audit saved. You can resume it later."
4. Navigate away (go to home screen)
5. Return to Audit Entry
6. Verify list of draft audits shown
7. Verify draft shows:
   - Location name
   - Last saved time
   - % complete
   - Resume button
8. Click "Resume" on draft audit
9. Verify all previously entered data restored
10. Verify form shows equipment data entered before
11. Complete remaining fields
12. Submit audit

EXPECTED RESULT:
- Draft audit saved with all entered data
- Draft record created in Audit list with SubmissionStatus = "Draft"
- User can navigate away without losing data
- Draft list accessible from audit entry screen
- Resume restores all data exactly as saved
- Form allows completion from where it was saved
- After submission, draft changed to "Submitted"

PASS/FAIL CRITERIA:
[ ] Draft saves successfully
[ ] Draft appears in draft list
[ ] Resume restores all data
[ ] Data integrity maintained
[ ] Can complete and submit draft
[ ] Draft to Submitted transition works
```

#### TC-AE-013: Audit Validation - Cannot Submit Incomplete

```
ID: TC-AE-013
Title: Validation - Cannot Submit Audit with Missing Required Data
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that audit submission validation prevents incomplete audits from being submitted.

PREREQUISITES:
- Audit partially completed
- Missing key required data

TEST STEPS:
1. Complete Documentation Check screen with all fields
2. Skip Condition Check screen
3. Go directly to Equipment Check (if allowed)
4. Click "Submit" without filling all equipment quantities
5. Verify validation error appears
6. Verify error lists all required fields missing
7. Return to required screens and complete them
8. Verify Submit button becomes enabled
9. Submit successfully

EXPECTED RESULT:
- Validation prevents submission with missing data
- Error message lists all missing required fields
- Submit button disabled until all requirements met
- User guided back to complete missing data
- After completion, submit succeeds
- No partial records created

PASS/FAIL CRITERIA:
[ ] Validation active and enforced
[ ] Error messages specific and helpful
[ ] Submit prevented when incomplete
[ ] All required fields identified
[ ] Submit succeeds when complete
```

#### TC-AE-014: Multiple Audits In Progress - Prevent Duplicate

```
ID: TC-AE-014
Title: Prevent Duplicate Audits - Only One In Progress Per Location
Module: Audit Entry
Priority: High

OBJECTIVE:
Verify that system prevents creation of duplicate in-progress audits for same trolley.

PREREQUISITES:
- User has draft/in-progress audit for location "ICU Pod 1"
- Attempting to start new audit for same location

TEST STEPS:
1. Start new audit for "ICU Pod 1"
2. Verify warning message appears:
   "There is an existing draft/in-progress audit for this trolley started at [time]. Resume existing audit?"
3. Options: Resume existing / Start new anyway
4. Click "Resume existing"
5. Verify existing audit data loads
6. Cancel and try again
7. Click "Start new anyway"
8. Verify confirmation: "Starting new audit will abandon the existing draft"
9. Click "Confirm"
10. Verify new audit started, old draft still accessible

EXPECTED RESULT:
- System detects existing in-progress audit
- Warning message alerts user
- Option to resume or override provided
- If resumed, old draft loads with existing data
- If overridden, both audit records exist in SharePoint
- User prevented from accidentally creating true duplicates
- Audit trail tracks all audit attempts

PASS/FAIL CRITERIA:
[ ] Duplicate detection working
[ ] Warning message clear
[ ] Resume option works
[ ] Override option works
[ ] Both audits tracked if created
[ ] No data loss
```

#### TC-AE-015: Audit Data Persistence During Navigation

```
ID: TC-AE-015
Title: Audit Data Persists When Navigating Between Screens
Module: Audit Entry
Priority: Medium

OBJECTIVE:
Verify that AuditData context variable persists through all screen navigation.

PREREQUISITES:
- Audit entry in progress with data in multiple screens

TEST STEPS:
1. Complete Documentation Check screen
2. Navigate to Condition Check
3. Return to Documentation Check using Back button
4. Verify all previous documentation entries still present
5. Go forward to Condition Check
6. Enter condition data
7. Go to Routine Checks
8. Return to Equipment Check (not yet filled)
9. Return to Condition Check
10. Verify condition data still present
11. Continue through all screens to review
12. Verify all data present on review screen

EXPECTED RESULT:
- All data persists through forward/back navigation
- No data loss when switching screens
- Form fields populate with previously entered values
- Context variable maintains integrity
- User can edit any section and continue
- Final review shows all entered data

PASS/FAIL CRITERIA:
[ ] Data persists back/forward
[ ] No fields reset unexpectedly
[ ] Context variable intact
[ ] All screens restore previous data
[ ] Review shows complete information
```

#### TC-AE-016: Audit Timestamp Recording

```
ID: TC-AE-016
Title: Verify Audit Timestamps - Start and Completion
Module: Audit Entry
Priority: Medium

OBJECTIVE:
Verify that audit start and completion times are recorded correctly in SharePoint.

PREREQUISITES:
- Audit entry in progress

TEST STEPS:
1. Start new audit for trolley "ICU Pod 1"
2. Note current time (approximately)
3. Complete all audit screens
4. Submit audit
5. Navigate to SharePoint Audit list
6. Open newly created audit record
7. Verify StartedDateTime = approximately when audit began
8. Verify CompletedDateTime = when audit was submitted
9. Note duration between timestamps
10. Verify timestamps in app match SharePoint

EXPECTED RESULT:
- StartedDateTime recorded when audit initiated (screen shown)
- CompletedDateTime recorded when audit submitted
- Timestamps accurate to within 1-2 minutes
- Timestamps stored in audit history for reporting
- Duration can be calculated from timestamps
- Timestamps use system time (not user-entered)

PASS/FAIL CRITERIA:
[ ] StartedDateTime recorded correctly
[ ] CompletedDateTime recorded correctly
[ ] Timestamps accurate
[ ] Timestamps in SharePoint match app
[ ] Timestamps can be used for reporting
```

---

### Task 4.3.4: Issue Management Test Cases (15+ cases)

Issue management covers the complete lifecycle from identification through resolution. Issues can be created during audits or independently.

#### TC-IM-001: Create Issue During Audit

```
ID: TC-IM-001
Title: Create Issue from Within Audit Entry Screen
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that auditors can create issues inline during audit entry.

PREREQUISITES:
- User is logged in as Auditor role
- In progress on Equipment Check screen
- Found a missing or defective equipment item

TEST STEPS:
1. On Equipment Check screen, find an item marked as missing
2. Click "Log Issue" button for that item
3. Verify Issue form appears with:
   - Location pre-populated from selected trolley
   - AuditId pre-populated from current audit
   - EquipmentId pre-populated from selected item
4. Fill issue form:
   - Title: "Adrenaline ampoules missing"
   - Description: "Only 4 of 6 required adrenaline 1mg ampoules present. 2 expired Dec 2023"
   - Severity: Select "Critical"
   - Category: Select "Equipment"
5. Click "Save Issue" button
6. Verify issue created and linked to audit
7. Verify issue appears on audit review screen
8. Complete and submit audit

EXPECTED RESULT:
- Issue form appears inline with trolley/audit context
- Equipment item linked to issue
- Issue saved successfully
- IssueNumber generated automatically (e.g., "ISS-2024-0042")
- Issue linked to audit through AuditId
- Issue appears in location issue history
- Issue status set to "Open"
- ReportedBy set to current user
- ReportedDate set to current date/time

PASS/FAIL CRITERIA:
[ ] Issue form accessible from audit
[ ] Fields pre-populated correctly
[ ] Issue saved successfully
[ ] IssueNumber generated
[ ] Issue linked to location, audit, equipment
[ ] Issue appears in history
[ ] Status set to "Open"
```

#### TC-IM-002: Create Issue Independently

```
ID: TC-IM-002
Title: Create Issue Outside of Audit Entry
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that users can create issues independently (not from audit).

PREREQUISITES:
- User is logged in with issue creation permission
- On Issues screen or main Issues menu

TEST STEPS:
1. Click "New Issue" button
2. Verify issue creation form appears
3. Select Location: "7A North"
4. Leave AuditId blank (independent issue)
5. Fill issue form:
   - Title: "Defibrillator battery low"
   - Description: "Battery indicator shows low level. Needs replacement."
   - Severity: "High"
   - Category: "Equipment"
   - Equipment: Select "LIFEPAK 20/20e defib unit"
   - Impact: "Device may not function in emergency"
6. Click "Save Issue"

EXPECTED RESULT:
- Issue created successfully
- IssueNumber generated
- Issue status = "Open"
- ReportedBy = current user
- ReportedDate = current date
- AuditId = null (independent issue)
- Issue appears in location issue list
- Issue appears in system-wide issue list

PASS/FAIL CRITERIA:
[ ] Issue form accessible
[ ] Issue saved successfully
[ ] IssueNumber generated
[ ] Status set to "Open"
[ ] Issue appears in lists
[ ] Can be linked to audit later
```

#### TC-IM-003: Assign Issue to User

```
ID: TC-IM-003
Title: Assign Open Issue to Responsible User
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that issues can be assigned to specific users.

PREREQUISITES:
- Issue with Status = "Open" exists
- Issue not yet assigned
- On issue detail view

TEST STEPS:
1. Click "Edit" or "Assign" button on open issue
2. Verify assignment section appears
3. Click "Assigned To" field
4. Verify list of users appears
5. Select "John Smith (NUM)" to assign
6. Verify "Assigned Date" auto-populated to today
7. Verify "Assigned By" shows current user
8. Click "Save" button
9. Verify status automatically changes to "Assigned"
10. Verify issue now appears in "John Smith's Issues"

EXPECTED RESULT:
- Issue assigned to selected user
- AssignedTo = "John Smith (NUM)"
- AssignedDate = current date
- AssignedBy = current user
- Status changes to "Assigned" automatically
- Issue no longer in "Unassigned" queue
- Assignee notified (if notifications enabled)
- Issue appears in assignee's personal list

PASS/FAIL CRITERIA:
[ ] Assignment successful
[ ] Assignee populated
[ ] Date and user tracked
[ ] Status updated automatically
[ ] Issue visible to assignee
[ ] Audit trail recorded
```

#### TC-IM-004: Add Corrective Action to Issue

```
ID: TC-IM-004
Title: Add Corrective Action to Issue
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that users can record corrective actions taken to resolve issues.

PREREQUISITES:
- Issue with Status = "Assigned" or "In_Progress"
- On issue detail view
- Action has been or will be taken

TEST STEPS:
1. Scroll to "Corrective Actions" section
2. Click "Add Action" button
3. Verify action form appears with fields:
   - Action Type (dropdown)
   - Description (text area)
   - Action Taken By (user field)
   - Action Date (date field)
   - Evidence/Photo (optional)
4. Fill form:
   - Action Type: "Immediate Fix"
   - Description: "Replaced 2 expired adrenaline ampoules from ward emergency stock"
   - Action Taken By: "Jane Doe (Nurse Manager)"
   - Action Date: Today
5. Click "Save Action"
6. Verify action appears in timeline

EXPECTED RESULT:
- Action form appears
- Action saved successfully
- ActionNumber assigned (sequence 1, 2, 3...)
- Action appears in timeline under issue
- Issue status can advance to "In_Progress"
- Action tracked with date and user
- Multiple actions can be added to one issue
- Actions displayed in reverse chronological order (newest first)

PASS/FAIL CRITERIA:
[ ] Action form accessible
[ ] Action saved successfully
[ ] Action number assigned
[ ] Timeline updated
[ ] Multiple actions supported
[ ] Action history preserved
```

#### TC-IM-005: Change Issue Status - Workflow Progression

```
ID: TC-IM-005
Title: Progress Issue Through Status Workflow
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that issues follow proper state machine workflow through resolution.

PREREQUISITES:
- Issue in system with Status = "Open"
- On issue detail view

TEST STEPS:
1. Start with Status = "Open"
2. Click "Assign Issue" and assign to NUM
3. Verify Status = "Assigned"
4. Add corrective action
5. Click "Mark In Progress" button
6. Verify Status = "In_Progress"
7. Add additional corrective action
8. Click "Mark Ready for Verification" button
9. Verify Status = "Pending_Verification"
10. Verify different user can now verify
11. As verifying user, click "Verify Resolved"
12. Verify Status = "Resolved"
13. As admin, click "Close Issue"
14. Verify Status = "Closed"

EXPECTED RESULT:
- Status transitions follow proper workflow
- Each transition recorded with timestamp and user
- StatusChangedDate and StatusChangedBy updated
- Cannot skip transitions (e.g., cannot go from Open directly to Closed)
- Issue timeline shows all status changes
- Workflow enforced at system level

PASS/FAIL CRITERIA:
[ ] Status workflow enforced
[ ] Transitions recorded
[ ] Cannot skip workflow steps
[ ] Timeline shows all changes
[ ] Proper user roles required
[ ] Audit trail complete
```

#### TC-IM-006: Reopen Issue - Verification Failed

```
ID: TC-IM-006
Title: Reopen Issue When Verification Fails
Module: Issue Management
Priority: Medium

OBJECTIVE:
Verify that resolved issues can be reopened if verification fails.

PREREQUISITES:
- Issue with Status = "Pending_Verification"
- Verifier determines action ineffective

TEST STEPS:
1. As verifier, click "Verification Failed"
2. Verify "Reason for Reopening" text field appears
3. Enter reason: "Adrenaline count still only 4 units. Pharmacy delivery delayed."
4. Click "Reopen Issue"
5. Verify Status returns to "In_Progress"
6. Verify ReopenCount increments (now shows "reopened 1 time")
7. Verify issue timestamp resets for urgent action
8. New corrective action can be added

EXPECTED RESULT:
- Issue returned to "In_Progress" status
- ReopenCount incremented
- Reopen reason recorded
- Reopen timestamp and user recorded
- Issue escalated for faster resolution
- Original corrective actions preserved in history
- New actions can be added

PASS/FAIL CRITERIA:
[ ] Issue reopens successfully
[ ] Status set to "In_Progress"
[ ] ReopenCount incremented
[ ] Reason recorded
[ ] Escalation triggered
[ ] History preserved
```

#### TC-IM-007: Escalate Overdue Issue

```
ID: TC-IM-007
Title: Escalate Issue That Exceeds Target Resolution Date
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that issues can be escalated when approaching or exceeding target resolution date.

PREREQUISITES:
- Issue created 7 days ago with "High" severity
- Target resolution date = 7 days (already past)
- Auto-escalation rule should trigger

TEST STEPS:
1. Verify issue with overdue target date shows escalation indicator
2. Verify Status shows as "Escalated" (auto-escalation)
3. Click "Escalate Issue" to manually escalate
4. Verify escalation form appears
5. Select EscalatedTo: "MERT Nurse Educator"
6. Enter escalation reason: "Resolution exceeds target date"
7. Click "Escalate"

EXPECTED RESULT:
- Escalation flag set on issue
- EscalationLevel incremented
- EscalatedTo user assigned
- Status reflects escalation (may stay In_Progress but flag escalated)
- Issue appears in escalation queue
- Senior users notified for attention
- Issue timestamp priority increased
- Historical escalations tracked

PASS/FAIL CRITERIA:
[ ] Escalation recorded
[ ] Senior user assigned
[ ] Issue prioritized
[ ] Notification sent
[ ] Escalation history tracked
```

#### TC-IM-008: Issue Comments and Communication

```
ID: TC-IM-008
Title: Add Comments to Issue for Team Communication
Module: Issue Management
Priority: Medium

OBJECTIVE:
Verify that team members can add comments to issues for coordination.

PREREQUISITES:
- Issue open in detail view
- Multiple team members working on issue

TEST STEPS:
1. Scroll to "Comments" section
2. Click "Add Comment" button
3. Enter comment: "Pharmacy confirmed delivery today by 2pm"
4. Click "Add Comment"
5. Verify comment appears with:
   - Timestamp
   - User name
   - Comment text
6. Add another comment: "@MERT_Educator: Please verify when stock received"
7. Verify @mention captures user name
8. Return to issue detail
9. Verify all comments in chronological order

EXPECTED RESULT:
- Comment saved successfully
- Comment timestamps accurate
- User attribution correct
- Comments appear in issue detail
- @mentions captured (used for notifications)
- Comments thread preserved
- Internal vs. external comments tracked (if applicable)
- Comments sorted by date (newest last or newest first per config)

PASS/FAIL CRITERIA:
[ ] Comments save successfully
[ ] Timestamps accurate
[ ] User attribution correct
[ ] Comments visible to all
[ ] @mentions functional
[ ] Thread preserved
```

#### TC-IM-009: Link Issue to Follow-up Audit

```
ID: TC-IM-009
Title: Link Issue Resolution to Follow-up Audit
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that resolved issues can be linked to the follow-up audit that verified resolution.

PREREQUISITES:
- Issue in "Resolved" status
- Follow-up audit completed for same location
- On issue detail view

TEST STEPS:
1. Verify issue shows as "Resolved" (action taken and verified)
2. Click "Link Follow-up Audit" button
3. Verify list of audits for same location appears
4. Select follow-up audit that verified resolution
5. Click "Link"
6. Verify LinkedFollowUpAuditId populated
7. Verify issue detail shows linked audit with link to full audit
8. Navigate to linked audit
9. Verify audit shows as follow-up for this issue

EXPECTED RESULT:
- Follow-up audit selected and linked
- LinkedFollowUpAuditId stored
- Audit link appears in issue detail
- Audit shows linked issue in its detail
- Two-way relationship established
- Reporting can show issue resolution cycle
- Closure verified through follow-up audit

PASS/FAIL CRITERIA:
[ ] Audit selection available
[ ] Link created successfully
[ ] Both directions show link
[ ] Link can be removed if needed
[ ] Reporting shows relationship
```

#### TC-IM-010: Issue List - Filter and Search

```
ID: TC-IM-010
Title: Filter and Search Issue List
Module: Issue Management
Priority: High

OBJECTIVE:
Verify that issue lists can be filtered by various criteria for management.

PREREQUISITES:
- Multiple issues exist in system with various statuses and severities
- On Issue List view

TEST STEPS:
1. Verify issue list shows all open and in-progress issues
2. Click "Filter" button
3. Apply filter: Status = "Open"
4. Verify list shows only "Open" issues
5. Add filter: Severity = "Critical"
6. Verify list shows only "Open" AND "Critical" issues
7. Clear filters
8. Use search box: Enter "adrenaline"
9. Verify list shows only issues with "adrenaline" in title or description
10. Combine search + filter: Search "adrenaline" with Status = "Pending_Verification"

EXPECTED RESULT:
- Filter dropdowns appear for Status, Severity, Category
- Single and multiple filters work correctly (AND logic)
- Search filters across title, description, equipment
- Search is case-insensitive
- Filters persist until cleared
- Count of matching issues displayed
- Performance acceptable for large lists

PASS/FAIL CRITERIA:
[ ] Single filters work
[ ] Multiple filters work (AND)
[ ] Search functional
[ ] Search case-insensitive
[ ] Results accurate
[ ] Performance acceptable
```

---

### Task 4.3.5: Random Selection Test Cases (10+ cases)

Random selection algorithm ensures fair audit coverage prioritizing long-overdue trolleys. These tests validate algorithm correctness and data integrity.

#### TC-RS-001: Generate Weekly Random Selection

```
ID: TC-RS-001
Title: Generate Weekly Random Audit Selection
Module: Random Selection
Priority: Critical

OBJECTIVE:
Verify that system correctly generates random selection of 10 trolleys for the week.

PREREQUISITES:
- User is logged in as MERT_Educator role
- Current week is defined (Monday-Sunday)
- 76 active trolleys exist in system
- On Random Selection admin screen

TEST STEPS:
1. Verify current week displayed (Monday date to Sunday date)
2. Verify previous week's selection shown (if exists)
3. Click "Generate New Selection" button
4. Verify algorithm runs and completes (30-60 seconds)
5. Verify new selection displayed with:
   - 10 trolley locations
   - SelectionRank (1-10)
   - DaysSinceAudit values
   - PriorityScore values
6. Verify list sorted by PriorityScore (highest first)
7. Verify selection shows spread across service lines
8. Verify each trolley appears only once in selection

EXPECTED RESULT:
- Exactly 10 trolleys selected
- Selection includes high-priority trolleys (6+ months since audit)
- Selection includes some medium-priority trolleys
- Service line diversity represented
- No duplicates in selection
- RandomAuditSelection record created
- RandomAuditSelectionItem records created (10 items)
- Timestamp and user attribution recorded

PASS/FAIL CRITERIA:
[ ] Exactly 10 trolleys selected
[ ] Highest priority trolleys included
[ ] Service line spread achieved
[ ] No duplicates
[ ] Records created in SharePoint
[ ] Timestamp accurate
[ ] Algorithm completed successfully
```

#### TC-RS-002: Verify Priority Score Calculation

```
ID: TC-RS-002
Title: Verify Priority Score Calculation for Random Selection
Module: Random Selection
Priority: High

OBJECTIVE:
Verify that priority scores are calculated correctly per algorithm business logic.

PREREQUISITES:
- Random selection generated
- On Random Selection admin screen with selection displayed

TEST STEPS:
1. Note trolleys with DaysSinceAudit values:
   - Trolley A: Never audited (NULL LastAuditDate) → Should have score 1000
   - Trolley B: 400 days since audit → Should have score 500+400=900
   - Trolley C: 150 days since audit → Should have score 200+150=350
   - Trolley D: 45 days since audit → Should have score 45
2. Verify PriorityScore values match expected calculations
3. Verify selection algorithm prioritized higher scores
4. Verify trolleys with no audits always selected first (if available)

EXPECTED RESULT:
- Priority scores calculated per algorithm:
  - NULL LastAuditDate: 1000 (highest)
  - 365+ days: 500 + DaysSinceLastAudit
  - 180-364 days: 200 + DaysSinceLastAudit
  - <180 days: DaysSinceLastAudit
- High-priority trolleys appear first in selection
- Algorithm prioritizes audit coverage for under-audited trolleys
- Calculation results match documented algorithm

PASS/FAIL CRITERIA:
[ ] Priority scores accurate
[ ] Calculation matches algorithm
[ ] Never-audited trolleys highest priority
[ ] 6+ month trolleys prioritized
[ ] Selection results correct
```

#### TC-RS-003: Random Selection Excludes Recently Audited

```
ID: TC-RS-003
Title: Verify Selection Excludes Recently Audited Trolleys
Module: Random Selection
Priority: High

OBJECTIVE:
Verify that algorithm excludes trolleys audited within last 30 days.

PREREQUISITES:
- Random selection generated
- Some trolleys audited within last 30 days
- On Random Selection admin screen

TEST STEPS:
1. Review trolleys in system with audits within last 30 days
2. Verify none of these trolleys appear in current week's selection
3. Exception: If trolley has never been audited, should still be included
4. Verify trolley audited exactly 31 days ago IS included in selection
5. Verify trolley audited exactly 29 days ago NOT included in selection

EXPECTED RESULT:
- Trolleys audited in last 30 days excluded from selection
- 30-day window strictly enforced
- Never-audited trolleys still included (even if theoretically "recently" added)
- Algorithm prevents audit fatigue on same locations
- Ensures spread of audit effort across system

PASS/FAIL CRITERIA:
[ ] Recently audited excluded (< 30 days)
[ ] 31+ days included
[ ] Never-audited included
[ ] 30-day threshold precise
```

#### TC-RS-004: Random Selection - Service Line Distribution

```
ID: TC-RS-004
Title: Verify Service Line Distribution in Selection
Module: Random Selection
Priority: Medium

OBJECTIVE:
Verify that selection algorithm distributes selections across service lines fairly.

PREREQUISITES:
- Random selection generated
- On Random Selection admin screen

TEST STEPS:
1. List 10 selected trolleys with their service lines
2. Count how many from each service line:
   - Critical Care: [count]
   - Emergency Medicine: [count]
   - Paediatrics: [count]
   - [Other service lines]
3. Compare to total trolley distribution:
   - Critical Care has ~25 trolleys → Should have ~3-4 in selection
   - Smaller service lines should have at least 1
4. Verify no service line has 0 selections if it has trolleys needing audit

EXPECTED RESULT:
- Service line distribution roughly proportional to trolley count
- Smaller service lines represented (if they have high-priority trolleys)
- No service line overwhelmingly selected unless others have no eligible trolleys
- Distribution appears fair and unbiased
- Selection ensures comprehensive campus coverage

PASS/FAIL CRITERIA:
[ ] Service line distribution fair
[ ] Proportional representation achieved
[ ] No service line ignored
[ ] Algorithm balances priority and distribution
```

#### TC-RS-005: Mark Selection Item as Completed

```
ID: TC-RS-005
Title: Mark Random Selection Item as Completed
Module: Random Selection
Priority: High

OBJECTIVE:
Verify that auditors can mark selected trolley audits as completed.

PREREQUISITES:
- Random selection active for current week
- Audit completed for one of selected trolleys
- On Random Selection view

TEST STEPS:
1. Verify random selection shows 10 trolleys with AuditStatus
2. For completed audit, click trolley in selection
3. Verify AuditStatus changes to "Completed"
4. Verify link to completed audit appears
5. Verify selection progress updates (e.g., "2/10 completed")
6. Verify completed trolley can be seen in selection list

EXPECTED RESULT:
- AuditStatus updated to "Completed"
- AuditId linked to audit record
- Completion timestamp recorded
- Progress indicator updated
- Completed status persists
- Cannot re-audit completed selection item (or creates new entry)

PASS/FAIL CRITERIA:
[ ] Status updated to Completed
[ ] Audit linked
[ ] Progress updated
[ ] Status persists
```

#### TC-RS-006: Handle Skipped Selection Item

```
ID: TC-RS-006
Title: Mark Selection Item as Skipped
Module: Random Selection
Priority: Medium

OBJECTIVE:
Verify that selection items can be marked as skipped with reason.

PREREQUISITES:
- Random selection active
- Trolley cannot be audited this week (e.g., location closed)
- On Random Selection view

TEST STEPS:
1. Click on selection item to mark as skipped
2. Verify skip form appears with "Skip Reason" field
3. Select reason: "Location temporarily closed for renovation"
4. Click "Skip"
5. Verify AuditStatus = "Skipped"
6. Verify SkipReason recorded
7. Verify trolley excluded from weekly audit requirement
8. Note that trolley will be re-selected in future weeks

EXPECTED RESULT:
- Selection item marked as Skipped
- Skip reason recorded
- Trolley removed from active selection
- Trolley remains eligible for future selections
- Skip reason appears in report

PASS/FAIL CRITERIA:
[ ] Skip recorded successfully
[ ] Reason captured
[ ] Trolley excluded from weekly count
[ ] Skip reason visible
```

#### TC-RS-007: Random Selection Auto-Generation Schedule

```
ID: TC-RS-007
Title: Verify Random Selection Auto-Generates Weekly
Module: Random Selection
Priority: Medium

OBJECTIVE:
Verify that system automatically generates new selection every Monday.

PREREQUISITES:
- Power Automate flow for weekly generation configured
- Current day is Sunday or before Monday auto-run time

TEST STEPS:
1. Note current date/time
2. Wait until Monday 6:00 AM (or configured time)
3. Check Random Selection screen for new selection
4. Verify selection generated automatically (not manually)
5. Verify GeneratedBy = "System"
6. Verify GeneratedDate shows Monday 6:00 AM
7. Verify previous week's selection marked as inactive

EXPECTED RESULT:
- New selection appears on schedule (weekly)
- Auto-generation timestamp recorded
- GeneratedBy field shows "System"
- Previous week marked inactive
- Selection automatically available to auditors
- No manual intervention required

PASS/FAIL CRITERIA:
[ ] Auto-generation triggered on schedule
[ ] Selection created automatically
[ ] Timestamp accurate
[ ] System attribution recorded
[ ] Previous week marked inactive
```

#### TC-RS-008: Random Selection Recalculation After Audit

```
ID: TC-RS-008
Title: Verify Location Priority Recalculated After Audit Submission
Module: Random Selection
Priority: High

OBJECTIVE:
Verify that trolley priority scores recalculate when audit is submitted.

PREREQUISITES:
- Trolley "ICU Pod 1" in current week's selection
- LastAuditDate = 180 days ago (high priority)
- Audit just submitted for this trolley

TEST STEPS:
1. Verify trolley had high priority before audit (PriorityScore > 350)
2. Submit new audit for trolley
3. Verify Location.LastAuditDate updated to today
4. Verify Location.DaysSinceLastAudit recalculated to 0
5. Verify Location.AuditPriorityScore recalculated to 0
6. Verify trolley moves to low priority
7. In next week's selection generation, verify this trolley has low priority

EXPECTED RESULT:
- Priority scores recalculated immediately after audit
- Trolley moves to low priority
- Next week's selection excludes trolley (recently audited)
- Algorithm correctly reflects audit completion

PASS/FAIL CRITERIA:
[ ] Priority recalculated after audit
[ ] LastAuditDate updated
[ ] DaysSinceLastAudit recalculated
[ ] Priority score drops
[ ] Next selection excludes trolley
```

---

### Task 4.3.6: Reporting Test Cases (10+ cases)

Reporting validates Power BI dashboards, data accuracy, and analytics functionality.

#### TC-RP-001: Compliance Dashboard - KPI Calculations

```
ID: TC-RP-001
Title: Verify Compliance Dashboard KPI Calculations Accuracy
Module: Reporting
Priority: Critical

OBJECTIVE:
Verify that dashboard KPIs calculate correctly and reflect system data.

PREREQUISITES:
- Power BI dashboard published
- Test data with known values in SharePoint lists
- On Power BI Compliance Dashboard

TEST STEPS:
1. Navigate to Compliance Dashboard
2. Verify four KPI cards display:
   - Audit Completion Rate: [percentage]
   - Average Compliance Score: [percentage]
   - Open Issues Count: [number]
   - Trolleys >6 Months Since Audit: [number]
3. Manually calculate expected values:
   - Count audits submitted this period / active trolleys
   - Average all OverallCompliance scores
   - Count issues where Status not "Closed"
   - Count locations where DaysSinceLastAudit > 180
4. Compare dashboard values to manual calculations
5. Verify within acceptable tolerance (±0.5%)

EXPECTED RESULT:
- Audit Completion Rate accurate
- Average Compliance Score reflects all audits
- Open Issues count matches active issues
- Over-6-month count correct
- All values refresh when new data added
- Performance acceptable (dashboard loads < 5 seconds)

PASS/FAIL CRITERIA:
[ ] KPI values accurate
[ ] Calculations match business logic
[ ] Within tolerance (±0.5%)
[ ] Refresh works correctly
[ ] Performance acceptable
```

#### TC-RP-002: This Week's Audits Widget

```
ID: TC-RP-002
Title: Verify This Week's Audits Widget Shows Current Selection
Module: Reporting
Priority: High

OBJECTIVE:
Verify that dashboard widget displays current week's random selection with status.

PREREQUISITES:
- Current week's random selection exists
- Some audits completed, some pending
- On dashboard

TEST STEPS:
1. Locate "This Week's Audits" widget
2. Verify list shows 10 trolleys from current selection
3. For each trolley, verify displays:
   - Rank (1-10)
   - Location name
   - Audit status (Pending, Completed, Skipped)
4. Verify completed audits show checkmark or green status
5. Verify pending audits show progress indicator
6. Click on trolley to navigate to detail
7. Verify progress bar: "3 / 10 completed"

EXPECTED RESULT:
- Widget shows current week's selection
- Status accurately reflects audit state
- Progress tracked and displayed
- All 10 items from selection visible
- Interactive drill-down available
- Auto-refreshes when audits completed

PASS/FAIL CRITERIA:
[ ] All 10 items displayed
[ ] Status accurate
[ ] Progress bar correct
[ ] Drill-down functional
[ ] Auto-refresh working
```

#### TC-RP-003: Compliance Trend Chart

```
ID: TC-RP-003
Title: Verify Compliance Trend Chart - Historical Data
Module: Reporting
Priority: High

OBJECTIVE:
Verify that compliance trend chart displays historical compliance scores over time.

PREREQUISITES:
- Historical audit data with multiple entries per month
- On Power BI dashboard or trend report

TEST STEPS:
1. Navigate to trend report
2. Verify chart displays last 12 months
3. X-axis shows months (Jan, Feb, Mar, etc.)
4. Y-axis shows compliance percentage (0-100%)
5. Each month shows average compliance score
6. Verify line chart shows trend (generally increasing or stable)
7. Hover over data point to see exact value and date range
8. Filter by service line: "Critical Care"
9. Verify chart updates to show only Critical Care trend

EXPECTED RESULT:
- Chart displays historical compliance data
- Trend accurately reflects audit scores
- Filtering by service line works
- Visual trend clear and interpretable
- Hover details available
- Data source accurate (from Audit list)

PASS/FAIL CRITERIA:
[ ] Trend chart displays correctly
[ ] Data accurate
[ ] Filtering works
[ ] Visual clear
[ ] Hover details available
```

#### TC-RP-004: Issue Status Distribution Chart

```
ID: TC-RP-004
Title: Verify Issue Distribution by Status and Severity
Module: Reporting
Priority: High

OBJECTIVE:
Verify that issue reports show breakdown by status and severity.

PREREQUISITES:
- Multiple issues exist with various statuses and severities
- On issue reporting view

TEST STEPS:
1. Navigate to Issue Status report
2. Verify pie chart showing issue distribution by status:
   - Open: [number and %]
   - Assigned: [number and %]
   - In Progress: [number and %]
   - Pending Verification: [number and %]
   - Resolved: [number and %]
   - Closed: [number and %]
3. Verify totals add up to total issues in system
4. Navigate to Severity report
5. Verify stacked bar chart showing issues by severity:
   - Critical: [count]
   - High: [count]
   - Medium: [count]
   - Low: [count]
6. Filter chart by location "ICU Pod 1"

EXPECTED RESULT:
- Status distribution chart accurate
- Severity distribution accurate
- Charts updateable with filters
- Counts match issue list
- Visual presentation clear

PASS/FAIL CRITERIA:
[ ] Status distribution accurate
[ ] Severity distribution accurate
[ ] Totals correct
[ ] Filtering works
[ ] Visual presentation clear
```

#### TC-RP-005: Equipment Deficiency Report

```
ID: TC-RP-005
Title: Verify Equipment Deficiency Report - Most Missing Items
Module: Reporting
Priority: High

OBJECTIVE:
Verify that report shows which equipment items are most frequently missing.

PREREQUISITES:
- Multiple audits completed with equipment detail records
- On equipment deficiency report

TEST STEPS:
1. Navigate to Equipment Deficiency Report
2. Verify list sorted by frequency of shortage:
   - Item Name | Times Missing | % of Audits
3. Verify top items match known shortages:
   - Adrenaline 1mg: 12 times | 15% of audits
   - Defib pads (spare): 8 times | 10% of audits
   - [Other items]
4. Click on item to drill down to affected locations
5. Verify shows which trolleys missing this item most frequently

EXPECTED RESULT:
- Deficiency report shows actual missing items
- Sorted by frequency (most common first)
- Percentage calculation accurate
- Drill-down to locations functional
- Can filter by time period, service line
- Useful for procurement planning

PASS/FAIL CRITERIA:
[ ] Report shows correct items
[ ] Sorted by frequency
[ ] Percentages accurate
[ ] Drill-down works
[ ] Filtering available
```

#### TC-RP-006: Trolley History Report

```
ID: TC-RP-006
Title: Verify Trolley History Report - Single Trolley Details
Module: Reporting
Priority: Medium

OBJECTIVE:
Verify that single-trolley report shows complete history.

PREREQUISITES:
- Trolley with multiple audits and issues exists
- On trolley history report

TEST STEPS:
1. Select trolley "ICU Pod 1" for detailed report
2. Verify report displays:
   - Trolley metadata (location, service line, etc.)
   - All audits (newest first)
   - Compliance score trend (chart)
   - All issues (open and closed)
   - Change log (all modifications)
3. Verify audit table shows:
   - Date
   - Type (Comprehensive/Spot Check)
   - Auditor
   - Overall Compliance Score
   - Link to full audit
4. Verify issues table shows:
   - Issue ID
   - Status
   - Days open
   - Link to issue detail
5. Export report to PDF

EXPECTED RESULT:
- Complete trolley history displayed
- All audits and issues shown
- Trend chart shows compliance pattern
- Export to PDF functional
- Formatting professional and readable
- All data accurate

PASS/FAIL CRITERIA:
[ ] Trolley history complete
[ ] All audits displayed
[ ] All issues displayed
[ ] Trend chart accurate
[ ] Export functional
[ ] Formatting professional
```

#### TC-RP-007: Service Line Comparison Report

```
ID: TC-RP-007
Title: Verify Service Line Comparison Report
Module: Reporting
Priority: High

OBJECTIVE:
Verify that report compares compliance and performance across service lines.

PREREQUISITES:
- Audits completed for trolleys across all service lines
- On service line comparison report

TEST STEPS:
1. Navigate to Service Line Comparison
2. Verify bar chart showing average compliance by service line:
   - Critical Care: 88%
   - Emergency: 92%
   - Paediatrics: 85%
   - Surgery: 90%
   - [Others]
3. Verify table showing:
   - Service Line | Trolley Count | Audits Completed | Avg Compliance | Open Issues
4. Identify highest and lowest performing service lines
5. Click on service line to drill down to location details

EXPECTED RESULT:
- Comparison shows relative performance
- Identifies high and low performers
- Data accurate and complete
- Drill-down available
- Can be used for service line accountability
- Professional presentation

PASS/FAIL CRITERIA:
[ ] Comparison accurate
[ ] All service lines included
[ ] Drill-down functional
[ ] Data complete
[ ] Professional format
```

#### TC-RP-008: Overdue Audits Report

```
ID: TC-RP-008
Title: Verify Overdue Audits Report - Trolleys Past Due
Module: Reporting
Priority: High

OBJECTIVE:
Verify that report identifies trolleys overdue for audit.

PREREQUISITES:
- Trolleys with audits past 365 days exist
- On overdue audits report

TEST STEPS:
1. Navigate to Overdue Audits Report
2. Verify list shows trolleys where DaysSinceLastAudit > [threshold]
3. Verify columns:
   - Location | Days Since Audit | Last Audit Date | Compliance | Service Line
4. Verify sorted by days overdue (most overdue first)
5. Verify count matches manual calculation
6. Filter by service line
7. Export to Excel

EXPECTED RESULT:
- Report shows overdue trolleys
- Sorted correctly
- Days calculation accurate
- Last audit date correct
- Filtering works
- Export functional

PASS/FAIL CRITERIA:
[ ] Overdue trolleys identified
[ ] Sorted correctly
[ ] Days calculation accurate
[ ] Filtering works
[ ] Export works
```

#### TC-RP-009: Power BI Data Refresh

```
ID: TC-RP-009
Title: Verify Power BI Datasets Refresh on Schedule
Module: Reporting
Priority: Medium

OBJECTIVE:
Verify that Power BI datasets refresh at configured schedule to keep reports current.

PREREQUISITES:
- Power BI workspace configured
- Refresh schedule set (daily)
- On Power BI admin portal or dashboard

TEST STEPS:
1. Verify Power BI refresh history in admin portal
2. Note last refresh time
3. Add new test audit to SharePoint
4. Wait for next scheduled refresh (or manual refresh)
5. Verify Power BI datasets refresh completed successfully
6. Navigate to dashboard
7. Verify new audit appears in relevant reports
8. Verify no refresh errors in admin logs

EXPECTED RESULT:
- Datasets refresh on schedule (daily or configured frequency)
- Refresh completes successfully (no errors)
- New data appears in reports within refresh window
- Refresh history tracked
- Performance acceptable

PASS/FAIL CRITERIA:
[ ] Refresh scheduled correctly
[ ] Refresh completes successfully
[ ] New data appears
[ ] No errors in logs
[ ] Performance acceptable
```

#### TC-RP-010: Report Filtering and Drill-Down

```
ID: TC-RP-010
Title: Verify Report Filtering and Drill-Down Navigation
Module: Reporting
Priority: Medium

OBJECTIVE:
Verify that reports support interactive filtering and drill-down.

PREREQUISITES:
- Reports deployed with slicers and drill-through
- On Power BI dashboard

TEST STEPS:
1. Navigate to main compliance dashboard
2. Verify filter slicers available at top:
   - Service Line
   - Building
   - Date Range
3. Filter by Service Line = "Critical Care"
4. Verify all KPIs and charts update to show only Critical Care data
5. Click on specific trolley in chart
6. Verify drill-through to trolley detail report
7. Verify trolley detail shows filtered data
8. Back button returns to main dashboard

EXPECTED RESULT:
- Filter slicers available and functional
- Filters apply correctly across all visuals
- Drill-through navigates to detail views
- Back navigation works
- All visuals update together
- Performance acceptable

PASS/FAIL CRITERIA:
[ ] Filters functional
[ ] Filters apply correctly
[ ] Drill-through works
[ ] Back navigation works
[ ] Performance acceptable
```

---

## Part 3: Defect Tracking and Management

### Task 4.3.7-4.3.8: UAT Schedule and Defect Tracking

#### UAT Schedule and Participants

```
UAT PHASE SCHEDULE

Week 1: UAT Kickoff and Light Functional Testing
├─ Day 1 (Monday): UAT Kickoff Meeting
│  ├─ 9:00 AM: Meet with business team
│  ├─ Overview of testing approach
│  ├─ Environment walkthrough
│  └─ Test case review
├─ Day 2-3: Self-directed exploratory testing
│  └─ Users test familiar workflows
├─ Day 4-5: Guided functional testing
│  ├─ Trolley management operations
│  ├─ Basic audit entry workflow
│  └─ Issue creation and tracking

Week 2: Intensive Functional Testing
├─ Day 1-2: Audit workflow complete cycles
├─ Day 3: Random selection verification
├─ Day 4-5: Dashboard and reporting validation

Week 3: Edge Cases and Error Handling
├─ Day 1-2: Exploratory testing of edge cases
├─ Day 3: Performance and load testing
├─ Day 4-5: Integration testing (multiple users, overlapping actions)

Week 4: Defect Resolution and Sign-Off
├─ Day 1-3: Verify defect fixes
├─ Day 4: Final functionality check
├─ Day 5: Sign-off meeting and approval

UAT PARTICIPANTS

Primary Testers:
├─ MERT Nurse Educators (2-3 staff)
│  ├─ Test trolley management
│  ├─ Test admin functions
│  └─ Full system authority
├─ Nurse Unit Managers (2-3 staff)
│  ├─ Test issue management
│  ├─ Test assignment workflow
│  └─ Service line perspectives
├─ Clinical Auditors (2-4 staff)
│  ├─ Test complete audit workflow
│  ├─ Test data entry accuracy
│  └─ Real-world usage patterns
└─ Leadership (1-2 staff)
   ├─ Review dashboards
   └─ Verify reporting accuracy

Supporting Team:
├─ Project Lead - Coordinates UAT activities
├─ QA Lead - Supports test execution, logs issues
├─ Developer - Available for issues requiring code fixes
└─ IT Support - Manages access, environment issues
```

#### Defect Severity Classification

```
SEVERITY LEVELS

CRITICAL (P0)
├─ Definition: System cannot function, data loss risk, security breach
├─ Examples:
│  ├─ App crashes or won't load
│  ├─ Audit data not saving to SharePoint
│  ├─ Permission checks failing (non-MERT users seeing admin functions)
│  ├─ Compliance score calculation incorrect by >5%
│  └─ Cannot navigate between screens
├─ SLA: Fix within 4 business hours
└─ Must block go-live if open

HIGH (P1)
├─ Definition: Major feature not working, workaround exists but difficult
├─ Examples:
│  ├─ Equipment checklist doesn't filter by trolley type correctly
│  ├─ Issue status workflow states skipped
│  ├─ Random selection algorithm excludes entire service line
│  ├─ Dashboard refresh delayed >1 hour
│  └─ Date formatting incorrect in reports
├─ SLA: Fix within 8 business hours
└─ May delay go-live if not resolved

MEDIUM (P2)
├─ Definition: Feature working but suboptimal, minor user friction
├─ Examples:
│  ├─ Form validation error messages unclear
│  ├─ Dropdown takes >2 seconds to load
│  ├─ Column headers in list misaligned
│  ├─ Report export missing minor formatting
│  └─ Notification text has typo
├─ SLA: Fix within 2-3 business days
└─ Acceptable to proceed with plan to fix

LOW (P3)
├─ Definition: Cosmetic issue, documentation, future improvement
├─ Examples:
│  ├─ Label capitalization inconsistent
│  ├─ Button color slightly off brand
│  ├─ Help text missing
│  ├─ Report includes extra blank page on export
│  └─ Legend order on chart suboptimal
├─ SLA: Fix in next release (post-launch)
└─ Always acceptable to defer

DEFECT PRIORITY MATRIX

Priority = Impact × Likelihood × Scope

Where:
- Impact: How severe if defect occurs (1-10)
- Likelihood: How often encountered (1-10)
- Scope: How many users/workflows affected (1-10)

Score >= 500: CRITICAL
Score 250-499: HIGH
Score 100-249: MEDIUM
Score < 100: LOW
```

#### Defect Tracking Template

```
DEFECT TRACKING FORM

ID: [Auto-generated, e.g., BUG-2024-0001]
Title: [Concise description of issue]
Severity: [Critical / High / Medium / Low]
Priority: [P0 / P1 / P2 / P3]
Status: [Open / Assigned / In Progress / Fixed / Testing / Closed / Deferred]
Component: [PowerApp / SharePoint / Power Automate / Power BI / Other]

REPORTED BY
├─ Name: [Tester name]
├─ Role: [MERT / NUM / Auditor / etc.]
└─ Date: [Report date]

DESCRIPTION
├─ Summary: [One-sentence summary]
├─ Steps to Reproduce:
│  1. [Step 1]
│  2. [Step 2]
│  └─ [Continue as needed]
├─ Expected Result: [What should happen]
└─ Actual Result: [What actually happens]

ENVIRONMENT
├─ Browser: [Chrome / Edge / Safari / etc.]
├─ Device: [Desktop / Tablet / Phone]
├─ SharePoint Tenant: [Test / Production]
└─ App Version: [Version number]

ATTACHED EVIDENCE
├─ Screenshot: [Yes / No]
├─ Video/Recording: [Yes / No]
├─ Error Message: [Full text if applicable]
└─ Console Log: [Yes / No]

ASSIGNMENT
├─ Assigned To: [Developer name]
├─ Assigned Date: [Date]
└─ Target Fix Date: [Date]

RESOLUTION
├─ Root Cause: [Technical analysis]
├─ Fix Description: [What code changed]
├─ Fixed By: [Developer name]
├─ Fixed Date: [Date]
└─ Fix Verified By: [QA name]

CLOSURE
├─ Status: [Closed]
├─ Closed By: [Name]
├─ Closed Date: [Date]
└─ Notes: [Any follow-up items]

METRICS
├─ Days Open: [Calculated]
├─ Resolution Time: [Calculated]
└─ Reopened: [Yes / No]
```

---

### Task 4.3.9: Defect Resolution and Regression Testing

#### Defect Resolution Workflow

```
DEFECT LIFECYCLE

1. REPORT
   ├─ Tester discovers issue
   ├─ Completes defect form
   ├─ Status: OPEN
   └─ Severity determined

2. TRIAGE
   ├─ QA lead reviews defect
   ├─ Validates reproduction
   ├─ Assigns priority
   ├─ Status: ASSIGNED (if needs fix) or CLOSED (if not a defect)
   └─ If ASSIGNED, developer notified

3. INVESTIGATION
   ├─ Developer analyzes root cause
   ├─ Identifies affected components
   ├─ Estimates fix effort
   ├─ Status: IN_PROGRESS
   └─ May ask for clarification from reporter

4. FIX DEVELOPMENT
   ├─ Developer implements fix
   ├─ Code reviewed by lead
   ├─ Fix deployed to test environment
   ├─ Status: FIXED (code changes complete)
   └─ QA notified to verify

5. VERIFICATION
   ├─ QA tests fix in test environment
   ├─ Steps to reproduce executed again
   ├─ Verifies expected result now occurs
   ├─ Checks for side effects
   ├─ Status: TESTING
   ├─ If verified: Status = CLOSED
   └─ If still broken: Status = REOPENED (return to Investigation)

6. REGRESSION TESTING
   ├─ Related test cases re-run
   ├─ Verify fix didn't break other functionality
   ├─ Sanity check of affected module
   └─ Sign-off on stability

7. CLOSURE
   ├─ Status: CLOSED
   ├─ Closed date recorded
   ├─ Notes on resolution
   └─ Added to release notes
```

#### Regression Testing Protocol

```
REGRESSION TEST CASES

When defect is fixed, re-run these related test cases:

Equipment-Related Fix:
├─ TC-AE-007 (Equipment Check - Dynamic Checklist)
├─ TC-AE-008 (Equipment Check - Quantity Validation)
├─ TC-AE-009 (Equipment Check - Critical Items)
├─ TC-RP-005 (Equipment Deficiency Report)
└─ TC-RP-004 (Issue Distribution by Equipment)

Issue Management Fix:
├─ TC-IM-001 (Create Issue During Audit)
├─ TC-IM-002 (Create Issue Independently)
├─ TC-IM-005 (Status Workflow Progression)
├─ TC-IM-010 (Issue List - Filter and Search)
└─ TC-RP-004 (Issue Status Distribution)

Random Selection Fix:
├─ TC-RS-001 (Generate Random Selection)
├─ TC-RS-002 (Priority Score Calculation)
├─ TC-RS-003 (Exclude Recently Audited)
├─ TC-RS-004 (Service Line Distribution)
└─ TC-RP-002 (This Week's Audits Widget)

Compliance Score Fix:
├─ TC-AE-010 (Audit Review and Compliance Calculation)
├─ TC-AE-011 (Submit Audit - Save to SharePoint)
├─ TC-RP-001 (Dashboard KPI Calculations)
└─ TC-RP-003 (Compliance Trend Chart)

Dashboard/Reporting Fix:
├─ TC-RP-001 through TC-RP-010 (All reporting tests)
└─ Verify data refresh within 5 minutes

REGRESSION TEST EXECUTION

For each defect fix:
1. Run all related test cases
2. Execute at least 5 smoke test scenarios
3. Verify no new issues introduced
4. Performance acceptable (page loads < 3 sec)
5. All tests pass before deployment to UAT
```

---

### Task 4.3.10: Sign-Off Checklist and Go-Live Criteria

#### Production Readiness Checklist

```
PRE-GO-LIVE VERIFICATION CHECKLIST

FUNCTIONALITY
├─ [ ] All critical functionality working in test environment
├─ [ ] All high-priority defects resolved
├─ [ ] Medium-priority defects either fixed or documented as deferred
├─ [ ] UAT sign-off received from MERT Educators
├─ [ ] UAT sign-off received from Nurse Unit Managers
├─ [ ] UAT sign-off received from Clinical Auditors
├─ [ ] All test cases executed with pass/fail documented
└─ [ ] Regression testing completed after all fixes

DATA INTEGRITY
├─ [ ] Sample audits submitted and verified in SharePoint
├─ [ ] Equipment data complete and correct
├─ [ ] Location master data complete and current
├─ [ ] Compliance score calculations verified for accuracy
├─ [ ] Issue records created with correct relationships
├─ [ ] Audit trail entries created for all changes
├─ [ ] No orphaned records or data inconsistencies
└─ [ ] Historical data migration verified (if applicable)

SECURITY & ACCESS CONTROL
├─ [ ] MERT Educator permissions verified (add/edit/delete trolleys)
├─ [ ] Manager permissions verified (assign/verify issues)
├─ [ ] Auditor permissions verified (conduct audits, create issues)
├─ [ ] Viewer permissions verified (read-only access)
├─ [ ] Non-users cannot access system
├─ [ ] SharePoint list permissions match app security model
├─ [ ] No permission escalation vulnerabilities
└─ [ ] Audit trail shows correct user attribution

PERFORMANCE
├─ [ ] App loads within 3 seconds on typical network
├─ [ ] Trolley dropdown search completes within 1 second
├─ [ ] Audit entry screens navigate smoothly
├─ [ ] Dashboard loads within 5 seconds
├─ [ ] Power BI reports refresh within 1 hour (scheduled)
├─ [ ] No performance degradation during 10+ concurrent users
├─ [ ] Sorting/filtering on lists performs acceptably
└─ [ ] Export to PDF/Excel completes within 30 seconds

DOCUMENTATION
├─ [ ] User guide completed and reviewed
├─ [ ] Administrator guide completed
├─ [ ] Troubleshooting guide available
├─ [ ] Training materials prepared
├─ [ ] System architecture documentation current
├─ [ ] Data dictionary documented
├─ [ ] Support procedures documented
└─ [ ] Release notes prepared

DEPLOYMENT READINESS
├─ [ ] All code merged to main branch
├─ [ ] All Power Automate flows deployed to production tenant
├─ [ ] PowerApp published to production SharePoint
├─ [ ] Power BI datasets configured and initial refresh successful
├─ [ ] SharePoint lists verified in production environment
├─ [ ] Notification configuration tested
├─ [ ] Backup and recovery procedures documented
├─ [ ] Rollback plan prepared if needed

SUPPORT & OPERATIONS
├─ [ ] Support team trained on system and common issues
├─ [ ] Help desk scripts prepared for common questions
├─ [ ] Escalation procedures documented
├─ [ ] On-call support arranged for first week post-launch
├─ [ ] Performance monitoring configured
├─ [ ] Error logging and alerting configured
├─ [ ] Incident response plan activated
└─ [ ] Post-launch review meeting scheduled (1 week, 1 month)
```

#### Sign-Off Meeting Agenda

```
GO-LIVE SIGN-OFF MEETING

Date: [1-2 days before scheduled go-live]
Duration: 1 hour
Location: [Conference room / Teams]

ATTENDEES
├─ Project Sponsor
├─ MERT Nurse Educator Lead
├─ Nurse Unit Manager Representative
├─ IT Director or representative
├─ QA Lead / Test Lead
├─ Developer Lead
└─ Implementation PM

AGENDA

1. TESTING SUMMARY (10 min)
   ├─ Test cases executed: X/X (100%)
   ├─ Critical defects: 0 remaining
   ├─ High defects: 0 remaining
   ├─ Medium defects: [number] deferred to next release
   └─ UAT completion rate: 100%

2. BUSINESS SIGN-OFF (10 min)
   ├─ MERT Educator: "System meets requirements and is ready for launch"
   ├─ NUM Representative: "Issue management workflow acceptable"
   ├─ Auditors: "Audit entry process user-friendly and functional"
   └─ Ask: "Any concerns or issues before go-live?"

3. TECHNICAL SIGN-OFF (10 min)
   ├─ Infrastructure ready for production
   ├─ All integrations tested and functional
   ├─ Performance benchmarks met
   ├─ Security controls verified
   └─ Backup and disaster recovery confirmed

4. RISKS & MITIGATION (5 min)
   ├─ Identified risks reviewed
   ├─ Mitigation strategies confirmed
   ├─ Escalation procedures confirmed
   └─ Rollback plan acknowledged

5. GO/NO-GO DECISION (10 min)
   ├─ Review sign-off checklist: All items green/acceptable
   ├─ Individual sign-offs:
   │  ├─ MERT Educator: ☐ GO / ☐ NO-GO
   │  ├─ NUM Representative: ☐ GO / ☐ NO-GO
   │  ├─ IT Lead: ☐ GO / ☐ NO-GO
   │  ├─ Project Lead: ☐ GO / ☐ NO-GO
   │  └─ Sponsor: ☐ GO / ☐ NO-GO
   ├─ Result: [GO / NO-GO / CONDITIONAL GO]
   ├─ If conditional, list conditions:
   └─ If no-go, reschedule for [date]

6. GO-LIVE COORDINATION (5 min)
   ├─ Go-live date/time confirmed
   ├─ Deployment window discussed
   ├─ Communication plan reviewed
   ├─ Post-launch support confirmed
   └─ Action items assigned
```

#### Go-Live Checklist

```
GO-LIVE DAY CHECKLIST (24 hours before through 24 hours after)

ONE WEEK BEFORE GO-LIVE
├─ [ ] All stakeholders confirm availability on go-live day
├─ [ ] Support team briefing completed
├─ [ ] Rollback plan documented and accessible
├─ [ ] Database backups verified
├─ [ ] Contact list for escalation updated
└─ [ ] Final sanity check in production environment

24 HOURS BEFORE GO-LIVE
├─ [ ] Production environment verification
├─ [ ] All lists and apps deployed and accessible
├─ [ ] Power BI refresh completed
├─ [ ] Initial test data present in production
├─ [ ] Notification flows tested
├─ [ ] Performance baseline established
└─ [ ] Emergency contact numbers confirmed

GO-LIVE DAY - MORNING (2 hours before)
├─ [ ] All team members logged in and ready
├─ [ ] Support team in communication channel
├─ [ ] Help desk briefed on system
├─ [ ] Performance monitoring activated
├─ [ ] Incident log started
└─ [ ] Go/No-Go final decision confirmed

GO-LIVE - DEPLOYMENT
├─ [ ] App published to production tenant
├─ [ ] Power Automate flows activated in production
├─ [ ] Power BI datasets connected to production SharePoint
├─ [ ] Notification system activated
├─ [ ] Access permissions applied
└─ [ ] All integrations verified

GO-LIVE - IMMEDIATE AFTER (1-2 hours)
├─ [ ] Spot check app functionality
├─ [ ] Verify data entry works
├─ [ ] Test critical workflows end-to-end
├─ [ ] Monitor system performance
├─ [ ] Check for error messages in logs
├─ [ ] Verify notifications sending
└─ [ ] Initial user feedback collection

FIRST 24 HOURS POST-GO-LIVE
├─ [ ] Support team monitoring incident log
├─ [ ] Critical issues prioritized and fixed
├─ [ ] User questions documented
├─ [ ] Performance metrics collected
├─ [ ] Hourly status updates to stakeholders
├─ [ ] First audit/issue created and verified
└─ [ ] No critical defects blocking operations

FIRST WEEK POST-GO-LIVE
├─ [ ] Daily stand-ups with support team
├─ [ ] Incident log reviewed for patterns
├─ [ ] User training conducted
├─ [ ] Documentation updates based on real usage
├─ [ ] Performance trends analyzed
├─ [ ] Lessons learned documented
└─ [ ] Week 1 review meeting scheduled

FIRST MONTH POST-GO-LIVE
├─ [ ] Full month of operation completed
├─ [ ] All user workflows tested by actual staff
├─ [ ] At least one complete audit cycle completed
├─ [ ] Issue management tested by users
├─ [ ] Random selection generated and tested
├─ [ ] Reports and dashboards verified
├─ [ ] Performance metrics stable
├─ [ ] No critical unresolved issues
└─ [ ] Month 1 review meeting and retrospective
```

---

## Testing Execution Standards

### Test Case Execution Protocol

**For Each Test Case:**

1. **Prepare Environment**
   - Verify all prerequisites met
   - Clear any stale data if required
   - Ensure test account has appropriate permissions

2. **Execute Steps**
   - Follow each step exactly as written
   - Document any deviations from expected path
   - Take screenshots of unexpected behavior

3. **Record Results**
   - Mark as PASS if all acceptance criteria met
   - Mark as FAIL if any criteria not met
   - Document actual result vs. expected

4. **Log Issues**
   - For any failures, create defect record
   - Include test case ID and step where failure occurred
   - Attach evidence (screenshot, error message)

5. **Sign Off**
   - Initial and date execution
   - Note any environment issues
   - Indicate tester name and role

### Defect Reproduction Steps

When a defect is reported, include:

```
1. Test Case Reference: [TC-XX-XXX]
2. Test Environment: [Browser/Device/Network/etc.]
3. Date/Time: [When observed]
4. Steps to Reproduce:
   - Exact sequence leading to issue
   - All input data used
   - Any timing considerations
5. Expected Behavior: [What should happen]
6. Actual Behavior: [What actually happens]
7. Screenshots/Logs: [Evidence]
8. Reproducibility: [Always / Sometimes / Rarely]
9. Impact: [How does this affect users?]
```

---

## Sign-Off Authority and Approval

| Role | Sign-Off Authority | Approval Conditions |
|------|-------------------|-------------------|
| MERT Educator Lead | Functional Testing | All critical/high defects resolved, UAT completed |
| Nurse Unit Manager | Issue Management | Issue workflow tested and approved |
| Clinical Auditor | Audit Entry | Complete audit workflow tested, ease of use verified |
| IT Lead | Technical Deployment | Security/permissions verified, performance acceptable |
| Project Sponsor | Overall Go-Live | All stakeholder sign-offs obtained, risks mitigated |

---

## Appendices

### Test Data Preparation

Test database should include:

```
MASTER DATA
├─ Locations: 76 (varied buildings, service lines, operating hours)
├─ Equipment: 89 items (various categories, critical/non-critical)
├─ EquipmentCategory: 8 categories
├─ ServiceLine: 7 service lines
└─ AuditPeriod: 1 active period

SAMPLE AUDIT DATA (50 records)
├─ 30 submitted/verified audits (various compliance scores)
├─ 10 draft audits
├─ 10 audits with issues identified
├─ Date range: Last 12 months

SAMPLE ISSUE DATA (30 records)
├─ 5 critical issues
├─ 8 high issues
├─ 10 medium issues
├─ 7 low issues
├─ Various statuses: Open, Assigned, In Progress, Resolved, Closed
└─ Multiple actions and comments per issue

SAMPLE RANDOM SELECTIONS (4 records)
├─ Current week: 10 trolleys, various completion statuses
├─ Previous 3 weeks: completed selections
└─ Mixed completion: some completed, some pending, some skipped
```

### Testing Resources

**Required Tools:**
- Power Apps test environment
- SharePoint Online test tenant
- Power BI Premium workspace
- Test browser(s): Chrome, Edge, Safari
- Screen capture tool (built-in or Snagit)
- Defect tracking system (Jira, Azure DevOps, or similar)

**Training Materials:**
- System overview presentation (30 min)
- User role walkthroughs (1 hour per role)
- Test case execution guide (15 min)
- Defect reporting procedure (15 min)

---

## Success Metrics

Phase 4.3 testing is considered successful when:

1. **Coverage:** ≥95% of planned test cases executed
2. **Quality:** 0 critical defects, 0 high defects at sign-off
3. **Performance:** 95%+ of tests pass on first execution
4. **Schedule:** Testing completed within planned timeline
5. **Stakeholder:** 100% of required sign-offs obtained
6. **Documentation:** All test results documented and archived
7. **Confidence:** Go-live decision made with high confidence

---

## Related Documents

- RBWH_Trolley_Audit_Program_Specification_v2.md
- RBWH_Resuscitation_Trolley_Audit_Schema.md
- Phase 1-4.2 Implementation Guides
- Risk Register and Mitigation Plan
- User Training Materials (to be created in Phase 4.4)

---

**Document Version:** 1.0
**Last Updated:** January 2026
**Next Phase:** 4.4 Deployment Preparation
**Estimated Phase Duration:** 4-6 weeks (concurrent with other preparation tasks)

*End of Phase 4.3 Testing Implementation Guide*
