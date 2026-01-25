# Phase 2.1 Trolley Management Screens Implementation Guide

**RBWH Resuscitation Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 2.1 establishes comprehensive trolley management functionality within the RBWH Trolley Audit PowerApp. This phase creates a complete Trolley List screen with advanced filtering, sorting, and colour-coded status indicators, along with detailed Trolley Detail screens supporting both view and edit modes, optional equipment configuration, trolley creation workflows, and historical audit tracking.

**Phase Scope:** Tasks 2.1.1 through 2.1.18
**Estimated Duration:** 18 hours
**Prerequisites:** Phase 1.6 must be complete (PowerApp foundation with colour theme, navigation, and data connections)

---

## Colour Theme Reference

All components in Phase 2.1 use the following colour variables (defined in Phase 1.6):

| Colour Variable | Hex Code | Usage |
|-----------------|----------|-------|
| PrimaryColor | #005FAD | Headers, primary buttons, navigation |
| SecondaryColor | #78BE20 | Success states, positive indicators |
| AccentColor | #E35205 | Warnings, attention-required items |
| BackgroundColor | #F5F5F5 | Screen backgrounds, card backgrounds |
| TextPrimary | #333333 | Headings, body text |
| TextSecondary | #666666 | Helper text, captions, secondary info |
| BorderColor | #C8C8C8 | Dividers, borders, separator lines |
| ErrorColor | #E53D3D | Error messages, failed validations |
| SuccessColor | #4CAF50 | Success messages, completed actions |

---

## Task 2.1.1: Create Trolley List Screen

### Objective

Build the primary Trolley List screen displaying all trolley locations with key attributes, audit status, and quick-access actions.

### Prerequisites

- Phase 1.6 completed (app foundation, colour theme, navigation)
- Location SharePoint list populated with 76+ trolley records
- All trolleys have Department Name, Service Line, Building, and Status fields

### Step-by-Step Instructions

#### Step 1: Create New Screen

1. In Power Apps Studio, select **Insert** → **New screen** → **Blank**
2. Name the screen: `TrolleysScreen`
3. Set screen properties:
   - **Width:** 1366
   - **Height:** 688 (account for header at Y:0-80)
   - **Fill:** `BackgroundColor`
   - **Orientation:** Portrait

#### Step 2: Add Screen Title and Breadcrumb

1. Insert a **Label** at top of screen content area:
   - **X:** 20
   - **Y:** 100
   - **Width:** 400
   - **Height:** 40
   - **Text:** "Trolley Management"
   - **Font Size:** 24pt, Bold
   - **Color:** `TextPrimary`
   - **Align:** Left

2. Add a secondary label for description:
   - **X:** 20
   - **Y:** 145
   - **Width:** 600
   - **Height:** 20
   - **Text:** "View, edit, and manage all resuscitation trolley locations"
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`

#### Step 3: Create Filter Bar Container

1. Insert a **Rectangle** as filter container background:
   - **X:** 20
   - **Y:** 175
   - **Width:** 1326
   - **Height:** 70
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 1
   - **Radius:** 4px

2. Add filter label:
   - **X:** 30
   - **Y:** 185
   - **Width:** 100
   - **Height:** 20
   - **Text:** "Filters:"
   - **Font Size:** 12pt, Bold
   - **Color:** `TextPrimary`

#### Step 4: Add Filter Dropdowns

Now add the filter controls. Each control will be positioned horizontally within the filter container.

**Service Line Filter Dropdown:**

1. Insert a **Dropdown** control:
   - **X:** 130
   - **Y:** 183
   - **Width:** 200
   - **Height:** 35
   - **Label:** "Service Line"
   - **Items:**
   ```powerfx
   Table(
       {Value: "", Display: "All Service Lines"},
       Table("Value", "Display", ServiceLine)
   )
   ```

2. Set **Value** property to variable:
   ```powerfx
   If(IsBlank(varServiceLineFilter), "", varServiceLineFilter.Value)
   ```

3. Set **OnChange** event:
   ```powerfx
   Set(varServiceLineFilter, ThisItem);
   Refresh(Location)
   ```

**Building Filter Dropdown:**

1. Insert a **Dropdown** control:
   - **X:** 350
   - **Y:** 183
   - **Width:** 200
   - **Height:** 35
   - **Label:** "Building"
   - **Items:**
   ```powerfx
   Table(
       {Value: "", Display: "All Buildings"},
       {Value: "James Mayne Building", Display: "James Mayne Building"},
       {Value: "Ned Hanlon Building", Display: "Ned Hanlon Building"},
       {Value: "Joyce Tweddell Building", Display: "Joyce Tweddell Building"},
       {Value: "Mental Health Block", Display: "Mental Health Block"},
       {Value: "HIRF Building", Display: "HIRF Building"},
       {Value: "STARS Building", Display: "STARS Building"},
       {Value: "Offsite", Display: "Offsite"}
   )
   ```

2. Set **OnChange** event:
   ```powerfx
   Set(varBuildingFilter, ThisItem.Value);
   Refresh(Location)
   ```

**Status Filter Dropdown:**

1. Insert a **Dropdown** control:
   - **X:** 570
   - **Y:** 183
   - **Width:** 150
   - **Height:** 35
   - **Label:** "Status"
   - **Items:**
   ```powerfx
   Table(
       {Value: "", Display: "All Status"},
       {Value: "Active", Display: "Active"},
       {Value: "Inactive", Display: "Inactive"},
       {Value: "Pending", Display: "Pending"}
   )
   ```

2. Set **OnChange** event:
   ```powerfx
   Set(varStatusFilter, ThisItem.Value);
   Refresh(Location)
   ```

**Days Since Audit Filter:**

1. Insert a **Dropdown** control:
   - **X:** 740
   - **Y:** 183
   - **Width:** 150
   - **Height:** 35
   - **Label:** "Audit Status"
   - **Items:**
   ```powerfx
   Table(
       {Value: "All", Display: "All Trolleys"},
       {Value: "Green", Display: "Recent (<30 days)"},
       {Value: "Yellow", Display: "Pending (30-60 days)"},
       {Value: "Red", Display: "Overdue (>60 days)"}
   )
   ```

2. Set **OnChange** event:
   ```powerfx
   Set(varAuditStatusFilter, ThisItem.Value);
   Refresh(Location)
   ```

**Clear Filters Button:**

1. Insert a **Button**:
   - **X:** 910
   - **Y:** 183
   - **Width:** 130
   - **Height:** 35
   - **Text:** "Clear Filters"
   - **Fill:** `BorderColor`
   - **TextColor:** `TextPrimary`
   - **Font Size:** 11pt

2. Set **OnSelect** event:
   ```powerfx
   Set(varServiceLineFilter, Blank());
   Set(varBuildingFilter, "");
   Set(varStatusFilter, "");
   Set(varAuditStatusFilter, "All");
   Set(varSearchText, "");
   Refresh(Location)
   ```

#### Step 5: Add Search Box

1. Insert a **Text input** control for search:
   - **X:** 1060
   - **Y:** 183
   - **Width:** 280
   - **Height:** 35
   - **Placeholder:** "Search by name or building..."
   - **Mode:** SingleLine

2. Set **OnChange** event:
   ```powerfx
   Set(varSearchText, Self.Value);
   Refresh(Location)
   ```

#### Step 6: Create Table/Gallery for Trolley List

1. Insert a **Data table** control (or gallery for more customization):
   - **X:** 20
   - **Y:** 260
   - **Width:** 1326
   - **Height:** 380
   - **BorderThickness:** 1
   - **BorderColor:** `BorderColor`
   - **Radius:** 4px

2. Set the **Items** property to include filters:
   ```powerfx
   Sort(
       Filter(
           Location,
           (IsBlank(varServiceLineFilter) Or ServiceLine.Value = varServiceLineFilter.Value) And
           (IsBlank(varBuildingFilter) Or varBuildingFilter = Building) And
           (IsBlank(varStatusFilter) Or varStatusFilter = Status) And
           (
               If(
                   varAuditStatusFilter = "All",
                   true,
                   varAuditStatusFilter = "Green",
                   DaysSinceLastAudit < 30 Or IsBlank(DaysSinceLastAudit),
                   varAuditStatusFilter = "Yellow",
                   And(DaysSinceLastAudit >= 30, DaysSinceLastAudit < 60),
                   varAuditStatusFilter = "Red",
                   DaysSinceLastAudit >= 60
               )
           ) And
           (
               IsBlank(varSearchText) Or
               ContainsIgnoreCase(Title, varSearchText) Or
               ContainsIgnoreCase(DisplayName, varSearchText) Or
               ContainsIgnoreCase(Building, varSearchText)
           )
       ),
       Title,
       Ascending
   )
   ```

#### Step 7: Configure Table Columns

Configure these columns in the data table:

| Column | Source Field | Width | Notes |
|--------|--------------|-------|-------|
| Department | Title | 200 | Primary identifier |
| Building | Building | 150 | Location building |
| Service Line | ServiceLine | 140 | Service line name |
| Status | Status | 80 | Active/Inactive |
| Last Audit | LastAuditDate | 120 | Format as date |
| Days Since | DaysSinceLastAudit | 100 | Numeric value |
| Compliance | LastAuditCompliance | 100 | Format as % |
| Issues | (Calculated) | 80 | Count open issues |
| Actions | (Buttons) | 150 | View/Edit/Audit |

#### Step 8: Add Row Colour Coding (Days Since Audit)

For each table row, add conditional formatting based on audit recency:

1. Select the table row fill or add a rectangle behind rows
2. Set **Fill** property:
   ```powerfx
   If(
       IsBlank(DaysSinceLastAudit),
       RGBA(255, 200, 200, 0.3),  // Light red for never audited
       DaysSinceLastAudit < 30,
       RGBA(120, 190, 32, 0.2),   // Light green for <30 days
       DaysSinceLastAudit < 60,
       RGBA(255, 200, 0, 0.2),    // Light yellow for 30-60 days
       RGBA(229, 61, 61, 0.2)     // Light red for >60 days
   )
   ```

#### Step 9: Add Action Buttons to Table

In the Actions column, add three buttons per row:

**View Button:**
```powerfx
Button(
    Text: "View",
    Fill: PrimaryColor,
    TextColor: White,
    OnSelect: Set(varSelectedTrolley, ThisItem); Navigate(TrolleyDetailScreen, ScreenTransition.Fade)
)
```

**Edit Button (MERT Only):**
```powerfx
If(
    User().Email in colMERTEducators,
    Button(
        Text: "Edit",
        Fill: SecondaryColor,
        TextColor: White,
        OnSelect: Set(varSelectedTrolley, ThisItem); Set(varEditMode, true); Navigate(TrolleyDetailScreen, ScreenTransition.Fade)
    ),
    Blank()
)
```

**Audit Button:**
```powerfx
Button(
    Text: "Audit",
    Fill: AccentColor,
    TextColor: White,
    OnSelect: Set(varSelectedTrolley, ThisItem); Navigate(AuditSelectionScreen, ScreenTransition.Fade)
)
```

#### Step 10: Add List Statistics Panel

1. Add a **Rectangle** below the table for statistics:
   - **X:** 20
   - **Y:** 650
   - **Width:** 1326
   - **Height:** 30
   - **Fill:** `BackgroundColor`

2. Add labels showing:
   - **Total Trolleys:** `CountRows(Filter(Location, Status = "Active"))`
   - **Overdue Audits:** `CountRows(Filter(Location, DaysSinceLastAudit > 60))`
   - **Recent Audits:** `CountRows(Filter(Location, And(Status = "Active", DaysSinceLastAudit < 30)))`

### PowerFx Code

Complete formula for Trolley List Items with advanced filtering:

```powerfx
// Trolley List Gallery/Table Items Property
Sort(
    Filter(
        Location,
        // Service Line Filter
        If(
            IsBlank(varServiceLineFilter),
            true,
            ServiceLine.Value = varServiceLineFilter.Value
        ) And
        // Building Filter
        If(
            IsBlank(varBuildingFilter) Or varBuildingFilter = "",
            true,
            Building = varBuildingFilter
        ) And
        // Status Filter
        If(
            IsBlank(varStatusFilter) Or varStatusFilter = "",
            true,
            Status = varStatusFilter
        ) And
        // Audit Status Filter (Days Since Last Audit)
        If(
            varAuditStatusFilter = "All" Or IsBlank(varAuditStatusFilter),
            true,
            varAuditStatusFilter = "Green",
            Or(DaysSinceLastAudit < 30, IsBlank(DaysSinceLastAudit)),
            varAuditStatusFilter = "Yellow",
            And(DaysSinceLastAudit >= 30, DaysSinceLastAudit < 60),
            varAuditStatusFilter = "Red",
            DaysSinceLastAudit >= 60
        ) And
        // Search Filter
        If(
            IsBlank(varSearchText) Or varSearchText = "",
            true,
            Or(
                ContainsIgnoreCase(Title, varSearchText),
                ContainsIgnoreCase(DisplayName, varSearchText),
                ContainsIgnoreCase(Building, varSearchText),
                ContainsIgnoreCase(ServiceLine, varSearchText)
            )
        ) And
        // Always show active trolleys
        Status = "Active"
    ),
    Title,
    Ascending
)
```

Colour coding formula for row highlighting:

```powerfx
// Audit Status Row Colour
If(
    IsBlank(ThisItem.DaysSinceLastAudit) Or ThisItem.DaysSinceLastAudit > 999,
    // Never audited - red
    RGBA(229, 61, 61, 0.15),
    ThisItem.DaysSinceLastAudit < 30,
    // Recently audited - green
    RGBA(76, 175, 80, 0.15),
    ThisItem.DaysSinceLastAudit < 60,
    // Pending audit - yellow
    RGBA(255, 193, 7, 0.15),
    // Overdue - red
    RGBA(229, 61, 61, 0.15)
)
```

Global variable initialization in App.OnStart (add to existing OnStart):

```powerfx
// Trolley List Screen Variables
Set(varServiceLineFilter, Blank());
Set(varBuildingFilter, "");
Set(varStatusFilter, "");
Set(varAuditStatusFilter, "All");
Set(varSearchText, "");
Set(varSelectedTrolley, Blank());
Set(varEditMode, false);

