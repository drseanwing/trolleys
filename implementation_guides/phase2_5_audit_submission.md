# Phase 2.5 Audit Submission Implementation Guide

**RBWH Resuscitation Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 2.5 implements the Audit Submission workflow, including the Review screen, compliance scoring calculations, and Power Automate flows for submitting completed audits and saving draft audits. This phase enables users to review all audit responses, see their compliance score breakdown, make final edits, and submit or save their audit work.

**Phase Scope:** Tasks 2.5.1 through 2.5.15
**Estimated Duration:** 26 hours
**Prerequisites:**
- Phase 1.1-1.6 complete (SharePoint foundation, PowerApp foundation, data connections)
- Phase 2.3-2.4 complete (Audit entry screens, equipment checklist)
- All audit data collection screens implemented

---

## Part 1: Review Screen Design (Tasks 2.5.1-2.5.5)

### Task 2.5.1: Create Review Screen

#### Objective

Build the Review screen that displays a comprehensive summary of all audit responses collected across all sections.

#### Prerequisites

- All audit entry screens completed (Documentation, Condition, Routine Checks, Equipment)
- HomeScreen navigation configured
- Global colour theme variables available

#### Step-by-Step Instructions

##### Step 1: Create New Screen

1. In Power Apps Studio, create a new screen called `ReviewScreen`
2. Set screen properties:
   - **Width:** 1366
   - **Height:** 768
   - **Fill:** `BackgroundColor`

##### Step 2: Add Navigation Header

1. Copy the header from HomeScreen or another screen
2. Paste at the top (Y: 0, Height: 80)
3. Ensure navigation menu is functional

##### Step 3: Create Main Review Container

1. Insert a **Rectangle** for the main content area:
   - **X:** 20
   - **Y:** 100
   - **Width:** 1326
   - **Height:** 650
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 1
   - **Radius:** 8px

##### Step 4: Add Review Screen Title

1. Insert a **Label** at the top of the review container:
   - **Text:** "Audit Review & Submit"
   - **Font Size:** 20pt, Bold
   - **Color:** `TextPrimary`
   - **Y:** 120
   - **X:** 40

##### Step 5: Add Summary Sections Container

1. Create a **Vertical Gallery** to display summary sections:
   - **X:** 40
   - **Y:** 160
   - **Width:** 1280
   - **Height:** 550
   - **Items:** Collection of summary section objects (to be populated)
   - **TemplatePadding:** 20
   - **TemplateSize:** 120

2. Inside the gallery template, structure sections for:
   - Documentation Checks Summary
   - Condition Checks Summary
   - Routine Checks Summary
   - Equipment Checks Summary

##### Step 6: Make Sections Collapsible (Optional Enhancement)

1. Add a **Toggle** or **Dropdown** icon to each section header
2. Implement show/hide logic using variables:
   ```powerfx
   Set(varShowDocumentationDetails, !varShowDocumentationDetails)
   ```

#### PowerFx Code

Initialize collection on screen OnVisible:

```powerfx
// ReviewScreen.OnVisible

// Create summary data structure
ClearCollect(
    colReviewSections,
    {
        Section: "Documentation Checks",
        Order: 1,
        Expanded: true,
        Icon: "📄"
    },
    {
        Section: "Trolley Condition",
        Order: 2,
        Expanded: true,
        Icon: "🔧"
    },
    {
        Section: "Routine Checks",
        Order: 3,
        Expanded: true,
        Icon: "✓"
    },
    {
        Section: "Equipment Checklist",
        Order: 4,
        Expanded: true,
        Icon: "📦"
    }
);

// Load current audit data
Set(varCurrentAudit, LookUp(Audit, Title = varAuditId));

// Load related child records
ClearCollect(
    colCurrentDocuments,
    Filter(AuditDocuments, Audit.Value = varAuditId)
);

ClearCollect(
    colCurrentCondition,
    Filter(AuditCondition, Audit.Value = varAuditId)
);

ClearCollect(
    colCurrentChecks,
    Filter(AuditChecks, Audit.Value = varAuditId)
);

ClearCollect(
    colCurrentEquipment,
    Filter(AuditEquipment, Audit.Value = varAuditId)
)
```

#### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Main Container | Width | 1326 |
| | Height | 650 |
| | Background | White |
| Summary Gallery | Items | colReviewSections |
| | TemplatePadding | 20 |
| Section Headers | Font Size | 16pt Bold |
| | Color | PrimaryColor |

#### Verification Checklist

- [ ] ReviewScreen created successfully
- [ ] Navigation header displays correctly
- [ ] Title "Audit Review & Submit" visible
- [ ] Main content container displays
- [ ] Gallery structure ready for sections
- [ ] OnVisible event loads summary collections
- [ ] No formula errors in Power Apps Monitor
- [ ] Screen saves without errors

---

### Task 2.5.2: Display All Responses Summary

#### Objective

Show all audit responses from each section in a readable, organized format within the review screen.

#### Prerequisites

- ReviewScreen created (Task 2.5.1)
- All audit entry data available in collections
- Current audit reference available in variable

#### Step-by-Step Instructions

##### Step 1: Create Documentation Summary Section

1. In the gallery template from Task 2.5.1, add section content for Documentation:

   **Section Header Label:**
   - **Text:** `"📄 Documentation Checks"`
   - **Font Size:** 14pt Bold
   - **Color:** `PrimaryColor`

   **Summary Content (Nested Labels):**

   ```
   Check Record: [Current/Old/None]
   Checking Guidelines: [Current/Old/None]
   BLS Poster Present: [Yes/No]
   Equipment List: [Current/Old/None]
   Notes: [Any notes entered]
   ```

2. For each response, create a label pair:
   - **Label 1 (Field Name):** `TextSecondary` colour, right-aligned, 12pt
   - **Label 2 (Value):** `TextPrimary` colour, bold, 12pt

3. Add conditional styling:
   ```powerfx
   // For BLS Poster value
   If(
       colCurrentDocuments[1].BLSPosterPresent,
       "Yes - ✓",
       "No"
   )
   ```

##### Step 2: Create Condition Summary Section

1. Add similar section for trolley condition checks:

   **Summary Content:**

   ```
   Trolley Clean: [Yes/No] ✓
   Working Order: [Yes/No] ✓
   Issue Description: [If not working]
   Rubber Bands Used: [Yes/No] ✗ (should be No)
   O2 Tubing Correct: [Yes/No] ✓
   INHALO Cylinder OK: [Yes/No] ✓
   Additional Notes: [Any notes]
   ```

2. Use conditional formatting to highlight issues:
   ```powerfx
   // For each boolean check
   If(
       ThisItem.IsClean,
       RGBA(76, 175, 80, 1),    // Green checkmark
       RGBA(229, 61, 61, 1)      // Red X
   )
   ```

##### Step 3: Create Routine Checks Summary Section

1. Display check count information:

   **Summary Content:**

   ```
   Outside Checks Completed: [Number]
   Outside Checks Expected: [Number]
   Outside Compliance: [Percentage]%

   Inside Checks Completed: [Number]
   Inside Checks Expected: [Number]
   Inside Compliance: [Percentage]%

   Counts Not Available: [Yes/No]
   Reason (if N/A): [Text]
   ```

2. Use conditional display for "Counts Not Available" reason:
   ```powerfx
   // Show reason field only if CountNotAvailable = true
   Visible: colCurrentChecks[1].CountNotAvailable
   ```

##### Step 4: Create Equipment Summary Section

1. Display equipment checklist in summary format:

   **Summary Header:**
   - Total items checked: `CountRows(colCurrentEquipment)`
   - Compliant items: `CountRows(Filter(colCurrentEquipment, IsCompliant))`
   - Non-compliant items: `CountRows(Filter(colCurrentEquipment, NOT(IsCompliant)))`

2. Create a scrollable summary list:
   ```powerfx
   // Summary by category
   Filter(
       colCurrentEquipment,
       NOT(IsCompliant)  // Show only items below expected quantity
   )
   ```

3. For non-compliant items, display:
   - **Equipment Name**
   - **Expected Quantity:** [X]
   - **Quantity Found:** [Y]
   - **Shortfall:** [X - Y]
   - **Notes:** [Any notes entered]

##### Step 5: Add Edit Navigation Buttons

1. Below each section summary, add an "Edit" button:
   - **Text:** "Edit [Section Name]"
   - **Fill:** `SecondaryColor` (soft blue for navigation)
   - **Text Color:** White
   - **OnSelect:**
     ```powerfx
     Set(varEditingSection, ThisItem.Section);
     Navigate(DocumentationCheckScreen)  // Or appropriate screen
     ```

2. Create a mapping collection for section navigation:
   ```powerfx
   ClearCollect(
       colSectionNavigation,
       {
           Section: "Documentation Checks",
           Screen: "DocumentationCheckScreen"
       },
       {
           Section: "Trolley Condition",
           Screen: "ConditionCheckScreen"
       },
       {
           Section: "Routine Checks",
           Screen: "RoutineChecksScreen"
       },
       {
           Section: "Equipment Checklist",
           Screen: "EquipmentCheckScreen"
       }
   )
   ```

#### PowerFx Code

Complete summary display formulas:

