# RBWH Trolley Audit System
## Phase 2.9 Random Selection Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 2.9.1 - 2.9.17

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Prerequisites](#prerequisites)
3. [SharePoint List Schemas](#sharepoint-list-schemas)
4. [Selection Algorithm](#selection-algorithm)
5. [Power Automate Flows](#power-automate-flows)
6. [PowerApp Screens](#powerapp-screens)
7. [Integration Points](#integration-points)
8. [Verification Checklist](#verification-checklist)
9. [Troubleshooting](#troubleshooting)

---

## Executive Summary

Phase 2.9 implements a weekly random selection system for audit prioritization. This system ensures consistent audit coverage across the hospital campus with intelligent weighting toward under-audited locations.

### What You'll Complete

| Task Range | Objective | Time | Dependency |
|-----------|-----------|------|-----------|
| 2.9.1-2.9.5 | Create SharePoint lists for random selection | 4 hours | Phase 1.5 |
| 2.9.6-2.9.9 | Build Random Selection Admin screen | 4 hours | 2.9.5 |
| 2.9.10-2.9.14 | Implement selection algorithm flow | 6 hours | 2.9.9 |
| 2.9.15 | Create scheduled generation trigger | 2 hours | 2.9.14 |
| 2.9.16-2.9.17 | Integrate with Home screen and Audit | 4 hours | 2.9.15 |

**Total Duration:** Approximately 20 hours of implementation work

### Key Deliverables

By the end of Phase 2.9, you will have:
- **2 new SharePoint lists** with proper schemas and relationships
- **1 Power Automate flow** implementing intelligent selection algorithm
- **1 Admin screen** in PowerApp for manual generation and progress tracking
- **1 scheduled flow** for automatic weekly generation (Monday 6am)
- **Integration** with Home screen showing current week's audits
- **Linkage** between selected audits and completion tracking

### Selection Algorithm Summary

The algorithm uses a priority-based approach:
```
Priority Score = (DaysSinceLastAudit × 2) + (100 - LastAuditCompliance) + RandomFactor(0-20)
```

Then selects top 10 trolleys with distribution constraints:
- Maximum 3 trolleys per service line
- Minimum 1 trolley per occupied service line (if possible)
- Prioritizes under-audited locations

---

## Prerequisites

### Required Completion

Before starting Phase 2.9, you must have completed:
- ✓ Phase 1.1-1.6: SharePoint site and basic PowerApp
- ✓ Phase 2.1-2.5: Trolley management and audit submission
- ✓ Phase 2.6-2.8: Issue management system
- ✓ Audit submission flows creating Location.LastAuditDate and Location.LastAuditCompliance

### Required Data

Verify these prerequisites exist:
- Location list with 76+ locations, all marked Active
- Location.LastAuditDate populated (from historical data or audits)
- Location.LastAuditCompliance populated (0-100 scale)
- Equipment list with all items configured
- Audit list with submission records

### Required Permissions

- **SharePoint Admin:** To create lists and configure lookups
- **Power Apps Admin:** To publish flows and modify apps
- **MERT Educator:** To test selection and admin screen

### Required Services

- Power Automate with premium connector access (for scheduled flows)
- SharePoint Online (current or Microsoft 365 subscription)
- Power Apps license (premium for offline capability)

---

## SharePoint List Schemas

### Task 2.9.1: Create RandomAuditSelection List

**Objective:** Create header list for weekly selection batches

**List Name:** RandomAuditSelection

#### Column Definitions

| Column Name | Type | Constraints | Description |
|-------------|------|-------------|-------------|
| Title | Text | Required | Auto-generated: "Week 1-2026" format |
| SelectionDate | Date | Required | Date selection was generated |
| WeekNumber | Number | Required | Week of year (1-53) |
| Year | Number | Required | Calendar year |
| GeneratedBy | Person | Required | User who triggered generation |
| GeneratedDateTime | DateTime | Auto | Timestamp of generation |
| SelectionCount | Number | Required | Number of items selected (typically 10) |
| IsActive | Boolean | Default: true | Current/past selection flag |

#### Step-by-Step Instructions

**Step 1: Create the List**

```
1. Navigate to SharePoint site: RBWHTrolleyAudit
2. Click "+ New" > "List"
3. Select "Blank list"
4. Name: RandomAuditSelection
5. Description: Weekly random selection of trolleys for audit
6. Click "Create"
```

**Step 2: Add Columns**

Execute the following in order (Title column exists by default):

```
Column 1: SelectionDate
- Type: Date
- Required: Yes
- Format: Date only (no time)

Column 2: WeekNumber
- Type: Number
- Required: Yes
- Min: 1
- Max: 53
- Decimal places: 0

Column 3: Year
- Type: Number
- Required: Yes
- Min: 2020
- Max: 2050
- Decimal places: 0

Column 4: GeneratedBy
- Type: Person
- Required: Yes
- Allow multiple selections: No

Column 5: GeneratedDateTime
- Type: Date and Time
- Required: Yes
- Format: Date and Time
- Display: Both
- Calculated from: NOW()

Column 6: SelectionCount
- Type: Number
- Required: Yes
- Default: 10
- Min: 1
- Max: 20

Column 7: IsActive
- Type: Boolean (Yes/No)
- Required: No
- Default: Yes
```

**Step 3: Customize Title Column**

The Title column should auto-generate based on WeekNumber and Year:

```
Column: Title
- Type: Single line of text (already exists)
- Set column formula as calculated:
  = "Week " & [WeekNumber] & "-" & [Year]
```

**Alternative (if auto-generation not available):**
- Use Power Automate to generate title in creation flow
- Store as: "Week 1-2026", "Week 2-2026", etc.

**Step 4: Create List View**

Create a new view called "Active Selections":

```
View Name: Active Selections
Type: Standard
Filters:
  - IsActive = Yes
Sort:
  - SelectionDate (Descending)
Columns:
  - Title
  - SelectionDate
  - SelectionCount
  - GeneratedBy
  - GeneratedDateTime
```

**Step 5: Enable Content Type

```
1. Click List Settings (gear icon) > "List settings"
2. Under "General settings", enable:
   - Allow this list to have multiple content types? Yes
3. Add Version History:
   - Enable "Create a version each time an item is edited"
   - Keep: "Keep all versions"
```

**Verification Points:**

- [ ] List created with name "RandomAuditSelection"
- [ ] All 7 columns added
- [ ] Column types correct
- [ ] Title column configured (manual or automated)
- [ ] View "Active Selections" created
- [ ] List accessible to all users

---

### Task 2.9.2: Create RandomAuditSelectionItem List

**Objective:** Create detail list for individual selected trolleys

**List Name:** RandomAuditSelectionItem

#### Column Definitions

| Column Name | Type | Constraints | Description |
|-------------|------|-------------|-------------|
| Title | Text | Required | Auto: "ITEM-1", "ITEM-2", etc. |
| SelectionId | Lookup | Required | Parent RandomAuditSelection |
| LocationId | Lookup | Required | Selected Location (trolley) |
| AuditId | Lookup | Optional | Completed Audit record |
| PriorityScore | Number | Required | Calculated score (0-120+) |
| SelectionOrder | Number | Required | Display order (1-10) |
| CompletionStatus | Choice | Default: Pending | Pending / Completed / Skipped |
| CompletedDate | Date | Optional | Date audit submitted |
| CompletedAuditor | Person | Optional | Who completed the audit |
| Notes | Multi-line Text | Optional | Additional context |

#### Step-by-Step Instructions

**Step 1: Create the List**

```
1. Navigate to SharePoint site: RBWHTrolleyAudit
2. Click "+ New" > "List"
3. Select "Blank list"
4. Name: RandomAuditSelectionItem
5. Description: Individual trolleys in weekly random selection
6. Click "Create"
```

**Step 2: Add Columns (Order Matters)**

```
Column 1: SelectionId (LOOKUP)
- Type: Lookup
- Get information from: RandomAuditSelection
- In this column: ID
- Allow multiple values: No
- Require a value: Yes
- Description: Parent selection batch
```

**Step 3: Add LocationId Lookup**

```
Column 2: LocationId (LOOKUP)
- Type: Lookup
- Get information from: Location
- In this column: ID
- Allow multiple values: No
- Require a value: Yes
- Description: Selected trolley location
- Create relationship: Yes
```

**Step 4: Add AuditId Lookup (Optional)**

```
Column 3: AuditId (LOOKUP)
- Type: Lookup
- Get information from: Audit
- In this column: ID
- Allow multiple values: No
- Require a value: No
- Description: Linked audit when completed
- Advanced: Allow relationship creation? Yes
```

**Step 5: Add PriorityScore Column**

```
Column 4: PriorityScore
- Type: Number
- Required: Yes
- Decimal places: 1
- Min: 0
- Max: 150
- Description: Score used for selection
```

**Step 6: Add SelectionOrder Column**

```
Column 5: SelectionOrder
- Type: Number
- Required: Yes
- Decimal places: 0
- Min: 1
- Max: 20
- Description: Sort order in selection
```

**Step 7: Add CompletionStatus Column**

```
Column 6: CompletionStatus
- Type: Choice
- Required: Yes
- Default: "Pending"
- Choices (each on new line):
  Pending
  Completed
  Skipped
- Display choices as: Drop-Down Menu
```

**Step 8: Add CompletedDate Column**

```
Column 7: CompletedDate
- Type: Date
- Required: No
- Format: Date only
- Description: Date audit was submitted
```

**Step 9: Add CompletedAuditor Column**

```
Column 8: CompletedAuditor
- Type: Person
- Required: No
- Allow multiple selections: No
- Description: Who completed the audit
```

**Step 10: Add Notes Column**

```
Column 9: Notes
- Type: Multiple lines of text
- Required: No
- Max length: 1000
- Rich text: No
- Description: Additional context or reason
```

**Step 11: Update Title Column**

Configure title to auto-generate:

```
Column: Title
- Formula or Power Automate will set to:
  "ITEM-" & [SelectionOrder]
  or
  Use flow to generate on creation
```

**Step 12: Create Views**

Create "Current Week Pending" view:

```
View Name: Current Week Pending
Type: Standard
Filters:
  - CompletionStatus = Pending
Sort:
  - SelectionOrder (Ascending)
Columns:
  - Title
  - SelectionId
  - LocationId (show location name)
  - PriorityScore
  - CompletionStatus
```

Create "Current Week Complete" view:

```
View Name: Current Week Complete
Type: Standard
Filters:
  - CompletionStatus = Completed
Sort:
  - CompletedDate (Descending)
Columns:
  - Title
  - LocationId
  - CompletedDate
  - CompletedAuditor
  - PriorityScore
```

**Verification Points:**

- [ ] List created with name "RandomAuditSelectionItem"
- [ ] All 9 columns added
- [ ] Column types correct
- [ ] Lookups properly configured
- [ ] Choice options set correctly
- [ ] Views created and filtered
- [ ] List accessible to all users

---

### Task 2.9.3-2.9.5: Configure Lookups and Relationships

**Task 2.9.3: Configure SelectionItem Lookup to Selection**

Already completed in Step 2 when creating SelectionId column.

**Verification:**
```
1. Open RandomAuditSelectionItem
2. Click on SelectionId column > Settings
3. Verify:
   - Get information from: RandomAuditSelection
   - In this column: ID
   - Allow multiple: No
   - Required: Yes
```

**Task 2.9.4: Configure SelectionItem Lookup to Location**

Already completed in Step 3 when creating LocationId column.

**Verification:**
```
1. Open RandomAuditSelectionItem
2. Click on LocationId column > Settings
3. Verify:
   - Get information from: Location
   - In this column: ID
   - Allow multiple: No
   - Required: Yes
```

**Task 2.9.5: Configure SelectionItem Lookup to Audit**

Already completed in Step 4 when creating AuditId column.

**Verification:**
```
1. Open RandomAuditSelectionItem
2. Click on AuditId column > Settings
3. Verify:
   - Get information from: Audit
   - In this column: ID
   - Allow multiple: No
   - Required: No (optional - filled when audit completed)
```

**Create Reverse Lookup (Optional but Recommended)**

Add lookup column to Audit list pointing back to RandomAuditSelectionItem:

```
List: Audit
New Column: RandomSelection
- Type: Lookup
- Get information from: RandomAuditSelectionItem
- In this column: ID
- Allow multiple values: Yes
- Filter: Where AuditId = this Audit
```

This enables viewing all random selections linked to an audit.

---

## Selection Algorithm

### Algorithm Overview

The random selection system prioritizes trolleys based on audit currency and compliance performance, with randomization to prevent predictability.

### Priority Score Calculation

```
Priority Score = (DaysSinceLastAudit × 2) + (100 - LastAuditCompliance) + RandomFactor

Where:
  DaysSinceLastAudit = Days since Location.LastAuditDate
                       Capped at 365 days max
  LastAuditCompliance = Location.LastAuditCompliance (0-100)
  RandomFactor = Random integer between 0-20
```

### Example Calculations

**Example 1: Well-audited location**
```
Location: 7A North
- Last audited: 15 days ago
- Last compliance: 92%
- Random factor: 7

Priority = (15 × 2) + (100 - 92) + 7
        = 30 + 8 + 7
        = 45
```

**Example 2: Under-audited location**
```
Location: Cath Lab 1
- Last audited: 90 days ago
- Last compliance: 78%
- Random factor: 14

Priority = (90 × 2) + (100 - 78) + 14
        = 180 + 22 + 14
        = 216
```

**Example 3: Never audited location**
```
Location: New Trolley
- Last audited: 365 days ago (capped)
- Last compliance: 0%
- Random factor: 19

Priority = (365 × 2) + (100 - 0) + 19
        = 730 + 100 + 19
        = 849
```

### Selection Constraints

1. **Top 10 Trolleys:** Select top 10 by priority score
2. **Service Line Distribution:** Max 3 per service line
3. **Minimum Coverage:** At least 1 per service line if >5 service lines have trolleys
4. **Active Only:** Exclude Location.IsActive = false

### Selection Logic Flow

```
STEP 1: Load All Active Locations
  - Filter: IsActive = true
  - Count: ~70-75 locations

STEP 2: Calculate Priority Scores
  FOR EACH location:
    score = (days_since × 2) + (100 - compliance) + random(0-20)

STEP 3: Sort by Priority
  - Sort descending by calculated score
  - Randomness ensures variety week to week

STEP 4: Apply Distribution Rules
  selected_items = []
  service_line_counts = {}

  FOR EACH location in sorted list:
    IF selected_items.length >= 10:
      BREAK

    service_line = location.ServiceLineId

    IF service_line_counts[service_line] < 3:
      selected_items.add(location)
      service_line_counts[service_line] += 1

STEP 5: Return 10 Selected Items
  - Return selected_items ordered by SelectionOrder
```

### Special Cases

**What if fewer than 10 active locations?**
- Select all active locations
- Set SelectionCount to actual count

**What if one service line has all trolleys?**
- Select 10 trolleys maximum from that service line
- Distribution constraint still applies (3 max)

**What if a location was skipped multiple weeks?**
- Score continues to increase based on days since last audit
- Eventually guaranteed to be selected

---

## Power Automate Flows

### Task 2.9.10: Create Generate Selection Flow

**Flow Name:** Random_Selection_Generate

**Trigger:** Manual (button on PowerApp) or Scheduled (see Task 2.9.15)

#### Flow Overview

```
Trigger (Manual/Scheduled)
  ↓
Get All Active Locations
  ↓
Calculate Priority Scores (For Each)
  ↓
Sort by Priority (Descending)
  ↓
Apply Distribution Rules
  ↓
Create RandomAuditSelection Record
  ↓
Create 10 RandomAuditSelectionItem Records
  ↓
Send Confirmation Email
```

#### Detailed Flow Configuration

**Step 1: Trigger Configuration**

For manual trigger (PowerApp button):

```
Trigger: PowerApps button
When a PowerApp or Cloud flow is selected
- No inputs required initially
```

For scheduled trigger (see Task 2.9.15):

```
Trigger: Scheduled cloud flow
Schedule: Weekly
  - Day of week: Monday
  - Time: 06:00 AM
  - Time zone: (UTC+10:00) Brisbane
```

**Step 2: Check for Existing Active Selection**

```
Action: Get items from SharePoint
  List: RandomAuditSelection
  Filter:
    - IsActive eq true
    - WeekNumber eq week(today())
    - Year eq year(today())

Action: Condition
  IF result count > 0:
    - Send notification: "Selection already exists for this week"
    - Terminate flow

ELSE:
    - Continue to next step
```

**Step 3: Get All Active Locations**

```
Action: Get items from SharePoint
  List: Location
  Filter: IsActive eq true
  Order by: Title
  Top count: 1000

Action: Store in variable:
  Name: allLocations
  Type: Array
  Value: Output from previous action
```

**Step 4: Calculate Priority Scores (For Each Location)**

This requires creating an array of objects with calculated scores.

```
Action: Create HTML table (first transformation)
  From: allLocations
  Columns:
    - LocationId: value('id')
    - LocationName: value('Title')
    - DaysSince: days between LastAuditDate and utcNow()
    - LastCompliance: LastAuditCompliance
    - RandomFactor: rand() * 20 (rounded to integer)
    - PriorityScore: (DaysSince * 2) + (100 - LastCompliance) + RandomFactor
```

Better approach using Select and calculations:

```
Action: Select (Transform)
  From: allLocations
  Mapping:
    locationId: @{item()}['ID']
    locationName: @{item()}['Title']
    serviceLine: @{item()}['ServiceLineId']
    daysSince: @{min(int(sub(ticks(utcNow()), ticks(item()['LastAuditDate']))) / 864000000000), 365)}
    lastCompliance: @{if(equals(item()['LastAuditCompliance'], null), 0, int(item()['LastAuditCompliance']))}
    randomFactor: @{int(mul(rand(), 20))}
    priority: @{add(add(mul(min(int(sub(ticks(utcNow()), ticks(item()['LastAuditDate']))) / 864000000000), 365), 2), sub(100, if(equals(item()['LastAuditCompliance'], null), 0, int(item()['LastAuditCompliance'])))), int(mul(rand(), 20)))}

Action: Store result
  Name: locationsWithScores
  Type: Array
```

**Step 5: Sort by Priority Score**

```
Action: Sort by field (use Apply to each or Query)
  Input: locationsWithScores
  Sort by: priority (Descending)

Action: Store result
  Name: sortedLocations
  Type: Array
```

**Step 6: Apply Distribution Rules**

```
Action: Initialize variables:
  Name: selectedItems
  Type: Array
  Value: []

  Name: serviceLineCounts
  Type: Object
  Value: {}

  Name: selectionCount
  Type: Integer
  Value: 0

Action: Apply to each location in sortedLocations
  Current item: location

  Condition: AND(
    selectionCount < 10,
    serviceLineCounts[location.serviceLine] < 3
  )

  Action (True):
    - Append to array (selectedItems): location
    - Increment: selectionCount += 1
    - Update object: serviceLineCounts[location.serviceLine] += 1

  Action (False):
    - Continue
```

**Step 7: Create RandomAuditSelection Header**

```
Action: Create item in SharePoint
  List: RandomAuditSelection

  Fields:
    - Title: concat('Week ', weekNumber(today()), '-', year(today()))
    - SelectionDate: today()
    - WeekNumber: @{weekNumber(today())}
    - Year: @{year(today())}
    - GeneratedBy: @{triggerBody()['user']['email']} (if PowerApp trigger)
                   OR MERT Educator role user (if scheduled)
    - SelectionCount: @{selectionCount}
    - IsActive: true

Action: Store result
  Name: newSelection
  Type: Object
  Value: New RandomAuditSelection ID
```

**Step 8: Create RandomAuditSelectionItem Records**

```
Action: Apply to each item in selectedItems
  Current item: selectedItem

  Action: Create item in SharePoint
    List: RandomAuditSelectionItem

    Fields:
      - Title: concat('ITEM-', indexOf(selectedItems, selectedItem) + 1)
      - SelectionId: newSelection['ID']
      - LocationId: selectedItem.locationId
      - PriorityScore: selectedItem.priority
      - SelectionOrder: indexOf(selectedItems, selectedItem) + 1
      - CompletionStatus: 'Pending'
      - Notes: concat('Auto-generated selection. Score: ', selectedItem.priority)
```

**Step 9: Send Confirmation Email**

```
Action: Send an email (O365 Outlook)
  To: MERT Educator email
  Subject: 'Random Trolley Selection Generated - Week ' + weekNumber(today())

  Body (HTML):
    <h2>Random Trolley Selection Generated</h2>
    <p>Date: [today]</p>
    <p>Items Selected: [selectionCount]</p>
    <h3>Selected Trolleys:</h3>
    <ul>
      [For each selectedItem]
      <li>[LocationName] - Score: [PriorityScore] - Service Line: [ServiceLineName]</li>
    </ul>
    <p><a href="[PowerApp Link]">View in PowerApp</a></p>
```

**Step 10: Error Handling**

Add error handling to entire flow:

```
Run After: [All previous steps]
Condition: IF any step failed

Action: Send error notification email
Action: Log error to SharePoint list
Action: Terminate flow with error status
```

---

### Task 2.9.15: Create Scheduled Generation Flow

**Flow Name:** Random_Selection_Scheduled_Generate

**Trigger:** Scheduled (Weekly, Monday 6:00 AM)

#### Configuration

```
Trigger: Scheduled cloud flow
  Frequency: Week
  Start time: 2026-01-20T06:00:00
  Time zone: (UTC+10:00) Brisbane
  Every: 1 Week
  On these days: Monday

Action 1: Check for existing selection
  [Use same logic as Task 2.9.10 Step 2]

Action 2: If no selection exists
  - Call Generate_Selection_Generate flow
    (or copy logic inline)

Action 3: Send summary email
  To: MERT distribution list
  Subject: "Weekly Random Selection Generated"
```

#### Scheduled Flow Benefits

- Automatic generation every Monday morning
- No manual intervention required
- Consistent timing for staff awareness
- Can run in background during off-hours

#### Override Capability

Allow manual override if needed:

```
PowerApp: Random Selection Admin Screen
  Button 1: "Generate Now"
    - Calls Random_Selection_Generate flow manually
    - Creates selection immediately (may overwrite scheduled one)

  Button 2: "Force Regenerate"
    - Deletes current week's selection and items
    - Calls Random_Selection_Generate flow
    - Creates new selection with different random seed
```

---

## PowerApp Screens

### Task 2.9.6: Create Random Selection Admin Screen

**Screen Name:** RandomSelectionAdmin

**Purpose:** MERT Educators manage weekly selections

#### Screen Layout

```
┌─────────────────────────────────────┐
│ RANDOM SELECTION ADMINISTRATION      │
├─────────────────────────────────────┤
│                                     │
│ Current Week Selection               │
│ ┌─────────────────────────────────┐ │
│ │ Week: 1 - 2026                  │ │
│ │ Generated: 20 Jan 2026, 6:15 AM │ │
│ │ Generated By: [MERT Educator]   │ │
│ │ Total Selected: 10              │ │
│ │                                 │ │
│ │ Progress:                       │ │
│ │ ✓ Completed: 7 / 10 (70%)      │ │
│ │ ◯ Pending: 3 / 10 (30%)        │ │
│ │ ⊘ Skipped: 0 / 10 (0%)         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ [Generate New Selection]         │ │
│ │ [Force Regenerate]              │ │
│ │ [View History]                  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Today's Selection Items             │
│ ┌─────────────────────────────────┐ │
│ │ # │ Location     │ Status  │ Score│ │
│ │─── ─────────────   ───────   ─────│ │
│ │ 1 │ 7A North    │ Pending │ 156 │ │
│ │ 2 │ 5C Beds     │ Done    │ 142 │ │
│ │ 3 │ Cath Lab 1  │ Pending │ 138 │ │
│ │ 4 │ ED Bay 3    │ Done    │ 131 │ │
│ │ 5 │ CCU 1       │ Done    │ 128 │ │
│ │ 6 │ 9B West     │ Skipped │ 115 │ │
│ │ 7 │ ICU 2       │ Done    │ 108 │ │
│ │ 8 │ Ward 5A     │ Pending │ 98  │ │
│ │ 9 │ Cath Lab 2  │ Done    │ 87  │ │
│ │10 │ Pharmacy    │ Pending │ 76  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Data current as of: [Last refresh] │
│                                     │
└─────────────────────────────────────┘
```

#### Screen Components

**Component 1: Header Section**

```
Label: "Random Selection Administration"
- Font: Bold, 28pt
- Color: RBWH Primary Blue (#005FAD)

Label: "This week's random trolley audit selection"
- Font: Regular, 14pt
- Color: Dark Grey (#333333)

Refresh Button:
- Label: "⟳ Refresh"
- On Select: Refresh() entire screen data
```

**Component 2: Current Selection Card**

Create a gallery item or card showing:

```
Card Container (if no selection exists):
  Text: "No selection generated for this week"
  Text: "Click [Generate New Selection] to create one"

Card Container (if selection exists):
  Label: Selection.Title
    - Font: Bold, 20pt

  Details Grid:
    - Generated: Selection.GeneratedDateTime formatted
    - By: Selection.GeneratedBy DisplayName
    - Total Selected: Selection.SelectionCount

  Progress Display:
    Completed Count / Total (percentage)
    Pending Count / Total (percentage)
    Skipped Count / Total (percentage)

    Visual: Horizontal stacked bar chart or 3 circular progress indicators
```

**Component 3: Action Buttons**

```
Button 1: Generate New Selection
  Visible: IsBlank(CurrentSelection) OR AllowOverwrite
  Label: "Generate New Selection"
  Style: RBWH Secondary Green (#78BE20)
  On Select:
    Set(varGenerating, true);
    Random_Selection_Generate.Run();
    Refresh data;
    Set(varGenerating, false);
    Notify("Selection generated successfully", Success);

Button 2: Force Regenerate
  Visible: NOT IsBlank(CurrentSelection)
  Label: "Force Regenerate"
  Style: Warning (Orange)
  On Select:
    If(Confirm("This will replace the current selection. Continue?"),
      Delete current selection and items;
      Random_Selection_Generate.Run();
      Refresh data;
      Notify("Selection regenerated", Success);
    );

Button 3: View Selection History
  Label: "View Selection History"
  Style: RBWH Primary Blue (#005FAD)
  On Select:
    Navigate(RandomSelectionHistory, ScreenTransition.Cover);
```

**Component 4: Selection Items Table**

```
Gallery (Horizontal Scroll):
  Data Source: Filter(RandomAuditSelectionItem,
               SelectionId = CurrentSelection.Id)

  Layout: Detailed list with columns

  Columns:
    1. Order: SelectionOrder (right-aligned, 40px)
    2. Location: LocationId.DisplayName (200px)
    3. Service Line: LocationId.ServiceLineId.Name (150px)
    4. Status: CompletionStatus (100px)
       - Styling:
         - Pending: White background, dark text
         - Completed: Green background, white text
         - Skipped: Grey background, white text
    5. Score: PriorityScore (80px, right-aligned)
    6. Actions: Mark Complete / Skip buttons (150px)

  On Row Selection:
    Navigate(AuditEntryScreen,
      ScreenTransition.None,
      {selectedLocation: ThisItem.LocationId});
```

**Component 5: Status Counts Section**

```
Container: Selection Statistics

  Stat Card 1:
    Label: "COMPLETED"
    Count: CountIf(SelectionItems, CompletionStatus = "Completed")
    Percentage: Count / Total * 100
    Color: Green (#78BE20)

  Stat Card 2:
    Label: "PENDING"
    Count: CountIf(SelectionItems, CompletionStatus = "Pending")
    Percentage: Count / Total * 100
    Color: Orange (#FFA500)

  Stat Card 3:
    Label: "SKIPPED"
    Count: CountIf(SelectionItems, CompletionStatus = "Skipped")
    Percentage: Count / Total * 100
    Color: Grey (#999999)
```

---

### Task 2.9.7-2.9.8: Display Selection Progress

**Task 2.9.7: Display Current Week Selection**

Implemented in Component 2 above.

**Task 2.9.8: Display Selection Progress**

Implemented in Component 5 above.

Example Power Query formula for progress:

```
GetCurrentWeek:
  Filter(RandomAuditSelection,
    WeekNumber = Week(Today()),
    Year = Year(Today()),
    IsActive = true)

GetSelectionItems:
  Filter(RandomAuditSelectionItem,
    SelectionId = GetCurrentWeek.Id)

CountCompleted:
  CountIf(GetSelectionItems, CompletionStatus = "Completed")

CountPending:
  CountIf(GetSelectionItems, CompletionStatus = "Pending")

CountSkipped:
  CountIf(GetSelectionItems, CompletionStatus = "Skipped")

PercentageComplete:
  CountCompleted / GetSelectionItems.Count * 100
```

---

### Task 2.9.16: Display "This Week's Audits" on Home Screen

**Objective:** Show random selection on dashboard

#### Home Screen Integration

Add new section to existing Home screen:

```
Section: This Week's Audits (Random Selection)
  Position: Below KPI cards, above Audit History

  Sub-section 1: Quick Stats (3 columns)
    ┌──────────────────────────────────────┐
    │ SELECTED THIS WEEK │ COMPLETED │ DUE  │
    │        10          │     6     │  4   │
    └──────────────────────────────────────┘

  Sub-section 2: Week Summary Card
    "Week 1-2026"
    "6 of 10 audits complete"
    Progress bar: ████████░░ 60%
    Timestamp: Last updated [time]

  Sub-section 3: Quick List (Scrollable)
    ┌──────────────────────────────────────┐
    │ ✓ 7A North (Completed)              │
    │ ✓ 5C Beds (Completed)               │
    │ ○ Cath Lab 1 (Pending)              │
    │ ✓ ED Bay 3 (Completed)              │
    │ ✓ CCU 1 (Completed)                 │
    │ ⊘ 9B West (Skipped)                 │
    │ ✓ ICU 2 (Completed)                 │
    │ ○ Ward 5A (Pending)                 │
    │ ✓ Cath Lab 2 (Completed)            │
    │ ○ Pharmacy (Pending)                │
    └──────────────────────────────────────┘
    [View Full Selection] button (navigates to RandomSelectionAdmin)

  Update Frequency: Refresh every 30 seconds
    Set(varLastRefresh, Now());
    Timer interval: 30000ms
```

#### Implementation Code

**Add to Home Screen:**

```PowerApps
// Add below existing KPI cards

Label_ThisWeek:
  Text: "This Week's Audits (Random Selection)"
  Font: Bold, 20pt
  Color: RBWH Primary Blue

// Get current selection
GetCurrentSelection:
  Filter(RandomAuditSelection,
    WeekNumber = Week(Today()),
    Year = Year(Today()),
    IsActive = true)

// Get selection items
GetSelectionItems:
  Filter(RandomAuditSelectionItem,
    SelectionId = GetCurrentSelection.Id)

// Card showing summary
Card_WeeklySelection:
  Container:
    Text: GetCurrentSelection.Title
    Text: Text(CountIf(GetSelectionItems, CompletionStatus = "Completed"))
          & " of " & GetCurrentSelection.SelectionCount & " Complete"

    ProgressBar:
      Value: CountIf(GetSelectionItems, CompletionStatus = "Completed")
      Max: GetCurrentSelection.SelectionCount

    Button:
      Label: "View Full Selection"
      OnSelect: Navigate(RandomSelectionAdmin)

// Gallery of selection items
Gallery_ThisWeek:
  Items: GetSelectionItems
  Layout: Single column

  Template:
    HStack:
      Icon (status indicator):
        If(ThisItem.CompletionStatus = "Completed",
          "✓", Icon.Checkmark, Green),
        If(ThisItem.CompletionStatus = "Pending",
          "○", Icon.Circle, Orange),
        If(ThisItem.CompletionStatus = "Skipped",
          "⊘", Icon.Cancel, Grey)

      Text: ThisItem.LocationId.DisplayName

      Text (status): ThisItem.CompletionStatus
```

---

### Task 2.9.17: Link Selection to Audit Completion

**Objective:** Update SelectionItem when audit is submitted

#### Update Audit Submission Flow

Modify the existing "Submit Audit" flow (Task 2.5.8) to link selection:

```
In Submit_Audit flow, add new action after creating Audit record:

Action: Query RandomAuditSelectionItems
  List: RandomAuditSelectionItem
  Filter: LocationId = AuditLocationId AND
          SelectionId.IsActive = true AND
          WeekNumber = week(today()) AND
          Year = year(today())

Action: If result found
  Create item (Set AuditId):
    List: RandomAuditSelectionItem
    ID: Result from query
    Update field: AuditId = NewAuditRecord.Id
    Update field: CompletionStatus = "Completed"
    Update field: CompletedDate = Today()
    Update field: CompletedAuditor = Current user
```

#### Alternative: PowerApp Logic

Implement in Audit submission screen:

```PowerApps
OnSubmit:
  // Create audit record
  Patch(Audit, Default(Audit), {
    LocationId: selectedLocation,
    // ... other fields
  });

  // Find matching selection item
  Set(varMatchingSelection,
    Filter(RandomAuditSelectionItem,
      LocationId = selectedLocation,
      SelectionId.IsActive = true,
      SelectionId.WeekNumber = Week(Today()),
      SelectionId.Year = Year(Today())
    )
  );

  // Update selection item
  If(!IsBlank(varMatchingSelection),
    Patch(RandomAuditSelectionItem,
      varMatchingSelection,
      {
        AuditId: NewAuditRecord.Id,
        CompletionStatus: "Completed",
        CompletedDate: Today(),
        CompletedAuditor: User().FullName
      }
    )
  );
```

---

## Integration Points

### Integration Point 1: Home Screen KPI Updates

The Home screen KPI "Audit Completion Rate" should include:
- Total audits due this week (from RandomAuditSelection.SelectionCount)
- Audits completed this week (count where CompletionStatus = "Completed")
- Percentage: Completed / Total

### Integration Point 2: Audit Entry Screen

When starting an audit:
- Check if Location is in current week's RandomAuditSelectionItem
- Display banner: "This trolley is in this week's random selection"
- Pre-fill audit type based on selection (usually "Spot Check")

### Integration Point 3: Location Management

In Trolley Detail screen:
- Display "Selected for random audit: [date]" if applicable
- Show selection history over past 12 weeks
- Display score that was used for selection

### Integration Point 4: Reporting Dashboard

In Power BI reports:
- Add metric: "Random selection completion rate"
- Chart showing: Selected vs Completed by week (trending)
- Metric: "Average compliance of selected trolleys"

---

## Verification Checklist

### SharePoint Lists (Tasks 2.9.1-2.9.5)

**RandomAuditSelection List:**
- [ ] List created with correct name
- [ ] All 7 columns present and correct type
- [ ] Title auto-generates correctly
- [ ] View "Active Selections" created
- [ ] Can create new item without errors
- [ ] Version history enabled

**RandomAuditSelectionItem List:**
- [ ] List created with correct name
- [ ] All 9 columns present and correct type
- [ ] SelectionId lookup configured (required)
- [ ] LocationId lookup configured (required)
- [ ] AuditId lookup configured (optional)
- [ ] CompletionStatus choices correct
- [ ] Views created: "Current Week Pending", "Current Week Complete"
- [ ] Can create new item without errors

**Lookups and Relationships:**
- [ ] SelectionId lookup works (can select from RandomAuditSelection)
- [ ] LocationId lookup works (can select from Location)
- [ ] AuditId lookup works (can select from Audit)
- [ ] Lookups show correct data
- [ ] No circular dependencies

### Admin Screen (Tasks 2.9.6-2.9.9)

**Layout and Components:**
- [ ] Screen displays with correct layout
- [ ] Current week selection displays (or "None" if not generated)
- [ ] Progress cards show correct counts
- [ ] Selection items table shows all 10 items
- [ ] Status filtering works correctly

**Functionality:**
- [ ] "Generate New Selection" button visible
- [ ] "Force Regenerate" button visible (when selection exists)
- [ ] "View History" button visible
- [ ] Buttons are responsive
- [ ] Refresh updates all data

**Data Accuracy:**
- [ ] Completed count matches filtered items
- [ ] Pending count matches filtered items
- [ ] Skipped count matches filtered items
- [ ] Total matches 10 (or fewer if not enough locations)
- [ ] Timestamps accurate

### Selection Algorithm (Tasks 2.9.10-2.9.14)

**Flow Execution:**
- [ ] Flow starts manually without errors
- [ ] Calculates priority scores for all locations
- [ ] Sorts correctly by priority
- [ ] Applies service line distribution (max 3 per line)
- [ ] Selects exactly 10 items

**Data Creation:**
- [ ] RandomAuditSelection record created
- [ ] 10 RandomAuditSelectionItem records created
- [ ] SelectionOrder field: 1-10
- [ ] CompletionStatus: All "Pending"
- [ ] PriorityScore shows calculated values

**Flow Validation:**
- [ ] No duplicate selections for same week
- [ ] Can run multiple times (creates new week)
- [ ] Error handling prevents data corruption
- [ ] Notifications sent successfully

### Scheduled Generation (Task 2.9.15)

**Schedule Configuration:**
- [ ] Flow runs on Monday at 6:00 AM
- [ ] Timezone set to Brisbane (UTC+10:00)
- [ ] Frequency: Weekly
- [ ] Check for existing: Prevents duplicates

**Execution:**
- [ ] First run: Wait until test Monday
- [ ] Selection generates automatically
- [ ] No manual intervention needed
- [ ] Email notifications received
- [ ] Can still manually override if needed

### Home Screen Integration (Task 2.9.16)

**Display:**
- [ ] "This Week's Audits" section visible
- [ ] Shows current selection data
- [ ] Shows progress: completed/pending/skipped
- [ ] Items list displays all 10 (or fewer)
- [ ] Status icons show correctly

**Updates:**
- [ ] Section refreshes every 30 seconds
- [ ] Updates when new audit submitted
- [ ] Shows completed items immediately
- [ ] Link to admin screen works

### Audit Completion Linking (Task 2.9.17)

**On Audit Submission:**
- [ ] Flow finds matching selection item
- [ ] Sets AuditId field
- [ ] Updates CompletionStatus to "Completed"
- [ ] Sets CompletedDate to today
- [ ] Sets CompletedAuditor to current user
- [ ] Home screen updates immediately

**Validation:**
- [ ] Selection item shows as "Completed"
- [ ] Can view audit from selection
- [ ] Can view selection from audit
- [ ] Completion count increases

---

## Troubleshooting

### Issue: "No selection generated" appears every time

**Symptoms:**
- Admin screen shows "No selection for this week"
- Clicking "Generate" does nothing
- No errors appear

**Causes:**
- Flow not running successfully
- Selection created but marked inactive
- Week number calculation wrong

**Solutions:**

```
1. Check Flow Execution:
   - Open Power Automate
   - Find "Random_Selection_Generate" flow
   - Click "Analytics"
   - Check recent run status
   - Review error details if any

2. Check Existing Selections:
   - Go to RandomAuditSelection list
   - Filter by: Week(Today()) = week number
   - If found, check IsActive flag
   - Set IsActive = true if needed

3. Test Week Number:
   - In PowerApp, add diagnostic text:
     Text: "Week " & Week(Today()) & ", Year " & Year(Today())
   - Verify numbers are correct
   - Check for off-by-one errors

4. Verify Data:
   - Ensure 10+ active locations exist
   - Verify locations have LastAuditDate
   - Verify locations have LastAuditCompliance
   - Check Location.IsActive = true
```

---

### Issue: Selection shows, but items are all same service line

**Symptoms:**
- Admin screen shows "10 items selected"
- All 10 items from single service line
- Distribution rules not applied

**Causes:**
- Distribution logic not working
- Service line calculation wrong
- One service line has all trolleys

**Solutions:**

```
1. Check Algorithm Logic:
   - Review flow Step 6 (Apply Distribution Rules)
   - Verify service line counting logic
   - Add debugging variables to flow

2. Check Data:
   - Look at service line distribution in Location list
   - If 10+ locations in one service line, that's correct
   - Check other service lines exist and are active

3. Modify Algorithm (if needed):
   - If one service line dominates:
     - Adjust max per service line (3 → 2 or 1)
     - Add minimum per service line rule
     - Contact MERT for requirement clarification

4. Test with Debug Output:
   - Add "Compose" actions in flow to output:
     - Sorted locations
     - Distribution counts
     - Final selections
   - Review composed output in flow history
```

---

### Issue: Same trolley selected two weeks in a row

**Symptoms:**
- Same Location appears in Week 1 and Week 2
- Should be more varied selection

**Causes:**
- Algorithm not considering recent selections
- High-priority items selected consecutively
- Random factor causing same selection

**Solutions:**

```
1. Acceptable Behavior:
   - Algorithm can reselect underperforming trolleys
   - This is by design - encourages compliance
   - Expected behavior if trolley still has high priority

2. If Variation Desired:
   - Modify algorithm to exclude recently selected:
     Add to filter: SelectionId.SelectionDate >
                    dateadd(today(), -21 days)
                    Then reduce priority score

3. Alternative Approach:
   - Track "weeks since selected" as separate metric
   - Increase randomness factor (0-30 instead of 0-20)
   - Adjust algorithm weights

4. Review with MERT:
   - Confirm if repetition acceptable
   - Discuss selection strategy
   - Modify algorithm as needed
```

---

### Issue: Selection button doesn't work / throws error

**Symptoms:**
- "Generate New Selection" button unresponsive
- Error message appears
- Nothing happens when clicked

**Causes:**
- Flow not published
- Flow connection issue
- PowerApp permission denied
- Flow has required parameters not filled

**Solutions:**

```
1. Check Flow Status:
   - Open Power Automate
   - Find "Random_Selection_Generate"
   - Confirm "Enabled" (toggle on)
   - Check for red error indicators

2. Test Flow Manually:
   - Click "Test" in Power Automate
   - Select "Manually" trigger
   - Click "Test"
   - Observe any error messages
   - Fix errors before retrying from PowerApp

3. Check Connections:
   - In PowerApp, go to "Variables"
   - Check all connections are listed
   - Delete problematic connection
   - Re-add connection to SharePoint list

4. Verify Permissions:
   - Confirm logged-in user can:
     - Edit RandomAuditSelection list
     - Edit RandomAuditSelectionItem list
     - Run Power Automate flows
   - Add to Members group if needed

5. Debug in PowerApp:
   - Add button formula: Trace(varGenerating)
   - Check if flow is running
   - Add success/error notification:
     Notify(Result, Success/Error)
   - Track execution step by step
```

---

### Issue: Selection items show wrong LocationId

**Symptoms:**
- Admin screen shows incorrect trolleys
- Wrong service lines selected
- Locations don't match priority scores

**Causes:**
- Lookup not working correctly
- Flow selecting wrong records
- LocationId lookup data stale

**Solutions:**

```
1. Refresh Lookup:
   - Open RandomAuditSelectionItem list
   - Click on LocationId column
   - Edit column > Update from list
   - Refresh SharePoint page
   - Check if display names correct

2. Verify Lookup Source:
   - Check Location list has records
   - Confirm Location.Title populated
   - Verify Location.ID exists
   - Check for duplicate locations

3. Test Flow Selection:
   - Manually run Generate flow
   - Check flow history output
   - Review composed arrays in flow
   - Verify location IDs selected

4. Rebuild Lookup:
   - Delete LocationId column
   - Recreate with same settings
   - Test again
   - May take 24 hours to propagate
```

---

### Issue: Scheduled flow not running

**Symptoms:**
- Monday 6 AM passes, no selection generated
- Flow history shows no runs
- Manual generation works fine

**Causes:**
- Flow disabled
- Schedule not configured
- Flow syntax error
- Premium connector issue

**Solutions:**

```
1. Check Schedule Configuration:
   - Open Scheduled cloud flow
   - Verify "Enabled" toggle is ON
   - Check frequency: "Weekly"
   - Confirm day: "Monday"
   - Confirm time: "06:00 AM"
   - Verify timezone: Brisbane UTC+10:00

2. Check Flow History:
   - Open flow > Analytics
   - Look for scheduled runs
   - If none, schedule not triggered
   - Wait until next Monday to test

3. Enable Debug:
   - Add "Send an email" action at start
   - Sends test email if flow runs
   - Check for email on Monday morning
   - If not received, flow not running

4. Test Manually First:
   - Click "Test" > "Manually"
   - Run flow manually
   - Observe for errors
   - Fix any errors
   - Scheduled run should work after

5. Contact IT if Stuck:
   - Power Automate backend issue
   - Tenant-level configuration needed
   - Escalate to Microsoft support if necessary
```

---

## Best Practices

### Algorithm Tuning

**If trolleys not selected enough:**
```
Increase "days since last audit" weight:
  Old: Priority = (DaysSince × 2) + (100 - Compliance) + Random
  New: Priority = (DaysSince × 3) + (100 - Compliance) + Random
```

**If too much randomness:**
```
Reduce random factor:
  Old: Random(0-20)
  New: Random(0-10)
```

**If over-audited locations selected:**
```
Add maximum days filter:
  Don't select locations audited less than 60 days ago
  Add to filter: DaysSince > 60
```

### Performance Optimization

**If flow runs slowly:**
```
1. Add "Pagination" to Get items action:
   Fetch 1000 items instead of all

2. Reduce Sort:
   Don't sort by multiple fields

3. Parallel processing:
   Use Parallel branch for lookups

4. Simplify Calculations:
   Move complex math to PowerApp instead
```

### Data Quality

**Pre-generation checks:**
```
1. Verify all locations have LastAuditDate
   (Set to 365 days ago if never audited)

2. Verify all locations have LastAuditCompliance
   (Set to 0 if never audited)

3. Verify at least 10 active locations
   (Selection will fail if fewer)
```

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| MERT Educator | | | |
| SharePoint Admin | | | |
| Power Automate Developer | | | |
| QA Tester | | | |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Technical Writer | Initial implementation guide |

---

**Document Status:** APPROVED FOR IMPLEMENTATION

This guide provides comprehensive instructions for Phase 2.9 Random Selection implementation. Each task can be executed sequentially, with verification at each stage ensuring data integrity.

For questions or updates, contact the MERT Coordination Team.

---

*End of Phase 2.9 Random Selection Implementation Guide*