// MERT Educators collection (for permission checks)
ClearCollect(
    colMERTEducators,
    {"Email": "mert.educator@rbwh.health.qld.gov.au"},
    {"Email": User().Email}
)
```

### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Screen | Width | 1366 |
| | Height | 688 |
| | Fill | BackgroundColor |
| Title Label | Font Size | 24pt, Bold |
| | Color | TextPrimary |
| Filter Container | Width | 1326 |
| | Height | 70 |
| | Fill | White |
| Service Line Dropdown | Width | 200 |
| Building Dropdown | Width | 200 |
| Status Dropdown | Width | 150 |
| Audit Status Dropdown | Width | 150 |
| Search Box | Width | 280 |
| Trolley Table | Width | 1326 |
| | Height | 380 |
| | Columns | 9 (see table above) |
| Row Colour | Conditional | Based on DaysSinceLastAudit |

### Verification Checklist

- [ ] TrolleysScreen created and accessible from navigation
- [ ] Filter bar displays all 5 filter controls
- [ ] Service Line dropdown populated with unique service lines
- [ ] Building dropdown shows all 8 building options
- [ ] Status dropdown shows Active/Inactive/Pending
- [ ] Audit Status dropdown shows all 4 options
- [ ] Search box accepts text input
- [ ] Clear Filters button resets all filters
- [ ] Trolley table displays 20+ records initially
- [ ] Table shows all 9 required columns
- [ ] Row colours change based on DaysSinceLastAudit value
- [ ] Records filter correctly when filters are selected
- [ ] Search works across department name and building
- [ ] Sort order is alphabetical by department name
- [ ] Statistics panel displays correct counts
- [ ] View/Edit/Audit buttons present and functional
- [ ] No errors in formula bar

---

## Task 2.1.2: Add ServiceLine Filter Dropdown

### Objective

Implement a Service Line filter that dynamically populates from the ServiceLine list and filters the trolley gallery.

### Prerequisites

- Task 2.1.1 completed (Trolley List screen created)
- ServiceLine SharePoint list connected with 7 records

### Step-by-Step Instructions

#### Step 1: Verify ServiceLine List Connection

1. In Data panel, verify ServiceLine list appears and contains these service lines:
   - Surgical & Perioperative Services
   - Internal Medicine Services
   - Women's & Newborn Services
   - Cancer Care Services
   - Mental Health
   - Critical Care & Clinical Support Services
   - Allied Health

#### Step 2: Update Dropdown Items Formula

1. Select the Service Line dropdown (created in Task 2.1.1)
2. Set the **Items** property to:
   ```powerfx
   Distinct(ServiceLine, Title)
   ```

3. This creates a sorted list of unique service lines from the lookup field

#### Step 3: Set Dropdown Default Selection

1. Select the dropdown control
2. Set **Default** property:
   ```powerfx
   If(
       IsBlank(varServiceLineFilter),
       Blank(),
       varServiceLineFilter.Value
   )
   ```

#### Step 4: Update Filter Logic to Use Lookup

1. In the trolley gallery Items formula (from Task 2.1.1), update the Service Line portion:
   ```powerfx
   If(
       IsBlank(varServiceLineFilter),
       true,
       ServiceLine.Value = varServiceLineFilter.Value
   )
   ```

This ensures the filter correctly compares the lookup field value.

#### Step 5: Add Display Name to Dropdown

1. Select the dropdown
2. Set **AllowSearching** to `true` (enables search within dropdown)
3. Set **SearchPlaceholder** to "Search service line..."

### PowerFx Code

Complete Service Line filter formula:

```powerfx
// Service Line Dropdown Items
// Load distinct service lines from Location records
Distinct(Location, ServiceLine)

// Service Line Dropdown OnChange
Set(varServiceLineFilter, If(IsBlank(ThisItem.Value), Blank(), ThisItem));
Set(varCurrentPage, 1);  // Reset to first page when filter changes
Refresh(Location)

// Filter logic in Gallery/Table Items (portion for Service Line)
If(
    IsBlank(varServiceLineFilter),
    true,
    And(
        Not(IsBlank(ServiceLine)),
        ServiceLine.Value = varServiceLineFilter.Value
    )
)
```

### Verification Checklist

- [ ] Service Line dropdown displays all 7 unique service lines
- [ ] Dropdown defaults to "All" or blank when no selection
- [ ] Search feature works in dropdown
- [ ] Selecting a service line filters trolley table
- [ ] Filtering shows only trolleys in selected service line
- [ ] Count updates to show filtered results
- [ ] Can select multiple service lines (if using multi-select variant)
- [ ] Filter persists when scrolling table
- [ ] No errors in formula bar
- [ ] Clear Filters button resets service line selection

---

## Task 2.1.3: Add Building Filter Dropdown

### Objective

Implement Building filter with all 8 RBWH buildings/locations, filtering trolley list accordingly.

### Prerequisites

- Task 2.1.1-2.1.2 completed

### Step-by-Step Instructions

#### Step 1: Verify Building Values

1. Review existing seed data for valid building values:
   - James Mayne Building
   - Ned Hanlon Building
   - Joyce Tweddell Building
   - Mental Health Block
   - HIRF Building
   - STARS Building
   - Offsite
   - (Future: Any additional buildings)

#### Step 2: Create Building Dropdown Items

1. Select the Building dropdown (created in Task 2.1.1)
2. Verify **Items** property contains:
   ```powerfx
   Table(
       {Value: "", Display: "All Buildings"},
       {Value: "James Mayne Building", Display: "James Mayne Building"},
       {Value: "Ned Hanlon Building", Display: "Ned Hanlon Building"},
       {Value: "Joyce Tweddell Building", Display: "Joyce Tweddell Building"},
       {Value: "Mental Health Block", Display: "Mental Health Block"},
       {Value: "HIRF Building", Display: "HIRF Building"},
       {Value: "STARS Building", Display: "STARS Building"},
       {Value: "Offsite", Display: "Offsite"}
   )
   ```

#### Step 3: Set Dropdown Change Handler

1. Set **OnChange** event:
   ```powerfx
   Set(varBuildingFilter, ThisItem.Value);
   Set(varCurrentPage, 1);
   Refresh(Location)
   ```

#### Step 4: Update Gallery Filter Logic

1. Ensure gallery Items formula includes:
   ```powerfx
   If(
       IsBlank(varBuildingFilter) Or varBuildingFilter = "",
       true,
       Building = varBuildingFilter
   )
   ```

#### Step 5: Add Building Count Summary

1. Add a label below the filter showing building count:
   - **Text:**
   ```powerfx
   "Trolleys in " & If(IsBlank(varBuildingFilter), "all buildings: ", varBuildingFilter & ": ") &
   CountRows(
       Filter(
           Location,
           If(IsBlank(varBuildingFilter), true, Building = varBuildingFilter)
       )
   )
   ```

### PowerFx Code

Building filter implementation:

```powerfx
// Building Dropdown Items
Table(
    {Value: "", Display: "All Buildings"},
    {Value: "James Mayne Building", Display: "James Mayne Building"},
    {Value: "Ned Hanlon Building", Display: "Ned Hanlon Building"},
    {Value: "Joyce Tweddell Building", Display: "Joyce Tweddell Building"},
    {Value: "Mental Health Block", Display: "Mental Health Block"},
    {Value: "HIRF Building", Display: "HIRF Building"},
    {Value: "STARS Building", Display: "STARS Building"},
    {Value: "Offsite", Display: "Offsite"}
)

// Building Dropdown OnChange
Set(varBuildingFilter, ThisItem.Value);
Set(varCurrentPage, 1);
Refresh(Location)

// Building Filter Logic (in gallery Items)
If(
    IsBlank(varBuildingFilter) Or varBuildingFilter = "",
    true,
    Building = varBuildingFilter
)
```

### Verification Checklist

- [ ] Building dropdown displays all 8 building options
- [ ] Dropdown defaults to "All Buildings"
- [ ] Selecting a building filters trolley table correctly
- [ ] Count shows correct number of trolleys per building
- [ ] Can combine with Service Line filter
- [ ] Building filter persists across page navigation
- [ ] Clear Filters button resets building selection
- [ ] No errors in formula bar

---

## Task 2.1.4: Add Status Filter Dropdown

### Objective

Implement Status filter showing Active/Inactive/Pending trolleys with proper filtering logic.

### Prerequisites

- Task 2.1.1-2.1.3 completed

### Step-by-Step Instructions

#### Step 1: Set Status Filter Items

1. Select Status dropdown
2. Set **Items** property:
   ```powerfx
   Table(
       {Value: "", Display: "All Status"},
       {Value: "Active", Display: "Active"},
       {Value: "Inactive", Display: "Inactive"},
       {Value: "Pending", Display: "Pending"}
   )
   ```

#### Step 2: Configure Change Handler

1. Set **OnChange**:
   ```powerfx
   Set(varStatusFilter, ThisItem.Value);
   Set(varCurrentPage, 1);
   Refresh(Location)
   ```

#### Step 3: Update Gallery Filter

1. Ensure gallery Items includes status filter:
   ```powerfx
   If(
       IsBlank(varStatusFilter) Or varStatusFilter = "",
       true,
       Status = varStatusFilter
   )
   ```

#### Step 4: Add Status Badges to Rows

1. In each table row, add a status indicator badge:
   - Create small rectangle with conditional fill:
   ```powerfx
   If(
       Status = "Active",
       SecondaryColor,
       Status = "Inactive",
       BorderColor,
       AccentColor  // Pending
   )
   ```

2. Add text label showing status:
   ```powerfx
   Status
   ```

### PowerFx Code

Status filter implementation:

```powerfx
// Status Dropdown Items
Table(
    {Value: "", Display: "All Status"},
    {Value: "Active", Display: "Active"},
    {Value: "Inactive", Display: "Inactive"},
    {Value: "Pending", Display: "Pending"}
)

// Status Dropdown OnChange
Set(varStatusFilter, ThisItem.Value);
Set(varCurrentPage, 1);
Refresh(Location)

// Status Filter Logic
If(
    IsBlank(varStatusFilter) Or varStatusFilter = "",
    true,
    Status = varStatusFilter
)