```powerfx
// Documentation Summary Display
"Check Record: " & (
    LookUp(
        colCurrentDocuments,
        Audit.Value = varAuditId
    ).CheckRecordStatus ?? "None"
) &
Char(13) &
"Checking Guidelines: " & (
    LookUp(
        colCurrentDocuments,
        Audit.Value = varAuditId
    ).CheckGuidelinesStatus ?? "None"
) &
Char(13) &
"BLS Poster: " & If(
    LookUp(
        colCurrentDocuments,
        Audit.Value = varAuditId
    ).BLSPosterPresent,
    "Yes ✓",
    "No"
) &
Char(13) &
"Equipment List: " & (
    LookUp(
        colCurrentDocuments,
        Audit.Value = varAuditId
    ).EquipmentListStatus ?? "None"
)

// Condition Summary with Status Icons
"Clean: " & If(
    LookUp(
        colCurrentCondition,
        Audit.Value = varAuditId
    ).IsClean,
    "✓ Yes",
    "✗ No"
) &
Char(13) &
"Working Order: " & If(
    LookUp(
        colCurrentCondition,
        Audit.Value = varAuditId
    ).IsWorkingOrder,
    "✓ Yes",
    "✗ No"
) &
Char(13) &
"Rubber Bands: " & If(
    LookUp(
        colCurrentCondition,
        Audit.Value = varAuditId
    ).RubberBandsUsed,
    "✗ Yes (Inappropriate)",
    "✓ No"
) &
Char(13) &
"O2 Tubing: " & If(
    LookUp(
        colCurrentCondition,
        Audit.Value = varAuditId
    ).O2TubingCorrect,
    "✓ Correct",
    "✗ Incorrect"
) &
Char(13) &
"INHALO Cylinder: " & If(
    LookUp(
        colCurrentCondition,
        Audit.Value = varAuditId
    ).InhaloCylinderOK,
    "✓ OK",
    "✗ Low Pressure"
)

// Equipment Non-Compliant Items Summary
Filter(
    colCurrentEquipment,
    QuantityFound < QuantityExpected
)

// Count summary
"Equipment Status: " &
CountRows(Filter(colCurrentEquipment, IsCompliant)) &
" of " &
CountRows(colCurrentEquipment) &
" items compliant"
```

#### Component Specifications

| Section | Field Display | Format |
|---------|----------------|--------|
| Documentation | Check Record Status | Choice value with label |
| | Guidelines Status | Choice value with label |
| | BLS Poster | Boolean with "Yes/No" |
| | Equipment List Status | Choice value with label |
| Condition | Trolley Clean | Boolean with ✓/✗ icon |
| | Working Order | Boolean with ✓/✗ icon |
| | Rubber Bands | Boolean with warning if Yes |
| | O2 Tubing | Boolean with ✓/✗ icon |
| | INHALO Cylinder | Boolean with ✓/✗ icon |
| Checks | Outside Count | "X of Y (Z%)" format |
| | Inside Count | "X of Y (Z%)" format |
| | Not Available Reason | Text (conditional display) |
| Equipment | Item Summary | "Item: X of Y found" |
| | Shortfall | "Missing Z units" with warning |

#### Verification Checklist

- [ ] Documentation summary displays all four fields
- [ ] Check Record status shows (Current/Old/None)
- [ ] Condition checks display with ✓/✗ icons
- [ ] Rubber Bands show warning icon when Yes
- [ ] Routine check counts display as "X of Y (Z%)"
- [ ] Equipment non-compliant items highlighted
- [ ] Edit buttons present for each section
- [ ] All summaries pull from correct collections
- [ ] Conditional fields display only when relevant
- [ ] All text labels are clear and readable
- [ ] No formula errors in Power Apps Monitor
- [ ] Screen scrolls smoothly if content exceeds viewport

---

### Task 2.5.3: Calculate Overall Compliance Score

#### Objective

Implement the weighted compliance scoring formula to calculate the overall audit score from all four subscore categories.

#### Prerequisites

- All audit data captured and stored in collections
- Subscore calculations available (Documentation, Condition, Equipment, Checks)
- Power Automate flow infrastructure ready

#### Compliance Score Formula Specification

The overall compliance score is a weighted average of four subscores:

```
OVERALL = (DOC * 0.20) + (COND * 0.30) + (CHECKS * 0.20) + (EQUIP * 0.30)

Where:
- DOC (Documentation): 20% weight
- COND (Condition): 30% weight
- CHECKS (Routine Checks): 20% weight
- EQUIP (Equipment): 30% weight
```

#### Documentation Score Calculation (20% weight)

**Components (4 items, each 25% of Documentation score):**

| Item | Current | Old | None |
|------|---------|-----|------|
| Check Record | 1.0 | 0.5 | 0.0 |
| Checking Guidelines | 1.0 | 0.5 | 0.0 |
| BLS Poster | 1.0 | N/A | 0.0 |
| Equipment List | 1.0 | 0.5 | 0.0 |

**Formula:**
```
DocScore = (CheckRecord + Guidelines + BLSPoster + EquipmentList) / 4 * 100

Where:
- CheckRecord = 1 if Current, 0.5 if Old, 0 if None
- Guidelines = 1 if Current, 0.5 if Old, 0 if None
- BLSPoster = 1 if Yes, 0 if No
- EquipmentList = 1 if Current, 0.5 if Old, 0 if None
```

#### Condition Score Calculation (30% weight)

**Components (5 binary checks):**

| Item | Passing Value | Points |
|------|---------------|--------|
| Is Clean | True | 1.0 |
| Is Working Order | True | 1.0 |
| Rubber Bands (inverted) | False | 1.0 |
| O2 Tubing Correct | True | 1.0 |
| INHALO Cylinder OK | True | 1.0 |

**Formula:**
```
ConditionScore = (
    IF(IsClean, 1, 0) +
    IF(IsWorkingOrder, 1, 0) +
    IF(NOT(RubberBandsUsed), 1, 0) +
    IF(O2TubingCorrect, 1, 0) +
    IF(InhaloCylinderOK, 1, 0)
) / 5 * 100
```

#### Routine Checks Score Calculation (20% weight)

**Components:**

- **Outside Checks Compliance:** `(OutsideCheckCount / ExpectedOutside) * 100`, capped at 100%
- **Inside Checks Compliance:** `(InsideCheckCount / ExpectedInside) * 100`, capped at 100%

**Special Cases:**
- If `CountNotAvailable = true`, score is 0 (no credit if counts unavailable)
- If expected count is 0, score is 100% (no checks required)

**Formula:**
```
OutsideCompliance = IF(
    CountNotAvailable,
    0,
    IF(
        ExpectedOutside = 0,
        100,
        MIN(100, (OutsideCheckCount / ExpectedOutside) * 100)
    )
)

InsideCompliance = IF(
    CountNotAvailable,
    0,
    IF(
        ExpectedInside = 0,
        100,
        MIN(100, (InsideCheckCount / ExpectedInside) * 100)
    )
)

ChecksScore = (OutsideCompliance + InsideCompliance) / 2
```

#### Equipment Score Calculation (30% weight)

**Components:**

Count the number of equipment items that meet or exceed expected quantity:

```
CompliantItems = COUNT(QuantityFound >= QuantityExpected)
TotalItems = COUNT(ALL equipment items)

EquipmentScore = (CompliantItems / TotalItems) * 100
```

**Considerations:**
- Only count active equipment items
- Filter by trolley configuration (paediatric box, defibrillator type)
- Include all checked items in the audit
- If zero items checked, score is 0

#### Step-by-Step Implementation

##### Step 1: Create Calculation Variables in ReviewScreen.OnVisible

```powerfx
// ReviewScreen.OnVisible - Calculate all subscores

// Get current audit's child records
Set(varCurrentDocAudit,
    LookUp(
        colCurrentDocuments,
        Audit.Value = varAuditId
    )
);

Set(varCurrentCondAudit,
    LookUp(
        colCurrentCondition,
        Audit.Value = varAuditId
    )
);

Set(varCurrentCheckAudit,
    LookUp(
        colCurrentChecks,
        Audit.Value = varAuditId
    )
);

// Documentation Score Calculation (20% weight)
Set(
    varDocScore,
    (
        (
            If(varCurrentDocAudit.CheckRecordStatus = "Current", 1,
               varCurrentDocAudit.CheckRecordStatus = "Old", 0.5, 0) +
            If(varCurrentDocAudit.CheckGuidelinesStatus = "Current", 1,
               varCurrentDocAudit.CheckGuidelinesStatus = "Old", 0.5, 0) +
            If(varCurrentDocAudit.BLSPosterPresent, 1, 0) +
            If(varCurrentDocAudit.EquipmentListStatus = "Current", 1,
               varCurrentDocAudit.EquipmentListStatus = "Old", 0.5, 0)
        ) / 4
    ) * 100
);

// Condition Score Calculation (30% weight)
Set(
    varCondScore,
    (
        (
            If(varCurrentCondAudit.IsClean, 1, 0) +
            If(varCurrentCondAudit.IsWorkingOrder, 1, 0) +
            If(NOT(varCurrentCondAudit.RubberBandsUsed), 1, 0) +
            If(varCurrentCondAudit.O2TubingCorrect, 1, 0) +
            If(varCurrentCondAudit.InhaloCylinderOK, 1, 0)
        ) / 5
    ) * 100
);

// Routine Checks Score Calculation (20% weight)
Set(
    varOutsideCompliance,
    If(
        varCurrentCheckAudit.CountNotAvailable,
        0,
        If(
            varCurrentCheckAudit.ExpectedOutside = 0,
            100,
            Min(100, (varCurrentCheckAudit.OutsideCheckCount /
                      varCurrentCheckAudit.ExpectedOutside) * 100)
        )
    )
);

Set(
    varInsideCompliance,
    If(
        varCurrentCheckAudit.CountNotAvailable,
        0,
        If(
            varCurrentCheckAudit.ExpectedInside = 0,
            100,
            Min(100, (varCurrentCheckAudit.InsideCheckCount /
                      varCurrentCheckAudit.ExpectedInside) * 100)
        )
    )
);

Set(
    varCheckScore,
    (varOutsideCompliance + varInsideCompliance) / 2
);

// Equipment Score Calculation (30% weight)
Set(
    varEquipmentCompliantCount,
    CountRows(
        Filter(
            colCurrentEquipment,
            QuantityFound >= QuantityExpected
        )
    )
);

Set(
    varEquipmentTotalCount,
    CountRows(colCurrentEquipment)
);

Set(
    varEquipScore,
    If(
        varEquipmentTotalCount = 0,
        0,
        (varEquipmentCompliantCount / varEquipmentTotalCount) * 100
    )
);

// Overall Compliance Score Calculation (Weighted Average)
Set(
    varOverallCompliance,
    (
        (varDocScore * 0.20) +
        (varCondScore * 0.30) +
        (varCheckScore * 0.20) +
        (varEquipScore * 0.30)
    )
);

// Round to 1 decimal place for display
Set(
    varOverallComplianceDisplay,
    Text(varOverallCompliance, "0.0") & "%"
)
```

##### Step 2: Implement Follow-Up Trigger Logic

