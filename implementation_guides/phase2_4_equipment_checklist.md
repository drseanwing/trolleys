# RBWH Trolley Audit System
## Phase 2.4 Equipment Checklist Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 2.4.1 - 2.4.13
**Estimated Duration:** 24 hours

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Prerequisites](#prerequisites)
3. [Architecture Overview](#architecture-overview)
4. [Task 2.4.1-2.4.2: AuditEquipment SharePoint List](#task-241-242-auditequipment-sharepoint-list)
5. [Task 2.4.3-2.4.5: Equipment Check Screen Design](#task-243-245-equipment-check-screen-design)
6. [Task 2.4.6-2.4.7: Equipment Filtering Logic](#task-246-247-equipment-filtering-logic)
7. [Task 2.4.8-2.4.9: Quantity Input and Notes](#task-248-249-quantity-input-and-notes)
8. [Task 2.4.10-2.4.13: Scoring and Highlighting](#task-2410-2413-scoring-and-highlighting)
9. [Verification Checklist](#verification-checklist)
10. [Troubleshooting Guide](#troubleshooting-guide)

---

## Executive Summary

This guide covers the implementation of the Equipment Checklist feature (Phase 2.4), which represents a critical enhancement to the RBWH Trolley Audit system. Instead of a binary "all items stocked" response, the audit now captures item-level detail with quantity tracking, expiry verification, and real-time compliance scoring.

### What You'll Complete

| Task ID | Objective | Est. Hours | Dependency |
|---------|-----------|-----------|-----------|
| 2.4.1-2.4.2 | Create AuditEquipment list with lookups | 3 | Phase 1.5 |
| 2.4.3-2.4.5 | Build Equipment Check screen with accordion | 7 | 2.3.22 |
| 2.4.6-2.4.7 | Implement filtering by trolley config | 5 | 2.4.5 |
| 2.4.8-2.4.9 | Add quantity and notes inputs | 3 | 2.4.7 |
| 2.4.10-2.4.13 | Scoring, highlighting, and warnings | 4 | 2.4.9 |

**Total Duration:** Approximately 24 hours

### Key Features Delivered

- **89 equipment items** across 8 categories
- **Dynamic filtering** based on trolley configuration (paediatric box, defibrillator type)
- **Real-time scoring** showing equipment compliance percentage
- **Critical item highlighting** for items marked as essential
- **Quantity variance tracking** for understocked items
- **Item-level notes** for documenting issues or exceptions

### Site Architecture After Phase 2.4

```
Equipment Checklist Screen
├── Category Accordion (8 categories)
│   ├── Top of Trolley (12 items)
│   ├── Side of Trolley (8 items)
│   ├── Back of Trolley (6 items)
│   ├── Drawer 1 - IV Equipment (14 items)
│   ├── Drawer 2 - Medication & IV Fluids (18 items)
│   ├── Drawer 3 - Airway Equipment (15 items)
│   ├── Drawer 4 - PPE & Extra Equipment (12 items)
│   └── Paediatric Box (4 items)
└── Equipment Subscore Display
    ├── Compliant Items Count
    ├── Percentage (with colour coding)
    ├── Missing/Shortfall Summary
    └── Critical Item Warning (if any)
```

---

## Prerequisites

### Required from Previous Phases

- Phase 1.5: All core audit lists created (Audit, Equipment, EquipmentCategory)
- Phase 1.6: PowerApp foundation with data connections
- Phase 2.3: Audit selection and documentation screens complete
- Phase 2.3.22: Routine Checks screen ready (navigation point)

### Required Access & Permissions

- **SharePoint List Admin** - To create AuditEquipment list and configure lookups
- **PowerApp Editor** - To create/modify Equipment Check screen
- **Data source access** - To all existing SharePoint lists

### Required Information

Gather the following before starting:

1. **Equipment Master Data**
   - Copy of seed_data/Equipment.json
   - List of critical equipment items (for highlighting)
   - Any location-specific equipment overrides

2. **Trolley Configuration Data**
   - Which trolleys have paediatric boxes (HasPaedBox = true)
   - Which trolleys have which defibrillator types
   - Any equipment exceptions by location

3. **UI/UX Standards**
   - RBWH brand colours from Phase 1.1
   - Typography standards from Phase 1.6
   - Component library from Phase 1.6 (if available)

---

## Architecture Overview

### Data Model

The Equipment Checklist feature uses three interconnected SharePoint lists:

```
┌─────────────────────────┐
│ Audit (from Phase 1.5)  │
│ - AuditId (PK)          │
│ - LocationId (FK)       │
│ - AuditorName           │
│ - SubmissionStatus      │
└────────────┬────────────┘
             │ (1:N)
             ▼
┌─────────────────────────┐
│ AuditEquipment (NEW)    │
│ - AuditEquipId (PK)     │
│ - AuditId (FK)          │
│ - EquipmentId (FK)      │
│ - QuantityFound         │
│ - ExpiryOK              │
│ - IsCompliant (calc)    │
└────────────┬────────────┘
             │ (N:1)
             ▼
┌─────────────────────────┐
│ Equipment (from Phase 1.3)
│ - EquipmentId (PK)      │
│ - ItemName              │
│ - CategoryId (FK)       │
│ - StandardQuantity      │
│ - IsCritical            │
└─────────────────────────┘
             │ (N:1)
             ▼
┌─────────────────────────┐
│ EquipmentCategory       │
│ - CategoryId (PK)       │
│ - CategoryName          │
│ - SortOrder             │
└─────────────────────────┘
```

### Scoring Formula

```
EquipmentScore = (Compliant Items / Total Applicable Items) * 100

Where:
  Compliant Item = QuantityFound >= QuantityExpected AND
                   (not RequiresExpiryCheck OR ExpiryOK = true)

  Total Applicable Items = All Equipment marked IsActive = true
                          - Items filtered out (e.g., paediatric if no paed box)
```

---

## Task 2.4.1-2.4.2: AuditEquipment SharePoint List

### Objective

Create the AuditEquipment SharePoint list to store item-level equipment check results for each audit. This list captures the presence, quantity, and condition of each equipment item on the trolley.

### Prerequisites Checklist

- [ ] SharePoint site (RBWH Trolley Audit) exists
- [ ] Equipment list created with 89 items
- [ ] Audit list created with relationships configured
- [ ] EquipmentCategory list populated

### Step-by-Step Instructions

#### Step 1: Create the AuditEquipment List

**Action:** Navigate to your SharePoint site and create a new list

1. Go to **RBWH Trolley Audit** site
2. Click **+ New** → **List**
3. Select **Blank list**
4. Name the list: **AuditEquipment**
5. Description: *Item-level equipment check results from audits*
6. Click **Create**

#### Step 2: Add List Columns

After list creation, modify the default **Title** column and add the required columns:

**Column 1: Title (default, rename)**
- Internal Name: `Title`
- Type: Single line of text
- Description: *Equipment item name (from Equipment lookup)*
- Required: No
- Max Length: 150

**Column 2: Audit (Lookup)**
- Internal Name: `Audit`
- Type: Lookup
- Get information from: **Audit** list
- In this column: **Title** (or ID)
- Description: *Parent audit record*
- Required: Yes
- Allow multiple values: No

**Column 3: Equipment (Lookup)**
- Internal Name: `Equipment`
- Type: Lookup
- Get information from: **Equipment** list
- In this column: **Title** (or ID)
- Description: *Equipment item being checked*
- Required: Yes
- Allow multiple values: No

**Column 4: IsPresent (Yes/No)**
- Internal Name: `IsPresent`
- Type: Yes/No
- Description: *Was the item found on the trolley?*
- Default value: No

**Column 5: QuantityFound (Number)**
- Internal Name: `QuantityFound`
- Type: Number
- Description: *Actual count of items found*
- Required: No
- Decimals: 0
- Min: 0

**Column 6: QuantityExpected (Number)**
- Internal Name: `QuantityExpected`
- Type: Number
- Description: *Expected count from Equipment.StandardQuantity*
- Required: No
- Decimals: 0
- Min: 0

**Column 7: ExpiryChecked (Yes/No)**
- Internal Name: `ExpiryChecked`
- Type: Yes/No
- Description: *Was expiry date checked (if applicable)?*
- Default value: No

**Column 8: ExpiryOK (Yes/No)**
- Internal Name: `ExpiryOK`
- Type: Yes/No
- Description: *Is the item within expiry date?*
- Default value: Yes
- Note: Only relevant if ExpiryChecked = Yes

**Column 9: SizeChecked (Single line text)**
- Internal Name: `SizeChecked`
- Type: Single line of text
- Description: *Which sizes were found (e.g., "3, 4, 5")*
- Max Length: 50

**Column 10: ItemNotes (Multiple lines text)**
- Internal Name: `ItemNotes`
- Type: Multiple lines of text
- Description: *Issues or comments about this item*
- Number of lines: 3
- Rich text: No

#### Step 3: Add Calculated Columns

These computed columns are calculated in PowerFx during the audit, but optional to add in SharePoint for reporting:

**Calculated Column 1: QuantityVariance**
- Internal Name: `QuantityVariance`
- Type: Calculated (formula based on a list column)
- Formula: `=[QuantityFound]-[QuantityExpected]`
- Output type: Number
- Description: *Difference between found and expected (negative means shortfall)*

**Calculated Column 2: IsCompliant**
- Internal Name: `IsCompliant`
- Type: Calculated (formula based on a list column)
- Formula: `=[QuantityFound]>=[QuantityExpected]`
- Output type: Yes/No
- Description: *True if quantity meets or exceeds expected*
- Note: This is a simplified formula; PowerApp will also check ExpiryOK

#### Step 4: Create List Views

Create these views for operational use:

**View 1: All Items (Default)**
- Columns: Audit, Equipment, IsPresent, QuantityFound, QuantityExpected, IsCompliant
- Sort by: Equipment (Ascending)
- Filter: None

**View 2: By Audit**
- Columns: Equipment, IsPresent, QuantityFound, QuantityExpected, IsCompliant
- Group by: Audit
- Sort: Equipment (Ascending)

**View 3: Non-Compliant Items**
- Columns: Audit, Equipment, QuantityFound, QuantityExpected, QuantityVariance, ItemNotes
- Filter: `IsCompliant` equals `No`
- Sort by: QuantityVariance (Ascending)

**View 4: Missing Items**
- Columns: Audit, Equipment, ItemNotes
- Filter: `IsPresent` equals `No`
- Sort: Equipment (Ascending)

**View 5: Expiry Issues**
- Columns: Audit, Equipment, ExpiryChecked, ExpiryOK, ItemNotes
- Filter: `ExpiryChecked` equals `Yes` AND `ExpiryOK` equals `No`

### Verification Checkpoint

Test the new list:

```
✓ Can create a new AuditEquipment record
✓ Lookup to Audit list works (shows existing audits)
✓ Lookup to Equipment list works (shows all 89 items)
✓ Calculated columns show correct values
✓ All 5 views display without errors
✓ Can filter and sort all views
```

---

## Task 2.4.3-2.4.5: Equipment Check Screen Design

### Objective

Design and build the Equipment Check screen in the PowerApp with:
1. Category-based accordion (collapsible sections)
2. Equipment item row component (reusable for each item)
3. Dynamic loading of equipment based on trolley configuration

### Prerequisites Checklist

- [ ] AuditEquipment list created (Tasks 2.4.1-2.4.2)
- [ ] PowerApp foundation with Equipment data connection
- [ ] Audit Selection screen completed (2.3)
- [ ] Routine Checks screen completed (2.3.22)

### Architecture

The Equipment Check screen uses a hierarchical component structure:

```
EquipmentCheckScreen (Main screen)
├── Header
│   ├── Title: "Equipment Checklist"
│   ├── Trolley display: [Location.DisplayName]
│   └── Subtitle: "[Category Count] Categories, [Item Count] Items"
│
├── Equipment Subscore Display (Top)
│   ├── Percentage: "X% Complete"
│   ├── Colour-coded bar (Green/Yellow/Red)
│   ├── Count: "X/Y items at expected quantity"
│   └── Critical warning (if any)
│
├── CategoryAccordionContainer
│   │
│   ├── EquipmentCategory_1 (Top of Trolley)
│   │   ├── Header: Category name + item count
│   │   ├── EquipmentItemRow_1
│   │   ├── EquipmentItemRow_2
│   │   └── ... EquipmentItemRow_N
│   │
│   ├── EquipmentCategory_2 (Side of Trolley)
│   │   ├── Header: Category name + item count
│   │   ├── EquipmentItemRow_1
│   │   └── ... EquipmentItemRow_N
│   │
│   └── ... EquipmentCategory_8
│
└── Navigation Buttons
    ├── Back to Routine Checks
    ├── Review Summary (Preview)
    └── Next to Review Screen (Final submission)
```

### Step 1: Create Equipment Check Screen Structure

**Action:** Create a new screen in your PowerApp

1. In your RBWH Trolley Audit app, click **+ New screen**
2. Select **Blank**
3. Rename screen to **EquipmentCheckScreen**

**Screen Properties:**
- Width: 1024 (tablet)
- Height: 768
- Orientation: Landscape
- Background: #FFFFFF (white)

#### Add Screen Header

**Header Container (Rectangle)**
- Height: 80px
- Fill: #005FAD (RBWH Primary Blue)
- Position: Top, full width

**Title Label**
- Text: `"Equipment Checklist"`
- Font size: 28pt
- Font weight: Bold
- Colour: #FFFFFF
- Position: (20px, 15px)

**Trolley Display Label**
- Text: `Audit_SelectedTrolley.DisplayName`
- Font size: 16pt
- Colour: #FFFFFF
- Position: (20px, 50px)

#### Add Equipment Subscore Display Panel

**Subscore Container (Rectangle)**
- Height: 100px
- Fill: #F5F5F5 (light grey)
- Border: 1px #CCCCCC
- Position: Below header, full width

**Subscore Percentage Label**
- Text: `Text(Round(EquipmentSubscore, 0)) & "% Complete"`
- Font size: 24pt
- Font weight: Bold
- Colour: `If(EquipmentSubscore >= 90, ColorValue("#78BE20"), If(EquipmentSubscore >= 75, ColorValue("#FFB600"), ColorValue("#E81C23")))`
- Position: (20px, 15px)

**Subscore Detail Label**
- Text: `CompliantEquipmentCount & " of " & TotalEquipmentCount & " items at expected quantity"`
- Font size: 12pt
- Colour: #666666
- Position: (20px, 50px)

**Critical Warning Label** (Conditional)
- Visible: `HasCriticalMissingItems`
- Text: `"⚠️ CRITICAL ITEMS MISSING - See highlighted items below"`
- Font size: 14pt
- Font weight: Bold
- Colour: #E81C23 (Red)
- Background: #FFE6E6 (light red)
- Padding: 10px
- Position: Below percentage

### Step 2: Create Category Accordion Component

**Action:** Create a reusable component for category sections

1. Go to **Components** section
2. Click **+ New component**
3. Name: **EquipmentCategoryAccordion**
4. Width: 1000, Height: Variable

**Component Properties:**

| Property | Type | Description |
|----------|------|-------------|
| category | Record | Equipment category data |
| items | Table | Equipment items in this category |
| expandedByDefault | Boolean | Start expanded? |
| onItemChange | Event | Callback when item data changes |

**Component Structure:**

```
EquipmentCategoryAccordion
├── CategoryHeader (Rectangle + Button)
│   ├── Icon: ChevronDown (rotates when expanded)
│   ├── Title: category.CategoryName
│   ├── Count: CountRows(items) & " items"
│   └── Background: #E8F0F7 (light blue) on hover
│
└── CategoryContent (Conditional)
    └── VerticalContainer (if expanded)
        ├── EquipmentItemRow (repeating)
        ├── EquipmentItemRow
        └── ... for each item
```

**Category Header Code (OnSelect):**
```powerapps
Set(varCategoryExpanded, !varCategoryExpanded);
Notify("Category expanded");
```

### Step 3: Create Equipment Item Row Component

**Action:** Create a reusable row component for individual items

1. Click **+ New component**
2. Name: **EquipmentItemRow**
3. Width: 1000, Height: 120

**Component Properties:**

| Property | Type | Description |
|----------|------|-------------|
| equipment | Record | Equipment item data |
| quantityFound | Number | Actual quantity found |
| quantityExpected | Number | Expected quantity |
| notes | Text | Item notes |
| isCompliant | Boolean | Computed compliance |
| onQuantityChange | Event | Callback on qty change |
| onNotesChange | Event | Callback on notes change |

**Component Structure:**

```
EquipmentItemRow
├── Container (Rectangle)
│   ├── Background: #FFFFFF
│   ├── Border: 1px #EEEEEE
│   ├── Border Left: 4px [dynamic colour]
│   ├── Padding: 15px
│   └── Height: 120px
│
├── Row 1: Item Info
│   ├── CriticalBadge (if IsCritical)
│   │   └── Text: "CRITICAL"
│   │   └── Background: #E81C23
│   │   └── Colour: #FFFFFF
│   │
│   ├── ItemName
│   │   └── Text: equipment.ItemName
│   │   └── Font size: 14pt
│   │   └── Font weight: Bold
│   │
│   └── SupplierCode
│       └── Text: equipment.S4HANACode
│       └── Font size: 10pt
│       └── Colour: #999999
│
├── Row 2: Quantity Fields
│   ├── "Found:" Label + Numeric Input
│   │   └── Default: quantityExpected
│   │   └── Width: 60px
│   │   └── Validation: >= 0
│   │
│   ├── "/" + "Expected:" Label
│   │   └── Text: quantityExpected
│   │   └── Display only
│   │
│   ├── Variance Indicator
│   │   └── Text: If(quantityFound < quantityExpected,
│   │            quantityFound - quantityExpected & " SHORT", "✓")
│   │   └── Colour: If(quantityFound >= quantityExpected,
│   │            ColorValue("#78BE20"), ColorValue("#E81C23"))
│   │
│   └── Status Indicator
│       └── Icon: If(isCompliant, "✓", "✗")
│       └── Colour: If(isCompliant, #78BE20, #E81C23)
│
└── Row 3: Notes Field (if applicable)
    └── Notes input
    └── Placeholder: "Notes (optional)"
    └── Font size: 11pt
    └── Max length: 100
```

**Row Left Border Colour Logic:**

```powerapps
If(
  equipment.IsCritical && quantityFound = 0,
  ColorValue("#E81C23"),                    // Red: Critical missing
  If(
    quantityFound < quantityExpected,
    ColorValue("#FFB600"),                  // Orange: Shortfall
    ColorValue("#78BE20")                   // Green: Compliant
  )
)
```

### Step 4: Assemble Equipment Check Screen

**Action:** Add the accordion and rows to the main screen

1. Add a **Vertical scrollable container** below subscore panel
2. Add formula to generate category sections:

```powerapps
ForAll(
  AddColumns(
    EquipmentCategoryAccordion_LookUp,
    "Items",
    Filter(
      EquipmentData,
      CategoryId = [@Value],
      IsActive = true
    )
  ),
  EquipmentCategoryAccordion.EquipmentCategoryAccordion(
    Value,
    [@Items]
  )
)
```

3. Inside each accordion, add EquipmentItemRow for each item
4. Wire up OnSelect for expand/collapse logic

### Step 5: Add Navigation Buttons

**Footer Container**
- Height: 60px
- Background: #F5F5F5
- Position: Bottom, full width

**Back Button**
- Text: "← Back to Routine Checks"
- OnSelect: `Navigate(RoutineChecksScreen, ScreenTransition.Fade)`

**Preview Button**
- Text: "Preview Summary"
- OnSelect: `Navigate(ReviewScreen, ScreenTransition.Fade); Set(varEditMode, false)`

**Next Button**
- Text: "Next: Review & Submit →"
- OnSelect: `Navigate(ReviewScreen, ScreenTransition.Fade); Set(varEditMode, true)`

### Verification Checkpoint

Test the screen:

```
✓ Screen loads with correct header
✓ Equipment subscore displays and updates
✓ All 8 categories visible in accordion
✓ Categories can expand/collapse
✓ Each item shows in a row with correct formatting
✓ Critical items have red badge and left border
✓ Quantity input works and defaults to expected
✓ Notes field accepts text input
✓ Navigation buttons respond to clicks
```

---

## Task 2.4.6-2.4.7: Equipment Filtering Logic

### Objective

Implement dynamic equipment filtering so that:
1. Only applicable equipment items display based on trolley configuration
2. Defibrillator-specific equipment shows based on LIFEPAK type
3. Paediatric items only show if trolley has paediatric box

### Prerequisites Checklist

- [ ] Equipment Check Screen created (Tasks 2.4.3-2.4.5)
- [ ] Audit screen has trolley selection with Location record
- [ ] Equipment list includes IsCritical, IsPaediatric, DefibrillatorType fields
- [ ] Location record includes HasPaedBox and DefibrillatorType

### Filtering Strategy

The filtering logic executes in PowerApp formula, not SharePoint. This allows dynamic real-time filtering based on selected trolley properties.

### Step 1: Create Filter Configuration Variables

**Action:** Add these variables to your screen OnVisible:

```powerapps
// Get selected trolley location
Set(varSelectedLocation,
  LookUp(LocationData, ID = Audit_SelectedTrolley.ID)
);

// Extract trolley configuration
Set(varHasPaedBox, varSelectedLocation.HasPaedBox = true);
Set(varDefibrillatorType, varSelectedLocation.DefibrillatorType);

// Load all active equipment
Set(varAllEquipment,
  Filter(
    EquipmentData,
    IsActive = true
  )
);

// Initialize equipment tracking variables
Set(varEquipmentTracking, Blank());
Set(varFilteredEquipment, Blank());
```

### Step 2: Implement Primary Filtering Logic

**Action:** Add formula to filter equipment based on trolley config

```powerapps
Set(varFilteredEquipment,
  Filter(
    varAllEquipment,
    // Exclude paediatric items unless trolley has paed box
    (IsPaediatric = false OR varHasPaedBox = true) AND

    // Defibrillator-specific filtering
    (DefibrillatorType = "N/A" OR
     DefibrillatorType = varDefibrillatorType)
  )
)
```

### Step 3: Organize Filtered Equipment by Category

**Action:** Create grouped dataset for accordion display

```powerapps
Set(varEquipmentByCategory,
  GroupBy(
    varFilteredEquipment,
    CategoryId,
    "Items"
  )
)
```

**Data Structure Example:**
```
{
  CategoryId: "8f3a4b2c-1234-5678-9abc-def012345678",
  CategoryName: "Top of Trolley",
  SortOrder: 1,
  Items: [
    { EquipmentId: "...", ItemName: "Bag-Valve-Mask", ... },
    { EquipmentId: "...", ItemName: "Box of gloves", ... },
    ...
  ]
}
```

### Step 4: Handle Defibrillator-Specific Equipment

**Action:** Create more granular filtering for defib equipment

Some equipment items are specific to LIFEPAK defibrillator types:

| Equipment | LIFEPAK 1000 AED | LIFEPAK 20/20e |
|-----------|------------------|----------------|
| Adult Defibrillator Pads | ✓ | ✓ |
| Paediatric Pads (Bright Pink) | ✓ (if paed box) | ✗ |
| Combo Pads (Salmon Pink) | ✗ | ✓ (if paed box) |
| Cardiac monitoring cables | ✗ | ✓ |

**Defib Filter Logic:**

```powerapps
Set(varFilteredEquipmentByDefib,
  Filter(
    varFilteredEquipment,
    If(
      DefibrillatorType = "N/A",
      true,  // Equipment applies to all trolleys

      If(
        DefibrillatorType = "LIFEPAK_1000_AED",
        Or(
          SupplierCode <> "CELS_20_20e_ONLY",
          SupplierCode = ""
        ),

        If(
          DefibrillatorType = "LIFEPAK_20_20e",
          Or(
            SupplierCode = "CELS_20_20e_ONLY",
            SupplierCode = ""
          ),
          true
        )
      )
    )
  )
)
```

### Step 5: Recalculate on Trolley Change

**Action:** Add event handler when trolley selection changes

Add this to the screen's OnVisible and to any trolley selection control:

```powerapps
// When trolley changes, recalculate filters
OnSelect: (of trolley selection control)
Set(varSelectedLocation, ThisItem);
Set(varHasPaedBox, varSelectedLocation.HasPaedBox = true);
Set(varDefibrillatorType, varSelectedLocation.DefibrillatorType);

// Reapply all filters
Set(varFilteredEquipment,
  Filter(
    varAllEquipment,
    (IsPaediatric = false OR varHasPaedBox = true) AND
    (DefibrillatorType = "N/A" OR
     DefibrillatorType = varDefibrillatorType)
  )
);

// Update grouped by category
Set(varEquipmentByCategory,
  GroupBy(varFilteredEquipment, CategoryId, "Items")
);

Notify("Equipment list updated for " & varSelectedLocation.DisplayName)
```

### Step 6: Update Accordion to Use Filtered Data

**Action:** Modify accordion component to iterate filtered equipment

Replace the hardcoded data source with:

```powerapps
// In the accordion iteration formula:
ForAll(
  varEquipmentByCategory,
  EquipmentCategoryAccordion.EquipmentCategoryAccordion(
    Value,
    [@Items],
    false  // Don't expand by default
  )
)
```

### Filtering Examples

**Example 1: Standard Adult Trolley**
- HasPaedBox: false
- DefibrillatorType: LIFEPAK_1000_AED
- Result: 85 items (excludes paediatric items and LIFEPAK 20/20e specific)

**Example 2: Paediatric-Capable Trolley**
- HasPaedBox: true
- DefibrillatorType: LIFEPAK_1000_AED
- Result: 89 items (all items included)

**Example 3: Critical Care with 20/20e**
- HasPaedBox: false
- DefibrillatorType: LIFEPAK_20_20e
- Result: 82 items (includes 20/20e specific, excludes paediatric)

### Verification Checkpoint

Test filtering logic:

```
✓ Adult-only trolley shows 85 items
✓ Paediatric-capable trolley shows 89 items
✓ LIFEPAK 1000 shows correct defib pads
✓ LIFEPAK 20/20e shows correct defib pads
✓ Changing trolley selection updates equipment list
✓ Filtering preserves category organization
✓ All filtered items appear in correct categories
```

---

## Task 2.4.8-2.4.9: Quantity Input and Notes

### Objective

Implement quantity input fields with smart defaults and optional notes field for documenting item-specific issues.

### Prerequisites Checklist

- [ ] Equipment item row component created
- [ ] Equipment filtering working (Tasks 2.4.6-2.4.7)
- [ ] PowerApp data connections to Equipment list

### Step 1: Configure Quantity Found Input

**Action:** Update the EquipmentItemRow component's quantity input

**Quantity Input Control Properties:**

```
Control: NumberInput_QuantityFound

Type: Numeric input
Default value: quantityExpected
Minimum value: 0
Maximum value: 99
Decimals: 0
Width: 60px
Height: 36px

OnChange:
  Set(varItemChanged, true);
  varOnQuantityChange()

Format:
  If(Value < quantityExpected,
    Value & " ❌",
    Value & " ✓"
  )

BorderColor:
  If(Value < quantityExpected,
    ColorValue("#E81C23"),  // Red
    If(Value > quantityExpected,
      ColorValue("#FFB600"),  // Orange (overstocked)
      ColorValue("#78BE20")   // Green (at expected)
    )
  )
```

**Validation Rules:**

```powerapps
// OnChange validation
If(
  Value < 0,
  Notify("Quantity cannot be negative", NotificationType.Error);
  Set(NumberInput_QuantityFound, 0),

  If(
    Value > 99,
    Notify("Quantity exceeds maximum (99)", NotificationType.Warning);
    Set(NumberInput_QuantityFound, 99),

    // Valid entry
    Set(varItemChanged, true)
  )
)
```

### Step 2: Implement Smart Default Population

**Action:** Pre-populate quantity fields with expected values

When the EquipmentItemRow component loads:

```powerapps
// Component OnVisible
Set(varDefaultQuantity,
  LookUp(EquipmentData, ID = equipment.ID).StandardQuantity
);

Set(NumberInput_QuantityFound.Default, varDefaultQuantity)
```

**User Interaction Flow:**

1. **Item loads**: Quantity field shows expected quantity (e.g., "1")
2. **User edits**: Auditor changes value if different (e.g., "0" for missing)
3. **Live feedback**: Field shows visual indicator (✓ green, ❌ red, ⚠️ orange)
4. **Data persists**: Value saved when audit submitted

### Step 3: Add Item Notes Field

**Action:** Create optional notes input for each item

**Notes Input Control Properties:**

```
Control: TextInput_ItemNotes

Type: Multiline text input
Visible: By default hidden, show if:
  - User clicks "Add notes" button, OR
  - quantityFound <> quantityExpected (automatic)

Placeholder: "Document any issues (optional)"
Max length: 200
Height: 60px (expandable)
Default value: ""

OnChange:
  Set(varItemChanged, true)
```

**Conditional Visibility:**

```powerapps
// Show notes field if:
Visible:
  varShowNotes OR
  NumberInput_QuantityFound.Value <> quantityExpected
```

**Add Notes Toggle Button:**

```
Control: Button_AddNotes

Text: If(varShowNotes, "Hide notes", "Add notes")
OnSelect: Set(varShowNotes, !varShowNotes)
Visible: NumberInput_QuantityFound.Value = quantityExpected
```

### Step 4: Handle Notes for Expiry Issues

**Action:** Auto-show notes field for expiry-sensitive items

For equipment marked `RequiresExpiryCheck = true`:

```powerapps
// Add conditional notes prompting
If(
  equipment.RequiresExpiryCheck = true,
  [
    Label_ExpiryPrompt:
      Visible: true
      Text: "Expiry date checked?"

    Checkbox_ExpiryChecked:
      Visible: true
      Default: false
      OnChange: If(
        Value = true,
        Set(varShowExpiryNotes, true),
        Set(varShowExpiryNotes, false)
      )

    TextInput_ExpiryNotes:
      Visible: varShowExpiryNotes
      Placeholder: "e.g., Valid until 06/2026"
  ]
)
```

### Step 5: Create Item Change Tracking

**Action:** Track which items have been edited

At the component level:

```powerapps
// Global tracking for modified items
Set(varModifiedItems,
  Table(
    {
      EquipmentId: equipment.ID,
      OriginalQuantity: quantityExpected,
      NewQuantity: NumberInput_QuantityFound.Value,
      Notes: TextInput_ItemNotes.Value,
      Modified: NumberInput_QuantityFound.Value <> quantityExpected,
      LastModified: Now()
    }
  )
)
```

### Step 6: Bulk Notes Entry

**Action:** Create "Add common notes" dialog for repeated issues

```powerapps
// Add dialog screen for bulk notes
CommonNotesDialog:
  Visible: varShowCommonNotesDialog

  Controls:
    Title: "Add common issue to multiple items"

    NoteTemplate:
      Text input: "e.g., 'Not in stock', 'Expired', 'Damaged'"
      Options: [
        "Not in stock",
        "Expired",
        "Damaged",
        "Wrong size",
        "Misfiled location",
        "Unable to locate"
      ]

    SelectAffectedItems:
      Checkbox list of non-compliant items
      Pre-checked: All with shortage

    ApplyButton:
      OnSelect:
        ForAll(
          Filter(varFilteredEquipment, Checked = true),
          TextInput_ItemNotes.Value = NoteTemplate.Value
        );
        Set(varShowCommonNotesDialog, false)
```

### Step 7: Implement Data Validation

**Action:** Validate notes before submission

```powerapps
// Validation check when submitting audit
ValidateEquipmentNotes:
  Filter(
    varFilteredEquipment,
    And(
      NumberInput_QuantityFound.Value < quantityExpected,
      IsBlank(TextInput_ItemNotes.Value)
    )
  )

// On review screen, check for warnings
If(
  CountRows(ValidateEquipmentNotes) > 0,
  Notify(
    CountRows(ValidateEquipmentNotes) &
    " items with shortfalls are missing notes",
    NotificationType.Warning
  )
)
```

### Step 8: Update Review Screen with Notes Preview

**Action:** Show item notes in the review/summary screen

```powerapps
// In Review screen, add notes section
ItemsWithNotes:
  Filter(
    varFilteredEquipment,
    Not(IsBlank(TextInput_ItemNotes.Value))
  )

// Display in review
ForAll(
  ItemsWithNotes,
  Text(
    equipment.ItemName &
    " - Notes: " &
    TextInput_ItemNotes.Value
  )
)
```

### Verification Checkpoint

Test quantity and notes functionality:

```
✓ Quantity input defaults to expected value
✓ Can edit quantity to 0, 1, 2, etc.
✓ Visual indicators show (✓ green, ❌ red, ⚠️ orange)
✓ Notes field appears when quantity doesn't match expected
✓ Notes field shows for expiry-sensitive items
✓ Notes accept up to 200 characters
✓ Shortfalls without notes trigger warning
✓ Notes display in review screen
✓ Can add common notes to multiple items
```

---

## Task 2.4.10-2.4.13: Scoring and Highlighting

### Objective

Implement real-time equipment compliance scoring, visual highlighting of problem items, and critical item warnings.

### Prerequisites Checklist

- [ ] Equipment item row component complete
- [ ] Quantity and notes inputs working (Tasks 2.4.8-2.4.9)
- [ ] Equipment data includes IsCritical flag

### Step 1: Create Equipment Subscore Calculation

**Action:** Build real-time scoring formula

Add this formula to the Equipment Check screen OnVisible:

```powerapps
// Calculate equipment subscore
Set(varEquipmentSubscore,
  If(
    CountRows(varFilteredEquipment) = 0,
    0,

    (CountRows(
      Filter(
        varFilteredEquipment,
        And(
          NumberInput_QuantityFound.Value >= StandardQuantity,
          Or(
            RequiresExpiryCheck = false,
            ExpiryOK = true
          )
        )
      )
    ) / CountRows(varFilteredEquipment)) * 100
  )
)

// Track counts for display
Set(varCompliantEquipmentCount,
  CountRows(
    Filter(varFilteredEquipment, /* compliance check above */)
  )
);

Set(varTotalEquipmentCount, CountRows(varFilteredEquipment))
```

**Formula Explanation:**

```
Compliant Item =
  QuantityFound >= QuantityExpected AND
  (not RequiresExpiryCheck OR ExpiryOK = true)

EquipmentScore =
  (Count of Compliant Items / Total Applicable Items) × 100
```

### Step 2: Add Real-Time Score Updates

**Action:** Recalculate score on every quantity change

Add to each EquipmentItemRow's OnChange event:

```powerapps
// When quantity changes
OnChange (of NumberInput_QuantityFound):

  // Update tracking
  Set(varItemChanged, true);

  // Recalculate subscore
  Set(varEquipmentSubscore,
    If(
      CountRows(varFilteredEquipment) = 0,
      0,

      (CountRows(
        Filter(
          varFilteredEquipment,
          And(
            NumberInput_QuantityFound.Value >= StandardQuantity,
            Or(
              RequiresExpiryCheck = false,
              ExpiryOK = true
            )
          )
        )
      ) / CountRows(varFilteredEquipment)) * 100
    )
  );

  // Update display counts
  Set(varCompliantEquipmentCount,
    CountRows(
      Filter(
        varFilteredEquipment,
        NumberInput_QuantityFound.Value >= StandardQuantity
      )
    )
  )
```

### Step 3: Implement Subscore Display with Colour Coding

**Action:** Update the subscore display panel with dynamic styling

```powerapps
// Subscore Percentage Label
Label_SuscorePercentage:

Text:
  Text(Round(varEquipmentSubscore, 0)) & "%"

FontSize: 28

Bold: true

Color:
  If(
    varEquipmentSubscore >= 90,
    ColorValue("#78BE20"),    // Green
    If(
      varEquipmentSubscore >= 75,
      ColorValue("#FFB600"),  // Orange
      If(
        varEquipmentSubscore >= 50,
        ColorValue("#FF7700"), // Dark orange
        ColorValue("#E81C23")  // Red
      )
    )
  )

// Subscore Status Label
Label_SubscoreStatus:

Text:
  If(
    varEquipmentSubscore >= 90,
    "✓ Excellent",
    If(
      varEquipmentSubscore >= 75,
      "⚠️ Needs attention",
      If(
        varEquipmentSubscore >= 50,
        "❌ Concerning",
        "🚨 Critical"
      )
    )
  )

Color: (same as percentage label)
```

### Step 4: Create Item Highlighting Logic

**Action:** Highlight items that are below expected quantity

For each EquipmentItemRow, update the left border styling:

```powerapps
// ItemRow Border Colour

BorderColor:
  If(
    equipment.IsCritical = true && NumberInput_QuantityFound.Value = 0,
    ColorValue("#E81C23"),  // Red: Critical missing

    If(
      equipment.IsCritical = true && NumberInput_QuantityFound.Value < StandardQuantity,
      ColorValue("#FF7700"), // Dark orange: Critical shortage

      If(
        NumberInput_QuantityFound.Value < StandardQuantity,
        ColorValue("#FFB600"), // Orange: Non-critical shortage

        If(
          NumberInput_QuantityFound.Value > StandardQuantity,
          ColorValue("#FF9900"), // Light orange: Overstocked

          ColorValue("#78BE20")  // Green: At expected
        )
      )
    )
  )

// Item Row Background (subtle highlight)

Fill:
  If(
    equipment.IsCritical = true && NumberInput_QuantityFound.Value < StandardQuantity,
    ColorValue("#FFE6E6"),  // Light red background for critical

    If(
      NumberInput_QuantityFound.Value < StandardQuantity,
      ColorValue("#FFF5E6"), // Light orange background

      ColorValue("#FFFFFF")  // White background
    )
  )
```

### Step 5: Implement Critical Item Highlighting

**Action:** Identify and flag critical missing items

Critical items are defined as `IsCritical = true` in the Equipment list. Examples include:
- Bag-Valve-Mask Resuscitator
- Adrenaline
- Defibrillator pads
- Airway adjuncts
- IV cannulas

```powerapps
// Identify critical missing items
Set(varCriticalMissingItems,
  Filter(
    varFilteredEquipment,
    And(
      IsCritical = true,
      NumberInput_QuantityFound.Value = 0
    )
  )
);

// Set flag for display
Set(varHasCriticalMissingItems,
  CountRows(varCriticalMissingItems) > 0
);

// Identify critical shortfalls (below expected)
Set(varCriticalShortfalls,
  Filter(
    varFilteredEquipment,
    And(
      IsCritical = true,
      NumberInput_QuantityFound.Value > 0,
      NumberInput_QuantityFound.Value < StandardQuantity
    )
  )
)
```

### Step 6: Display Critical Warnings

**Action:** Show prominent warnings for critical issues

Add warning section to Equipment Check screen:

```powerapps
// CRITICAL WARNING BANNER
Label_CriticalWarning:

Visible: varHasCriticalMissingItems

Text:
  If(
    CountRows(varCriticalMissingItems) = 1,
    "⚠️ CRITICAL: " & First(varCriticalMissingItems).ItemName & " is MISSING",

    "⚠️ CRITICAL: " & CountRows(varCriticalMissingItems) &
    " critical items are MISSING: " &
    Concatenate(varCriticalMissingItems.ItemName, ", ")
  )

FontSize: 14
Bold: true
Color: ColorValue("#FFFFFF")

BackgroundFill: ColorValue("#E81C23")  // Red

Padding: 15px
BorderRadius: 4px

// Position at top of accordion, above all categories
```

### Step 7: Create Item Status Summary

**Action:** Show count of items by compliance status

```powerapps
// Item Status Tracking
Set(varItemStatusSummary,
  [
    {
      Status: "At Expected Quantity",
      Count: CountRows(Filter(
        varFilteredEquipment,
        NumberInput_QuantityFound.Value = StandardQuantity
      )),
      Colour: ColorValue("#78BE20")  // Green
    },

    {
      Status: "Overstocked",
      Count: CountRows(Filter(
        varFilteredEquipment,
        NumberInput_QuantityFound.Value > StandardQuantity
      )),
      Colour: ColorValue("#FF9900")  // Light orange
    },

    {
      Status: "Understocked",
      Count: CountRows(Filter(
        varFilteredEquipment,
        And(
          NumberInput_QuantityFound.Value > 0,
          NumberInput_QuantityFound.Value < StandardQuantity
        )
      )),
      Colour: ColorValue("#FFB600")  // Orange
    },

    {
      Status: "Missing",
      Count: CountRows(Filter(
        varFilteredEquipment,
        NumberInput_QuantityFound.Value = 0
      )),
      Colour: ColorValue("#E81C23")  // Red
    }
  ]
);

// Display as inline counts
Label_ItemStatusBar:

Text:
  Concatenate(
    ForAll(varItemStatusSummary,
      Status & ": " & Count & " | "
    )
  )

FontSize: 12
Colour: #333333
```

### Step 8: Add Critical Item Badge

**Action:** Mark each critical item with a badge

In the EquipmentItemRow component:

```powerapps
// Critical Badge (conditional)
Label_CriticalBadge:

Visible: equipment.IsCritical = true

Text: "CRITICAL"

BackgroundFill: ColorValue("#E81C23")  // Red
Color: ColorValue("#FFFFFF")
Bold: true
FontSize: 11

Padding: 5px 8px
BorderRadius: 3px

// Position: Top right of item row
```

### Step 9: Implement Scoring Persistence

**Action:** Save subscore to AuditEquipment records

When audit is submitted (via Power Automate flow):

```json
{
  "EquipmentSubscore": varEquipmentSubscore,
  "CompliantItemCount": varCompliantEquipmentCount,
  "TotalItemCount": varTotalEquipmentCount,
  "CriticalMissingCount": CountRows(varCriticalMissingItems),
  "CriticalShortfallCount": CountRows(varCriticalShortfalls),
  "CalculatedAt": Now()
}
```

### Step 10: Add Scoring Explanation Tooltip

**Action:** Help users understand the score

```powerapps
// Tooltip on subscore label
Hover (on Label_SubscorePercentage):

Tooltip:
  "Equipment Score = (Items at expected quantity / Total items) × 100" &
  Char(10) & Char(10) &
  "This trolley has:" & Char(10) &
  "✓ " & varCompliantEquipmentCount & " items at expected quantity" & Char(10) &
  "❌ " & (varTotalEquipmentCount - varCompliantEquipmentCount) &
  " items below expected quantity"
```

### Verification Checkpoint

Test scoring and highlighting:

```
✓ Subscore starts at 0% when all quantities are 0
✓ Subscore increases to 100% when all quantities meet expected
✓ Colour changes: Red < 50%, Orange 50-75%, Yellow 75-90%, Green ≥ 90%
✓ Critical items show red badge
✓ Critical items highlight with red left border
✓ Non-critical shortfalls show orange
✓ Overstocked items show light orange
✓ Critical missing warning displays prominently
✓ Item status summary shows counts
✓ Score recalculates on every quantity change
✓ Scoring formula is correct mathematically
```

---

## Integration with Review Screen

### Equipment Subscore in Overall Compliance

The Equipment Subscore contributes 40% to the overall audit compliance score:

```
Overall Compliance =
  (DocumentScore × 0.25) +
  (EquipmentScore × 0.40) +
  (ConditionScore × 0.15) +
  (CheckScore × 0.20)
```

In the Review screen, display:

```powerapps
// Equipment Score Breakdown
Label_EquipmentScoreBreakdown:

Text:
  "Equipment Compliance: " &
  Text(Round(varEquipmentSubscore, 1)) & "% " &
  "(40% of overall score = " &
  Text(Round((varEquipmentSubscore / 100) * 0.40 * 100, 1)) &
  " points)"

// Add to overall calculation
Set(varOverallCompliance,
  ((varDocumentScore/100) * 0.25) +
  ((varEquipmentSubscore/100) * 0.40) +
  ((varConditionScore/100) * 0.15) +
  ((varCheckScore/100) * 0.20)
)
```

---

## Verification Checklist

### SharePoint List Verification

- [ ] AuditEquipment list created with all columns
- [ ] Lookup columns reference Audit and Equipment lists correctly
- [ ] Calculated columns (QuantityVariance, IsCompliant) compute correctly
- [ ] All 5 views created and accessible
- [ ] Can create test records in AuditEquipment list

### Screen Design Verification

- [ ] Equipment Check screen loads without errors
- [ ] Header displays trolley name
- [ ] Subscore panel visible and formatted
- [ ] Category accordion displays all 8 categories
- [ ] Categories expand/collapse smoothly
- [ ] Each item row displays with correct formatting

### Filtering Verification

- [ ] Adult-only trolleys show 85 items
- [ ] Paediatric-capable trolleys show 89 items
- [ ] Defibrillator-specific items filter correctly
- [ ] Changing trolley updates equipment list dynamically
- [ ] Filtered items appear in correct categories

### Quantity and Notes Verification

- [ ] Quantity input defaults to expected value
- [ ] Can edit quantity from 0-99
- [ ] Visual indicators (✓ ❌ ⚠️) display correctly
- [ ] Notes field shows when quantity differs
- [ ] Can enter and save notes (max 200 chars)
- [ ] Shortfalls without notes trigger warning

### Scoring Verification

- [ ] Subscore starts at 0% with no items checked
- [ ] Subscore reaches 100% when all items at expected
- [ ] Score recalculates on each quantity change
- [ ] Colour coding: Red < 50%, Orange 50-75%, Yellow 75-90%, Green ≥ 90%
- [ ] Item count displays correctly (X/Y items)
- [ ] Critical missing items show warning banner
- [ ] Critical items have red badge and border

### Navigation Verification

- [ ] Back button returns to Routine Checks screen
- [ ] Preview button opens Review screen (read-only mode)
- [ ] Next button opens Review screen (edit-enabled mode)
- [ ] Can navigate between Equipment and Review screens
- [ ] Data persists when navigating

### Data Persistence Verification

- [ ] Equipment selections saved to AuditEquipment records
- [ ] Quantity values persist across screen navigation
- [ ] Notes persist across screen navigation
- [ ] Subscore calculated and stored

---

## Troubleshooting Guide

### Screen Performance Issues

**Problem:** Equipment Check screen loads slowly

**Diagnosis:**
1. Check number of items being filtered
2. Check for circular formulas in component
3. Monitor Power Automate call counts

**Solutions:**
- Use `AllowSideEffects(false)` in calculations
- Lazy-load categories (expand only what user clicks)
- Cache filtered equipment in variable instead of recalculating

```powerapps
// Cache filtered equipment on screen load (better performance)
OnVisible:
  Set(varFilteredEquipment, Filter(...));
  Set(varEquipmentByCategory, GroupBy(...))

// Don't recalculate on every refresh
```

### Filtering Not Working

**Problem:** Wrong items showing or items not appearing

**Diagnosis:**
1. Check varFilteredEquipment formula
2. Verify Location record HasPaedBox and DefibrillatorType values
3. Check Equipment data for IsPaediatric and DefibrillatorType

**Solutions:**
- Verify Location HasPaedBox is Boolean (not text "true"/"false")
- Check Equipment DefibrillatorType values match expected codes
- Add debugging label to show count of filtered items:

```powerapps
Label_DebugFilterCount:
  Text: "Filtered: " & CountRows(varFilteredEquipment) & " items"
  Visible: IsBlank(Text(varDebugMode))
```

### Quantity Input Not Updating

**Problem:** Changing quantity doesn't update subscore

**Diagnosis:**
1. Check NumberInput OnChange event
2. Verify subscore recalculation formula
3. Check for binding issues

**Solutions:**
- Ensure `Set(varEquipmentSubscore, ...)` is in OnChange
- Verify subscore label references varEquipmentSubscore
- Add refresh on explicit button click:

```powerapps
Button_RefreshScore:
  OnSelect:
    Set(varEquipmentSubscore,
      (CountRows(Filter(...)) / CountRows(varFilteredEquipment)) * 100
    )
```

### Critical Items Not Highlighting

**Problem:** Critical item badge or warning not showing

**Diagnosis:**
1. Check Equipment IsCritical field values
2. Verify varCriticalMissingItems formula
3. Check visibility condition on warning label

**Solutions:**
- Add debugging to show critical items:

```powerapps
Label_DebugCritical:
  Text: "Critical: " & CountRows(varCriticalMissingItems)
  Visible: true
```

- Verify IsCritical field in Equipment list is populated
- Test with known critical item (e.g., BVM)

### Accordion Expansion Issues

**Problem:** Categories won't expand/collapse

**Diagnosis:**
1. Check OnSelect event on category header
2. Verify varCategoryExpanded variable is set
3. Check visibility condition on content

**Solutions:**
- Add debugging to category expand logic:

```powerapps
Button_CategoryHeader:
  OnSelect:
    Set(varCategoryExpanded, !varCategoryExpanded);
    Notify("Category: " & varCategoryExpanded)
```

- Ensure content visibility condition correctly references varCategoryExpanded
- Verify container uses correct visibility syntax

### Data Not Saving to SharePoint

**Problem:** Audit submitted but AuditEquipment records not created

**Diagnosis:**
1. Check Power Automate flow execution
2. Verify Audit lookup in AuditEquipment works
3. Check for flow errors or throttling

**Solutions:**
- Review flow run history in Power Automate
- Test manual record creation in AuditEquipment list
- Verify Audit record exists before creating AuditEquipment items
- Add delay in flow if hitting throttling:

```
Delay: 100 milliseconds
Between each item creation
```

---

## Complete Equipment Checklist

### Final Verification Before Go-Live

- [ ] SharePoint lists created and populated
- [ ] PowerApp screens functional and styled
- [ ] All filtering logic working correctly
- [ ] Scoring calculations accurate
- [ ] Navigation flow smooth
- [ ] Data persists correctly
- [ ] Performance acceptable (< 2s load time)
- [ ] Tested on tablet and mobile devices
- [ ] Tested with 89 items (performance)
- [ ] Tested with paediatric box filtering
- [ ] Tested with both defibrillator types
- [ ] User acceptance testing passed
- [ ] Documentation complete
- [ ] Help text and tooltips in place

---

## Related Tasks

After completing Phase 2.4, proceed with:

- **2.5.1-2.5.15:** Audit Submission (Review screen and overall compliance calculation)
- **3.1.1-3.1.9:** Dashboard KPIs (Equipment subscore display)
- **3.2.3-3.2.16:** Power BI Reports (Equipment compliance trending)

---

## Reference Materials

- `sharepoint_schemas/AuditEquipment.json` - List schema
- `sharepoint_schemas/Equipment.json` - Equipment master schema
- `seed_data/Equipment.json` - 89 equipment items with all attributes
- `RBWH_Resuscitation_Trolley_Audit_Schema.md` - Data model reference
- `implementation_guides/phase1_6_powerapp_foundation.md` - Component patterns

---

## Support Contacts

For implementation questions or issues:

- **SharePoint Admin:** [Contact RBWH IT]
- **PowerApp Development:** [Contact Power Platform Team]
- **Business Logic:** [Contact MERT Educator]

---

**Document Version:** 1.0
**Last Updated:** January 2026
**Next Review:** After Phase 2.4 implementation complete