// Status Badge Fill (for row indicator)
If(
    ThisItem.Status = "Active",
    SecondaryColor,      // Green
    ThisItem.Status = "Inactive",
    ErrorColor,          // Red
    ThisItem.Status = "Pending",
    WarningColor,        // Orange
    BorderColor          // Grey fallback
)
```

### Verification Checklist

- [ ] Status dropdown shows All/Active/Inactive/Pending options
- [ ] Filter correctly shows only selected status trolleys
- [ ] Active trolleys dominate the list by default
- [ ] Can filter to show only inactive trolleys (MERT cleanup)
- [ ] Status badges display correct colour coding
- [ ] Can combine Status filter with Building and Service Line
- [ ] Clearing filters shows all trolleys again
- [ ] No errors in formula

---

## Task 2.1.5: Add Search Box Functionality

### Objective

Implement text search box allowing users to search trolleys by name, department, building, or service line.

### Prerequisites

- Task 2.1.1-2.1.4 completed

### Step-by-Step Instructions

#### Step 1: Update Search Input Properties

1. Select the search text input (created in Task 2.1.1)
2. Set properties:
   - **Mode:** SingleLine
   - **Placeholder:** "Search by name or building..."
   - **Font Size:** 12pt
   - **ClearIndicator:** true (allows one-click clear)
   - **RadiusBottomLeft:** 4px
   - **RadiusBottomRight:** 4px

#### Step 2: Create OnChange Handler

1. Set **OnChange** event:
   ```powerfx
   Set(varSearchText, Lower(Trim(Self.Value)));
   Set(varCurrentPage, 1);
   Refresh(Location)
   ```

Note: Using `Lower()` and `Trim()` for better matching

#### Step 3: Update Gallery Filter for Search

1. In gallery Items formula, add search condition:
   ```powerfx
   If(
       IsBlank(varSearchText) Or varSearchText = "",
       true,
       Or(
           ContainsIgnoreCase(Title, varSearchText),
           ContainsIgnoreCase(DisplayName, varSearchText),
           ContainsIgnoreCase(Building, varSearchText),
           ContainsIgnoreCase(ServiceLine.Value, varSearchText)
       )
   )
   ```

#### Step 4: Add Real-Time Search Results Counter

1. Add a label next to search box:
   - **X:** 1060
   - **Y:** 225
   - **Width:** 280
   - **Height:** 20
   - **Text:**
   ```powerfx
   If(
       IsBlank(varSearchText),
       "Showing all trolleys",
       CountRows(
           Filter(
               Location,
               Or(
                   ContainsIgnoreCase(Title, varSearchText),
                   ContainsIgnoreCase(DisplayName, varSearchText),
                   ContainsIgnoreCase(Building, varSearchText)
               )
           )
       ) & " trolleys found"
   )
   ```

#### Step 5: Add "No Results" Message

1. Add label below gallery:
   - **Visible:**
   ```powerfx
   And(
       Not(IsBlank(varSearchText)),
       CountRows(
           Filter(
               Location,
               Or(
                   ContainsIgnoreCase(Title, varSearchText),
                   ContainsIgnoreCase(DisplayName, varSearchText),
                   ContainsIgnoreCase(Building, varSearchText)
               )
           )
       ) = 0
   )
   ```
   - **Text:** "No trolleys match your search. Try a different term."
   - **Color:** `ErrorColor`

### PowerFx Code

Complete search implementation:

```powerfx
// Search Box OnChange
Set(varSearchText, Lower(Trim(Self.Value)));
Set(varCurrentPage, 1);
Refresh(Location)

// Gallery Items - Search Filter Portion
If(
    IsBlank(varSearchText) Or varSearchText = "",
    true,
    Or(
        ContainsIgnoreCase(Title, varSearchText),
        ContainsIgnoreCase(DisplayName, varSearchText),
        ContainsIgnoreCase(Building, varSearchText),
        ContainsIgnoreCase(ServiceLine.Value, varSearchText)
    )
)

// Search Results Counter Text
If(
    IsBlank(varSearchText),
    "Showing all active trolleys",
    CountRows(
        Filter(
            Location,
            Status = "Active" And Or(
                ContainsIgnoreCase(Title, varSearchText),
                ContainsIgnoreCase(DisplayName, varSearchText),
                ContainsIgnoreCase(Building, varSearchText)
            )
        )
    ) & " trolleys found"
)
```

### Verification Checklist

- [ ] Search box appears to right of filters
- [ ] Typing in search box filters trolleys in real-time
- [ ] Search works across department name, display name, building
- [ ] Results counter shows correct count
- [ ] "No results" message appears when search returns 0 trolleys
- [ ] Clearing search box shows all trolleys again
- [ ] Search is case-insensitive
- [ ] Extra spaces are trimmed
- [ ] Can combine search with other filters
- [ ] Performance acceptable with 76 trolleys

---

## Task 2.1.6: Add Sort Functionality

### Objective

Implement sorting capability allowing users to sort trolley list by multiple columns: Department name, Last Audit Date, Days Since Audit, Compliance Score.

### Prerequisites

- Task 2.1.1-2.1.5 completed

### Step-by-Step Instructions

#### Step 1: Add Sort Column Headers

1. In the table header row, add clickable sort buttons for each column:
   - Department Name
   - Building
   - Service Line
   - Last Audit Date
   - Days Since Audit
   - Compliance Score

#### Step 2: Create Sort Variables

1. Add to App.OnStart:
   ```powerfx
   Set(varSortColumn, "Title");      // Default sort by department name
   Set(varSortAscending, true);       // Default ascending order
   ```

#### Step 3: Create Column Header Sort Button

1. Create a button/label template for each sortable column:
   - **Text:** Column name + sort arrow
   - **OnSelect:**
   ```powerfx
   If(
       varSortColumn = "DaysSinceLastAudit",
       Set(varSortAscending, Not(varSortAscending)),
       Set(varSortColumn, "DaysSinceLastAudit");
       Set(varSortAscending, false)
   );
   Refresh(Location)
   ```

#### Step 4: Update Gallery Sort Formula

1. Update gallery Items formula to use sort variables:
   ```powerfx
   Sort(
       Filter(...),  // All filter logic from previous tasks
       If(varSortColumn = "Title", Title,
          varSortColumn = "LastAuditDate", LastAuditDate,
          varSortColumn = "DaysSinceLastAudit", DaysSinceLastAudit,
          varSortColumn = "LastAuditCompliance", LastAuditCompliance,
          varSortColumn = "Building", Building,
          Title),
       If(varSortAscending, Ascending, Descending)
   )
   ```

#### Step 5: Add Sort Direction Indicator

1. Add up/down arrow next to active sort column:
   ```powerfx
   If(
       varSortColumn = ThisColumn.Name,
       If(varSortAscending, " ▲", " ▼"),
       ""
   )
   ```

#### Step 6: Implement Multi-Sort Options (Optional)

1. Add dropdown for "Sort by":
   ```powerfx
   Table(
       {Value: "Title", Display: "Department Name (A-Z)"},
       {Value: "LastAuditDate", Display: "Last Audit (Newest First)"},
       {Value: "DaysSinceLastAudit", Display: "Days Since Audit (Most Overdue)"},
       {Value: "LastAuditCompliance", Display: "Compliance Score (Lowest First)"},
       {Value: "Building", Display: "Building (A-Z)"}
   )
   ```

### PowerFx Code

Complete sort implementation:

```powerfx
// Sort Variables (in App.OnStart)
Set(varSortColumn, "Title");
Set(varSortAscending, true);

// Column Header OnSelect (example for Department Name)
If(
    varSortColumn = "Title",
    Set(varSortAscending, Not(varSortAscending)),
    Set(varSortColumn, "Title");
    Set(varSortAscending, true)
);
Refresh(Location)

// Gallery/Table Items with Sort
Sort(
    Filter(
        Location,
        // All filter conditions from previous tasks
        (IsBlank(varServiceLineFilter) Or ServiceLine.Value = varServiceLineFilter.Value) And
        (IsBlank(varBuildingFilter) Or varBuildingFilter = Building) And
        (IsBlank(varStatusFilter) Or varStatusFilter = Status) And
        (IsBlank(varSearchText) Or Or(
            ContainsIgnoreCase(Title, varSearchText),
            ContainsIgnoreCase(DisplayName, varSearchText),
            ContainsIgnoreCase(Building, varSearchText)
        ))
    ),
    // Sort column selection
    If(
        varSortColumn = "Title", Title,
        varSortColumn = "LastAuditDate", LastAuditDate,
        varSortColumn = "DaysSinceLastAudit", DaysSinceLastAudit,
        varSortColumn = "LastAuditCompliance", LastAuditCompliance,
        varSortColumn = "Building", Building,
        Title
    ),
    // Sort direction
    If(varSortAscending, Ascending, Descending)
)

// Sort Direction Indicator Text (in column header)
If(
    varSortColumn = "DaysSinceLastAudit",
    If(varSortAscending, " ▲", " ▼"),
    ""
)
```

### Verification Checklist

- [ ] Column headers are clickable
- [ ] Default sort is by Department Name (A-Z)
- [ ] Clicking column header sorts by that column
- [ ] Clicking again reverses sort direction
- [ ] Sort arrow (▲/▼) appears next to active sort column
- [ ] Can sort by all 5 specified columns
- [ ] Sort persists when filters change
- [ ] Sorting works correctly with filtered results
- [ ] Performance acceptable with sort on 76 records

---

## Task 2.1.7: Implement Colour Coding for Audit Status

### Objective

Add colour-coded row backgrounds and status indicators showing audit recency: green for <30 days, yellow for 30-60 days, red for >60 days (never audited).

### Prerequisites

- Task 2.1.1-2.1.6 completed
- Colour variables available in app

### Step-by-Step Instructions

#### Step 1: Create Row Background Colour Formula

1. For each table row, set **Fill** property:
   ```powerfx
   If(
       Or(IsBlank(ThisItem.DaysSinceLastAudit), ThisItem.DaysSinceLastAudit > 999),
       // Never audited - light red
       RGBA(229, 61, 61, 0.15),
       ThisItem.DaysSinceLastAudit < 30,
       // Recently audited (<30 days) - light green
       RGBA(76, 175, 80, 0.15),
       And(ThisItem.DaysSinceLastAudit >= 30, ThisItem.DaysSinceLastAudit < 60),
       // Pending audit (30-60 days) - light yellow
       RGBA(255, 193, 7, 0.15),
       // Overdue audit (>60 days) - light red
       RGBA(229, 61, 61, 0.15)
   )
   ```

#### Step 2: Add Status Badge to "Days Since Audit" Column

1. In the table cell for "Days Since Audit", add:
   - A small coloured square/circle indicator
   - The numeric value
   - Optional: Days calculation

2. Set the badge **Fill**:
   ```powerfx
   If(
       Or(IsBlank(ThisItem.DaysSinceLastAudit), ThisItem.DaysSinceLastAudit > 999),
       ErrorColor,          // Red for never audited
       ThisItem.DaysSinceLastAudit < 30,
       SuccessColor,        // Green for recent
       ThisItem.DaysSinceLastAudit < 60,
       WarningColor,        // Yellow for pending
       ErrorColor           // Red for overdue
   )
   ```

#### Step 3: Add Audit Status Label

1. Add label next to days value showing status:
   ```powerfx
   If(
       Or(IsBlank(ThisItem.DaysSinceLastAudit), ThisItem.DaysSinceLastAudit > 999),
       "Never Audited",
       ThisItem.DaysSinceLastAudit < 30,
       "Green",
       ThisItem.DaysSinceLastAudit < 60,
       "Yellow",
       "Red"
   )
   ```

#### Step 4: Create Colour Legend

1. Add a legend above the table explaining the colour scheme:
   - Green box: "Audited within 30 days"
   - Yellow box: "Audited 30-60 days ago"
   - Red box: "Audited over 60 days ago or never"

2. Legend code:
   ```powerfx
   // Create as static labels with coloured rectangles
   Label1.Text = "● Green = <30 days"
   Label1.Color = SuccessColor

   Label2.Text = "● Yellow = 30-60 days"
   Label2.Color = WarningColor

   Label3.Text = "● Red = >60 days or never audited"
   Label3.Color = ErrorColor
   ```

#### Step 5: Add Hover Effect for Row

1. Optional: Add hover effect to highlight row on mouseover
   ```powerfx
   // Row Hover Fill
   If(
       HoverRow,
       RGBA(0, 0, 0, 0.05),  // Very light overlay on hover
       <previous fill formula>
   )
   ```

#### Step 6: Add Summary Stats by Colour

1. Below the table, add counts:
   ```powerfx
   CountRows(Filter(Location, Status = "Active", DaysSinceLastAudit < 30)) & " trolleys recently audited (green)"
   CountRows(Filter(Location, Status = "Active", And(DaysSinceLastAudit >= 30, DaysSinceLastAudit < 60))) & " trolleys pending audit (yellow)"
   CountRows(Filter(Location, Status = "Active", DaysSinceLastAudit >= 60)) & " trolleys overdue (red)"
   ```

### PowerFx Code

Complete colour coding implementation:

```powerfx
// Row Fill - Main Colour Coding
If(
    Or(IsBlank(ThisItem.DaysSinceLastAudit), ThisItem.DaysSinceLastAudit > 999),
    // Never audited or invalid
    RGBA(229, 61, 61, 0.12),        // Red @ 12% opacity
    ThisItem.DaysSinceLastAudit < 30,
    // Recently audited (< 30 days) - GOOD
    RGBA(76, 175, 80, 0.12),        // Green @ 12% opacity
    And(ThisItem.DaysSinceLastAudit >= 30, ThisItem.DaysSinceLastAudit < 60),
    // Pending audit (30-60 days) - WARNING
    RGBA(255, 193, 7, 0.12),        // Amber @ 12% opacity
    // Overdue audit (> 60 days) - CRITICAL
    RGBA(229, 61, 61, 0.12)         // Red @ 12% opacity
)