```powerfx
// Determine if follow-up is required based on audit findings
Set(
    varRequiresFollowUp,
    Or(
        varOverallCompliance < 80,  // Overall score below 80%
        varCurrentDocAudit.CheckRecordStatus = "None",  // No check record
        varCurrentCondAudit.IsWorkingOrder = false,  // Not working
        varCurrentCheckAudit.OutsideCheckCount = 0,  // No outside checks
        CountRows(Filter(
            colCurrentEquipment,
            QuantityFound = 0  // Critical equipment missing
        )) > 0
    )
);

// Generate follow-up notes if required
If(
    varRequiresFollowUp,
    Set(
        varFollowUpNotes,
        Concatenate(
            If(varOverallCompliance < 80, "Low overall compliance (" &
               Text(varOverallCompliance, "0.0") & "%). ", ""),
            If(varCurrentDocAudit.CheckRecordStatus = "None",
               "No check record found. ", ""),
            If(NOT(varCurrentCondAudit.IsWorkingOrder),
               "Trolley not in working order. ", ""),
            If(CountRows(Filter(colCurrentEquipment, QuantityFound = 0)) > 0,
               "Critical equipment missing. ", "")
        )
    ),
    Set(varFollowUpNotes, "")
)
```

#### Component Specifications

| Variable | Data Type | Calculation | Purpose |
|----------|-----------|-------------|---------|
| varDocScore | Number | Documentation items / 4 * 100 | 20% weight |
| varCondScore | Number | Condition items / 5 * 100 | 30% weight |
| varCheckScore | Number | (Outside + Inside) / 2 | 20% weight |
| varEquipScore | Number | Compliant / Total * 100 | 30% weight |
| varOverallCompliance | Number | Weighted sum of subscores | Final score |
| varRequiresFollowUp | Boolean | Trigger rules OR'd together | Follow-up flag |

#### Verification Checklist

- [ ] All four subscore calculations implemented
- [ ] Documentation score weights items correctly (1.0/0.5/0)
- [ ] Condition score inverts RubberBands logic correctly
- [ ] Routine checks capped at 100% minimum
- [ ] Equipment score handles zero items (returns 0)
- [ ] Weighted formula uses exact percentages (20/30/20/30)
- [ ] Overall score displays with one decimal place
- [ ] Follow-up trigger fires on score < 80%
- [ ] Follow-up trigger fires for missing documentation
- [ ] Follow-up trigger fires for non-working trolley
- [ ] All variables initialized in OnVisible
- [ ] Power Apps Monitor shows correct values
- [ ] No circular formula references

---

### Task 2.5.4: Display Compliance Score Breakdown

#### Objective

Show the calculated compliance scores and subscores to the user in a visual, easy-to-understand format on the review screen.

#### Prerequisites

- Compliance score calculations complete (Task 2.5.3)
- All subscore variables populated
- Review screen layout ready
- Colour theme variables available

#### Step-by-Step Instructions

##### Step 1: Create Overall Score Display Card

1. Add a prominent **Rectangle** card for the overall score:
   - **X:** 40
   - **Y:** 120
   - **Width:** 400
   - **Height:** 150
   - **Fill:** `PrimaryColor`
   - **Radius:** 8px

2. Inside the card, add a large **Label** for the score:
   - **Text:** `varOverallComplianceDisplay`
   - **Font Size:** 72pt, Bold
   - **Color:** White
   - **Align:** Center
   - **Y:** 20

3. Add a subtitle **Label** below:
   - **Text:** "Overall Compliance Score"
   - **Font Size:** 14pt
   - **Color:** White with 80% opacity
   - **Align:** Center
   - **Y:** 110

4. Optional: Add a background indicator bar:
   - Create a thin **Rectangle** at bottom of card
   - **Height:** 10px
   - **Fill:** Based on score level:
     ```powerfx
     If(
         varOverallCompliance >= 85,
         SuccessColor,  // Green
         varOverallCompliance >= 70,
         WarningColor,  // Orange
         ErrorColor     // Red
     )
     ```

##### Step 2: Create Subscore Breakdown Cards

1. Create 4 cards in a row for each subscore:

   **Card 1 - Documentation Score:**
   - **X:** 460
   - **Y:** 120
   - **Width:** 200
   - **Height:** 150
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 1

2. Repeat for Condition Score, Checks Score, Equipment Score:
   - **X positions:** 680, 900 (same height and size)

3. Inside each card, add:
   - Large number label for score (40pt font)
   - Subscore title (12pt font)
   - Percentage symbol

#### Step 3: Create Score Meter Visualization (Optional)

1. For the overall score card, add a visual progress indicator:
   - Create a thin **Rectangle** (score bar):
     - **Width:** `(varOverallCompliance / 100) * 350`
     - **Height:** 20px
     - **Fill:** `If(varOverallCompliance >= 80, SuccessColor, AccentColor)`
     - **Radius:** 10px
   - Add background bar behind it (gray)

2. Add percentage labels:
   - Left label: "0%"
   - Right label: "100%"
   - Current label: `Text(varOverallCompliance, "0.0%")`

##### Step 4: Create Score Breakdown Table

1. Below the score cards, add a **Label** title:
   - **Text:** "Score Breakdown"
   - **Font Size:** 16pt, Bold
   - **Color:** `TextPrimary`

2. Create a simple table layout using labels in a grid:

   ```
   Category                  Score    Weight   Contribution
   Documentation             XX%      20%      = (XX × 0.20)
   Trolley Condition         XX%      30%      = (XX × 0.30)
   Routine Checks            XX%      20%      = (XX × 0.20)
   Equipment Checklist       XX%      30%      = (XX × 0.30)
                                              ─────────────
   Overall Score            XX%               = Overall %
   ```

3. Use a **Gallery** for table rows (optional, cleaner approach):
   ```powerfx
   ClearCollect(
       colScoreBreakdown,
       {
           Category: "Documentation",
           Score: varDocScore,
           Weight: 0.20,
           Contribution: varDocScore * 0.20
       },
       {
           Category: "Trolley Condition",
           Score: varCondScore,
           Weight: 0.30,
           Contribution: varCondScore * 0.30
       },
       {
           Category: "Routine Checks",
           Score: varCheckScore,
           Weight: 0.20,
           Contribution: varCheckScore * 0.20
       },
       {
           Category: "Equipment Checklist",
           Score: varEquipScore,
           Weight: 0.30,
           Contribution: varEquipScore * 0.30
       }
   )
   ```

##### Step 5: Add Compliance Status Indicator

1. Add a **Label** below the breakdown:
   - **Text:** `If(varOverallCompliance >= 85, "✓ COMPLIANT", If(varOverallCompliance >= 70, "⚠ NEEDS IMPROVEMENT", "✗ NON-COMPLIANT"))`
   - **Font Size:** 20pt, Bold
   - **Color:** `If(varOverallCompliance >= 85, SuccessColor, If(varOverallCompliance >= 70, WarningColor, ErrorColor))`

2. Optional: Add status explanation below:
   - **Text:** Dynamic message based on score
     ```powerfx
     If(
         varOverallCompliance >= 85,
         "This trolley meets compliance standards.",
         varOverallCompliance >= 70,
         "This trolley requires attention in some areas.",
         "This trolley requires follow-up action."
     )
     ```

##### Step 6: Add Follow-Up Flag Display

1. If `varRequiresFollowUp = true`, display a prominent warning:
   - Create an alert **Rectangle**:
     - **Fill:** `ErrorColor`
     - **Radius:** 8px
   - Add icon and text:
     - **Text:** "⚠ This audit requires follow-up action"
     - **Color:** White
     - **Font Size:** 14pt

2. Below the alert, show `varFollowUpNotes`

#### PowerFx Code

Complete score display and formatting:

```powerfx
// Display overall compliance score
Text(varOverallCompliance, "0.0") & "%"

// Display subscores with formatting
"Documentation: " & Text(varDocScore, "0.0") & "%"
"Condition: " & Text(varCondScore, "0.0") & "%"
"Checks: " & Text(varCheckScore, "0.0") & "%"
"Equipment: " & Text(varEquipScore, "0.0") & "%"

// Calculate contribution to overall score
"Documentation: " & Text(varDocScore * 0.20, "0.0") & "% (weight: 20%)"
"Condition: " & Text(varCondScore * 0.30, "0.0") & "% (weight: 30%)"
"Checks: " & Text(varCheckScore * 0.20, "0.0") & "% (weight: 20%)"
"Equipment: " & Text(varEquipScore * 0.30, "0.0") & "% (weight: 30%)"

// Compliance status
If(
    varOverallCompliance >= 85,
    "✓ COMPLIANT",
    varOverallCompliance >= 70,
    "⚠ NEEDS IMPROVEMENT",
    "✗ NON-COMPLIANT"
)

// Status colour
If(
    varOverallCompliance >= 85,
    SuccessColor,
    varOverallCompliance >= 70,
    WarningColor,
    ErrorColor
)

// Score bar width
(varOverallCompliance / 100) * 350

// Initialize breakdown collection
ClearCollect(
    colScoreBreakdown,
    {
        Category: "Documentation Checks",
        Score: varDocScore,
        Weight: "20%",
        WeightDecimal: 0.20,
        Contribution: varDocScore * 0.20
    },
    {
        Category: "Trolley Condition",
        Score: varCondScore,
        Weight: "30%",
        WeightDecimal: 0.30,
        Contribution: varCondScore * 0.30
    },
    {
        Category: "Routine Checks",
        Score: varCheckScore,
        Weight: "20%",
        WeightDecimal: 0.20,
        Contribution: varCheckScore * 0.20
    },
    {
        Category: "Equipment Checklist",
        Score: varEquipScore,
        Weight: "30%",
        WeightDecimal: 0.30,
        Contribution: varEquipScore * 0.30
    }
)
```

#### Component Specifications

| Component | Size | Colour | Data |
|-----------|------|--------|------|
| Overall Score Card | 400x150 | PrimaryColor | varOverallComplianceDisplay |
| Documentation Card | 200x150 | White | varDocScore & "%" |
| Condition Card | 200x150 | White | varCondScore & "%" |
| Checks Card | 200x150 | White | varCheckScore & "%" |
| Equipment Card | 200x150 | White | varEquipScore & "%" |
| Score Bar | 350px wide | Dynamic | varOverallCompliance |
| Status Label | Dynamic | Dynamic | Compliant/Improvement/Non-Compliant |

