# Phase 2.7 Issue Management Screens Implementation Guide

**RBWH Resuscitation Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 2.7 implements the complete Issue Management system for the RBWH Trolley Audit application. This phase creates screens for browsing, viewing, creating, and managing maintenance issues with corrective actions and comments.

**Phase Scope:** Tasks 2.7.1 through 2.7.20
**Estimated Duration:** 25 hours
**Prerequisites:**
- Phase 2.6 complete (Issue, CorrectiveAction, IssueComment lists created)
- Phase 2.1 complete (Trolley Management screens)
- Phase 1.6 complete (PowerApp foundation)

---

## Table of Contents

1. [Issue List Screen (Tasks 2.7.1-2.7.7)](#issue-list-screen-tasks-271-277)
2. [Issue Detail Screen (Tasks 2.7.8-2.7.12)](#issue-detail-screen-tasks-278-2712)
3. [Add Issue Screen (Tasks 2.7.13-2.7.18)](#add-issue-screen-tasks-2713-2718)
4. [Issue Dialogs (Tasks 2.7.19-2.7.20)](#issue-dialogs-tasks-2719-2720)
5. [Data Relationships & Colour Coding](#data-relationships--colour-coding)

---

## Issue List Screen (Tasks 2.7.1-2.7.7)

### Objective

Create a filterable gallery view of all issues with multi-select filters for Status and Severity, dropdown filters for Location and Assigned To, severity colour coding, and age calculation in days.

### Prerequisites

- Phase 2.6 complete (Issue list created with all columns)
- SharePoint lists: Issue, Location, Equipment
- Navigation header available from Phase 1.6

### Screen Layout Specification

```
┌─────────────────────────────────────────────────────────────┐
│         HEADER (Navigation Component)                       │
├─────────────────────────────────────────────────────────────┤
│ Filter Controls Row:                                         │
│ [Status Filter ▼] [Severity Filter ▼] [Location ▼] [Assigned To ▼]  │
│                                                              │
│ Issue Gallery (Scrollable):                                 │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ ISS-2024-0001 | Title...              | [Badge] [Badge] ││
│ │ Location: 5C East | Age: 14 days | Assigned: John Smith ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────────────────────┐│
│ │ ISS-2024-0002 | Title...              | [Badge] [Badge] ││
│ │ Location: 7A North | Age: 7 days | Assigned: Unassigned ││
│ └─────────────────────────────────────────────────────────┘│
│ ... (more rows)                                              │
│                                                              │
│ [Add Issue Button]                [Total: 24 Issues]        │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Instructions

#### Step 1: Create Issue List Screen

1. Create a new screen named "IssueScreen"
2. Set screen properties:
   - **Width:** 1366
   - **Height:** 768
   - **Fill:** `BackgroundColor`

#### Step 2: Add Navigation Header

1. Copy the navigation header from HomeScreen
2. Paste at top (Y: 0, Height: 80)

#### Step 3: Create Filter Controls Row

Create a horizontal container for filters below the header:

1. Insert a **Rectangle** for filter background:
   - **X:** 20
   - **Y:** 100
   - **Width:** 1326
   - **Height:** 60
   - **Fill:** White
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`

2. Add Status multi-select filter:
   - Insert **Combo Box** control
   - **X:** 30
   - **Y:** 110
   - **Width:** 200
   - **Label:** "Status"
   - **Items:** `{"Open", "In Progress", "Pending Verification", "Resolved", "Closed"}`
   - **SelectMultiple:** true
   - **SearchEnabled:** true

3. Add Severity multi-select filter:
   - Insert **Combo Box** control
   - **X:** 250
   - **Y:** 110
   - **Width:** 200
   - **Label:** "Severity"
   - **Items:** `{"Critical", "High", "Medium", "Low"}`
   - **SelectMultiple:** true
   - **SearchEnabled:** true

4. Add Location dropdown filter:
   - Insert **Dropdown** control
   - **X:** 470
   - **Y:** 110
   - **Width:** 250
   - **Label:** "Location"
   - **Items:** `Location`
   - **Value:** `DisplayName`

5. Add Assigned To filter with "My Issues" option:
   - Insert **Combo Box** control
   - **X:** 740
   - **Y:** 110
   - **Width:** 250
   - **Label:** "Assigned To"
   - **Items:** `Distinct(Issue, AssignedTo)`
   - **SelectMultiple:** false
   - Add manual option for "My Issues" (see PowerFx section)

6. Add Reset Filters button:
   - Insert **Button**
   - **X:** 1010
   - **Y:** 110
   - **Width:** 100
   - **Height:** 40
   - **Text:** "Reset Filters"
   - **OnSelect:** (See PowerFx section)

#### Step 4: Create Issue Gallery

1. Insert a **Gallery** control below filter row:
   - **X:** 20
   - **Y:** 170
   - **Width:** 1326
   - **Height:** 530
   - **Items:** (See PowerFx section for filtered formula)
   - **Layout:** "Vertical list"
   - **TemplateSize:** Auto
   - **Margin:** 10

2. Inside gallery template, add the following controls:

   **Header Row (Issue Number + Title + Status/Severity Badges):**

   - **Label** (Issue Number):
     - **Text:** `ThisItem.IssueNumber`
     - **Font:** 14pt, Bold
     - **Color:** `TextPrimary`
     - **X:** 10
     - **Y:** 5
     - **Width:** 150

   - **Label** (Title):
     - **Text:** `ThisItem.Title`
     - **Font:** 14pt
     - **Color:** `TextPrimary`
     - **X:** 170
     - **Y:** 5
     - **Width:** 600

   - **Shape** (Status Badge):
     - **Shape:** Rounded rectangle
     - **X:** 800
     - **Y:** 5
     - **Width:** 100
     - **Height:** 30
     - **Fill:** (See colour coding section)
     - **Text:** `ThisItem.Status`
     - **Font Color:** White
     - **Alignment:** Center

   - **Shape** (Severity Badge):
     - **Shape:** Rounded rectangle
     - **X:** 920
     - **Y:** 5
     - **Width:** 100
     - **Height:** 30
     - **Fill:** (See colour coding section)
     - **Text:** `ThisItem.Severity`
     - **Font Color:** White
     - **Alignment:** Center

   **Details Row (Location, Age, Assigned To):**

   - **Label** (Location):
     - **Text:** `"Location: " & ThisItem.LocationId.DisplayName`
     - **Font:** 11pt
     - **Color:** `TextSecondary`
     - **X:** 10
     - **Y:** 40
     - **Width:** 350

   - **Label** (Age in Days):
     - **Text:** `"Age: " & Text(DateDiff(Now(), ThisItem.DateCreated, Days)) & " days"`
     - **Font:** 11pt
     - **Color:** `TextSecondary`
     - **X:** 380
     - **Y:** 40
     - **Width:** 200

   - **Label** (Assigned To):
     - **Text:** `"Assigned To: " & If(IsBlank(ThisItem.AssignedTo), "Unassigned", ThisItem.AssignedTo)`
     - **Font:** 11pt
     - **Color:** `TextSecondary`
     - **X:** 610
     - **Y:** 40
     - **Width:** 310

3. Set gallery row height:
   - **TemplateHeight:** 60

#### Step 5: Add Row Click Navigation

1. Select the gallery container rectangle
2. Set **OnSelect** event:
   ```powerfx
   Set(varSelectedIssueID, ThisItem.ID);
   Set(varSelectedIssue, ThisItem);
   Navigate(IssueDetailScreen)
   ```

#### Step 6: Add Info and Action Controls

1. Add total issue count label at bottom:
   - **Label**
   - **Text:** `"Total Issues: " & CountRows(Gallery_Issues.Items)`
   - **Font:** 12pt
   - **Color:** `TextSecondary`
   - **X:** 20
   - **Y:** 720

2. Add "Add Issue" button:
   - **Button**
   - **X:** 1050
   - **Y:** 720
   - **Width:** 150
   - **Height:** 35
   - **Text:** "+ Add Issue"
   - **Fill:** `SecondaryColor`
   - **Text Color:** White
   - **OnSelect:** `Navigate(AddIssueScreen)`

### PowerFx Code

Complete filtering logic for gallery items:

```powerfx
// IssueScreen.Gallery_Issues.Items
// Complex filter combining multiple filter selections

ClearCollect(
    colFilteredIssues,
    Filter(
        Issue,
        // Status filter (multi-select)
        If(
            IsEmpty(ComboBox_Status.SelectedItems),
            true,
            Status in ComboBox_Status.SelectedItems
        ) &&
        // Severity filter (multi-select)
        If(
            IsEmpty(ComboBox_Severity.SelectedItems),
            true,
            Severity in ComboBox_Severity.SelectedItems
        ) &&
        // Location filter (single select)
        If(
            IsBlank(Dropdown_Location.Value),
            true,
            LocationId.ID = Dropdown_Location.Selected.ID
        ) &&
        // Assigned To filter with "My Issues" option
        If(
            IsBlank(ComboBox_AssignedTo.Value),
            true,
            If(
                ComboBox_AssignedTo.Value = "My Issues",
                AssignedTo = User().FullName,
                AssignedTo = ComboBox_AssignedTo.Value
            )
        )
    )
);

// Return sorted results (newest first)
Sort(
    colFilteredIssues,
    DateCreated,
    Descending
)
```

Reset filters button formula:

```powerfx
// Button_ResetFilters.OnSelect
Reset(ComboBox_Status);
Reset(ComboBox_Severity);
Reset(Dropdown_Location);
Reset(ComboBox_AssignedTo);
Refresh(Issue)
```

Age calculation in days (for detail row label):

```powerfx
// For "Age: X days" label in gallery
Text(
    DateDiff(
        Now(),
        ThisItem.DateCreated,
        Days
    )
) & " days"
```

### Verification Checklist

- [ ] IssueScreen created with correct dimensions
- [ ] Navigation header displays correctly
- [ ] Status multi-select filter works
- [ ] Severity multi-select filter works
- [ ] Location dropdown filter works
- [ ] Assigned To filter includes "My Issues" option
- [ ] Reset Filters button clears all selections
- [ ] Gallery displays filtered issues correctly
- [ ] Gallery rows show: Issue Number, Title, Status Badge, Severity Badge
- [ ] Gallery rows show: Location, Age in days, Assigned To
- [ ] Clicking gallery row navigates to Issue Detail
- [ ] Total issue count displays at bottom
- [ ] Add Issue button navigates to Add Issue screen
- [ ] No visible filter conflicts or errors
- [ ] Gallery scrolls smoothly with many records

---

## Issue Detail Screen (Tasks 2.7.8-2.7.12)

### Objective

Create a comprehensive issue detail view with header information, description section, corrective actions gallery, and comments thread in chronological order.

### Prerequisites

- Issue List screen complete (Task 2.7.1)
- CorrectiveAction and IssueComment lists created
- Colour coding system established

### Screen Layout Specification

```
┌─────────────────────────────────────────────────────────────┐
│         HEADER (Navigation Component)                       │
├─────────────────────────────────────────────────────────────┤
│ Issue Header:                                                │
│ ISS-2024-0001 | Defective Wheel on Trolley 5C-East         │
│ Status: [In Progress] Severity: [Critical]                  │
│ Location: 5C East | Equipment: Trolley Wheels               │
│ Reported: 14 Jan 2024 | Assigned To: John Smith            │
├─────────────────────────────────────────────────────────────┤
│ Description:                                                 │
│ The front left wheel of the trolley is stuck and cannot be  │
│ rotated. This is a patient safety hazard.                   │
├─────────────────────────────────────────────────────────────┤
│ Corrective Actions:                                          │
│ [Action 1] Immediate: Replace wheel | By: Jan 20           │
│ [Action 2] Document: Submit incident report | By: Jan 18   │
│ [+ Add Action]                                               │
├─────────────────────────────────────────────────────────────┤
│ Comments (Newest First):                                     │
│ John Smith - 15 Jan 2024 10:30am                            │
│ "Wheel has been replaced. Trolley now mobile."              │
│ [Edit] [Delete]                                              │
│                                                              │
│ Sarah Jones - 14 Jan 2024 2:15pm                            │
│ "Added to maintenance queue. Awaiting parts."                │
│ [Edit] [Delete]                                              │
│ [+ Add Comment]                                              │
├─────────────────────────────────────────────────────────────┤
│ [Edit] [Mark Resolved] [Close Issue]                        │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Instructions

#### Step 1: Create Issue Detail Screen

1. Create new screen: "IssueDetailScreen"
2. Set properties:
   - **Width:** 1366
   - **Height:** 768
   - **Fill:** `BackgroundColor`

#### Step 2: Add Navigation Header

1. Copy navigation header from HomeScreen
2. Paste at top (Y: 0, Height: 80)

#### Step 3: Create Issue Header Section

1. Insert **Rectangle** for header background:
   - **X:** 20
   - **Y:** 100
   - **Width:** 1326
   - **Height:** 120
   - **Fill:** White
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`

2. Add Issue Number label:
   - **Text:** `varSelectedIssue.IssueNumber`
   - **Font:** 16pt, Bold
   - **Color:** `TextPrimary`
   - **X:** 30
   - **Y:** 110

3. Add Issue Title label:
   - **Text:** `varSelectedIssue.Title`
   - **Font:** 20pt, Bold
   - **Color:** `TextPrimary`
   - **X:** 200
   - **Y:** 110
   - **Width:** 600

4. Add Status badge:
   - **Shape:** Rounded rectangle
   - **X:** 900
   - **Y:** 110
   - **Width:** 100
   - **Height:** 30
   - **Fill:** (Status colour - see colour coding)
   - **Text:** `varSelectedIssue.Status`
   - **Text Color:** White

5. Add Severity badge:
   - **Shape:** Rounded rectangle
   - **X:** 1020
   - **Y:** 110
   - **Width:** 100
   - **Height:** 30
   - **Fill:** (Severity colour - see colour coding)
   - **Text:** `varSelectedIssue.Severity`
   - **Text Color:** White

6. Add issue metadata (Location, Equipment, Reported Date, Assigned To):
   - Insert 4 **Labels** in a row below badges:
     - Label 1: `"Location: " & varSelectedIssue.LocationId.DisplayName`
     - Label 2: `"Equipment: " & If(IsBlank(varSelectedIssue.EquipmentId), "N/A", varSelectedIssue.EquipmentId.ItemName)`
     - Label 3: `"Reported: " & Text(varSelectedIssue.DateCreated, "d mmm yyyy")`
     - Label 4: `"Assigned To: " & If(IsBlank(varSelectedIssue.AssignedTo), "Unassigned", varSelectedIssue.AssignedTo)`

#### Step 4: Create Description Section

1. Insert **Rectangle** for description area:
   - **X:** 20
   - **Y:** 235
   - **Width:** 1326
   - **Height:** 100
   - **Fill:** White
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`

2. Add section title:
   - **Label:** "Description"
   - **Font:** 14pt, Bold
   - **X:** 30
   - **Y:** 245

3. Add description text:
   - **Text Input** (multi-line, read-only)
   - **X:** 30
   - **Y:** 270
   - **Width:** 1300
   - **Height:** 55
   - **Default:** `varSelectedIssue.Description`
   - **Editable:** false
   - **Font:** 12pt

#### Step 5: Create Corrective Actions Section

1. Insert **Rectangle** for actions background:
   - **X:** 20
   - **Y:** 350
   - **Width:** 640
   - **Height:** 350
   - **Fill:** White
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`

2. Add section title:
   - **Label:** "Corrective Actions"
   - **Font:** 14pt, Bold
   - **X:** 30
   - **Y:** 360

3. Create **Gallery** for actions:
   - **X:** 30
   - **Y:** 390
   - **Width:** 600
   - **Height:** 270
   - **Items:** `Filter(CorrectiveAction, IssueId.ID = varSelectedIssueID)`
   - **Layout:** Vertical list
   - **TemplateSize:** Auto

   Inside gallery template add:
   - **Label** (Action Type):
     - **Text:** `ThisItem.ActionType`
     - **Font:** 12pt, Bold
     - **Color:** `TextPrimary`
     - **X:** 5
     - **Y:** 5

   - **Label** (Description):
     - **Text:** `ThisItem.Description`
     - **Font:** 11pt
     - **Color:** `TextPrimary`
     - **X:** 5
     - **Y:** 25

   - **Label** (Notes/Status):
     - **Text:** `If(IsBlank(ThisItem.Notes), "Pending", ThisItem.Notes)`
     - **Font:** 10pt
     - **Color:** `TextSecondary`
     - **X:** 5
     - **Y:** 45

   - Set **TemplateHeight:** 60

4. Add "Add Action" button below gallery:
   - **Button**
   - **X:** 30
   - **Y:** 670
   - **Width:** 130
   - **Height:** 35
   - **Text:** "+ Add Action"
   - **Fill:** `SecondaryColor`
   - **OnSelect:** `Navigate(Dialog_AddAction)`

#### Step 6: Create Comments Section

1. Insert **Rectangle** for comments background:
   - **X:** 700
   - **Y:** 350
   - **Width:** 640
   - **Height:** 350
   - **Fill:** White
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`

2. Add section title:
   - **Label:** "Comments (Newest First)"
   - **Font:** 14pt, Bold
   - **X:** 710
   - **Y:** 360

3. Create **Gallery** for comments:
   - **X:** 710
   - **Y:** 390
   - **Width:** 610
   - **Height:** 270
   - **Items:** `Sort(Filter(IssueComment, IssueId.ID = varSelectedIssueID), DateCreated, Descending)`
   - **Layout:** Vertical list
   - **TemplateSize:** Auto

   Inside gallery template add:
   - **Label** (Author and Date):
     - **Text:** `ThisItem.CommentAuthor & " - " & Text(ThisItem.DateCreated, "d mmm yyyy h:mm am/pm")`
     - **Font:** 11pt, Bold
     - **Color:** `TextPrimary`
     - **X:** 5
     - **Y:** 5

   - **Label** (Comment Text):
     - **Text:** `ThisItem.CommentText`
     - **Font:** 11pt
     - **Color:** `TextPrimary`
     - **X:** 5
     - **Y:** 25
     - **Width:** 580

   - **Button** (Edit - conditional):
     - **Text:** "Edit"
     - **Visible:** `ThisItem.CommentAuthor = User().FullName`
     - **X:** 500
     - **Y:** 50

   - **Button** (Delete - conditional):
     - **Text:** "Delete"
     - **Visible:** `ThisItem.CommentAuthor = User().FullName`
     - **X:** 560
     - **Y:** 50

   - Set **TemplateHeight:** 75

4. Add "Add Comment" button below gallery:
   - **Button**
   - **X:** 710
   - **Y:** 670
   - **Width:** 130
   - **Height:** 35
   - **Text:** "+ Add Comment"
   - **Fill:** `SecondaryColor`
   - **OnSelect:** `Navigate(Dialog_AddComment)`

#### Step 7: Add Action Buttons at Bottom

1. Add "Edit Issue" button:
   - **Button**
   - **X:** 30
   - **Y:** 720
   - **Width:** 100
   - **Height:** 35
   - **Text:** "Edit"
   - **Fill:** `PrimaryColor`
   - **OnSelect:** (See PowerFx)

2. Add "Mark Resolved" button:
   - **Button**
   - **X:** 150
   - **Y:** 720
   - **Width:** 150
   - **Height:** 35
   - **Text:** "Mark Resolved"
   - **Fill:** `SecondaryColor`
   - **OnSelect:** (See PowerFx)

3. Add "Close Issue" button:
   - **Button**
   - **X:** 320
   - **Y:** 720
   - **Width:** 120
   - **Height:** 35
   - **Text:** "Close Issue"
   - **Fill:** `TextSecondary`
   - **OnSelect:** (See PowerFx)

4. Add "Back" button:
   - **Button**
   - **X:** 1220
   - **Y:** 720
   - **Width:** 100
   - **Height:** 35
   - **Text:** "Back"
   - **Fill:** `BorderColor`
   - **OnSelect:** `Navigate(IssueScreen)`

### PowerFx Code

Load issue details on screen visible:

```powerfx
// IssueDetailScreen.OnVisible
// Load selected issue and related data

// Reload issue from SharePoint to ensure fresh data
Set(
    varSelectedIssue,
    LookUp(
        Issue,
        ID = varSelectedIssueID
    )
);

// Preload corrective actions
ClearCollect(
    colIssueActions,
    Filter(
        CorrectiveAction,
        IssueId.ID = varSelectedIssueID
    )
);

// Preload comments in reverse chronological order
ClearCollect(
    colIssueComments,
    Sort(
        Filter(
            IssueComment,
            IssueId.ID = varSelectedIssueID
        ),
        DateCreated,
        Descending
    )
)
```

Mark issue resolved button:

```powerfx
// Button_MarkResolved.OnSelect
Patch(
    Issue,
    varSelectedIssue,
    {
        Status: "Pending_Verification"
    }
);
Set(varSelectedIssue, Patch_Result);
Notify("Issue marked as pending verification", NotificationType.Success);
Refresh(Issue);
Refresh(CorrectiveAction);
Refresh(IssueComment)
```

Close issue button:

```powerfx
// Button_CloseIssue.OnSelect
Patch(
    Issue,
    varSelectedIssue,
    {
        Status: "Closed",
        ResolvedDate: Now()
    }
);
Set(varSelectedIssue, Patch_Result);
Notify("Issue closed", NotificationType.Success);
Navigate(IssueScreen)
```

Edit issue button (for future enhancement):

```powerfx
// Button_EditIssue.OnSelect
Set(varEditMode, true);
Set(varEditingIssueID, varSelectedIssueID);
Navigate(EditIssueScreen)
```

### Verification Checklist

- [ ] IssueDetailScreen created with correct dimensions
- [ ] Issue header displays number, title, status, severity
- [ ] Location and equipment info displays correctly
- [ ] Description displays as multi-line text
- [ ] Corrective Actions gallery displays all actions for issue
- [ ] Each action shows: Type, Description, Status
- [ ] Add Action button navigates to dialog
- [ ] Comments gallery displays in newest-first order
- [ ] Comments show author and timestamp
- [ ] Edit/Delete buttons appear only for own comments
- [ ] Add Comment button navigates to dialog
- [ ] Mark Resolved button updates status
- [ ] Close Issue button closes and returns to list
- [ ] Back button returns to Issue List
- [ ] No overlapping components or text truncation
- [ ] OnVisible event loads data without errors

---

## Add Issue Screen (Tasks 2.7.13-2.7.18)

### Objective

Create a form for logging new issues with Category, Severity, Title, Description fields, and optional Equipment item dropdown filtered by location.

### Prerequisites

- Issue list created
- Location and Equipment lists populated
- Issue number auto-generation configured

### Screen Layout Specification

```
┌─────────────────────────────────────────────────────────────┐
│         HEADER (Navigation Component)                       │
├─────────────────────────────────────────────────────────────┤
│ Add New Issue Form                                           │
├─────────────────────────────────────────────────────────────┤
│ Category: [Equipment ▼]                                      │
│ Severity: [High ▼]                                           │
│                                                              │
│ Title:                                                       │
│ [Defective wheel on trolley in 5C East................]      │
│                                                              │
│ Description:                                                 │
│ [The front left wheel is stuck and cannot rotate......]     │
│ [This is a patient safety hazard.............]              │
│                                                              │
│ Location (Auto-filled):                                      │
│ [5C East ▼]                                                  │
│                                                              │
│ Related Equipment (Optional):                                │
│ [Trolley Wheels ▼]                                           │
│                                                              │
│ [Submit] [Save as Draft] [Cancel]                           │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Instructions

#### Step 1: Create Add Issue Screen

1. Create new screen: "AddIssueScreen"
2. Set properties:
   - **Width:** 1366
   - **Height:** 768
   - **Fill:** `BackgroundColor`

#### Step 2: Add Navigation Header

1. Copy navigation header from HomeScreen
2. Paste at top

#### Step 3: Create Form Container

1. Insert **Rectangle** for form background:
   - **X:** 200
   - **Y:** 120
   - **Width:** 966
   - **Height:** 600
   - **Fill:** White
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`
   - **Radius:** 8px

2. Add form title:
   - **Label:** "Add New Issue"
   - **Font:** 24pt, Bold
   - **Color:** `TextPrimary`
   - **X:** 220
   - **Y:** 140

#### Step 4: Add Category Dropdown

1. Add label:
   - **Text:** "Category"
   - **Font:** 12pt, Bold
   - **X:** 220
   - **Y:** 190

2. Add **Dropdown** control:
   - **X:** 220
   - **Y:** 215
   - **Width:** 430
   - **Height:** 40
   - **Items:** `{"Equipment", "Documentation", "Staffing", "Process", "Safety", "Other"}`
   - **Value:** "Equipment" (default)

#### Step 5: Add Severity Dropdown

1. Add label:
   - **Text:** "Severity"
   - **Font:** 12pt, Bold
   - **X:** 700
   - **Y:** 190

2. Add **Dropdown** control:
   - **X:** 700
   - **Y:** 215
   - **Width:** 430
   - **Height:** 40
   - **Items:** `{"Critical", "High", "Medium", "Low"}`
   - **Value:** "Medium" (default)

#### Step 6: Add Title Field

1. Add label:
   - **Text:** "Title"
   - **Font:** 12pt, Bold
   - **X:** 220
   - **Y:** 270

2. Add **Text Input** control:
   - **X:** 220
   - **Y:** 295
   - **Width:** 910
   - **Height:** 40
   - **Hint text:** "Brief description of issue"
   - **Mode:** SingleLine

#### Step 7: Add Description Field

1. Add label:
   - **Text:** "Description"
   - **Font:** 12pt, Bold
   - **X:** 220
   - **Y:** 350

2. Add **Text Input** control (multi-line):
   - **X:** 220
   - **Y:** 375
   - **Width:** 910
   - **Height:** 100
   - **Hint text:** "Detailed description of the issue and any relevant context"
   - **Mode:** MultiLine

#### Step 8: Add Location Dropdown

1. Add label:
   - **Text:** "Location"
   - **Font:** 12pt, Bold
   - **X:** 220
   - **Y:** 490

2. Add **Dropdown** control:
   - **X:** 220
   - **Y:** 515
   - **Width:** 430
   - **Height:** 40
   - **Items:** `Location`
   - **Value:** `DisplayName`
   - **Required:** true

#### Step 9: Add Equipment Dropdown (Optional)

1. Add label:
   - **Text:** "Related Equipment (Optional)"
   - **Font:** 12pt, Bold
   - **X:** 700
   - **Y:** 490

2. Add **Dropdown** control:
   - **X:** 700
   - **Y:** 515
   - **Width:** 430
   - **Height:** 40
   - **Items:** `Filter(Equipment, LocationId.ID = Dropdown_Location.Selected.ID)` (See PowerFx)
   - **Value:** `ItemName`

#### Step 10: Add Action Buttons

1. Add Submit button:
   - **Button**
   - **X:** 220
   - **Y:** 680
   - **Width:** 120
   - **Height:** 40
   - **Text:** "Submit"
   - **Fill:** `SecondaryColor`
   - **OnSelect:** (See PowerFx)

2. Add Save Draft button:
   - **Button**
   - **X:** 370
   - **Y:** 680
   - **Width:** 140
   - **Height:** 40
   - **Text:** "Save as Draft"
   - **Fill:** `PrimaryColor`
   - **OnSelect:** (See PowerFx)

3. Add Cancel button:
   - **Button**
   - **X:** 530
   - **Y:** 680
   - **Width:** 100
   - **Height:** 40
   - **Text:** "Cancel"
   - **Fill:** `BorderColor`
   - **OnSelect:** `Navigate(IssueScreen)`

### PowerFx Code

Equipment dropdown filtered by location:

```powerfx
// Dropdown_Equipment.Items
// Show only equipment for the selected location

Filter(
    Equipment,
    And(
        IsActive = true,
        Or(
            LocationId.ID = Dropdown_Location.Selected.ID,
            CategoryId.Value = "General"
        )
    )
)
```

Form submission with validation:

```powerfx
// Button_Submit.OnSelect
// Validate and create new issue

If(
    IsBlank(TextInput_Title.Value) || IsBlank(TextInput_Description.Value),
    (
        Notify("Title and Description are required", NotificationType.Error);
        false
    ),
    IsBlank(Dropdown_Location.Value),
    (
        Notify("Location is required", NotificationType.Error);
        false
    ),
    // Form validation passed, create issue
    (
        Patch(
            Issue,
            Defaults(Issue),
            {
                Title: TextInput_Title.Value,
                Description: TextInput_Description.Value,
                Category: Dropdown_Category.Value,
                Severity: Dropdown_Severity.Value,
                LocationId: { ID: Dropdown_Location.Selected.ID },
                EquipmentId: If(
                    IsBlank(Dropdown_Equipment.Selected),
                    Blank(),
                    { ID: Dropdown_Equipment.Selected.ID }
                ),
                Status: "Open",
                DateCreated: Now(),
                CreatedBy: User().FullName,
                AssignedTo: Blank()
            }
        );
        ClearCollect(varNewIssueID, Patch_Result.ID);
        Notify("Issue created successfully", NotificationType.Success);
        Wait(1000);
        Navigate(IssueScreen)
    )
)
```

Save as draft functionality:

```powerfx
// Button_SaveDraft.OnSelect
Patch(
    Issue,
    Defaults(Issue),
    {
        Title: TextInput_Title.Value,
        Description: TextInput_Description.Value,
        Category: Dropdown_Category.Value,
        Severity: Dropdown_Severity.Value,
        LocationId: { ID: Dropdown_Location.Selected.ID },
        EquipmentId: If(
            IsBlank(Dropdown_Equipment.Selected),
            Blank(),
            { ID: Dropdown_Equipment.Selected.ID }
        ),
        Status: "Draft",
        DateCreated: Now(),
        CreatedBy: User().FullName
    }
);
Notify("Draft saved", NotificationType.Success);
Navigate(IssueScreen)
```

### Verification Checklist

- [ ] AddIssueScreen created with form layout
- [ ] Category dropdown displays all 6 categories
- [ ] Severity dropdown displays Critical/High/Medium/Low
- [ ] Title field accepts text input
- [ ] Description field accepts multi-line text
- [ ] Location dropdown filters to active locations
- [ ] Equipment dropdown filters by selected location
- [ ] All required fields validated before submit
- [ ] Submit button creates new issue
- [ ] Save as Draft button creates draft issue
- [ ] Cancel button returns to Issue List
- [ ] Success notification displays after submit
- [ ] Equipment items filtered correctly by location
- [ ] No form submission without required fields

---

## Issue Dialogs (Tasks 2.7.19-2.7.20)

### Objective

Create two modal dialogs for adding corrective actions and comments to issues.

### Task 2.7.19: Add Action Dialog

#### Screen Layout

```
┌────────────────────────────────┐
│ Add Corrective Action          │
├────────────────────────────────┤
│ Action Type:                   │
│ [Immediate/Follow-up/Routine ▼]│
│                                │
│ Description:                   │
│ [Text field..................] │
│                                │
│ Notes/Status:                  │
│ [Text field..................] │
│                                │
│ [Add] [Cancel]                 │
└────────────────────────────────┘
```

#### Step-by-Step Instructions

1. Create new screen: "Dialog_AddAction"
2. Set screen as **Modal**:
   - **Right panel** → Select screen → Turn on **Modal**

3. Add semi-transparent overlay (optional):
   - **Rectangle** covering full screen
   - **Fill:** `RGBA(0, 0, 0, 0.3)`

4. Create dialog box **Rectangle**:
   - **X:** 400
   - **Y:** 250
   - **Width:** 550
   - **Height:** 300
   - **Fill:** White
   - **BorderThickness:** 2
   - **BorderColor:** `PrimaryColor`
   - **Radius:** 8px

5. Add dialog title:
   - **Label:** "Add Corrective Action"
   - **Font:** 16pt, Bold
   - **Color:** `TextPrimary`
   - **X:** 420
   - **Y:** 270

6. Add Action Type dropdown:
   - **Label:** "Action Type"
   - **Dropdown**
   - **Items:** `{"Immediate", "Follow-up", "Routine"}`
   - **X:** 420
   - **Y:** 310
   - **Width:** 510
   - **Height:** 40

7. Add Description field:
   - **Label:** "Description"
   - **Text Input** (MultiLine)
   - **X:** 420
   - **Y:** 370
   - **Width:** 510
   - **Height:** 80

8. Add Notes field:
   - **Label:** "Notes/Status"
   - **Text Input**
   - **X:** 420
   - **Y:** 460
   - **Width:** 510
   - **Height:** 40

9. Add Add button:
   - **Button**
   - **X:** 420
   - **Y:** 520
   - **Width:** 100
   - **Height:** 40
   - **Text:** "Add"
   - **Fill:** `SecondaryColor`
   - **OnSelect:** (See PowerFx)

10. Add Cancel button:
    - **Button**
    - **X:** 830
    - **Y:** 520
    - **Width:** 100
    - **Height:** 40
    - **Text:** "Cancel"
    - **Fill:** `BorderColor`
    - **OnSelect:** `Back()`

#### PowerFx Code

Add action button:

```powerfx
// Button_AddAction.OnSelect
If(
    IsBlank(Dropdown_ActionType.Value),
    (
        Notify("Action Type is required", NotificationType.Error);
        false
    ),
    IsBlank(TextInput_ActionDescription.Value),
    (
        Notify("Description is required", NotificationType.Error);
        false
    ),
    // Create corrective action record
    (
        Patch(
            CorrectiveAction,
            Defaults(CorrectiveAction),
            {
                IssueId: { ID: varSelectedIssueID },
                ActionType: Dropdown_ActionType.Value,
                Description: TextInput_ActionDescription.Value,
                Notes: TextInput_ActionNotes.Value,
                DateCreated: Now(),
                CreatedBy: User().FullName,
                Status: "Open"
            }
        );
        // Refresh collections
        Refresh(CorrectiveAction);
        Refresh(colIssueActions);
        Notify("Action added successfully", NotificationType.Success);
        Reset(Dropdown_ActionType);
        Reset(TextInput_ActionDescription);
        Reset(TextInput_ActionNotes);
        Back()
    )
)
```

### Task 2.7.20: Add Comment Dialog

#### Screen Layout

```
┌────────────────────────────────┐
│ Add Comment                    │
├────────────────────────────────┤
│ Comment:                       │
│ [Multi-line text field.......] │
│ [Multi-line text field.......] │
│                                │
│ [Add] [Cancel]                 │
└────────────────────────────────┘
```

#### Step-by-Step Instructions

1. Create new screen: "Dialog_AddComment"
2. Set screen as **Modal**

3. Add semi-transparent overlay:
   - **Rectangle** covering full screen
   - **Fill:** `RGBA(0, 0, 0, 0.3)`

4. Create dialog box:
   - **X:** 350
   - **Y:** 250
   - **Width:** 650
   - **Height:** 280
   - **Fill:** White
   - **BorderThickness:** 2
   - **BorderColor:** `PrimaryColor`
   - **Radius:** 8px

5. Add dialog title:
   - **Label:** "Add Comment"
   - **Font:** 16pt, Bold
   - **X:** 370
   - **Y:** 270

6. Add Comment field:
   - **Label:** "Comment"
   - **Text Input** (MultiLine)
   - **X:** 370
   - **Y:** 310
   - **Width:** 610
   - **Height:** 120

7. Add Add button:
   - **Button**
   - **X:** 370
   - **Y:** 450
   - **Width:** 100
   - **Height:** 40
   - **Text:** "Add"
   - **Fill:** `SecondaryColor`
   - **OnSelect:** (See PowerFx)

8. Add Cancel button:
   - **Button**
   - **X:** 880
   - **Y:** 450
   - **Width:** 100
   - **Height:** 40
   - **Text:** "Cancel"
   - **Fill:** `BorderColor`
   - **OnSelect:** `Back()`

#### PowerFx Code

Add comment button:

```powerfx
// Button_AddComment.OnSelect
If(
    IsBlank(TextInput_CommentText.Value),
    (
        Notify("Comment cannot be empty", NotificationType.Error);
        false
    ),
    // Create comment record
    (
        Patch(
            IssueComment,
            Defaults(IssueComment),
            {
                IssueId: { ID: varSelectedIssueID },
                CommentText: TextInput_CommentText.Value,
                CommentAuthor: User().FullName,
                DateCreated: Now()
            }
        );
        // Refresh collections
        Refresh(IssueComment);
        Refresh(colIssueComments);
        Notify("Comment added successfully", NotificationType.Success);
        Reset(TextInput_CommentText);
        Back()
    )
)
```

### Verification Checklist - Add Action Dialog

- [ ] Dialog_AddAction screen created as modal
- [ ] Dialog displays correctly with overlay
- [ ] Action Type dropdown shows all options
- [ ] Description field accepts multi-line input
- [ ] Notes field displays
- [ ] Add button creates CorrectiveAction record
- [ ] Validation prevents empty submission
- [ ] Cancel button closes without saving
- [ ] Success notification displays
- [ ] Dialog closes automatically after submit
- [ ] Collections refresh after adding

### Verification Checklist - Add Comment Dialog

- [ ] Dialog_AddComment screen created as modal
- [ ] Dialog displays correctly with overlay
- [ ] Comment field accepts multi-line input
- [ ] Add button creates IssueComment record
- [ ] Validation prevents empty submission
- [ ] Cancel button closes without saving
- [ ] Success notification displays
- [ ] Author/date auto-populated from User()
- [ ] Dialog closes automatically after submit
- [ ] Collections refresh after adding

---

## Data Relationships & Colour Coding

### Issue Data Relationships

```
┌──────────────┐
│   Location   │
└──────────────┘
      △
      │ LocationId (FK)
      │
┌──────────────┐       ┌──────────────┐
│    Issue     │◄─────►│  Equipment   │
└──────────────┘       └──────────────┘
      │                 (Optional FK)
      │
      ├──────► ┌──────────────────┐
      │        │ CorrectiveAction │
      │        └──────────────────┘
      │        (IssueId FK)
      │
      └──────► ┌──────────────────┐
               │  IssueComment    │
               └──────────────────┘
               (IssueId FK)
```

### Status Colour Coding

| Status | Colour | Hex Code | Meaning |
|--------|--------|----------|---------|
| Open | `InfoColor` | #17A2B8 | New issue, not yet assigned |
| In Progress | `AccentColor` | #E55B64 | Being actively worked on |
| Pending Verification | `WarningColor` | #FFC107 | Awaiting review/confirmation |
| Resolved | `SuccessColor` | #28A745 | Issue fixed and verified |
| Closed | `TextSecondary` | #666666 | Issue completed and archived |

### Severity Colour Coding

| Severity | Colour | Hex Code | Meaning |
|----------|--------|----------|---------|
| Critical | `ErrorColor` | #DC3545 | Immediate action required, patient safety risk |
| High | `AccentColor` | #E55B64 | Significant issue, action needed soon |
| Medium | `WarningColor` | #FFC107 | Notable issue, plan resolution |
| Low | `InfoColor` | #17A2B8 | Minor issue, can be scheduled |

### PowerFx Colour Assignment Functions

Status colour formula:

```powerfx
// Returns colour based on status
Switch(
    ThisItem.Status,
    "Open", InfoColor,
    "In Progress", AccentColor,
    "Pending Verification", WarningColor,
    "Resolved", SuccessColor,
    "Closed", TextSecondary,
    TextPrimary
)
```

Severity colour formula:

```powerfx
// Returns colour based on severity
Switch(
    ThisItem.Severity,
    "Critical", ErrorColor,
    "High", AccentColor,
    "Medium", WarningColor,
    "Low", InfoColor,
    TextSecondary
)
```

### Issue Number Auto-Generation

The Issue list should have a calculated column for IssueNumber:

**Formula (in SharePoint):**
```
="ISS-"&YEAR(NOW())&"-"&TEXT([ID],"0000")
```

**Example Results:**
- ISS-2024-0001 (Issue ID 1, Year 2024)
- ISS-2024-0042 (Issue ID 42, Year 2024)
- ISS-2025-0015 (Issue ID 15, Year 2025)

---

## Collections and Variables

### Screen-Level Variables

| Variable | Type | Purpose | Example |
|----------|------|---------|---------|
| `varSelectedIssueID` | Number | ID of currently viewed issue | 42 |
| `varSelectedIssue` | Record | Complete issue record | {ID: 42, Title: "...", ...} |
| `varEditMode` | Boolean | Whether in edit mode | true/false |
| `varEditingIssueID` | Number | ID of issue being edited | 42 |

### Collections

| Collection | Source | Purpose |
|-----------|--------|---------|
| `colFilteredIssues` | Issue list | Filtered and sorted issues |
| `colIssueActions` | CorrectiveAction list | Actions for current issue |
| `colIssueComments` | IssueComment list | Comments for current issue |

### Initialize Collections in App.OnStart

```powerfx
// Initialize empty collections
ClearCollect(colFilteredIssues, Defaults(Issue));
ClearCollect(colIssueActions, Defaults(CorrectiveAction));
ClearCollect(colIssueComments, Defaults(IssueComment));

// Initialize variables
Set(varSelectedIssueID, Blank());
Set(varSelectedIssue, Blank());
Set(varEditMode, false)
```

---

## Phase 2.7 Completion Checklist

### Task 2.7.1-2.7.7: Issue List Screen
- [ ] IssueScreen created with navigation header
- [ ] Status multi-select filter working
- [ ] Severity multi-select filter working
- [ ] Location dropdown filter working
- [ ] Assigned To filter with "My Issues" option working
- [ ] Reset Filters button clears all selections
- [ ] Gallery displays filtered issues
- [ ] Gallery rows colour-coded by severity
- [ ] Age calculation in days displays
- [ ] Total issue count displays
- [ ] Add Issue button navigates to Add Issue screen
- [ ] Gallery row click navigates to Issue Detail

### Task 2.7.8-2.7.12: Issue Detail Screen
- [ ] IssueDetailScreen created
- [ ] Header displays: Issue Number, Title, Status, Severity
- [ ] Location and Equipment info displays
- [ ] Description section displays full text
- [ ] Corrective Actions gallery displays all actions
- [ ] Comments gallery displays in newest-first order
- [ ] Add Action button opens dialog
- [ ] Add Comment button opens dialog
- [ ] Edit/Delete buttons appear only for user's comments
- [ ] Mark Resolved button updates status
- [ ] Close Issue button closes issue
- [ ] Back button returns to list

### Task 2.7.13-2.7.18: Add Issue Screen
- [ ] AddIssueScreen created with form layout
- [ ] Category dropdown working
- [ ] Severity dropdown working
- [ ] Title field required and displays
- [ ] Description field accepts multi-line text
- [ ] Location dropdown required and working
- [ ] Equipment dropdown filters by location
- [ ] Submit button validates and creates issue
- [ ] Save as Draft button creates draft
- [ ] Cancel button returns to list
- [ ] Success notifications display
- [ ] Form clears after submission

### Task 2.7.19-2.7.20: Issue Dialogs
- [ ] Dialog_AddAction created as modal
- [ ] Action Type dropdown working
- [ ] Description field working
- [ ] Notes field working
- [ ] Add button creates CorrectiveAction
- [ ] Cancel button closes dialog
- [ ] Dialog_AddComment created as modal
- [ ] Comment field accepts multi-line text
- [ ] Add button creates IssueComment
- [ ] Cancel button closes dialog
- [ ] Author and date auto-populated

### General Quality Checks
- [ ] All screens use colour variables (not hardcoded)
- [ ] Severity colour coding applied consistently
- [ ] Status colour coding applied consistently
- [ ] No overlapping components
- [ ] All formulas reference correct data sources
- [ ] No console errors or warnings
- [ ] Responsive to different screen sizes
- [ ] Collections initialize without errors
- [ ] Navigation between screens smooth

---

## Common Issues and Troubleshooting

### Issue: Multi-Select Filter Not Working

**Symptom:** Combo Box with SelectMultiple=true not filtering correctly

**Solution:**
1. Verify SelectMultiple property is set to true
2. Check filter formula uses `in` operator for array comparison
3. Verify collection is being updated after filter selection
4. Test with simple filter first: `Status = ComboBox_Status.Value`

### Issue: Gallery Not Updating After Filter Change

**Symptom:** Gallery items don't change when filter is adjusted

**Solution:**
1. Verify gallery Items formula references current filter values
2. Use `ClearCollect` to rebuild collection when filters change
3. Add `Refresh(Issue)` after filter changes
4. Check for circular references in formulas

### Issue: Issue Detail Not Loading

**Symptom:** Issue detail screen shows blank or error

**Solution:**
1. Verify `varSelectedIssueID` is set before navigating
2. Check that issue exists in SharePoint
3. Verify all lookups (LocationId, EquipmentId) are valid
4. Use Power Apps Monitor to debug variable values

### Issue: Comments Not Displaying in Correct Order

**Symptom:** Comments appear in random or oldest-first order

**Solution:**
1. Verify gallery Items formula uses `Sort(..., DateCreated, Descending)`
2. Check DateCreated column has valid timestamp data
3. Clear browser cache and reload app
4. Verify IssueComment records have DateCreated values

### Issue: Edit/Delete Buttons Appear for All Comments

**Symptom:** Users can edit/delete other users' comments

**Solution:**
1. Verify Visible property checks: `ThisItem.CommentAuthor = User().FullName`
2. Ensure User().FullName matches exactly with CommentAuthor field
3. Test with different user accounts
4. Add error handling for permission checks

### Issue: Equipment Dropdown Empty

**Symptom:** Equipment dropdown shows no items

**Solution:**
1. Verify Equipment list has records
2. Check filter formula for LocationId comparison
3. Verify Location dropdown is populated first
4. Test with simple formula: `Equipment` (all items)
5. Check for data type mismatch (GUID vs String)

---

## Performance Optimization Tips

### Gallery Performance

1. **Limit initial load:** Use `FirstN(Filter(...), 50)` to load only first 50 items
2. **Enable virtualization:** Gallery settings → Experimental features → Enable virtualization
3. **Defer data loading:** Load related data (comments, actions) only when needed
4. **Use server-side filtering:** Filter in PowerFx before loading to gallery

### Collection Management

1. **Clear unused collections:** Use `Clear()` when done with collection
2. **Minimize collection size:** Only load needed columns
3. **Use filters instead of collections:** `Filter()` is faster than `ClearCollect()` for large lists
4. **Cache reference data:** Load ServiceLine, Location once in App.OnStart

### Formula Optimization

1. **Avoid nested loops:** Use `FirstN()` instead of counting all rows
2. **Use `LookUp()` instead of `Filter()` when expecting single record**
3. **Pre-calculate summary values:** Don't calculate in gallery template
4. **Use early return in If statements:** Put most likely condition first

---

## Security Considerations

### Data Access Control

1. **Verify user permissions:** Check user has access to issue
2. **Owner-only editing:** Only allow editing own comments
3. **Role-based actions:** Restrict Mark Resolved, Close Issue to admins
4. **Audit trail:** Log all issue modifications
5. **Data validation:** Validate all inputs before submission

### Formula Security

1. **Avoid User() in filters:** Don't trust User().Email alone
2. **Validate dropdown selections:** Ensure selected items exist
3. **Check for injection:** Validate text input for special characters
4. **Use allowlists:** For category, severity, status - use fixed lists

---

## Next Steps

After completing Phase 2.7, proceed with:

### Phase 2.8: Issue Workflow Flows
- Create Power Automate flows for issue status transitions
- Implement notification flows for issue assignment
- Build escalation workflows for aging issues

### Phase 3: Reporting & Analytics
- Create Power BI dashboard for issue analytics
- Build issue trending reports
- Implement issue aging analysis

---

## References

### Related Documentation
- RBWH Data Schema: `RBWH_Resuscitation_Trolley_Audit_Schema.md`
- Task List: `RBWH_Trolley_Audit_Task_List.md`
- Phase 1.6 Foundation: `implementation_guides/phase1_6_powerapp_foundation.md`

### External Resources
- [Power Apps Gallery Control](https://docs.microsoft.com/power-apps/maker/canvas-apps/controls/control-gallery)
- [Power Apps Filters](https://docs.microsoft.com/power-apps/maker/canvas-apps/functions/function-filter-lookup)
- [PowerFx Language Reference](https://docs.microsoft.com/power-platform/power-fx/formula-reference)

### Key Contacts
- **Power Apps Documentation:** https://docs.microsoft.com/power-apps/
- **SharePoint REST API:** https://docs.microsoft.com/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Documentation Team | Initial implementation guide for Phase 2.7 |

---

**Document prepared for:** Royal Brisbane and Women's Hospital - MERT Program
**Document classification:** Internal - Implementation Guide
**Last updated:** January 2026