// Status Indicator Badge Fill
If(
    Or(IsBlank(ThisItem.DaysSinceLastAudit), ThisItem.DaysSinceLastAudit > 999),
    ErrorColor,                      // Red
    ThisItem.DaysSinceLastAudit < 30,
    SuccessColor,                    // Green
    ThisItem.DaysSinceLastAudit < 60,
    WarningColor,                    // Orange/Amber
    ErrorColor                       // Red
)

// Status Text Label
If(
    Or(IsBlank(ThisItem.DaysSinceLastAudit), ThisItem.DaysSinceLastAudit > 999),
    "Never Audited",
    ThisItem.DaysSinceLastAudit < 30,
    "Green (Recent)",
    ThisItem.DaysSinceLastAudit < 60,
    "Yellow (Pending)",
    "Red (Overdue)"
)

// Days Since Audit Display with Status
ThisItem.DaysSinceLastAudit & If(IsBlank(ThisItem.DaysSinceLastAudit), " days", " days ago")

// Legend Labels (static)
"● Green = Recently audited (<30 days)"
"● Yellow = Pending audit (30-60 days)"
"● Red = Overdue audit (>60 days)"

// Summary Statistics
Label_GreenCount.Text =
    CountRows(
        Filter(
            Location,
            Status = "Active",
            DaysSinceLastAudit < 30
        )
    ) & " trolleys (Green)"

Label_YellowCount.Text =
    CountRows(
        Filter(
            Location,
            Status = "Active",
            And(DaysSinceLastAudit >= 30, DaysSinceLastAudit < 60)
        )
    ) & " trolleys (Yellow)"

Label_RedCount.Text =
    CountRows(
        Filter(
            Location,
            Status = "Active",
            DaysSinceLastAudit >= 60
        )
    ) & " trolleys (Red)"
```

### Component Specifications

| Component | Specification |
|-----------|----------------|
| Green Row Fill | RGBA(76, 175, 80, 0.12) |
| Yellow Row Fill | RGBA(255, 193, 7, 0.12) |
| Red Row Fill | RGBA(229, 61, 61, 0.12) |
| Badge Size | 20x20 pixels |
| Font Size | 11pt for status text |
| Legend Position | 20px above table |
| Opacity | 12% (subtle, not overwhelming) |

### Verification Checklist

- [ ] Trolleys audited <30 days show green row background
- [ ] Trolleys audited 30-60 days ago show yellow row background
- [ ] Trolleys audited >60 days ago show red row background
- [ ] Never-audited trolleys show red row background
- [ ] Status badge appears next to days count
- [ ] Badge colour matches row colour scheme
- [ ] Status text displays correctly (Green/Yellow/Red/Never Audited)
- [ ] Colour legend appears above table
- [ ] Summary counts at bottom are accurate
- [ ] Colours update when new audit completes
- [ ] Printed output shows colours clearly (if printed)

---

## Task 2.1.8: Create Trolley Detail Screen - View Mode

### Objective

Build the Trolley Detail screen displaying comprehensive information about a single trolley in read-only view mode, including core attributes, equipment configuration, audit history, and open issues.

### Prerequisites

- Task 2.1.1-2.1.7 completed
- TrolleysScreen functional and navigating to detail view
- varSelectedTrolley variable set when user selects a trolley

### Step-by-Step Instructions

#### Step 1: Create New Screen

1. Create new screen named: `TrolleyDetailScreen`
2. Set screen properties:
   - **Width:** 1366
   - **Height:** 688
   - **Fill:** `BackgroundColor`

#### Step 2: Add Navigation Header

1. Copy the navigation header from TrolleysScreen to maintain consistency
2. Position at Y: 0, Height: 80

#### Step 3: Add Breadcrumb Navigation

1. Add label showing current location:
   - **X:** 20
   - **Y:** 100
   - **Width:** 400
   - **Height:** 30
   - **Text:**
   ```powerfx
   "Trolleys > " & varSelectedTrolley.Title & " (View)"
   ```
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`

#### Step 4: Create Tabs Container

1. Add a **Horizontal Gallery** or buttons for tabs:
   - **X:** 20
   - **Y:** 140
   - **Width:** 1326
   - **Height:** 40
   - **Items:**
   ```powerfx
   Table(
       {Label: "Details", Screen: "Details", Icon: "ℹ"},
       {Label: "Equipment", Screen: "Equipment", Icon: "⚙"},
       {Label: "Audit History", Screen: "History", Icon: "📊"},
       {Label: "Issues", Screen: "Issues", Icon: "⚠"},
       {Label: "Change Log", Screen: "ChangeLog", Icon: "📝"}
   )
   ```

2. Set up click handler on each tab:
   ```powerfx
   Set(varSelectedTab, ThisItem.Screen)
   ```

#### Step 5: Build Details Tab Content

1. Create a **Rectangle** for Details tab container:
   - **X:** 20
   - **Y:** 190
   - **Width:** 1326
   - **Height:** 480
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 1
   - **Visible:**
   ```powerfx
   varSelectedTab = "Details"
   ```

2. Add section for basic information:
   ```
   Department: [Title]
   Display Name: [DisplayName]
   Service Line: [ServiceLine]
   Building: [Building]
   Level: [Level]
   Specific Location: [SpecificLocation]
   Status: [Status] (with colour badge)
   Trolley Type: [TrolleyType]
   ```

3. Format with labels and values:
   - Label width: 150px
   - Value width: 300px
   - Each row height: 30px
   - Vertical spacing: 10px

#### Step 6: Add Equipment Configuration Section

1. Under basic info, add section:
   ```
   EQUIPMENT CONFIGURATION
   Defibrillator Type: [DefibrillatorType]
   Has Paediatric Box: [HasPaedBox] (Yes/No)
   Operating Hours: [OperatingHours]
   Expected Daily Checks: [ExpectedDailyChecks]
   ```

#### Step 7: Add Audit Information Section

1. Add last audit information:
   ```
   LAST AUDIT
   Last Audit Date: [LastAuditDate] formatted as date
   Days Since Audit: [DaysSinceLastAudit]
   Last Compliance Score: [LastAuditCompliance] formatted as %
   ```

2. Add colour indicator:
   ```powerfx
   If(
       DaysSinceLastAudit < 30, "✓ Green - Recently Audited",
       DaysSinceLastAudit < 60, "⚠ Yellow - Pending",
       "✗ Red - Overdue"
   )
   ```

#### Step 8: Add Notes Section

1. Display trolley notes:
   - **Text:** `varSelectedTrolley.Notes`
   - Height: 80px (allows wrapping)
   - Font: 11pt
   - Color: `TextSecondary`

#### Step 9: Add Action Buttons (Bottom)

1. Add buttons for common actions:
   - **Edit** (visible to MERT only)
   ```powerfx
   If(
       User().Email in colMERTEducators,
       Button(
           Text: "Edit Trolley",
           Fill: PrimaryColor,
           OnSelect: Set(varEditMode, true); Set(varSelectedTab, "Details")
       ),
       Blank()
   )
   ```

   - **View Full Audit History**
   ```powerfx
   Button(
       Text: "Full Audit History",
       Fill: SecondaryColor,
       OnSelect: Set(varSelectedTab, "History")
   )
   ```

   - **Back to List**
   ```powerfx
   Button(
       Text: "Back to List",
       Fill: BorderColor,
       TextColor: TextPrimary,
       OnSelect: Navigate(TrolleysScreen, ScreenTransition.Fade)
   )
   ```

### PowerFx Code

Details tab display formula:

```powerfx
// Details Tab Container Visible
varSelectedTab = "Details" And Not(varEditMode)

// Status Badge Display Text and Colour
If(
    varSelectedTrolley.Status = "Active",
    "● Active",
    varSelectedTrolley.Status = "Inactive",
    "● Inactive",
    "● Pending"
)

// Status Badge Fill
If(
    varSelectedTrolley.Status = "Active",
    SuccessColor,
    varSelectedTrolley.Status = "Inactive",
    ErrorColor,
    WarningColor
)

// Days Since Audit Formatted
If(
    IsBlank(varSelectedTrolley.DaysSinceLastAudit),
    "Never audited",
    varSelectedTrolley.DaysSinceLastAudit = 0,
    "Today",
    varSelectedTrolley.DaysSinceLastAudit = 1,
    "1 day ago",
    varSelectedTrolley.DaysSinceLastAudit & " days ago"
)

// Audit Status Indicator
If(
    Or(IsBlank(varSelectedTrolley.DaysSinceLastAudit), varSelectedTrolley.DaysSinceLastAudit > 999),
    "⚠ Red - Never audited",
    varSelectedTrolley.DaysSinceLastAudit < 30,
    "✓ Green - Recently audited",
    varSelectedTrolley.DaysSinceLastAudit < 60,
    "⚠ Yellow - Pending audit",
    "✗ Red - Overdue audit"
)

// Last Audit Date Formatted
If(
    IsBlank(varSelectedTrolley.LastAuditDate),
    "No audit on record",
    Text(varSelectedTrolley.LastAuditDate, "ddd, d mmmm yyyy")
)

// Compliance Score Display
If(
    IsBlank(varSelectedTrolley.LastAuditCompliance),
    "N/A",
    varSelectedTrolley.LastAuditCompliance & "%"
)
```

### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Details Container | Width | 1326 |
| | Height | 480 |
| | Fill | White |
| | Border | 1px, BorderColor |
| Label (field names) | Width | 150 |
| | Font Size | 11pt, Bold |
| | Color | TextPrimary |
| Value Text | Width | 300+ |
| | Font Size | 11pt |
| | Color | TextSecondary |
| Row Spacing | Vertical | 10px |
| Status Badge | Width | 20 |
| | Height | 20 |
| | Radius | 10 |

### Verification Checklist

- [ ] TrolleyDetailScreen created and displays
- [ ] Breadcrumb shows correct trolley name
- [ ] Details tab is default/active tab
- [ ] All basic fields display correctly
- [ ] Department name, building, level show accurately
- [ ] Service line correctly populated from lookup
- [ ] Status shows with correct colour badge
- [ ] Equipment configuration displays (Defib type, Paediatric box, etc.)
- [ ] Last audit information displays correctly
- [ ] Days since audit calculated and formatted properly
- [ ] Audit status indicator shows correct colour/message
- [ ] Notes display if present
- [ ] Edit button visible only to MERT educators
- [ ] Back to List button navigates to trolley list
- [ ] No errors in formulas

---

## Task 2.1.9: Create Trolley Detail Screen - Edit Mode

### Objective

Implement edit functionality in Trolley Detail screen allowing MERT educators to modify trolley attributes, save changes, and audit the modification history.

### Prerequisites

- Task 2.1.8 completed (View mode)
- varEditMode variable controls mode switching
- User permissions validated in App.OnStart

### Step-by-Step Instructions

#### Step 1: Add Edit Mode Toggle Logic

1. Update Details tab container Visible formula:
   ```powerfx
   varSelectedTab = "Details"
   ```

2. Create two sections within Details tab:
   - View section (visible when NOT in edit mode)
   - Edit section (visible when in edit mode)

#### Step 2: Create Edit Form Controls

1. In edit section, create input fields replacing labels:

   **Department Name (Read-Only):**
   ```powerfx
   Label("Department Name: " & varSelectedTrolley.Title)
   ```

   **Display Name (Editable):**
   ```powerfx
   TextInput(
       Name: "DisplayNameEdit",
       Default: varSelectedTrolley.DisplayName,
       BorderColor: BorderColor
   )
   ```

   **Building (Dropdown):**
   ```powerfx
   Dropdown(
       Name: "BuildingEdit",
       Items: Table(
           {Value: "James Mayne Building", Display: "James Mayne Building"},
           {Value: "Ned Hanlon Building", Display: "Ned Hanlon Building"},
           {Value: "Joyce Tweddell Building", Display: "Joyce Tweddell Building"},
           {Value: "Mental Health Block", Display: "Mental Health Block"},
           {Value: "HIRF Building", Display: "HIRF Building"},
           {Value: "STARS Building", Display: "STARS Building"},
           {Value: "Offsite", Display: "Offsite"}
       ),
       Default: varSelectedTrolley.Building
   )
   ```

   **Level (Text Input):**
   ```powerfx
   TextInput(
       Name: "LevelEdit",
       Default: varSelectedTrolley.Level,
       BorderColor: BorderColor
   )
   ```

   **Specific Location (Text Input):**
   ```powerfx
   TextInput(
       Name: "SpecificLocationEdit",
       Default: varSelectedTrolley.SpecificLocation,
       BorderColor: BorderColor,
       Mode: Multiline,
       Height: 60
   )
   ```

   **Status (Dropdown):**
   ```powerfx
   Dropdown(
       Name: "StatusEdit",
       Items: Table(
           {Value: "Active", Display: "Active"},
           {Value: "Inactive", Display: "Inactive"},
           {Value: "Pending", Display: "Pending"}
       ),
       Default: varSelectedTrolley.Status
   )
   ```

   **Trolley Type (Dropdown):**
   ```powerfx
   Dropdown(
       Name: "TrolleyTypeEdit",
       Items: Table(
           {Value: "Standard", Display: "Standard"},
           {Value: "Emergency", Display: "Emergency"},
           {Value: "Other", Display: "Other"}
       ),
       Default: varSelectedTrolley.TrolleyType
   )
   ```

   **Notes (Text Area):**
   ```powerfx
   TextInput(
       Name: "NotesEdit",
       Default: varSelectedTrolley.Notes,
       BorderColor: BorderColor,
       Mode: Multiline,
       Height: 80
   )
   ```