#### Verification Checklist

- [ ] Overall score displays prominently (large font)
- [ ] Score shows one decimal place (XX.X%)
- [ ] Four subscore cards visible and readable
- [ ] Score breakdown table displays all categories and weights
- [ ] Compliance status indicator shows correct message
- [ ] Status indicator colour matches score level (green/orange/red)
- [ ] Score bar width updates based on overall compliance
- [ ] Follow-up warning displays when required
- [ ] Follow-up notes display when applicable
- [ ] All subscores calculate correctly
- [ ] Weighted contributions sum to overall score
- [ ] Percentage formatting consistent throughout
- [ ] No errors in Power Apps Monitor

---

### Task 2.5.5: Add Edit Buttons Per Section

#### Objective

Enable users to navigate back to previous audit entry screens to make changes before final submission.

#### Prerequisites

- Review screen layout complete (Tasks 2.5.1-2.5.4)
- All audit entry screens exist and are functional
- Navigation system configured

#### Step-by-Step Instructions

##### Step 1: Create Edit Navigation Handler

1. Create a collection in ReviewScreen.OnVisible for navigation mapping:
   ```powerfx
   ClearCollect(
       colEditNavigation,
       {
           Section: "Documentation Checks",
           ScreenName: "DocumentationCheckScreen",
           Icon: "✎",
           Order: 1
       },
       {
           Section: "Trolley Condition",
           ScreenName: "ConditionCheckScreen",
           Icon: "✎",
           Order: 2
       },
       {
           Section: "Routine Checks",
           ScreenName: "RoutineChecksScreen",
           Icon: "✎",
           Order: 3
       },
       {
           Section: "Equipment Checklist",
           ScreenName: "EquipmentCheckScreen",
           Icon: "✎",
           Order: 4
       }
   )
   ```

##### Step 2: Add Edit Buttons to Summary Sections

1. For each summary section in the gallery, add an Edit button:
   - **Text:** "✎ Edit " & ThisItem.Section
   - **Width:** 150px
   - **Height:** 40px
   - **Fill:** `SecondaryColor`
   - **Text Color:** White
   - **Font Size:** 12pt
   - **Border:** None
   - **Radius:** 4px
   - **Hover Fill:** Slightly darker `SecondaryColor`

2. Position edit button at bottom-right of each section summary:
   - **Align:** Right-aligned, 20px from right edge
   - **Vertical Align:** Bottom, 20px from bottom

##### Step 3: Implement Edit Navigation Logic

1. Set **OnSelect** handler for each Edit button:
   ```powerfx
   // Store current section for potential reference
   Set(varEditingSection, ThisItem.Section);

   // Navigate based on section
   Switch(
       ThisItem.Section,
       "Documentation Checks",
       Navigate(DocumentationCheckScreen, ScreenTransition.Fade),
       "Trolley Condition",
       Navigate(ConditionCheckScreen, ScreenTransition.Fade),
       "Routine Checks",
       Navigate(RoutineChecksScreen, ScreenTransition.Fade),
       "Equipment Checklist",
       Navigate(EquipmentCheckScreen, ScreenTransition.Fade)
   )
   ```

2. Alternative approach using collection lookup (more scalable):
   ```powerfx
   Set(varEditingSection, ThisItem.Section);
   Set(
       varTargetScreen,
       LookUp(
           colEditNavigation,
           Section = ThisItem.Section
       ).ScreenName
   );
   Navigate(Screen(varTargetScreen), ScreenTransition.Fade)
   ```

##### Step 4: Add Return-to-Review Functionality

1. On each edit screen (Documentation, Condition, etc.), add a "Review" button:
   - **Text:** "Review & Submit"
   - **Fill:** `AccentColor`
   - **OnSelect:**
     ```powerfx
     Navigate(ReviewScreen, ScreenTransition.Fade)
     ```

2. Optionally, track edit history:
   ```powerfx
   // When returning to ReviewScreen
   Set(varLastEditedSection, LookUp(colEditNavigation, ScreenName = [previous screen]).Section);
   Set(varLastEditedTime, Now())
   ```

##### Step 5: Add Visual Indicators for Edited Sections

1. Optional enhancement: Show which sections have been edited:
   - Create a collection to track edit timestamps:
     ```powerfx
     ClearCollect(
         colSectionEditHistory,
         {
             Section: "Documentation Checks",
             LastEditedTime: Blank(),
             EditCount: 0
         },
         {
             Section: "Trolley Condition",
             LastEditedTime: Blank(),
             EditCount: 0
         }
     )
     ```

2. When leaving edit screen, update history:
   ```powerfx
   // On DocumentationCheckScreen.OnHidden
   If(
       varChangesWereMade,
       Patch(
           colSectionEditHistory,
           LookUp(colSectionEditHistory, Section = "Documentation Checks"),
           {
               LastEditedTime: Now(),
               EditCount: EditCount + 1
           }
       )
   )
   ```

3. Display edit indicator in summary section:
   ```powerfx
   // In section header
   If(
       Not(IsBlank(
           LookUp(colSectionEditHistory, Section = ThisItem.Section).LastEditedTime
       )),
       "✓ " & ThisItem.Section & " (edited)",
       ThisItem.Section
   )
   ```

##### Step 6: Add Breadcrumb Navigation (Optional)

1. At top of ReviewScreen, show current location:
   - **Text:** "Audit Review > [Current Section]"
   - **Font Size:** 10pt
   - **Color:** `TextSecondary`

2. After returning from edit, update breadcrumb:
   ```powerfx
   "Audit Review" & If(Not(IsBlank(varEditingSection)), " > " & varEditingSection, "")
   ```

#### PowerFx Code

Complete edit navigation implementation:

```powerfx
// ReviewScreen.OnVisible - Initialize edit navigation
ClearCollect(
    colEditNavigation,
    {
        Section: "Documentation Checks",
        ScreenName: "DocumentationCheckScreen",
        Icon: "✎",
        Order: 1,
        Description: "Edit documentation questions"
    },
    {
        Section: "Trolley Condition",
        ScreenName: "ConditionCheckScreen",
        Icon: "✎",
        Order: 2,
        Description: "Edit trolley condition checks"
    },
    {
        Section: "Routine Checks",
        ScreenName: "RoutineChecksScreen",
        Icon: "✎",
        Order: 3,
        Description: "Edit routine check counts"
    },
    {
        Section: "Equipment Checklist",
        ScreenName: "EquipmentCheckScreen",
        Icon: "✎",
        Order: 4,
        Description: "Edit equipment checklist"
    }
);

// Edit button OnSelect handler
If(
    ThisItem.Section = "Documentation Checks",
    Navigate(DocumentationCheckScreen, ScreenTransition.Fade),
    ThisItem.Section = "Trolley Condition",
    Navigate(ConditionCheckScreen, ScreenTransition.Fade),
    ThisItem.Section = "Routine Checks",
    Navigate(RoutineChecksScreen, ScreenTransition.Fade),
    ThisItem.Section = "Equipment Checklist",
    Navigate(EquipmentCheckScreen, ScreenTransition.Fade)
)

// Return to review button (OnSelect on edit screens)
Navigate(ReviewScreen, ScreenTransition.Fade)

// Breadcrumb display
"Audit Review" & If(
    Not(IsBlank(varEditingSection)),
    " > " & varEditingSection,
    ""
)

// Edit indicator
If(
    Not(IsBlank(LookUp(
        colSectionEditHistory,
        Section = ThisItem.Section
    ).LastEditedTime)),
    "✓ ",
    ""
) & ThisItem.Section
```

#### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Edit Button | Width | 150px |
| | Height | 40px |
| | Fill | SecondaryColor |
| | Text Color | White |
| | Font Size | 12pt |
| | Border Radius | 4px |
| Return Button | Width | 150px |
| | Height | 40px |
| | Fill | AccentColor |
| | Text Color | White |
| Navigation Map | Array | 4 entries (one per section) |
| Breadcrumb | Font Size | 10pt |
| | Color | TextSecondary |

#### Verification Checklist

- [ ] Edit button displays on each summary section
- [ ] Edit button text includes section name
- [ ] Edit button positioned clearly (right side, bottom of section)
- [ ] Clicking Edit button navigates to correct screen
- [ ] Return button present on all edit screens
- [ ] Clicking Return button navigates back to ReviewScreen
- [ ] Navigation uses Fade transition for smooth experience
- [ ] Edit navigation mapping collection initializes correctly
- [ ] varEditingSection tracks which section is being edited
- [ ] Breadcrumb displays correct section name
- [ ] Edit history tracking working (optional feature)
- [ ] No formula errors in Power Apps Monitor
- [ ] All screens save without errors

---

## Part 2: Audit Submission Flows (Tasks 2.5.6-2.5.14)

### Task 2.5.6: Add Submit Button

#### Objective

Add a prominent Submit button to the Review screen that triggers the audit submission flow.

#### Prerequisites

- ReviewScreen complete with all components
- Power Automate flow structure ready (will be detailed in Task 2.5.8)
- Compliance score calculations verified

#### Step-by-Step Instructions

##### Step 1: Add Submit Button to Review Screen

1. Insert a **Button** control at the bottom of ReviewScreen:
   - **X:** 800
   - **Y:** 700
   - **Width:** 200
   - **Height:** 50
   - **Text:** "Submit Audit"
   - **Fill:** `SuccessColor` (green)
   - **Text Color:** White
   - **Font Size:** 14pt, Bold
   - **Border:** None
   - **Radius:** 4px

2. Add visual feedback on hover:
   - **HoverFill:** Slightly darker green (RGBA(60, 150, 65, 1))
   - **Cursor:** `Pointer`

##### Step 2: Implement Pre-Submission Validation

1. Add validation checks in button's **OnSelect** handler:
   ```powerfx
   // Validate all required fields are complete
   If(
       IsBlank(varCurrentAudit),
       Notify("Audit not loaded. Please return to previous screen.", NotificationType.Error),
       IsBlank(varOverallCompliance),
       Notify("Compliance score not calculated. Please review all sections.", NotificationType.Error),
       CountRows(colCurrentDocuments) = 0,
       Notify("Documentation checks not recorded. Please complete all sections.", NotificationType.Error),
       CountRows(colCurrentCondition) = 0,
       Notify("Condition checks not recorded. Please complete all sections.", NotificationType.Error),
       CountRows(colCurrentChecks) = 0,
       Notify("Routine checks not recorded. Please complete all sections.", NotificationType.Error),
       CountRows(colCurrentEquipment) = 0,
       Notify("Equipment checklist not recorded. Please complete all sections.", NotificationType.Error),
       // All validations passed, proceed with submission
       ContinueWithSubmission()
   )
   ```

2. Create `ContinueWithSubmission()` function (custom function or separate handler):
   ```powerfx
   Set(varSubmitInProgress, true);
   Notify("Submitting audit...", NotificationType.Information);

   // Call Power Automate flow
   SubmitAuditFlow.Run(
       varCurrentAudit.ID,
       varOverallCompliance,
       varDocScore,
       varCondScore,
       varCheckScore,
       varEquipScore,
       varRequiresFollowUp,
       varFollowUpNotes
   )
   ```

##### Step 3: Add Submission Confirmation Dialog (Optional)

1. Before actual submission, show confirmation:
   ```powerfx
   // OnSelect of Submit button
   Set(varShowSubmitConfirm, true)
   ```

2. Create a dialog/modal rectangle over the screen:
   - **Visible:** `varShowSubmitConfirm`
   - **Fill:** RGBA(0, 0, 0, 0.5) (dark overlay)
   - **Width:** 1366
   - **Height:** 768

3. Inside dialog, add confirmation message:
   - **Text:** "Ready to submit this audit?"
   - **Font Size:** 16pt
   - Add detailed info:
     - Location: [Location name]
     - Audit Type: [Comprehensive/SpotCheck]
     - Overall Compliance: [XX%]
     - Requires Follow-Up: [Yes/No]

4. Add two buttons in dialog:
   - **"Confirm & Submit"** button → Triggers actual submission
   - **"Cancel"** button → Sets `varShowSubmitConfirm = false`

##### Step 4: Add Loading/Progress Indicator

1. While submission is in progress, show a loading indicator:
   - **Visible:** `varSubmitInProgress`
   - Add spinning icon or progress bar
   - **Text:** "Submitting audit... Please wait."
   - Block user from interacting with other elements

#### PowerFx Code

Complete submit button implementation:

```powerfx
// Submit button OnSelect handler
If(
    IsBlank(varCurrentAudit),
    Notify("Audit not loaded. Please return to previous screen.", NotificationType.Error),
    IsBlank(varOverallCompliance),
    Notify("Compliance score not calculated. Please review all sections.", NotificationType.Error),
    CountRows(colCurrentDocuments) = 0,
    Notify("Documentation checks not recorded.", NotificationType.Error),
    CountRows(colCurrentCondition) = 0,
    Notify("Condition checks not recorded.", NotificationType.Error),
    CountRows(colCurrentChecks) = 0,
    Notify("Routine checks not recorded.", NotificationType.Error),
    CountRows(colCurrentEquipment) = 0,
    Notify("Equipment checklist not recorded.", NotificationType.Error),
    // All validations passed
    Set(varShowSubmitConfirm, true)
);

// Confirmation dialog: Confirm button OnSelect
Set(varSubmitInProgress, true);
Set(varShowSubmitConfirm, false);

// Call Power Automate flow with all audit data
SubmitAuditFlow.Run(
    {
        AuditID: varCurrentAudit.ID,
        AuditTitle: varCurrentAudit.Title,
        LocationID: varCurrentAudit.'Location'.Value,
        LocationName: varCurrentAudit.'Location'.'Display Name',
        AuditPeriodID: varCurrentAudit.'AuditPeriod'.Value,
        AuditType: varCurrentAudit.AuditType,
        AuditorName: varCurrentAudit.AuditorName,
        AuditorEmail: varCurrentAudit.AuditorEmail,
        StartedDateTime: varCurrentAudit.StartedDateTime,
        CompletedDateTime: Now(),
        OverallCompliance: varOverallCompliance,
        DocumentationScore: varDocScore,
        ConditionScore: varCondScore,
        ChecksScore: varCheckScore,
        EquipmentScore: varEquipScore,
        RequiresFollowUp: varRequiresFollowUp,
        FollowUpNotes: varFollowUpNotes,
        DocumentationData: colCurrentDocuments,
        ConditionData: colCurrentCondition,
        ChecksData: colCurrentChecks,
        EquipmentData: colCurrentEquipment
    }
);

// Confirmation dialog: Cancel button OnSelect
Set(varShowSubmitConfirm, false)
```

#### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Submit Button | Width | 200px |
| | Height | 50px |
| | Fill | SuccessColor |
| | Text | "Submit Audit" |
| | Font Size | 14pt Bold |
| Confirmation Overlay | Fill | RGBA(0,0,0,0.5) |
| | Visible | varShowSubmitConfirm |
| Loading Indicator | Visible | varSubmitInProgress |
| | Text | "Submitting..." |

#### Verification Checklist

- [ ] Submit button displays at bottom of review screen
- [ ] Button colour is success green
- [ ] Button text is "Submit Audit"
- [ ] Clicking button triggers validation checks
- [ ] Validation error messages display for incomplete fields
- [ ] Confirmation dialog appears when validation passes
- [ ] Confirmation shows audit summary (location, type, scores)
- [ ] Confirm button in dialog triggers submission
- [ ] Cancel button closes confirmation dialog
- [ ] Loading indicator shows during submission
- [ ] Power Automate flow called with all audit data
- [ ] Button disabled/hidden during submission
- [ ] No errors in Power Apps Monitor

---

### Task 2.5.7: Add Save Draft Button

#### Objective

Implement a Save Draft button allowing users to save incomplete audits for later completion and submission.

#### Prerequisites

- ReviewScreen completed
- Save Draft Power Automate flow ready (Task 2.5.15)
- Current audit record accessible

#### Step-by-Step Instructions

##### Step 1: Add Save Draft Button

1. Insert a **Button** control next to Submit button:
   - **X:** 580
   - **Y:** 700
   - **Width:** 200
   - **Height:** 50
   - **Text:** "Save Draft"
   - **Fill:** `AccentColor` (orange)
   - **Text Color:** White
   - **Font Size:** 14pt, Bold
   - **Border:** None
   - **Radius:** 4px

##### Step 2: Implement Draft Save Logic

1. Set **OnSelect** handler for Save Draft button:
   ```powerfx
   Set(varSavingDraft, true);

   Notify("Saving draft audit...", NotificationType.Information);

   // Call Save Draft flow
   SaveDraftAuditFlow.Run(
       {
           AuditID: varCurrentAudit.ID,
           AuditTitle: varCurrentAudit.Title,
           LocationID: varCurrentAudit.'Location'.Value,
           AuditPeriodID: varCurrentAudit.'AuditPeriod'.Value,
           SubmissionStatus: "Draft",
           OverallCompliance: varOverallCompliance,
           DocumentationScore: varDocScore,
           ConditionScore: varCondScore,
           ChecksScore: varCheckScore,
           EquipmentScore: varEquipScore,
           DocumentationData: colCurrentDocuments,
           ConditionData: colCurrentCondition,
           ChecksData: colCurrentChecks,
           EquipmentData: colCurrentEquipment
       }
   )
   ```

##### Step 3: Add Draft Save Success Handler

1. After Power Automate completes, handle success:
   ```powerfx
   // In ReviewScreen OnVisible or as separate event handler
   If(
       varDraftSaveSuccess = true,
       Set(varSavingDraft, false);
       Notify("Draft audit saved successfully.", NotificationType.Success);
       Set(varDraftSaveSuccess, false),
       // Optional: provide option to return to home or previous audits
       Set(varShowDraftSaveOptions, true)
   )
   ```

2. Create optional dialog offering next actions:
   - "Continue Editing This Audit"
   - "Start New Audit"
   - "Return to Home"

##### Step 4: Add Loading Indicator for Draft Save

1. Show loading state during save:
   - **Visible:** `varSavingDraft`
   - Display: "Saving your draft... Do not close this window."

#### PowerFx Code

Complete draft save implementation:

```powerfx
// Save Draft button OnSelect
Set(varSavingDraft, true);
Notify("Saving draft audit...", NotificationType.Information);

SaveDraftAuditFlow.Run(
    {
        AuditID: varCurrentAudit.ID,
        AuditTitle: varCurrentAudit.Title,
        LocationID: varCurrentAudit.'Location'.Value,
        LocationName: varCurrentAudit.'Location'.'Display Name',
        AuditPeriodID: varCurrentAudit.'AuditPeriod'.Value,
        AuditType: varCurrentAudit.AuditType,
        AuditorName: varCurrentAudit.AuditorName,
        StartedDateTime: varCurrentAudit.StartedDateTime,
        SubmissionStatus: "Draft",
        OverallCompliance: Round(varOverallCompliance, 2),
        DocumentationScore: Round(varDocScore, 2),
        ConditionScore: Round(varCondScore, 2),
        ChecksScore: Round(varCheckScore, 2),
        EquipmentScore: Round(varEquipScore, 2),
        DocumentationData: JSON(colCurrentDocuments),
        ConditionData: JSON(colCurrentCondition),
        ChecksData: JSON(colCurrentChecks),
        EquipmentData: JSON(colCurrentEquipment),
        UserEmail: User().Email,
        SaveTime: Now()
    }
);

// Success handling (added after flow completes)
If(
    varDraftSaveSuccess = true,
    Set(varSavingDraft, false),
    Notify("Draft saved successfully. You can return later to complete this audit.", NotificationType.Success),
    Set(varDraftSaveSuccess, false)
)
```

#### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Save Draft Button | Width | 200px |
| | Height | 50px |
| | Fill | AccentColor |
| | Text | "Save Draft" |
| | Font Size | 14pt Bold |
| | X Position | 580 |

#### Verification Checklist

- [ ] Save Draft button displays next to Submit button
- [ ] Button colour is accent orange
- [ ] Button text is "Save Draft"
- [ ] Clicking button shows loading indicator
- [ ] Loading message prevents user action
- [ ] Power Automate flow called with audit data
- [ ] Flow receives all subsection data
- [ ] Success notification displays after save
- [ ] SubmissionStatus set to "Draft"
- [ ] Audit can be retrieved and reopened later
- [ ] No errors in Power Apps Monitor
- [ ] Button disabled during save process