#### Step 3: Add Edit Mode Header

1. Add label showing "EDIT MODE" with warning colour:
   - **Text:** "EDIT MODE - Changes will be saved to SharePoint"
   - **Color:** `AccentColor`
   - **Font Size:** 12pt, Bold
   - **Visible:**
   ```powerfx
   varEditMode = true
   ```

#### Step 4: Add Validation Logic

1. Create validation function:
   ```powerfx
   Set(
       varEditValidationErrors,
       Filter(
           Table(
               If(IsBlank(DisplayNameEdit.Value), "Display Name is required"),
               If(IsBlank(BuildingEdit.Value), "Building is required"),
               If(IsBlank(LevelEdit.Value), "Level is required"),
               If(IsBlank(StatusEdit.Value), "Status is required")
           ),
           Not(IsBlank(Value))
       )
   );

   If(
       CountRows(varEditValidationErrors) = 0,
       true,
       Set(varValidationError, Concatenate(varEditValidationErrors, ","));
       false
   )
   ```

#### Step 5: Add Save Button

1. Add **Button** for saving:
   - **Text:** "Save Changes"
   - **Fill:** `SuccessColor`
   - **TextColor:** White
   - **OnSelect:**
   ```powerfx
   If(
       Validate(),
       Patch(
           Location,
           varSelectedTrolley,
           {
               DisplayName: DisplayNameEdit.Value,
               Building: BuildingEdit.Value,
               Level: LevelEdit.Value,
               SpecificLocation: SpecificLocationEdit.Value,
               Status: StatusEdit.Value,
               TrolleyType: TrolleyTypeEdit.Value,
               Notes: NotesEdit.Value,
               ModifiedDate: Now(),
               ModifiedBy: User().FullName
           }
       );
       LogLocationChangeEvent();
       Set(varEditMode, false);
       Notify("Changes saved successfully", NotificationType.Success);
       Refresh(Location),
       Notify("Please fix validation errors", NotificationType.Error)
   )
   ```

#### Step 6: Add Cancel Button

1. Add **Button** for canceling edits:
   - **Text:** "Cancel"
   - **Fill:** `BorderColor`
   - **TextColor:** `TextPrimary`
   - **OnSelect:**
   ```powerfx
   Set(varEditMode, false);
   Refresh(Location)
   ```

#### Step 7: Create Change Log Function

1. Add function to log changes to LocationChangeLog:
   ```powerfx
   Procedure LogLocationChangeEvent()

   // Compare old vs new values and log changes
   If(varSelectedTrolley.Building <> BuildingEdit.Value,
       Patch(
           LocationChangeLog,
           Defaults(LocationChangeLog),
           {
               LocationId: varSelectedTrolley.ID,
               ChangeType: "Modified",
               FieldChanged: "Building",
               OldValue: varSelectedTrolley.Building,
               NewValue: BuildingEdit.Value,
               ChangeReason: "User edit",
               ChangedBy: User().FullName,
               ChangedDate: Now()
           }
       )
   );

   // Repeat for each editable field
   // ... similar patterns for other fields

   EndProcedure
   ```

### PowerFx Code

Complete edit mode implementation:

```powerfx
// Validation Function
Procedure ValidateEditForm()
    Set(
        varEditFormErrors,
        Filter(
            Table(
                {Field: "DisplayName", Error: IsBlank(DisplayNameEdit.Value), Message: "Display Name is required"},
                {Field: "Building", Error: IsBlank(BuildingEdit.Value), Message: "Building is required"},
                {Field: "Level", Error: IsBlank(LevelEdit.Value), Message: "Level is required"},
                {Field: "Status", Error: IsBlank(StatusEdit.Value), Message: "Status is required"}
            ),
            Error = true
        )
    );

    Return(CountRows(varEditFormErrors) = 0)
EndProcedure

// Save Changes Handler
If(
    ValidateEditForm(),
    // All validations passed - proceed with save
    Patch(
        Location,
        varSelectedTrolley,
        {
            DisplayName: Trim(DisplayNameEdit.Value),
            Building: BuildingEdit.Value,
            Level: Trim(LevelEdit.Value),
            SpecificLocation: Trim(SpecificLocationEdit.Value),
            Status: StatusEdit.Value,
            TrolleyType: TrolleyTypeEdit.Value,
            Notes: Trim(NotesEdit.Value),
            ModifiedDate: Now(),
            ModifiedBy: User().FullName
        }
    );

    // Log each change to LocationChangeLog
    ForAll(
        Filter(
            Table(
                {Field: "DisplayName", Old: varSelectedTrolley.DisplayName, New: DisplayNameEdit.Value},
                {Field: "Building", Old: varSelectedTrolley.Building, New: BuildingEdit.Value},
                {Field: "Level", Old: varSelectedTrolley.Level, New: LevelEdit.Value},
                {Field: "SpecificLocation", Old: varSelectedTrolley.SpecificLocation, New: SpecificLocationEdit.Value},
                {Field: "Status", Old: varSelectedTrolley.Status, New: StatusEdit.Value},
                {Field: "TrolleyType", Old: varSelectedTrolley.TrolleyType, New: TrolleyTypeEdit.Value},
                {Field: "Notes", Old: varSelectedTrolley.Notes, New: NotesEdit.Value}
            ),
            Old <> New
        ),
        Patch(
            LocationChangeLog,
            Defaults(LocationChangeLog),
            {
                LocationId: varSelectedTrolley.ID,
                ChangeType: "Modified",
                FieldChanged: Field,
                OldValue: Text(Old),
                NewValue: Text(New),
                ChangeReason: "User edit from trolley detail screen",
                ChangedBy: User().FullName,
                ChangedDate: Now()
            }
        )
    );

    // Refresh and notify
    Refresh(Location);
    Set(varEditMode, false);
    Notify("Trolley information updated successfully", NotificationType.Success, 3000),

    // Validation failed
    Notify(
        "Please correct the following errors: " &
        Concatenate(varEditFormErrors.Message, "; "),
        NotificationType.Error,
        5000
    )
)

// Cancel Edit Handler
Set(varEditMode, false);
Refresh(Location)
```

### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Text Input | BorderColor | BorderColor |
| | BorderThickness | 1 |
| Dropdown | BorderColor | BorderColor |
| Save Button | Fill | SuccessColor (#4CAF50) |
| | TextColor | White |
| Cancel Button | Fill | BorderColor |
| Validation Error | Color | ErrorColor |
| Edit Mode Header | Color | AccentColor |
| | Font Weight | Bold |

### Verification Checklist

- [ ] Edit button visible only to MERT educators
- [ ] Clicking Edit button switches to edit mode
- [ ] All editable fields display current values
- [ ] Read-only fields (Department Name) cannot be edited
- [ ] Dropdowns show correct options
- [ ] Multiline text fields allow text wrapping
- [ ] Validation detects missing required fields
- [ ] Validation error message displays clearly
- [ ] Save button submits changes to SharePoint
- [ ] Change log entries created for each modified field
- [ ] Cancel button reverts unsaved changes
- [ ] Success notification appears after save
- [ ] Screen returns to view mode after save
- [ ] No orphaned or incomplete records created

---

## Task 2.1.10: Add Trolley Detail - Optional Equipment Toggles

### Objective

Implement optional equipment configuration toggles in Trolley Detail screen allowing MERT educators to configure paediatric box, altered airway equipment, and specialty medications.

### Prerequisites

- Task 2.1.8-2.1.9 completed
- Location list includes HasPaedBox, HasAlteredAirway, HasSpecialtyMeds fields
- Equipment configuration screen accessible in edit mode

### Step-by-Step Instructions

#### Step 1: Create Equipment Configuration Section

1. Add new tab to detail screen: "Equipment Config"
2. Set Visible formula:
   ```powerfx
   varSelectedTab = "Equipment"
   ```

#### Step 2: Build Equipment Tab in View Mode

1. Display equipment configuration as read-only:
   ```
   OPTIONAL EQUIPMENT

   Paediatric Box: ☑ (or ☐) Yes/No
   Description: Includes paediatric BVM, masks, and defibrillator pads

   Altered Airway Equipment: ☑ (or ☐) Yes/No
   Description: Includes catheter mount, swivel connectors

   Specialty Medications: ☑ (or ☐) Yes/No
   Notes: [Display SpecialtyMedsNotes if present]

   Defibrillator Type: [DefibrillatorType]

   STANDARD EQUIPMENT
   All trolleys include:
   - Standard adult resuscitation equipment
   - BVM with adult and infant masks
   - Defibrillator pads (type-specific)
   - Airway management tools
   - Medications (adrenaline, amiodarone, etc.)
   ```

#### Step 3: Add Edit Mode for Equipment

1. Create edit section within Equipment tab
2. Add checkbox toggles (read-only in view mode):

   **Paediatric Box Checkbox:**
   ```powerfx
   If(
       varEditMode,
       Checkbox(
           Name: "PaedBoxEdit",
           Default: varSelectedTrolley.HasPaedBox,
           CheckboxLabel: "Include Paediatric Equipment Box"
       ),
       Label(
           If(varSelectedTrolley.HasPaedBox, "☑ ", "☐ ") & "Paediatric Equipment Box"
       )
   )
   ```

   **Altered Airway Checkbox:**
   ```powerfx
   If(
       varEditMode,
       Checkbox(
           Name: "AlteredAirwayEdit",
           Default: varSelectedTrolley.HasAlteredAirway,
           CheckboxLabel: "Include Altered Airway Equipment"
       ),
       Label(
           If(varSelectedTrolley.HasAlteredAirway, "☑ ", "☐ ") & "Altered Airway Equipment"
       )
   )
   ```

   **Specialty Medications Checkbox:**
   ```powerfx
   If(
       varEditMode,
       Checkbox(
           Name: "SpecialtyMedsEdit",
           Default: varSelectedTrolley.HasSpecialtyMeds,
           CheckboxLabel: "Department has Specialty Medications"
       ),
       Label(
           If(varSelectedTrolley.HasSpecialtyMeds, "☑ ", "☐ ") & "Specialty Medications"
       )
   )
   ```

#### Step 4: Add Specialty Medications Notes Field

1. Add conditional text input for specialty meds details:
   ```powerfx
   If(
       And(varEditMode, SpecialtyMedsEdit.Value = true),
       TextInput(
           Name: "SpecialtyMedsNotesEdit",
           Placeholder: "Enter details of specialty medications (e.g., chemotherapy agents, dialysis meds)",
           Default: varSelectedTrolley.SpecialtyMedsNotes,
           Mode: Multiline,
           Height: 80,
           BorderColor: BorderColor
       ),
       If(
           And(Not(varEditMode), Not(IsBlank(varSelectedTrolley.SpecialtyMedsNotes))),
           Label(
               "Notes: " & varSelectedTrolley.SpecialtyMedsNotes
           )
       )
   )
   ```

#### Step 5: Add Defibrillator Type Selection

1. Add defibrillator type dropdown in edit mode:
   ```powerfx
   If(
       varEditMode,
       Dropdown(
           Name: "DefibTypeEdit",
           Items: Table(
               {Value: "LIFEPAK_1000_AED", Display: "LIFEPAK 1000 (AED)"},
               {Value: "LIFEPAK_20_20e", Display: "LIFEPAK 20/20e (Monitoring)"}
           ),
           Default: varSelectedTrolley.DefibrillatorType,
           Label: "Defibrillator Type"
       ),
       Label(
           "Defibrillator: " & varSelectedTrolley.DefibrillatorType
       )
   )
   ```

#### Step 6: Add Equipment Descriptions

1. Display descriptions below toggles:
   ```powerfx
   Label(
       "PAEDIATRIC BOX: Includes appropriately-sized BVM, endotracheal tubes, defibrillator pads, medications"
   );
   Label(
       "ALTERED AIRWAY: For departments with patients requiring specialized airway management"
   );
   Label(
       "SPECIALTY MEDS: Department-specific medications beyond standard resuscitation kit"
   )
   ```

#### Step 7: Add Impact Information

1. Add informational box showing impact of each option:
   ```
   IMPACT OF EQUIPMENT SELECTIONS:

   - Paediatric Box: Adds ~15 items to audit checklist
   - Altered Airway: Adds ~8 items to audit checklist
   - Specialty Meds: Requires manual entry per department
   - Defibrillator Type: Determines correct pads in audit
   ```

#### Step 8: Integrate with Audit Equipment Configuration

1. Create procedure to build audit checklist based on equipment config:
   ```powerfx
   Procedure BuildAuditEquipmentList(trolleyId)
       // Get base equipment
       ClearCollect(
           colAuditEquipment,
           Filter(Equipment, IsStandardItem = true)
       );

       // Add paediatric if selected
       If(
           varSelectedTrolley.HasPaedBox,
           Append(
               colAuditEquipment,
               Filter(Equipment, IsPaediatricItem = true)
           )
       );

       // Add altered airway if selected
       If(
           varSelectedTrolley.HasAlteredAirway,
           Append(
               colAuditEquipment,
               Filter(Equipment, IsAlteredAirwayItem = true)
           )
       );

       Return(colAuditEquipment)
   EndProcedure
   ```

#### Step 9: Update Equipment Tab Save Logic

1. When saving from Equipment tab, update all fields:
   ```powerfx
   Patch(
       Location,
       varSelectedTrolley,
       {
           HasPaedBox: If(varEditMode, PaedBoxEdit.Value, varSelectedTrolley.HasPaedBox),
           HasAlteredAirway: If(varEditMode, AlteredAirwayEdit.Value, varSelectedTrolley.HasAlteredAirway),
           HasSpecialtyMeds: If(varEditMode, SpecialtyMedsEdit.Value, varSelectedTrolley.HasSpecialtyMeds),
           SpecialtyMedsNotes: If(varEditMode And SpecialtyMedsEdit.Value, SpecialtyMedsNotesEdit.Value, ""),
           DefibrillatorType: If(varEditMode, DefibTypeEdit.Value, varSelectedTrolley.DefibrillatorType),
           ModifiedDate: Now(),
           ModifiedBy: User().FullName
       }
   );

   // Log changes
   LogLocationChangeEvent()
   ```

### PowerFx Code

Complete optional equipment implementation:

```powerfx
// Equipment Configuration View Mode Display
If(
    Not(varEditMode),
    // VIEW MODE - Read-only display
    Table(
        {Label: "Paediatric Box", Enabled: varSelectedTrolley.HasPaedBox, Description: "Includes paediatric BVM, masks, pads"},
        {Label: "Altered Airway", Enabled: varSelectedTrolley.HasAlteredAirway, Description: "Specialized airway equipment"},
        {Label: "Specialty Medications", Enabled: varSelectedTrolley.HasSpecialtyMeds, Description: "Department-specific medications"}
    ),
    // EDIT MODE - Editable checkboxes
    ""
)

// Checkbox Display (View Mode)
If(ThisItem.Enabled, "☑ ", "☐ ") & ThisItem.Label

// Equipment Selection Checkboxes (Edit Mode)
[
    Checkbox(PaedBoxEdit, "Paediatric Equipment Box"),
    Checkbox(AlteredAirwayEdit, "Altered Airway Equipment"),
    Checkbox(SpecialtyMedsEdit, "Specialty Medications")
]

// Specialty Notes Field Visibility
And(varEditMode, SpecialtyMedsEdit.Value = true)

// Save Equipment Configuration
Patch(
    Location,
    varSelectedTrolley,
    {
        HasPaedBox: PaedBoxEdit.Value,
        HasAlteredAirway: AlteredAirwayEdit.Value,
        HasSpecialtyMeds: SpecialtyMedsEdit.Value,
        SpecialtyMedsNotes: If(SpecialtyMedsEdit.Value, Trim(SpecialtyMedsNotesEdit.Value), ""),
        DefibrillatorType: DefibTypeEdit.Value,
        ModifiedDate: Now(),
        ModifiedBy: User().FullName
    }
);

Notify("Equipment configuration saved", NotificationType.Success)

// Build Equipment Checklist
Procedure BuildEquipmentChecklist()
    ClearCollect(
        colEquipmentChecklist,
        Filter(Equipment, IsStandardItem = true And Status = "Active")
    );

    If(
        varSelectedTrolley.HasPaedBox,
        Append(
            colEquipmentChecklist,
            Filter(Equipment, IsPaediatricItem = true And Status = "Active")
        )
    );

    If(
        varSelectedTrolley.HasAlteredAirway,
        Append(
            colEquipmentChecklist,
            Filter(Equipment, IsAlteredAirwayItem = true And Status = "Active")
        )
    );

    If(
        varSelectedTrolley.DefibrillatorType = "LIFEPAK_1000_AED",
        Append(
            colEquipmentChecklist,
            Filter(Equipment, And(
                RequiredForDefibType in ["LIFEPAK_1000_AED", "Both"],
                Status = "Active"
            ))
        )
    );

    Return(CountRows(colEquipmentChecklist))
EndProcedure
```

### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Checkbox | Label Font | 12pt |
| Checkbox | Color | TextPrimary |
| Toggle Icon | View Mode | "☑" or "☐" |
| Description Text | Font Size | 11pt |
| | Color | TextSecondary |
| Specialty Notes Field | Mode | Multiline |
| | Height | 80px |
| Impact Box | Background | BackgroundColor |
| | Border | 1px, BorderColor |
| | Padding | 10px |

### Verification Checklist

- [ ] Equipment Config tab displays in detail screen
- [ ] Checkboxes show read-only in view mode
- [ ] Edit mode allows toggling checkboxes
- [ ] Specialty Medications notes field appears only when checkbox enabled
- [ ] Defibrillator type dropdown shows both options
- [ ] Equipment descriptions display correctly
- [ ] Changes to equipment config save to SharePoint
- [ ] Change log records equipment modifications
- [ ] Equipment checklist dynamically updates based on selections
- [ ] Paediatric items added when HasPaedBox = true
- [ ] Altered airway items added when HasAlteredAirway = true
- [ ] Correct defibrillator pads included based on type
- [ ] Equipment impact information is helpful and accurate

---

## Task 2.1.11: Create Add New Trolley Screen

### Objective

Build a form-based screen for MERT educators to add new trolley locations with validation, duplicate checking, and automatic initialization of audit fields.

### Prerequisites

- Task 2.1.1-2.1.10 completed
- User permissions verified in App.OnStart
- Location list schema includes all required fields

### Step-by-Step Instructions

#### Step 1: Create New Screen

1. Create new screen: `AddTrolleyScreen`
2. Set properties:
   - **Width:** 1366
   - **Height:** 688
   - **Fill:** `BackgroundColor`

#### Step 2: Add Navigation Header

1. Copy navigation header from existing screens
2. Position at Y: 0, Height: 80

#### Step 3: Add Form Title and Description

1. Add title label:
   - **Text:** "Add New Trolley Location"
   - **Font Size:** 24pt, Bold
   - **Color:** `TextPrimary`
   - **Y:** 100

2. Add description:
   - **Text:** "Create a new resuscitation trolley location and configure its equipment requirements"
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`
   - **Y:** 135

#### Step 4: Create Form Container

1. Insert **Rectangle** as form background:
   - **X:** 40
   - **Y:** 175
   - **Width:** 1286
   - **Height:** 480
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 1
   - **Radius:** 4px

#### Step 5: Build Form Input Fields

Arrange fields in two columns, 20px spacing between rows:

**Left Column (X: 60) | Right Column (X: 700)**

1. **Department Name** (Full width, required):
   ```powerfx
   TextInput(
       Name: "DepartmentNameInput",
       Label: "Department Name *",
       Placeholder: "e.g., 7A North",
       MaxLength: 100,
       BorderColor: BorderColor,
       Width: 600
   )
   ```

2. **Display Name** (Full width, required):
   ```powerfx
   TextInput(
       Name: "DisplayNameInput",
       Label: "Display Name *",
       Placeholder: "Short name for lists",
       MaxLength: 50,
       BorderColor: BorderColor,
       Width: 600
   )
   ```

3. **Service Line** (Left column, required):
   ```powerfx
   Dropdown(
       Name: "ServiceLineInput",
       Label: "Service Line *",
       Items: Distinct(Location, ServiceLine),
       Width: 280
   )
   ```

4. **Building** (Right column, required):
   ```powerfx
   Dropdown(
       Name: "BuildingInput",
       Label: "Building *",
       Items: Table(
           {Value: "James Mayne Building", Display: "James Mayne Building"},
           {Value: "Ned Hanlon Building", Display: "Ned Hanlon Building"},
           {Value: "Joyce Tweddell Building", Display: "Joyce Tweddell Building"},
           {Value: "Mental Health Block", Display: "Mental Health Block"},
           {Value: "HIRF Building", Display: "HIRF Building"},
           {Value: "STARS Building", Display: "STARS Building"},
           {Value: "Offsite", Display: "Offsite"}
       ),
       Width: 280
   )
   ```

5. **Level** (Left column, required):
   ```powerfx
   TextInput(
       Name: "LevelInput",
       Label: "Level *",
       Placeholder: "Ground, L3, Level 5, etc.",
       MaxLength: 20,
       BorderColor: BorderColor,
       Width: 280
   )
   ```

6. **Specific Location** (Right column, optional):
   ```powerfx
   TextInput(
       Name: "SpecificLocationInput",
       Label: "Specific Location",
       Placeholder: "Room/bay details",
       MaxLength: 100,
       BorderColor: BorderColor,
       Width: 280,
       Mode: Multiline,
       Height: 50
   )
   ```

7. **Trolley Type** (Left column, required):
   ```powerfx
   Dropdown(
       Name: "TrolleyTypeInput",
       Label: "Trolley Type *",
       Items: Table(
           {Value: "Standard", Display: "Standard"},
           {Value: "Emergency", Display: "Emergency"},
           {Value: "Other", Display: "Other"}
       ),
       Width: 280
   )
   ```

8. **Defibrillator Type** (Right column, required):
   ```powerfx
   Dropdown(
       Name: "DefibTypeInput",
       Label: "Defibrillator Type *",
       Items: Table(
           {Value: "LIFEPAK_1000_AED", Display: "LIFEPAK 1000 (AED)"},
           {Value: "LIFEPAK_20_20e", Display: "LIFEPAK 20/20e (Monitoring)"}
       ),
       Width: 280
   )
   ```

9. **Operating Hours** (Left column, required):
   ```powerfx
   Dropdown(
       Name: "OperatingHoursInput",
       Label: "Operating Hours *",
       Items: Table(
           {Value: "24_7", Display: "24/7"},
           {Value: "Weekday_Business", Display: "Weekday Business Hours"},
           {Value: "Weekday_Extended", Display: "Weekday Extended Hours"}
       ),
       Width: 280
   )
   ```

10. **Status** (Right column, required):
    ```powerfx
    Dropdown(
        Name: "StatusInput",
        Label: "Status *",
        Items: Table(
            {Value: "Active", Display: "Active"},
            {Value: "Pending", Display: "Pending"}
        ),
        Default: "Active",
        Width: 280
    )
    ```

#### Step 6: Add Optional Equipment Section

Below the main fields:

```
OPTIONAL EQUIPMENT
☐ Paediatric Box
☐ Altered Airway Equipment
☐ Specialty Medications
  Notes: [Text input if selected]
```

#### Step 7: Add Validation Messages

Below each field (visible only if error), show error message:

```powerfx
If(
    And(varShowValidation, IsBlank(DepartmentNameInput.Value)),
    Label("This field is required", Color: ErrorColor, Font: 10pt),
    Blank()
)
```

#### Step 8: Add Duplicate Check

1. As user types Department Name, check for duplicates:
   ```powerfx
   DepartmentNameInput.OnChange:
   Set(
       varDuplicateCheck,
       CountRows(
           Filter(
               Location,
               Lower(Trim(Title)) = Lower(Trim(DepartmentNameInput.Value))
           )
       ) > 0
   )
   ```

2. Show warning if duplicate found:
   ```powerfx
   If(
       varDuplicateCheck,
       Label(
           "⚠ A trolley with this name already exists. Please use a unique name or verify this is a different location.",
           Color: WarningColor,
           Font: 11pt
       ),
       Blank()
   )
   ```

#### Step 9: Add Form Buttons

Bottom of form:

1. **Save Button** (Green, primary action):
   ```powerfx
   Button(
       Text: "Create Trolley",
       Fill: SuccessColor,
       TextColor: White,
       OnSelect: SaveNewTrolley()
   )
   ```

2. **Cancel Button** (Grey):
   ```powerfx
   Button(
       Text: "Cancel",
       Fill: BorderColor,
       TextColor: TextPrimary,
       OnSelect: Navigate(TrolleysScreen, ScreenTransition.Fade)
   )
   ```

#### Step 10: Create Save Function

```powerfx
Procedure SaveNewTrolley()
    If(
        ValidateNewTrolleyForm(),
        // Validation passed
        Patch(
            Location,
            Defaults(Location),
            {
                Title: Trim(DepartmentNameInput.Value),
                DisplayName: Trim(DisplayNameInput.Value),
                ServiceLine: ServiceLineInput.SelectedItem,
                Building: BuildingInput.Value,
                Level: Trim(LevelInput.Value),
                SpecificLocation: Trim(SpecificLocationInput.Value),
                TrolleyType: TrolleyTypeInput.Value,
                DefibrillatorType: DefibTypeInput.Value,
                OperatingHours: OperatingHoursInput.Value,
                HasPaedBox: PaedBoxCheckbox.Value,
                HasAlteredAirway: AlteredAirwayCheckbox.Value,
                HasSpecialtyMeds: SpecialtyMedsCheckbox.Value,
                SpecialtyMedsNotes: If(SpecialtyMedsCheckbox.Value, Trim(SpecialtyMedsNotesInput.Value), ""),
                Status: StatusInput.Value,
                LastAuditDate: Blank(),
                LastAuditCompliance: Blank(),
                DaysSinceLastAudit: Blank(),
                CreatedBy: User().FullName,
                ModifiedBy: User().FullName
            }
        );

        // Log creation event
        Patch(
            LocationChangeLog,
            Defaults(LocationChangeLog),
            {
                LocationId: <new ID>,
                ChangeType: "Created",
                FieldChanged: "N/A",
                OldValue: "",
                NewValue: DepartmentNameInput.Value,
                ChangeReason: "New trolley location created",
                ChangedBy: User().FullName,
                ChangedDate: Now()
            }
        );

        Refresh(Location);
        Notify("New trolley created successfully!", NotificationType.Success);
        Set(varShowValidation, false);
        Navigate(TrolleysScreen, ScreenTransition.Fade),

        // Validation failed
        Set(varShowValidation, true);
        Notify("Please correct the errors below", NotificationType.Error)
    )
EndProcedure
```

### PowerFx Code

Form validation function:

```powerfx
Procedure ValidateNewTrolleyForm()
    Set(
        varFormErrors,
        Filter(
            Table(
                {Field: "Department Name", Error: IsBlank(DepartmentNameInput.Value), Message: "Department Name is required"},
                {Field: "Display Name", Error: IsBlank(DisplayNameInput.Value), Message: "Display Name is required"},
                {Field: "Service Line", Error: IsBlank(ServiceLineInput.Value), Message: "Service Line is required"},
                {Field: "Building", Error: IsBlank(BuildingInput.Value), Message: "Building is required"},
                {Field: "Level", Error: IsBlank(LevelInput.Value), Message: "Level is required"},
                {Field: "Trolley Type", Error: IsBlank(TrolleyTypeInput.Value), Message: "Trolley Type is required"},
                {Field: "Defib Type", Error: IsBlank(DefibTypeInput.Value), Message: "Defibrillator Type is required"},
                {Field: "Operating Hours", Error: IsBlank(OperatingHoursInput.Value), Message: "Operating Hours is required"},
                {Field: "Status", Error: IsBlank(StatusInput.Value), Message: "Status is required"},
                {Field: "Duplicate", Error: varDuplicateCheck, Message: "A trolley with this name already exists"}
            ),
            Error = true
        )
    );

    Return(CountRows(varFormErrors) = 0)
EndProcedure
```

### Verification Checklist

- [ ] AddTrolleyScreen accessible from navigation
- [ ] All form fields display correctly
- [ ] Required fields marked with asterisk
- [ ] Dropdowns show correct options
- [ ] Department Name duplicate check working
- [ ] Warning appears if duplicate name entered
- [ ] Validation prevents save with missing required fields
- [ ] Validation messages clear and helpful
- [ ] Optional equipment checkboxes work
- [ ] Specialty Medications notes field appears when checkbox enabled
- [ ] Save button creates new trolley record in SharePoint
- [ ] Change log entry created for new trolley
- [ ] New trolley appears in Trolley List immediately
- [ ] Cancel button returns to trolley list
- [ ] No errors in formulas

---

## Task 2.1.12-2.1.14: Add Trolley Deactivate/Reactivate Dialogs

### Objective

Implement dialog screens allowing MERT educators to deactivate/reactivate trolley locations with reason capture, confirmation, and audit trail logging.

### Prerequisites

- Task 2.1.1-2.1.11 completed
- TrolleyDetailScreen has Edit mode implemented
- LocationChangeLog list connected

### Step-by-Step Instructions

#### Step 1: Create Deactivate Dialog

1. Insert a **Rectangle** as dialog overlay (initially hidden):
   - **X:** 0
   - **Y:** 0
   - **Width:** 1366
   - **Height:** 768
   - **Fill:** RGBA(0, 0, 0, 0.3)  // Semi-transparent black
   - **Visible:** `varShowDeactivateDialog`
   - **ZIndex:** 500

2. Insert a **Rectangle** as dialog box:
   - **X:** 400
   - **Y:** 250
   - **Width:** 600
   - **Height:** 280
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 2
   - **Radius:** 8px
   - **ZIndex:** 501

3. Add dialog title:
   - **Text:** "Deactivate Trolley"
   - **Font Size:** 18pt, Bold
   - **Color:** `ErrorColor`

4. Add confirmation message:
   - **Text:** `"Are you sure you want to deactivate " & varSelectedTrolley.Title & "? This trolley will no longer appear in active lists."`
   - **Font Size:** 12pt
   - **Color:** `TextPrimary`
   - **Mode:** Multiline

5. Add reason dropdown:
   ```powerfx
   Dropdown(
       Name: "DeactivateReasonDropdown",
       Label: "Reason for deactivation *",
       Items: Table(
           {Value: "Repair", Display: "Equipment requires repair"},
           {Value: "Replacement", Display: "Replaced with new equipment"},
           {Value: "Relocation", Display: "Moved to new location"},
           {Value: "Decommissioned", Display: "No longer needed"},
           {Value: "Other", Display: "Other"}
       ),
       Width: 550
   )
   ```

6. Add optional notes field:
   ```powerfx
   TextInput(
       Name: "DeactivateNotesInput",
       Label: "Additional notes (optional)",
       Placeholder: "Provide context...",
       Mode: Multiline,
       Height: 60,
       Width: 550,
       BorderColor: BorderColor
   )
   ```

7. Add action buttons:
   - **Confirm Button** (Red):
   ```powerfx
   Button(
       Text: "Deactivate",
       Fill: ErrorColor,
       TextColor: White,
       OnSelect: ConfirmDeactivate()
   )
   ```

   - **Cancel Button**:
   ```powerfx
   Button(
       Text: "Cancel",
       Fill: BorderColor,
       TextColor: TextPrimary,
       OnSelect: Set(varShowDeactivateDialog, false)
   )
   ```

#### Step 2: Create ConfirmDeactivate Procedure

```powerfx
Procedure ConfirmDeactivate()
    If(
        IsBlank(DeactivateReasonDropdown.Value),
        Notify("Please select a reason for deactivation", NotificationType.Error),
        // Proceed with deactivation
        Patch(
            Location,
            varSelectedTrolley,
            {
                Status: "Inactive",
                StatusChangeDate: Now(),
                StatusChangeReason: DeactivateReasonDropdown.Value & ": " & Trim(DeactivateNotesInput.Value),
                StatusChangedBy: User().FullName,
                ModifiedDate: Now(),
                ModifiedBy: User().FullName
            }
        );

        // Log change
        Patch(
            LocationChangeLog,
            Defaults(LocationChangeLog),
            {
                LocationId: varSelectedTrolley.ID,
                ChangeType: "Deactivated",
                FieldChanged: "Status",
                OldValue: "Active",
                NewValue: "Inactive",
                ChangeReason: DeactivateReasonDropdown.Value & " - " & Trim(DeactivateNotesInput.Value),
                ChangedBy: User().FullName,
                ChangedDate: Now()
            }
        );

        Refresh(Location);
        Set(varShowDeactivateDialog, false);
        Notify("Trolley deactivated successfully", NotificationType.Success);
        Navigate(TrolleysScreen, ScreenTransition.Fade)
    )
EndProcedure
```

#### Step 3: Create Reactivate Dialog

1. Similar to deactivate dialog, but:
   - Title: "Reactivate Trolley"
   - Title color: `SuccessColor`
   - Message: "Reactivate this trolley to include it in active audit lists"
   - Simplified form (no reason required, just optional notes)

2. Reactivate dialog formula:
   ```powerfx
   Procedure ConfirmReactivate()
       Patch(
           Location,
           varSelectedTrolley,
           {
               Status: "Active",
               StatusChangeDate: Now(),
               StatusChangeReason: "Reactivated: " & Trim(ReactivateNotesInput.Value),
               StatusChangedBy: User().FullName,
               LastAuditDate: Blank(),  // Force re-audit after reactivation
               ModifiedDate: Now(),
               ModifiedBy: User().FullName
           }
       );

       // Log change
       Patch(
           LocationChangeLog,
           Defaults(LocationChangeLog),
           {
               LocationId: varSelectedTrolley.ID,
               ChangeType: "Reactivated",
               FieldChanged: "Status",
               OldValue: "Inactive",
               NewValue: "Active",
               ChangeReason: "Reactivated: " & Trim(ReactivateNotesInput.Value),
               ChangedBy: User().FullName,
               ChangedDate: Now()
           }
       );

       Refresh(Location);
       Set(varShowReactivateDialog, false);
       Notify("Trolley reactivated successfully", NotificationType.Success);
       Navigate(TrolleysScreen, ScreenTransition.Fade)
   EndProcedure
   ```

#### Step 4: Add Deactivate/Reactivate Buttons to Detail Screen

In the Trolley Detail screen edit mode:

```powerfx
// Deactivate Button (visible if status is Active)
If(
    And(varEditMode, varSelectedTrolley.Status = "Active"),
    Button(
        Text: "Deactivate Trolley",
        Fill: ErrorColor,
        TextColor: White,
        OnSelect: Set(varShowDeactivateDialog, true)
    ),
    Blank()
)

// Reactivate Button (visible if status is Inactive)
If(
    And(varEditMode, varSelectedTrolley.Status = "Inactive"),
    Button(
        Text: "Reactivate Trolley",
        Fill: SuccessColor,
        TextColor: White,
        OnSelect: Set(varShowReactivateDialog, true)
    ),
    Blank()
)
```

### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Dialog Overlay | Fill | RGBA(0,0,0,0.3) |
| | ZIndex | 500 |
| Dialog Box | Width | 600 |
| | Height | 280 (deactivate) / 220 (reactivate) |
| | Border | 2px, BorderColor |
| | Fill | White |
| Title | Font Size | 18pt, Bold |
| | Color | ErrorColor (deactivate) / SuccessColor (reactivate) |
| Button | Fill | ErrorColor (deactivate) / SuccessColor (reactivate) |

### Verification Checklist

- [ ] Deactivate button visible in edit mode for active trolleys
- [ ] Reactivate button visible in edit mode for inactive trolleys
- [ ] Deactivate dialog appears with semi-transparent overlay
- [ ] Reason dropdown shows all 5 options
- [ ] Validation prevents deactivation without reason
- [ ] Deactivate creates LocationChangeLog entry
- [ ] Status updates to Inactive after deactivation
- [ ] Reactivate dialog appears for inactive trolleys
- [ ] Reactivate clears LastAuditDate to force re-audit
- [ ] Success notifications appear after actions
- [ ] Trolley disappears from active lists after deactivation
- [ ] No errors in formulas

---

## Task 2.1.15-2.1.18: Trolley History Tab and Compliance Trend

### Objective

Implement the Trolley History tab showing complete audit history, issues log, and compliance trend chart for a selected trolley.

### Prerequisites

- Task 2.1.1-2.1.14 completed
- Audit and Issue lists connected
- Power BI or native chart capabilities available

### Step-by-Step Instructions

#### Step 1: Create History Tab

1. Add "Audit History" tab to TrolleyDetailScreen
2. Create container visible when:
   ```powerfx
   varSelectedTab = "History"
   ```

#### Step 2: Add Audit History List

1. Insert a **Data Table** showing all audits for this trolley:
   - **Items:**
   ```powerfx
   Sort(
       Filter(
           Audit,
           LocationId.ID = varSelectedTrolley.ID
       ),
       CompletedDateTime,
       Descending
   )
   ```

2. Display columns:
   - Audit Date
   - Audit Type (Annual / Random / Follow-up)
   - Auditor Name
   - Overall Compliance %
   - Status (Draft / Submitted / Verified)
   - Actions (View Details)

#### Step 3: Add Compliance Trend Chart

1. Insert **Chart** control (or Power BI visual):
   - **Chart Type:** Line Chart
   - **X-Axis:** Audit Date
   - **Y-Axis:** Overall Compliance Score (%)
   - **Items:**
   ```powerfx
   Sort(
       Filter(
           Audit,
           And(LocationId.ID = varSelectedTrolley.ID, SubmissionStatus = "Submitted")
       ),
       CompletedDateTime,
       Ascending
   )
   ```

2. Format chart:
   - Y-axis range: 0-100%
   - Colour: `SecondaryColor` (green)
   - Target line at 80% (RBWH target)

#### Step 4: Add Issues History

Below audits, add open issues for this trolley:

1. Insert **Data Table** for issues:
   - **Items:**
   ```powerfx
   Sort(
       Filter(
           Issue,
           LocationId.ID = varSelectedTrolley.ID
       ),
       ReportedDate,
       Descending
   )
   ```

2. Display columns:
   - Issue Number
   - Title
   - Severity (with colour badge)
   - Status
   - Reported Date
   - Days Open
   - Actions (View)

#### Step 5: Add Summary Statistics

Above history list, show:

```powerfx
// Total Audits
"Total Audits: " & CountRows(
    Filter(Audit, LocationId.ID = varSelectedTrolley.ID)
)

// Average Compliance
"Average Compliance: " & Text(
    Average(
        Filter(Audit, LocationId.ID = varSelectedTrolley.ID),
        OverallCompliance
    ),
    "0.0%"
)

// Last Audit Info
"Last Audit: " & If(
    IsBlank(varSelectedTrolley.LastAuditDate),
    "Never",
    Text(varSelectedTrolley.LastAuditDate, "d mmm yyyy")
)

// Open Issues Count
"Open Issues: " & CountRows(
    Filter(Issue, And(LocationId.ID = varSelectedTrolley.ID, Status <> "Closed"))
)
```

#### Step 6: Add Trend Analysis

Include narrative analysis:

```
COMPLIANCE TREND ANALYSIS
- Highest Compliance: [score]% on [date]
- Lowest Compliance: [score]% on [date]
- Trend: [Improving/Stable/Declining]
- Recommendations: [Based on common issues found]
```

### PowerFx Code

Complete history tab implementation:

```powerfx
// Audit History Items
Sort(
    Filter(
        Audit,
        LocationId.ID = varSelectedTrolley.ID
    ),
    CompletedDateTime,
    Descending
)

// Compliance Trend Chart Data
Sort(
    Filter(
        Audit,
        And(
            LocationId.ID = varSelectedTrolley.ID,
            SubmissionStatus = "Submitted"
        )
    ),
    CompletedDateTime,
    Ascending
)

// Summary Statistics
"Total Audits: " & CountRows(Filter(Audit, LocationId.ID = varSelectedTrolley.ID))

"Average Compliance: " & Text(
    Average(
        Filter(Audit, LocationId.ID = varSelectedTrolley.ID),
        OverallCompliance
    ),
    "0.0%"
)

"Last Audit: " & If(
    IsBlank(varSelectedTrolley.LastAuditDate),
    "Never",
    Text(varSelectedTrolley.LastAuditDate, "ddd, d mmmm yyyy")
)

"Open Issues: " & CountRows(
    Filter(
        Issue,
        And(
            LocationId.ID = varSelectedTrolley.ID,
            Status <> "Closed"
        )
    )
)

// Trend Analysis
Procedure AnalyzeTrolleyTrend()
    Var maxCompliance = Max(
        Filter(Audit, LocationId.ID = varSelectedTrolley.ID),
        OverallCompliance
    );

    Var minCompliance = Min(
        Filter(Audit, LocationId.ID = varSelectedTrolley.ID),
        OverallCompliance
    );

    Var recentCompliance = Average(
        Filter(
            Audit,
            And(
                LocationId.ID = varSelectedTrolley.ID,
                CompletedDateTime >= DateAdd(Today(), -90, Days)
            )
        ),
        OverallCompliance
    );

    Var previousCompliance = Average(
        Filter(
            Audit,
            And(
                LocationId.ID = varSelectedTrolley.ID,
                CompletedDateTime >= DateAdd(Today(), -180, Days),
                CompletedDateTime < DateAdd(Today(), -90, Days)
            )
        ),
        OverallCompliance
    );

    Var trend = If(
        recentCompliance > previousCompliance + 0.05,
        "Improving",
        recentCompliance < previousCompliance - 0.05,
        "Declining",
        "Stable"
    );

    Return({
        MaxCompliance: maxCompliance,
        MinCompliance: minCompliance,
        Trend: trend
    })
EndProcedure
```

### Verification Checklist

- [ ] History tab displays in trolley detail
- [ ] Audit list shows all audits chronologically
- [ ] Compliance trend chart displays correctly
- [ ] Chart shows line connecting all audit scores
- [ ] Y-axis shows 0-100% range
- [ ] Target line at 80% visible (if applicable)
- [ ] Summary statistics calculate correctly
- [ ] Open issues list shows current issues
- [ ] Severity badges display correct colours
- [ ] Trend analysis provides useful insights
- [ ] Chart updates when new audits completed
- [ ] No errors in formulas or chart

---

## Phase 2.1 Completion Checklist

### Task 2.1.1: Trolley List Screen
- [ ] Screen created with 1326x380 table/gallery
- [ ] All 9 required columns display
- [ ] Row background colours for audit status
- [ ] Filter bar with all controls
- [ ] View/Edit/Audit action buttons
- [ ] Statistics panel at bottom

### Task 2.1.2: Service Line Filter
- [ ] Dropdown populated with 7 unique service lines
- [ ] Filtering works correctly
- [ ] Combines with other filters
- [ ] Clear Filters resets selection

### Task 2.1.3: Building Filter
- [ ] All 8 building options display
- [ ] Filtering isolates trolleys by building
- [ ] Count updates correctly

### Task 2.1.4: Status Filter
- [ ] Active/Inactive/Pending options show
- [ ] Status badges display with correct colours
- [ ] Filtering functional

### Task 2.1.5: Search Functionality
- [ ] Real-time search across name/building/service line
- [ ] Results counter displays
- [ ] "No results" message appears when appropriate
- [ ] Case-insensitive search

### Task 2.1.6: Sort Functionality
- [ ] Default sort by Department Name A-Z
- [ ] Sortable by Last Audit, Days Since, Compliance, Building
- [ ] Sort direction toggles
- [ ] Arrow indicators show active sort

### Task 2.1.7: Colour Coding (Days Since Audit)
- [ ] Green background for <30 days
- [ ] Yellow background for 30-60 days
- [ ] Red background for >60 days
- [ ] Status badges match row colours
- [ ] Colour legend displays above table
- [ ] Summary counts by colour accurate

### Task 2.1.8: Trolley Detail - View Mode
- [ ] TrolleyDetailScreen created
- [ ] All core fields display correctly
- [ ] Equipment configuration visible
- [ ] Last audit information shows
- [ ] Audit status indicator displays
- [ ] Back to List button functional

### Task 2.1.9: Trolley Detail - Edit Mode
- [ ] Edit button visible to MERT only
- [ ] All editable fields show input controls
- [ ] Validation prevents incomplete saves
- [ ] Change log entries created
- [ ] Save and Cancel buttons functional
- [ ] No errors in edit workflows

### Task 2.1.10: Optional Equipment Toggles
- [ ] Paediatric box checkbox works
- [ ] Altered airway checkbox works
- [ ] Specialty medications checkbox works
- [ ] Specialty notes field conditional
- [ ] Equipment configuration saves correctly
- [ ] Change log records equipment changes

### Task 2.1.11: Add New Trolley Screen
- [ ] AddTrolleyScreen created
- [ ] All required fields validated
- [ ] Duplicate name check functional
- [ ] Optional equipment options available
- [ ] Save creates new Location record
- [ ] Change log entry created for new trolley
- [ ] New trolley appears in list immediately

### Task 2.1.12-2.1.14: Deactivate/Reactivate
- [ ] Deactivate button visible for active trolleys
- [ ] Deactivate dialog shows with reason dropdown
- [ ] Deactivation creates change log entry
- [ ] Status updates to Inactive
- [ ] Reactivate button visible for inactive trolleys
- [ ] Reactivate clears LastAuditDate
- [ ] No errors in dialog workflows

### Task 2.1.15-2.1.18: History Tab
- [ ] History tab displays in trolley detail
- [ ] Audit list shows all audits for trolley
- [ ] Compliance trend chart displays
- [ ] Chart shows improving/declining trends
- [ ] Summary statistics calculate correctly
- [ ] Open issues list shows for trolley
- [ ] Trend analysis provides insights
- [ ] All data updates when new audits complete

### General Quality Checks
- [ ] All screens accessible from navigation
- [ ] No hardcoded colours (all use variables)
- [ ] Permissions enforced (MERT-only actions)
- [ ] No console errors or warnings
- [ ] App saves and publishes successfully
- [ ] Performance acceptable with 76 trolleys
- [ ] Formulas are efficient and optimized
- [ ] Data validation working throughout
- [ ] All notifications display correctly
- [ ] Mobile layout responsive (if applicable)

---

## Common Issues and Troubleshooting

### Issue: Filters Not Working

**Symptoms:** Selected filter has no effect on gallery/table

**Solutions:**
1. Verify filter variable is being set on dropdown change
2. Check Items formula includes all filter conditions
3. Ensure column names match exactly (case-sensitive in some contexts)
4. Use Power Apps Monitor to verify variable values
5. Test with simpler formula first: `Filter(Location, Status = "Active")`

### Issue: Colour Coding Not Appearing

**Symptoms:** Rows not displaying colour backgrounds

**Solutions:**
1. Verify DaysSinceLastAudit calculated field is populated
2. Check that formula is in row Fill property, not Visible
3. Ensure colour variables are initialized in App.OnStart
4. Test colour formula in simple label first
5. Clear Power Apps cache and reload

### Issue: Sort Not Persisting

**Symptoms:** Clicking sort header doesn't change order

**Solutions:**
1. Verify sort variables initialized in App.OnStart
2. Check gallery Items formula includes Sort() function
3. Ensure column header has OnSelect handler
4. Test sort with single column first
5. Verify sort direction logic (Ascending vs Descending)

### Issue: Edit Form Not Saving

**Symptoms:** Save button clicked but no data changes

**Solutions:**
1. Check validation passes (set breakpoint in validation procedure)
2. Verify user has edit permissions on Location list
3. Check for formula errors in Patch() statement
4. Ensure all field names match Location list columns exactly
5. Review Power Automate for any blocking flows

### Issue: Performance Slow with Galleries

**Symptoms:** App takes long to load or scrolling is laggy

**Solutions:**
1. Reduce gallery Items to first 50 rows: `FirstN(Filter(...), 50)`
2. Move filters to before Sort(): `Sort(Filter(...), ...)`
3. Avoid nested lookups in gallery rows
4. Use Index() for faster lookups instead of Find()
5. Consider pagination for large lists

---

## Next Steps

After completing Phase 2.1, proceed with:

### Phase 2.3: Audit Entry Screens (Tasks 2.3.1-2.3.22)
- Build audit selection screen
- Create documentation check screen
- Implement equipment check with dynamic checklist
- Add condition and routine check screens

### Phase 2.5: Audit Submission (Tasks 2.5.1-2.5.15)
- Build review screen with compliance calculations
- Create submission workflow
- Implement audit PDF export

### Phase 3: Reporting and Dashboards
- Power BI compliance dashboards
- Historical data analysis
- Trend reporting

---

## Support and References

### Key Resources

- **Phase 1.6 PowerApp Foundation:** `implementation_guides/phase1_6_powerapp_foundation.md`
- **RBWH Program Specification:** `RBWH_Trolley_Audit_Program_Specification_v2.md`
- **SharePoint Location Schema:** `sharepoint_schemas/Location.json`
- **Seed Data:** `seed_data/Location.json`

### Power Apps Documentation

- PowerFx Formulas: https://learn.microsoft.com/power-apps/maker/canvas-apps/formula-reference
- Gallery Control: https://learn.microsoft.com/power-apps/maker/canvas-apps/controls/control-gallery
- Data Tables: https://learn.microsoft.com/power-apps/maker/canvas-apps/controls/control-data-table
- Filter Function: https://learn.microsoft.com/power-apps/maker/canvas-apps/functions/function-filter-lookup
- Sort Function: https://learn.microsoft.com/power-apps/maker/canvas-apps/functions/function-sort

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Documentation Team | Initial Phase 2.1 implementation guide |

---

**Document prepared for:** Royal Brisbane and Women's Hospital - MERT Program
**Document classification:** Internal - Implementation Guide
**Last updated:** January 2026