---

### Tasks 2.5.8-2.5.14: Power Automate Submission Flow

This section details the comprehensive Power Automate flow that handles audit submission, including creating all child records and updating location data.

#### Overview of Flow Architecture

```
Trigger: PowerApp calls SubmitAuditFlow.Run()
│
├─→ Step 1: Receive audit data from PowerApp
│
├─→ Step 2: Update Audit record
│   ├─→ Set SubmissionStatus = "Submitted"
│   ├─→ Set CompletedDateTime = Now()
│   ├─→ Set OverallCompliance = [calculated score]
│   └─→ Set subscores (DocumentationScore, etc.)
│
├─→ Step 3: Create/Update AuditDocuments record
│   ├─→ Set CheckRecordStatus
│   ├─→ Set CheckGuidelinesStatus
│   ├─→ Set BLSPosterPresent
│   └─→ Set EquipmentListStatus
│
├─→ Step 4: Create/Update AuditCondition record
│   ├─→ Set IsClean
│   ├─→ Set IsWorkingOrder
│   ├─→ Set RubberBandsUsed
│   ├─→ Set O2TubingCorrect
│   └─→ Set InhaloCylinderOK
│
├─→ Step 5: Create/Update AuditChecks record
│   ├─→ Set OutsideCheckCount
│   ├─→ Set InsideCheckCount
│   ├─→ Set ExpectedOutside
│   ├─→ Set ExpectedInside
│   └─→ Set CountNotAvailable flag
│
├─→ Step 6: Create AuditEquipment records (multiple)
│   ├─→ For each equipment item:
│   │   ├─→ Set Equipment lookup
│   │   ├─→ Set IsPresent
│   │   ├─→ Set QuantityFound
│   │   ├─→ Set ExpiryOK
│   │   └─→ Set ItemNotes
│   └─→ Create all records in bulk
│
├─→ Step 7: Update Location record
│   ├─→ Set LastAuditDate = Now()
│   ├─→ Set LastAuditCompliance = OverallCompliance
│   └─→ Update DaysSinceLastAudit (if calculated)
│
├─→ Step 8: Handle Follow-Up (if required)
│   ├─→ If RequiresFollowUp = true:
│   │   └─→ Create Issue record (Task 2.6.1 - future)
│   └─→ Send notification emails
│
└─→ Step 9: Return success to PowerApp
    └─→ Set varSubmitSuccess = true
```

### Task 2.5.8: Create Submit Audit Flow (Overall Flow Structure)

#### Objective

Build the main Power Automate flow that orchestrates all submission steps.

#### Prerequisites

- All child lists created (AuditDocuments, AuditCondition, AuditChecks, AuditEquipment)
- Power Automate environment configured
- Location list accessible for updates

#### Step-by-Step Instructions

##### Step 1: Create Cloud Flow

1. Navigate to https://make.powerautomate.com
2. Create a new **Cloud flow** → **Instant cloud flow** (triggered by PowerApp)
3. Name the flow: `SubmitAuditFlow`
4. Configure trigger: **PowerApps (V2)**

##### Step 2: Add Flow Inputs

1. In the trigger, add these inputs (PowerApp will pass these):
   - **Input 1:** AuditID (Text)
   - **Input 2:** AuditTitle (Text)
   - **Input 3:** LocationID (Text)
   - **Input 4:** LocationName (Text)
   - **Input 5:** AuditType (Text)
   - **Input 6:** AuditorName (Text)
   - **Input 7:** OverallCompliance (Number)
   - **Input 8:** DocumentationScore (Number)
   - **Input 9:** ConditionScore (Number)
   - **Input 10:** ChecksScore (Number)
   - **Input 11:** EquipmentScore (Number)
   - **Input 12:** RequiresFollowUp (Boolean)
   - **Input 13:** FollowUpNotes (String)
   - **Input 14:** DocumentationData (Object - JSON)
   - **Input 15:** ConditionData (Object - JSON)
   - **Input 16:** ChecksData (Object - JSON)
   - **Input 17:** EquipmentData (Array - JSON array)

##### Step 3: Add First Action - Update Audit Record

Add action: **SharePoint** → **Update item**

Configure:
- **Site:** Select your SharePoint site
- **List:** Audit
- **ID:** triggerInputs('AuditID')
- **Title:** triggerInputs('AuditTitle')
- **Submission Status:** "Submitted"
- **Completed Date/Time:** utcNow()
- **Overall Compliance:** triggerInputs('OverallCompliance')
- **Documentation Score:** triggerInputs('DocumentationScore')
- **Condition Score:** triggerInputs('ConditionScore')
- **Routine Checks Score:** triggerInputs('ChecksScore')
- **Equipment Score:** triggerInputs('EquipmentScore')
- **Requires Follow Up:** triggerInputs('RequiresFollowUp')
- **Follow Up Notes:** triggerInputs('FollowUpNotes')

This updates the Audit header record with final submission data.

##### Step 4: Add Variables for Tracking

Add action: **Initialize variable**
- **Name:** varAuditID
- **Type:** String
- **Value:** triggerInputs('AuditID')

Repeat for LocationID, OverallCompliance, etc.

#### PowerFx Code

Flow trigger configuration (JSON):

```json
{
  "type": "OpenApiConnectionWebhook",
  "inputs": {
    "host": {
      "connection": {
        "name": "shared_powerapps"
      }
    },
    "body": {
      "NotificationUrl": "@{listCallbackUrl()}"
    }
  }
}
```

First action - Update Audit (SharePoint Update item):

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "UpdateItem"
    },
    "parameters": {
      "ItemId": "@triggerInputs('AuditID')",
      "item": {
        "Title": "@triggerInputs('AuditTitle')",
        "SubmissionStatus": "Submitted",
        "CompletedDateTime": "@utcNow()",
        "OverallCompliance": "@triggerInputs('OverallCompliance')",
        "DocumentationScore": "@triggerInputs('DocumentationScore')",
        "ConditionScore": "@triggerInputs('ConditionScore')",
        "ChecksScore": "@triggerInputs('ChecksScore')",
        "EquipmentScore": "@triggerInputs('EquipmentScore')",
        "RequiresFollowUp": "@triggerInputs('RequiresFollowUp')",
        "FollowUpNotes": "@triggerInputs('FollowUpNotes')"
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Flow created and named "SubmitAuditFlow"
- [ ] Trigger set to PowerApp (V2)
- [ ] All 17 inputs configured
- [ ] First action updates Audit record
- [ ] Submission Status set to "Submitted"
- [ ] Completed DateTime captures current time
- [ ] All scores passed through
- [ ] Variables initialized for later use
- [ ] Flow saves without errors

---

### Task 2.5.9: Save Audit Record

This task is covered above in Task 2.5.8 (first action).

---

### Task 2.5.10: Save AuditDocuments Record

#### Objective

Create the AuditDocuments child record with documentation check responses.

#### Prerequisites

- Audit record created (Task 2.5.9)
- AuditDocuments list exists with all columns

#### Step-by-Step Instructions

##### Step 1: Add Create Item Action for AuditDocuments

Add action: **SharePoint** → **Create item**

Configure:
- **Site:** Your SharePoint site
- **List:** AuditDocuments
- **Title:** `Concat(triggerInputs('AuditTitle'), " - Documentation")`
- **Audit:** `triggerInputs('AuditID')` (lookup to Audit)
- **Check Record Status:** `outputs('Parse_DocumentationData')?['body/CheckRecordStatus']`
- **Checking Guidelines Status:** `outputs('Parse_DocumentationData')?['body/CheckGuidelinesStatus']`
- **BLS Poster Present:** `outputs('Parse_DocumentationData')?['body/BLSPosterPresent']`
- **Equipment List Status:** `outputs('Parse_DocumentationData')?['body/EquipmentListStatus']`
- **Document Notes:** `outputs('Parse_DocumentationData')?['body/DocumentNotes']`

##### Step 2: Add Parse JSON Action (if needed)

If DocumentationData comes as JSON string, add:

Action: **Parse JSON**
- **Content:** `triggerInputs('DocumentationData')`
- **Schema:** (Define based on AuditDocuments structure)

##### Step 3: Store Created Record ID

Add action: **Set variable**
- **Name:** varDocumentsRecordID
- **Value:** `outputs('Create_AuditDocuments')?['body/ID']`

This allows linking in later steps.

#### PowerFx Code

Create AuditDocuments action (JSON):

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "CreateItem"
    },
    "parameters": {
      "ItemId": "@triggerInputs('AuditID')",
      "item": {
        "Title": "@concat(triggerInputs('AuditTitle'), ' - Documentation')",
        "AuditLookup": "@triggerInputs('AuditID')",
        "CheckRecordStatus": "@body('Parse_DocumentationData')?['CheckRecordStatus']",
        "CheckGuidelinesStatus": "@body('Parse_DocumentationData')?['CheckGuidelinesStatus']",
        "BLSPosterPresent": "@body('Parse_DocumentationData')?['BLSPosterPresent']",
        "EquipmentListStatus": "@body('Parse_DocumentationData')?['EquipmentListStatus']",
        "DocumentNotes": "@body('Parse_DocumentationData')?['DocumentNotes']"
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Parse JSON action processes DocumentationData
- [ ] Create item action creates AuditDocuments record
- [ ] Record linked to parent Audit
- [ ] All four documentation fields populated
- [ ] Record ID captured for reference
- [ ] No errors in flow execution

---

### Task 2.5.11: Save AuditCondition Record

#### Objective

Create the AuditCondition child record with trolley condition check responses.

#### Prerequisites

- Audit record created
- AuditCondition list exists

#### Step-by-Step Instructions

##### Step 1: Parse Condition Data

Add action: **Parse JSON**
- **Content:** `triggerInputs('ConditionData')`
- **Schema:** Matching AuditCondition structure

##### Step 2: Create AuditCondition Record

Add action: **SharePoint** → **Create item**

Configure:
- **Site:** Your SharePoint site
- **List:** AuditCondition
- **Title:** `Concat(triggerInputs('AuditTitle'), " - Condition")`
- **Audit:** `triggerInputs('AuditID')`
- **Is Clean:** `body('Parse_ConditionData')?['IsClean']`
- **Is Working Order:** `body('Parse_ConditionData')?['IsWorkingOrder']`
- **Issue Type:** `body('Parse_ConditionData')?['IssueType']` (if applicable)
- **Issue Description:** `body('Parse_ConditionData')?['IssueDescription']`
- **Rubber Bands Used:** `body('Parse_ConditionData')?['RubberBandsUsed']`
- **O2 Tubing Correct:** `body('Parse_ConditionData')?['O2TubingCorrect']`
- **INHALO Cylinder OK:** `body('Parse_ConditionData')?['InhaloCylinderOK']`
- **Condition Notes:** `body('Parse_ConditionData')?['ConditionNotes']`

##### Step 3: Store Record ID

Add action: **Set variable**
- **Name:** varConditionRecordID
- **Value:** `outputs('Create_AuditCondition')?['body/ID']`

#### PowerFx Code

Create AuditCondition action:

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "CreateItem"
    },
    "parameters": {
      "list": "AuditCondition",
      "item": {
        "Title": "@concat(triggerInputs('AuditTitle'), ' - Condition')",
        "AuditLookup": "@triggerInputs('AuditID')",
        "IsClean": "@body('Parse_ConditionData')?['IsClean']",
        "IsWorkingOrder": "@body('Parse_ConditionData')?['IsWorkingOrder']",
        "IssueType": "@body('Parse_ConditionData')?['IssueType']",
        "IssueDescription": "@body('Parse_ConditionData')?['IssueDescription']",
        "RubberBandsUsed": "@body('Parse_ConditionData')?['RubberBandsUsed']",
        "O2TubingCorrect": "@body('Parse_ConditionData')?['O2TubingCorrect']",
        "InhaloCylinderOK": "@body('Parse_ConditionData')?['InhaloCylinderOK']",
        "ConditionNotes": "@body('Parse_ConditionData')?['ConditionNotes']"
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Parse JSON action processes ConditionData
- [ ] Create item action creates AuditCondition record
- [ ] Record linked to parent Audit
- [ ] All five condition checks populated
- [ ] Issue details captured (if applicable)
- [ ] Record ID stored for reference

---

### Task 2.5.12: Save AuditChecks Record

#### Objective

Create the AuditChecks child record with routine check count data.

#### Prerequisites

- Audit record created
- AuditChecks list exists

#### Step-by-Step Instructions

##### Step 1: Parse Checks Data

Add action: **Parse JSON**
- **Content:** `triggerInputs('ChecksData')`

##### Step 2: Create AuditChecks Record

Add action: **SharePoint** → **Create item**

Configure:
- **Site:** Your SharePoint site
- **List:** AuditChecks
- **Title:** `Concat(triggerInputs('AuditTitle'), " - Checks")`
- **Audit:** `triggerInputs('AuditID')`
- **Outside Check Count:** `body('Parse_ChecksData')?['OutsideCheckCount']`
- **Inside Check Count:** `body('Parse_ChecksData')?['InsideCheckCount']`
- **Expected Outside:** `body('Parse_ChecksData')?['ExpectedOutside']`
- **Expected Inside:** `body('Parse_ChecksData')?['ExpectedInside']`
- **Count Not Available:** `body('Parse_ChecksData')?['CountNotAvailable']`
- **Not Available Reason:** `body('Parse_ChecksData')?['NotAvailableReason']`
- **Check Notes:** `body('Parse_ChecksData')?['CheckNotes']`

##### Step 3: Store Record ID

Add action: **Set variable**
- **Name:** varChecksRecordID
- **Value:** `outputs('Create_AuditChecks')?['body/ID']`

#### PowerFx Code

Create AuditChecks action:

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "CreateItem"
    },
    "parameters": {
      "list": "AuditChecks",
      "item": {
        "Title": "@concat(triggerInputs('AuditTitle'), ' - Checks')",
        "AuditLookup": "@triggerInputs('AuditID')",
        "OutsideCheckCount": "@int(body('Parse_ChecksData')?['OutsideCheckCount'])",
        "InsideCheckCount": "@int(body('Parse_ChecksData')?['InsideCheckCount'])",
        "ExpectedOutside": "@int(body('Parse_ChecksData')?['ExpectedOutside'])",
        "ExpectedInside": "@int(body('Parse_ChecksData')?['ExpectedInside'])",
        "CountNotAvailable": "@body('Parse_ChecksData')?['CountNotAvailable']",
        "NotAvailableReason": "@body('Parse_ChecksData')?['NotAvailableReason']",
        "CheckNotes": "@body('Parse_ChecksData')?['CheckNotes']"
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Parse JSON action processes ChecksData
- [ ] Create item action creates AuditChecks record
- [ ] Record linked to parent Audit
- [ ] Check counts (outside and inside) captured
- [ ] Expected counts populated
- [ ] "Not Available" flag and reason handled
- [ ] Record ID stored for reference

---

### Task 2.5.13: Save AuditEquipment Records

#### Objective

Create multiple AuditEquipment child records (one per equipment item checked).

#### Prerequisites

- Audit record created
- AuditEquipment list exists with all columns
- Equipment array passed from PowerApp

#### Step-by-Step Instructions

##### Step 1: Parse Equipment Data Array

Add action: **Parse JSON**
- **Content:** `triggerInputs('EquipmentData')`
- **Schema:** Array of equipment items

##### Step 2: Apply to Each Equipment Item

Add action: **Apply to each**
- **Select an output from previous steps:** `body('Parse_EquipmentData')`

##### Step 3: Inside Loop - Create Each AuditEquipment Record

Add action (inside the loop): **SharePoint** → **Create item**

Configure:
- **Site:** Your SharePoint site
- **List:** AuditEquipment
- **Title:** `items('Apply_to_each_equipment')?['EquipmentName']`
- **Audit:** `triggerInputs('AuditID')`
- **Equipment:** `items('Apply_to_each_equipment')?['EquipmentID']` (lookup)
- **Is Present:** `items('Apply_to_each_equipment')?['IsPresent']`
- **Quantity Found:** `items('Apply_to_each_equipment')?['QuantityFound']`
- **Quantity Expected:** `items('Apply_to_each_equipment')?['QuantityExpected']`
- **Expiry Checked:** `items('Apply_to_each_equipment')?['ExpiryChecked']`
- **Expiry OK:** `items('Apply_to_each_equipment')?['ExpiryOK']`
- **Sizes Checked:** `items('Apply_to_each_equipment')?['SizeChecked']`
- **Item Notes:** `items('Apply_to_each_equipment')?['ItemNotes']`

##### Step 4: Handle Bulk Creation (Alternative)

For better performance with many items, use batch create:

Add action: **Send an HTTP request to SharePoint**

Configure:
- **Method:** POST
- **URI:** `_api/web/lists/getByTitle('AuditEquipment')/items`
- **Headers:** Content-Type: application/json
- **Body:** (Array of items to create)

#### PowerFx Code

Loop-based equipment creation:

```json
{
  "type": "Foreach",
  "inputs": {
    "foreach": "@body('Parse_EquipmentData')",
    "actions": {
      "Create_AuditEquipment": {
        "type": "OpenApiConnection",
        "inputs": {
          "host": {
            "connectionName": "shared_sharepointonline",
            "operationId": "CreateItem"
          },
          "parameters": {
            "list": "AuditEquipment",
            "item": {
              "Title": "@items('Foreach')?['EquipmentName']",
              "AuditLookup": "@triggerInputs('AuditID')",
              "EquipmentLookup": "@items('Foreach')?['EquipmentID']",
              "IsPresent": "@items('Foreach')?['IsPresent']",
              "QuantityFound": "@int(items('Foreach')?['QuantityFound'])",
              "QuantityExpected": "@int(items('Foreach')?['QuantityExpected'])",
              "ExpiryChecked": "@items('Foreach')?['ExpiryChecked']",
              "ExpiryOK": "@items('Foreach')?['ExpiryOK']",
              "SizeChecked": "@items('Foreach')?['SizeChecked']",
              "ItemNotes": "@items('Foreach')?['ItemNotes']"
            }
          }
        }
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Equipment data array parsed correctly
- [ ] Loop iterates through all items
- [ ] Each item creates an AuditEquipment record
- [ ] Equipment lookup populated correctly
- [ ] Quantity fields captured as numbers
- [ ] Boolean fields (IsPresent, ExpiryOK) handled correctly
- [ ] All records linked to parent Audit
- [ ] No items skipped or missed
- [ ] Loop completes without errors

---

### Task 2.5.14: Update Location Last Audit Fields

#### Objective

Update the Location record with the audit completion date and compliance score for future reference.

#### Prerequisites

- Audit record created
- Location record exists and is accessible
- Compliance scores calculated

#### Step-by-Step Instructions

##### Step 1: Add Update Location Action

Add action: **SharePoint** → **Update item**

Configure:
- **Site:** Your SharePoint site
- **List:** Location
- **ID:** `triggerInputs('LocationID')`
- **Last Audit Date:** `utcNow()` (current date/time)
- **Last Audit Compliance:** `triggerInputs('OverallCompliance')`

##### Step 2: Optional - Calculate Days Since Audit

If Location has a calculated column for DaysSinceLastAudit:
- This will update automatically based on LastAuditDate
- No additional action needed

##### Step 3: Handle Multiple Audits Same Period

Add conditional check:

```json
{
  "type": "Condition",
  "expression": {
    "and": [
      {
        "equals": ["@triggerInputs('AuditType')", "Comprehensive"]
      }
    ]
  },
  "actions": {
    "UpdateLocation": {
      "type": "OpenApiConnection",
      "inputs": {
        "host": {
          "connectionName": "shared_sharepointonline",
          "operationId": "UpdateItem"
        },
        "parameters": {
          "ItemId": "@triggerInputs('LocationID')",
          "item": {
            "LastAuditDate": "@utcNow()",
            "LastAuditCompliance": "@triggerInputs('OverallCompliance')"
          }
        }
      }
    }
  }
}
```

#### PowerFx Code

Update Location action:

```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "UpdateItem"
    },
    "parameters": {
      "ItemId": "@triggerInputs('LocationID')",
      "item": {
        "LastAuditDate": "@utcNow()",
        "LastAuditCompliance": "@triggerInputs('OverallCompliance')",
        "LastAuditType": "@triggerInputs('AuditType')",
        "ModifiedDate": "@utcNow()"
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Update Location action accesses correct Location record
- [ ] Last Audit Date set to current date/time
- [ ] Last Audit Compliance updated with overall score
- [ ] Update completes without errors
- [ ] Location record accessible in SharePoint
- [ ] Calculated column (DaysSinceLastAudit) updates automatically
- [ ] Location searchable by last audit date

---

## Part 3: Draft Save Functionality (Task 2.5.15)

### Task 2.5.15: Create Save Draft Flow

#### Objective

Build a Power Automate flow that saves incomplete audits as drafts for later retrieval and completion.

#### Prerequisites

- Audit list with SubmissionStatus = "Draft" choice
- PowerApp can pass partial data
- Same child list structure as submission flow

#### Step-by-Step Instructions

##### Step 1: Create Save Draft Cloud Flow

1. Create new **Cloud flow** → **Instant cloud flow** (triggered by PowerApp)
2. Name: `SaveDraftAuditFlow`
3. Configure trigger: **PowerApps (V2)**

##### Step 2: Add Flow Inputs

Configure same inputs as submission flow, but allow partial data:

- **Input 1:** AuditID (Text)
- **Input 2:** AuditTitle (Text)
- **Input 3:** LocationID (Text)
- **Input 4:** AuditPeriodID (Text)
- **Input 5:** AuditorName (Text)
- **Input 6:** SubmissionStatus (Text - set to "Draft")
- **Input 7:** OverallCompliance (Number - nullable)
- **Input 8-11:** DocumentationData, ConditionData, ChecksData, EquipmentData (Optional)

##### Step 3: Create/Update Audit Record with Draft Status

Add action: **SharePoint** → **Update item** (or Create if new)

Configure:
- **ID:** `triggerInputs('AuditID')`
- **Title:** `triggerInputs('AuditTitle')`
- **Submission Status:** "Draft"
- **Overall Compliance:** `triggerInputs('OverallCompliance')`
- **ModifiedDate:** `utcNow()`
- **FollowUpNotes:** "Draft saved - completion pending"

##### Step 4: Conditionally Save Child Records (if provided)

Add conditional actions to create/update child records only if data is provided:

```json
{
  "type": "Condition",
  "expression": {
    "not": {
      "equals": ["@triggerInputs('DocumentationData')", null]
    }
  },
  "actions": {
    "Create_or_Update_Documentation": {
      // Create/Update AuditDocuments logic
    }
  }
}
```

Repeat for Condition, Checks, and Equipment data.

##### Step 5: Notify User of Draft Save

Add action: **Send an email notification** (optional)

Configure:
- **To:** `triggerInputs('AuditorEmail')`
- **Subject:** "Trolley Audit Draft Saved"
- **Body:**
  ```
  Your draft audit for [Location] has been saved.
  You can return to complete it at any time.
  Audit ID: [AuditID]
  ```

##### Step 6: Return Success Status

Add action: **Respond to PowerApp**

Configure:
- **Status Code:** 200
- **Body:**
  ```json
  {
    "success": true,
    "message": "Draft saved successfully",
    "auditID": "@triggerInputs('AuditID')",
    "savedTime": "@utcNow()"
  }
  ```

#### PowerFx Code

Save Draft flow structure (JSON):

```json
{
  "type": "Cloud Flow",
  "trigger": "PowerApps",
  "inputs": [
    {
      "name": "AuditID",
      "type": "string",
      "required": true
    },
    {
      "name": "SubmissionStatus",
      "type": "string",
      "default": "Draft"
    },
    {
      "name": "DocumentationData",
      "type": "object",
      "required": false
    },
    {
      "name": "ConditionData",
      "type": "object",
      "required": false
    },
    {
      "name": "ChecksData",
      "type": "object",
      "required": false
    },
    {
      "name": "EquipmentData",
      "type": "array",
      "required": false
    }
  ],
  "actions": {
    "Update_Audit_Draft": {
      "type": "OpenApiConnection",
      "inputs": {
        "host": {
          "connectionName": "shared_sharepointonline",
          "operationId": "UpdateItem"
        },
        "parameters": {
          "ItemId": "@triggerInputs('AuditID')",
          "item": {
            "SubmissionStatus": "Draft",
            "OverallCompliance": "@triggerInputs('OverallCompliance')",
            "ModifiedDate": "@utcNow()"
          }
        }
      }
    },
    "Respond_to_PowerApp": {
      "type": "Response",
      "inputs": {
        "statusCode": 200,
        "body": {
          "success": true,
          "message": "Draft saved successfully"
        }
      }
    }
  }
}
```

#### Verification Checklist

- [ ] Draft flow created and named "SaveDraftAuditFlow"
- [ ] Trigger configured for PowerApp inputs
- [ ] Audit record updates with SubmissionStatus = "Draft"
- [ ] Modified date captures save time
- [ ] Conditional logic handles optional data
- [ ] Child records created only when data provided
- [ ] Email notification sent (optional but recommended)
- [ ] Success response returned to PowerApp
- [ ] Draft audits retrievable by viewing Audit list with "Draft" filter
- [ ] Flow saves without errors

---

## Compliance Score Formula Summary

### Formula Components

```
OVERALL COMPLIANCE = (Documentation × 0.20) + (Condition × 0.30) +
                     (Checks × 0.20) + (Equipment × 0.30)

Where:

Documentation (20% weight):
  = (CheckRecord + Guidelines + BLSPoster + EquipmentList) / 4 × 100

  CheckRecord = 1.0 (Current), 0.5 (Old), 0.0 (None)
  Guidelines = 1.0 (Current), 0.5 (Old), 0.0 (None)
  BLSPoster = 1.0 (Yes), 0.0 (No)
  EquipmentList = 1.0 (Current), 0.5 (Old), 0.0 (None)

Condition (30% weight):
  = (IsClean + IsWorkingOrder + NOT(RubberBands) + O2Tubing + InhaloCyl) / 5 × 100

  Each check = 1.0 (Pass), 0.0 (Fail)
  RubberBands inverted: 1.0 if NO, 0.0 if YES

Routine Checks (20% weight):
  = (OutsideCompliance + InsideCompliance) / 2

  OutsideCompliance = min(100, OutsideCount / ExpectedOutside × 100)
  InsideCompliance = min(100, InsideCount / ExpectedInside × 100)
  If CountNotAvailable = true, both = 0

Equipment (30% weight):
  = CompliantItems / TotalItems × 100

  CompliantItem = QuantityFound ≥ QuantityExpected
  If zero items checked, score = 0
```

### Score Ranges

| Overall Score | Classification | Follow-Up Required |
|---------------|-----------------|-------------------|
| 85-100% | ✓ Compliant | No |
| 70-84% | ⚠ Needs Improvement | Assess |
| 0-69% | ✗ Non-Compliant | Yes |

---

## Implementation Checklist - Phase 2.5 Complete

### Review Screen (Tasks 2.5.1-2.5.5)
- [ ] ReviewScreen created
- [ ] All responses summary displays
- [ ] Compliance score calculated
- [ ] Score breakdown visible
- [ ] Edit buttons functional

### Submission Controls (Tasks 2.5.6-2.5.7)
- [ ] Submit button implemented
- [ ] Save Draft button implemented
- [ ] Pre-submission validation working
- [ ] Confirmation dialog displays
- [ ] Loading indicators show during processing

### Power Automate Flows (Tasks 2.5.8-2.5.14)
- [ ] SubmitAuditFlow created
- [ ] Audit record updated (Task 2.5.9)
- [ ] AuditDocuments record created (Task 2.5.10)
- [ ] AuditCondition record created (Task 2.5.11)
- [ ] AuditChecks record created (Task 2.5.12)
- [ ] AuditEquipment records created (Task 2.5.13)
- [ ] Location LastAuditDate updated (Task 2.5.14)
- [ ] Follow-up logic implemented

### Draft Save (Task 2.5.15)
- [ ] SaveDraftAuditFlow created
- [ ] Draft audits savable
- [ ] Partial data handling works
- [ ] Draft audits retrievable

### Quality Assurance
- [ ] All formulas calculate correctly
- [ ] No circular references
- [ ] No hardcoded values
- [ ] Responsive design on tablet
- [ ] Error handling in place
- [ ] User notifications clear
- [ ] All screens save without errors

---

## Troubleshooting Common Issues

### Issue: Compliance Score Calculation Incorrect

**Symptoms:** Overall score doesn't match manual calculation

**Solutions:**
1. Verify subscore calculations individually
2. Check weighting percentages sum to 100%
3. Ensure capping at 100% for check compliance
4. Test with known values and verify against formula
5. Check Power Apps Monitor for variable values
6. Verify data types (numbers vs. text)

### Issue: Power Automate Flow Fails to Create Child Records

**Symptoms:** Audit record created but child records missing

**Solutions:**
1. Verify all lists exist in SharePoint
2. Check lookup fields configured correctly
3. Ensure data types match (Text vs. Number)
4. Verify audit record created before child records
5. Check flow action order (dependencies)
6. Review flow run history for errors
7. Test with simplified data first

### Issue: Location Update Doesn't Save

**Symptoms:** Location record not showing last audit date

**Solutions:**
1. Verify Location list has LastAuditDate column
2. Confirm LocationID passed to flow correctly
3. Check field permissions (user must have edit rights)
4. Test updating Location manually to verify field works
5. Check flow receives correct LocationID
6. Verify calculated column DaysSinceLastAudit references LastAuditDate

---

## Next Steps

After completing Phase 2.5:

- **Phase 2.6-2.9:** Issue Management (create Issue list, build issue screens, implement workflows)
- **Phase 3:** Reporting & Analytics (Power BI dashboards, historical data migration)
- **Phase 4:** Enhancement (offline mode, photo capture, notifications)

---

**Document prepared for:** Royal Brisbane and Women's Hospital - MERT Program
**Document classification:** Internal - Implementation Guide
**Last updated:** January 2026
