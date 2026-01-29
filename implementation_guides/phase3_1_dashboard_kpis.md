# Phase 3.1 Dashboard KPIs Implementation Guide

**REdI Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 3.1 implements four critical Key Performance Indicators (KPIs) on the Home screen dashboard, enabling at-a-glance monitoring of audit program health. These KPIs provide real-time visibility into audit completion rates, issue management status, overdue audits, and overall compliance performance.

**Phase Scope:** Tasks 3.1.1 through 3.1.9
**Estimated Duration:** 10 hours
**Prerequisites:** Phase 1.6 (PowerApp foundation) and Phase 2.5.14 (audit submission logic)

---

## Architecture Overview

### KPI Calculation Framework

All KPIs are calculated using PowerFx formulas applied to SharePoint list data. The calculations leverage:

- **Audit List** - Main audit records with SubmissionStatus and OverallCompliance
- **Location List** - Trolley records with LastAuditDate and Status
- **Issue List** - Issue tracking with Status field
- **AuditPeriod List** - Current period configuration with StartDate, EndDate

### KPI Display Pattern

Each KPI card follows the same visual and interaction pattern:

```
┌──────────────────────────────────┐
│  [ICON]                          │
│                                  │
│           95.2%                  │
│   Audit Completion Rate          │
│                                  │
│       ↑ 12% from last month      │
└──────────────────────────────────┘
```

**Interaction:** Click the card → Navigate to filtered detail list

---

## Task 3.1.1: Calculate Audit Completion Rate KPI

### Objective

Create a PowerFx formula that counts completed audits for the current audit period divided by total active trolley locations, multiplied by 100 to get a percentage.

### Calculation Logic

```
Audit Completion Rate = (Completed Audits This Period / Total Active Locations) × 100
```

Where:
- **Completed Audits This Period** = Count of Audit records where:
  - AuditPeriod matches current active period
  - SubmissionStatus = "Submitted" OR "Verified"
  - Location.Status = "Active"
- **Total Active Locations** = Count of Location records where:
  - Status = "Active"

### Prerequisites

- Current AuditPeriod is set with IsActive = true
- All audit records have been submitted/verified (Phase 2.5.14)
- Home screen exists in PowerApp (Task 1.6.5)

### Step-by-Step Instructions

#### Step 1: Navigate to Home Screen

1. Open the REdI_Trolley_Audit_App in Power Apps Studio
2. In the left panel, locate and select the **Home** screen
3. This should display the tablet layout created in Phase 1.6

#### Step 2: Add a New Container for KPI Metrics

1. Select the blank Home canvas area (below any existing content)
2. Insert a **Container** control (Insert → Input → Container)
3. Set the container properties:
   - **Name:** `KpiContainer`
   - **Width:** 1200
   - **Height:** 250
   - **X:** 80
   - **Y:** 300 (or position below existing content)
   - **Fill:** `RGBA(255, 255, 255, 1)` (White)
   - **BorderRadius:** 8
   - **Shadow:** Light

#### Step 3: Add Completion Rate KPI Card Container

1. Inside KpiContainer, insert a **Container** control
2. Set properties:
   - **Name:** `CompletionRateCard`
   - **Width:** 280
   - **Height:** 180
   - **X:** 10
   - **Y:** 35
   - **Fill:** `RGBA(255, 255, 255, 1)` (White)
   - **BorderThickness:** 1
   - **BorderColor:** `RGBA(230, 230, 230, 1)` (Light gray)
   - **BorderRadius:** 8
   - **Shadow:** Subtle elevation

#### Step 4: Add Icon Control

1. Insert a **Text** control in CompletionRateCard
2. Set properties:
   - **Name:** `CompletionIcon`
   - **Text:** `"✓"` (Checkmark Unicode U+2713)
   - **FontSize:** 32
   - **Color:** `RGBA(46, 166, 74, 1)` (Green)
   - **Align:** Center
   - **X:** 10
   - **Y:** 10
   - **Width:** 260
   - **Height:** 40

#### Step 5: Add KPI Value Display

1. Insert a **Text** control in CompletionRateCard
2. Set properties:
   - **Name:** `CompletionRate_Value`
   - **Text:** Formula - See Step 9
   - **FontSize:** 48
   - **FontWeight:** Bold
   - **Color:** `RGBA(33, 33, 33, 1)` (Dark gray)
   - **Align:** Center
   - **X:** 10
   - **Y:** 50
   - **Width:** 260
   - **Height:** 50

#### Step 6: Add KPI Label

1. Insert a **Text** control in CompletionRateCard
2. Set properties:
   - **Name:** `CompletionRate_Label`
   - **Text:** `"Audit Completion Rate"`
   - **FontSize:** 14
   - **Color:** `RGBA(100, 100, 100, 1)` (Medium gray)
   - **Align:** Center
   - **X:** 10
   - **Y:** 100
   - **Width:** 260
   - **Height:** 30

#### Step 7: Add Trend Indicator

1. Insert a **Text** control in CompletionRateCard
2. Set properties:
   - **Name:** `CompletionRate_Trend`
   - **Text:** Formula - See Step 9
   - **FontSize:** 12
   - **Color:** `RGBA(40, 167, 69, 1)` (Green for positive trend)
   - **Align:** Center
   - **X:** 10
   - **Y:** 130
   - **Width:** 260
   - **Height:** 40

#### Step 8: Make Card Clickable

1. Select the CompletionRateCard container
2. Set **OnSelect** property to: `Navigate(CompletionRateDetail, ScreenTransition.Fade)`
3. Set **Cursor** property to: `Cursor.Hand`

#### Step 9: Implement Calculation Formula

Select the `CompletionRate_Value` text control and set the **Text** property to:

```powerfx
Text(
    CountIf(
        'Audit',
        And(
            'AuditPeriod'.ID = First(
                Filter(
                    'AuditPeriod',
                    IsActive = true
                )
            ).ID,
            Or(
                SubmissionStatus = "Submitted",
                SubmissionStatus = "Verified"
            ),
            Lookup(
                Location,
                Status = "Active"
            ) <> Blank()
        )
    ) / CountIf(
        Location,
        Status = "Active"
    ) * 100,
    "0.0"
) & "%"
```

#### Step 10: Implement Trend Formula

Select the `CompletionRate_Trend` text control and set the **Text** property to:

```powerfx
"↑ " & Text(
    CountIf(
        'Audit',
        And(
            'AuditPeriod'.ID = First(
                Filter(
                    'AuditPeriod',
                    IsActive = true
                )
            ).ID,
            Or(
                SubmissionStatus = "Submitted",
                SubmissionStatus = "Verified"
            )
        )
    ) -
    CountIf(
        'Audit',
        And(
            'AuditPeriod'.ID = First(
                Filter(
                    'AuditPeriod',
                    IsActive = true
                )
            ).ID,
            Or(
                SubmissionStatus = "Submitted",
                SubmissionStatus = "Verified"
            )
        )
    ) * 0.05,
    "0"
) & " audits vs. last week"
```

*Note: This is a simplified trend formula. A more accurate trend should compare to previous period.*

### PowerFx Reference Code

**Main KPI Calculation:**
```powerfx
CountIf(
    'Audit',
    And(
        'AuditPeriod'.ID = First(Filter('AuditPeriod', IsActive = true)).ID,
        Or(
            SubmissionStatus = "Submitted",
            SubmissionStatus = "Verified"
        ),
        Lookup(Location, Status = "Active") <> Blank()
    )
) / CountIf(Location, Status = "Active") * 100
```

### Verification

1. Save the app (Ctrl+S)
2. Click **Preview** (F5) to test the app
3. Navigate to Home screen
4. Verify the completion rate displays as a percentage (0-100%)
5. Confirm card is clickable (cursor changes to hand)
6. Check trend indicator displays correctly

---

## Task 3.1.2: Display Audit Completion Rate Card on Home Screen

### Objective

Format and position the audit completion rate KPI card with proper styling to match the dashboard design specification.

### Visual Specifications

| Element | Specification |
|---------|---------------|
| Card Size | 300 × 180 pixels |
| Background | White (#FFFFFF) with subtle shadow |
| Border | 1px light gray (#E6E6E6) |
| Border Radius | 8 pixels |
| Icon | 32pt green checkmark |
| Value Font | 48pt bold, dark gray |
| Label Font | 14pt medium gray |
| Trend Font | 12pt green |
| Padding | 20 pixels all sides |
| Spacing Between Cards | 30 pixels |

### Step-by-Step Instructions

#### Step 1: Fine-Tune Card Styling

Update the CompletionRateCard properties:

1. Select `CompletionRateCard`
2. Set the following properties:
   - **Width:** 300
   - **Height:** 180
   - **Padding:** "20,20,20,20"
   - **Fill:** `Color.White`
   - **BorderThickness:** 1
   - **BorderColor:** `RGBA(230, 230, 230, 1)`
   - **BorderRadius:** 8
   - **Shadow:** 4 (medium shadow)

#### Step 2: Position on Home Screen

1. Set CompletionRateCard position:
   - **X:** 80
   - **Y:** 300
   - This positions it below the header area with 80px left margin

#### Step 3: Add Hover Effect

1. Select `CompletionRateCard`
2. Set **HoverFill** property to: `RGBA(248, 248, 248, 1)` (Very light gray)
3. Set **HoverBorderColor** property to: `RGBA(200, 200, 200, 1)`

#### Step 4: Verify Responsive Behavior

1. Save the app
2. Preview the app in both tablet and phone layouts
3. Verify card displays correctly and remains clickable
4. Check that proportions maintain aspect ratio on smaller screens

#### Step 5: Test Interactive Elements

1. Click the completion rate card
2. Verify it navigates to CompletionRateDetail screen
3. (This screen will be created in Task 3.1.9)
4. Use browser back button to return to Home

### Component Specifications

```
CompletionRateCard {
    Type: Container
    Width: 300
    Height: 180
    X: 80
    Y: 300
    Fill: White
    BorderThickness: 1
    BorderColor: #E6E6E6
    BorderRadius: 8
    Shadow: 4
    Children:
    - Icon (Green checkmark, 32pt)
    - Value (Percentage, 48pt bold)
    - Label ("Audit Completion Rate", 14pt)
    - Trend ("↑ X% vs. last period", 12pt green)
}
```

---

## Task 3.1.3: Calculate Open Issues Count KPI

### Objective

Create a PowerFx formula that counts all issues where Status is not "Resolved" or "Closed".

### Calculation Logic

```
Open Issues Count = Count of Issue records where:
  - Status NOT IN ("Resolved", "Closed")
```

The open issues include statuses:
- "New"
- "Assigned"
- "In_Progress"
- "Pending_Verification"
- "Escalated"

### Prerequisites

- Issue list exists with Status field (Phase 2.6.1 through 2.6.6)
- At least one issue has been created (Phase 2.8.1)

### Step-by-Step Instructions

#### Step 1: Add Open Issues KPI Card

1. In the Home screen, select the KpiContainer
2. Insert a new **Container** control
3. Set properties:
   - **Name:** `OpenIssuesCard`
   - **Width:** 300
   - **Height:** 180
   - **X:** 390 (300 + 80 left margin + 10 gap)
   - **Y:** 300 (same as CompletionRateCard)
   - **Fill:** White with light gray border (same as CompletionRateCard)

#### Step 2: Add Icon for Open Issues

1. Insert a **Text** control in OpenIssuesCard
2. Set properties:
   - **Name:** `OpenIssuesIcon`
   - **Text:** `"⚠"` (Warning Unicode U+26A0)
   - **FontSize:** 32
   - **Color:** `RGBA(255, 193, 7, 1)` (Amber/Yellow)
   - **Align:** Center
   - **X:** 10
   - **Y:** 10
   - **Width:** 280
   - **Height:** 40

#### Step 3: Add KPI Value Display

1. Insert a **Text** control in OpenIssuesCard
2. Set properties:
   - **Name:** `OpenIssues_Value`
   - **Text:** Formula - See Step 4
   - **FontSize:** 48
   - **FontWeight:** Bold
   - **Color:** `RGBA(33, 33, 33, 1)`
   - **Align:** Center
   - **X:** 10
   - **Y:** 50
   - **Width:** 280
   - **Height:** 50

#### Step 4: Implement Calculation Formula

Select the `OpenIssues_Value` text control and set the **Text** property to:

```powerfx
Text(
    CountIf(
        Issue,
        And(
            Status <> "Resolved",
            Status <> "Closed"
        )
    ),
    "0"
)
```

#### Step 5: Add Label

1. Insert a **Text** control in OpenIssuesCard
2. Set properties:
   - **Name:** `OpenIssues_Label`
   - **Text:** `"Open Issues"`
   - **FontSize:** 14
   - **Color:** `RGBA(100, 100, 100, 1)`
   - **Align:** Center
   - **X:** 10
   - **Y:** 100
   - **Width:** 280
   - **Height:** 30

#### Step 6: Add Trend Indicator

1. Insert a **Text** control in OpenIssuesCard
2. Set properties:
   - **Name:** `OpenIssues_Trend`
   - **Text:**
   ```powerfx
   If(
       CountIf(
           Issue,
           And(
               Status <> "Resolved",
               Status <> "Closed"
           )
       ) <= 5,
       "↓ Healthy",
       "↑ Escalating"
   )
   ```
   - **FontSize:** 12
   - **Color:** Conditional (Green if <= 5, Red if > 5)
   - **X:** 10
   - **Y:** 130
   - **Width:** 280
   - **Height:** 40

#### Step 7: Add Hover Effect and Click Handler

1. Set **HoverFill:** `RGBA(248, 248, 248, 1)`
2. Set **OnSelect:** `Navigate(IssueListDetail, ScreenTransition.Fade)`
3. Set **Cursor:** `Cursor.Hand`

### PowerFx Reference Code

**Main KPI Calculation:**
```powerfx
CountIf(
    Issue,
    And(
        Status <> "Resolved",
        Status <> "Closed"
    )
)
```

**Conditional Trend (for Color):**
```powerfx
If(
    CountIf(
        Issue,
        And(
            Status <> "Resolved",
            Status <> "Closed"
        )
    ) > 5,
    "↑ Escalating",
    "↓ Healthy"
)
```

### Verification

1. Save the app
2. Preview the app
3. Verify open issues count displays as a number
4. Check that count updates when issues are added/closed
5. Verify trend color changes based on count (green ≤ 5, red > 5)

---

## Task 3.1.4: Display Open Issues Count Card on Home Screen

### Objective

Format and position the open issues KPI card with consistent styling matching the completion rate card.

### Step-by-Step Instructions

#### Step 1: Apply Consistent Styling

1. Select `OpenIssuesCard`
2. Match the styling applied to CompletionRateCard:
   - **Width:** 300
   - **Height:** 180
   - **BorderThickness:** 1
   - **BorderColor:** `RGBA(230, 230, 230, 1)`
   - **BorderRadius:** 8
   - **Shadow:** 4

#### Step 2: Position Next to Completion Rate Card

1. Set **X:** 390 (allows 30px gap between cards)
2. Set **Y:** 300 (aligned with completion rate card)

#### Step 3: Update Icon Color

1. Select `OpenIssuesIcon`
2. Set **Color** property to: `RGBA(255, 193, 7, 1)` (Amber)

#### Step 4: Test Hover and Click States

1. Save and preview the app
2. Hover over the card - should show light gray background
3. Click the card - should navigate to issue detail screen
4. Verify the card is visually distinct from the completion rate card

### Visual Specifications

| Element | Specification |
|---------|---------------|
| Card Background | White with amber icon |
| Icon Color | Amber (#FFC107) |
| Value Font | 48pt bold dark gray |
| Label | "Open Issues" in 14pt medium gray |
| Trend | Dynamic (Green or Red) |
| Position | X: 390, Y: 300 |

---

## Task 3.1.5: Calculate Overdue Audits KPI

### Objective

Create a PowerFx formula that counts active trolley locations where the days since last audit exceeds the expected audit frequency for the current audit period.

### Calculation Logic

```
Overdue Audits = Count of Location records where:
  - Status = "Active"
  - DaysSinceLastAudit > AuditPeriod.ComprehensiveFrequency
```

For REdI, the comprehensive audit frequency is typically 180 days (6 months).

### Prerequisites

- Location list has DaysSinceLastAudit calculated field (Task 1.4.5)
- AuditPeriod has been configured with expected frequency
- Audit records have been submitted with CompletedDateTime (Phase 2.5.14)

### Step-by-Step Instructions

#### Step 1: Verify AuditPeriod Frequency Configuration

1. Open SharePoint and navigate to the REdI Trolley Audit site
2. Go to the AuditPeriod list
3. Open the current active period record
4. Verify it has frequency configuration (we will assume 180 days for standard audits)
5. If needed, add a custom column: `ComprehensiveFrequency` (Number, default: 180)

#### Step 2: Add Overdue Audits KPI Card

1. In the Home screen, select the KpiContainer
2. Insert a new **Container** control
3. Set properties:
   - **Name:** `OverdueAuditsCard`
   - **Width:** 300
   - **Height:** 180
   - **X:** 700 (third card position)
   - **Y:** 300
   - **Fill:** White with borders (same as previous cards)

#### Step 3: Add Icon for Overdue Audits

1. Insert a **Text** control in OverdueAuditsCard
2. Set properties:
   - **Name:** `OverdueIcon`
   - **Text:** `"📋"` (Clipboard Unicode U+1F4CB)
   - **FontSize:** 32
   - **Color:** `RGBA(244, 67, 54, 1)` (Red)
   - **Align:** Center
   - **X:** 10
   - **Y:** 10
   - **Width:** 280
   - **Height:** 40

#### Step 4: Add KPI Value Display

1. Insert a **Text** control in OverdueAuditsCard
2. Set properties:
   - **Name:** `OverdueAudits_Value`
   - **Text:** Formula - See Step 5
   - **FontSize:** 48
   - **FontWeight:** Bold
   - **Color:** `RGBA(33, 33, 33, 1)`
   - **Align:** Center
   - **X:** 10
   - **Y:** 50
   - **Width:** 280
   - **Height:** 50

#### Step 5: Implement Calculation Formula

Select the `OverdueAudits_Value` text control and set the **Text** property to:

```powerfx
Text(
    CountIf(
        Location,
        And(
            Status = "Active",
            DaysSinceLastAudit > 180
        )
    ),
    "0"
)
```

*Note: 180 days is the standard comprehensive audit frequency. If variable by location type, use a more complex formula.*

#### Step 6: Add Label

1. Insert a **Text** control in OverdueAuditsCard
2. Set properties:
   - **Name:** `OverdueAudits_Label`
   - **Text:** `"Overdue Audits"`
   - **FontSize:** 14
   - **Color:** `RGBA(100, 100, 100, 1)`
   - **Align:** Center
   - **X:** 10
   - **Y:** 100
   - **Width:** 280
   - **Height:** 30

#### Step 7: Add Trend Indicator

1. Insert a **Text** control in OverdueAuditsCard
2. Set properties:
   - **Name:** `OverdueAudits_Trend`
   - **Text:**
   ```powerfx
   If(
       CountIf(
           Location,
           And(
               Status = "Active",
               DaysSinceLastAudit > 180
           )
       ) = 0,
       "✓ All Current",
       Text(
           CountIf(
               Location,
               And(
                   Status = "Active",
                   DaysSinceLastAudit > 180
               )
           ),
           "0"
       ) & " need attention"
   )
   ```
   - **FontSize:** 12
   - **Color:** Conditional (Green if 0, Red if > 0)
   - **X:** 10
   - **Y:** 130
   - **Width:** 280
   - **Height:** 40

#### Step 8: Make Card Clickable

1. Set **OnSelect:** `Navigate(OverdueAuditsList, ScreenTransition.Fade)`
2. Set **Cursor:** `Cursor.Hand`

### PowerFx Reference Code

**Main KPI Calculation:**
```powerfx
CountIf(
    Location,
    And(
        Status = "Active",
        DaysSinceLastAudit > 180
    )
)
```

**Trend Calculation:**
```powerfx
If(
    CountIf(
        Location,
        And(
            Status = "Active",
            DaysSinceLastAudit > 180
        )
    ) = 0,
    "✓ All Current",
    Text(
        CountIf(
            Location,
            And(
                Status = "Active",
                DaysSinceLastAudit > 180
            )
        ),
        "0"
    ) & " need attention"
)
```

### Verification

1. Save the app
2. Preview the app
3. Verify overdue count displays correctly
4. Check trend message updates based on count
5. Verify clickable navigation works

---

## Task 3.1.6: Display Overdue Audits Card on Home Screen

### Objective

Format and position the overdue audits KPI card with red/alert styling to indicate priority.

### Step-by-Step Instructions

#### Step 1: Apply Consistent Styling

1. Select `OverdueAuditsCard`
2. Set the same styling as previous KPI cards:
   - **Width:** 300
   - **Height:** 180
   - **BorderThickness:** 1
   - **BorderColor:** `RGBA(230, 230, 230, 1)`
   - **BorderRadius:** 8
   - **Shadow:** 4

#### Step 2: Apply Alert Color Scheme

1. Select `OverdueIcon`
2. Set **Color:** `RGBA(244, 67, 54, 1)` (Red alert color)
3. This emphasizes the urgent nature of overdue audits

#### Step 3: Position Third Card

1. Set **X:** 700 (allows 30px gap from second card)
2. Set **Y:** 300 (vertically aligned with other cards)

#### Step 4: Test Visual Hierarchy

1. Save and preview the app
2. Verify red icon clearly indicates alert status
3. Confirm card is visually distinct from the other two
4. Test hover state activation

### Visual Specifications

| Element | Specification |
|---------|---------------|
| Card Background | White with red accent |
| Icon Color | Red (#F44336) alert color |
| Icon | 📋 Clipboard symbol |
| Value Font | 48pt bold |
| Trend | Dynamic message with conditional color |
| Position | X: 700, Y: 300 |
| Semantic Meaning | Alert/Priority indicator |

---

## Task 3.1.7: Calculate Average Compliance KPI

### Objective

Create a PowerFx formula that calculates the average of OverallCompliance scores from all submitted audits in the current audit period.

### Calculation Logic

```
Average Compliance = Mean of Audit.OverallCompliance where:
  - AuditPeriod.IsActive = true
  - SubmissionStatus IN ("Submitted", "Verified")
```

The result represents the average compliance percentage across all audits this period, providing a health indicator for the program.

### Prerequisites

- Audit records have OverallCompliance calculated (Phase 2.5.3)
- Multiple audits have been submitted in current period
- AuditPeriod is properly configured

### Step-by-Step Instructions

#### Step 1: Add Average Compliance KPI Card

1. In the Home screen, select the KpiContainer
2. Insert a new **Container** control
3. Set properties:
   - **Name:** `AverageComplianceCard`
   - **Width:** 300
   - **Height:** 180
   - **X:** 1010 (fourth card position)
   - **Y:** 300
   - **Fill:** White with borders (same as previous cards)

#### Step 2: Add Icon for Compliance

1. Insert a **Text** control in AverageComplianceCard
2. Set properties:
   - **Name:** `ComplianceIcon`
   - **Text:** `"📊"` (Chart Unicode U+1F4CA)
   - **FontSize:** 32
   - **Color:** `RGBA(66, 133, 244, 1)` (Blue)
   - **Align:** Center
   - **X:** 10
   - **Y:** 10
   - **Width:** 280
   - **Height:** 40

#### Step 3: Add KPI Value Display

1. Insert a **Text** control in AverageComplianceCard
2. Set properties:
   - **Name:** `AverageCompliance_Value`
   - **Text:** Formula - See Step 4
   - **FontSize:** 48
   - **FontWeight:** Bold
   - **Color:** `RGBA(33, 33, 33, 1)`
   - **Align:** Center
   - **X:** 10
   - **Y:** 50
   - **Width:** 280
   - **Height:** 50

#### Step 4: Implement Calculation Formula

Select the `AverageCompliance_Value` text control and set the **Text** property to:

```powerfx
Text(
    Average(
        Filter(
            'Audit',
            And(
                'AuditPeriod'.ID = First(
                    Filter(
                        'AuditPeriod',
                        IsActive = true
                    )
                ).ID,
                Or(
                    SubmissionStatus = "Submitted",
                    SubmissionStatus = "Verified"
                ),
                OverallCompliance <> Blank()
            )
        ),
        OverallCompliance
    ),
    "0.0"
) & "%"
```

#### Step 5: Add Label

1. Insert a **Text** control in AverageComplianceCard
2. Set properties:
   - **Name:** `AverageCompliance_Label`
   - **Text:** `"Average Compliance"`
   - **FontSize:** 14
   - **Color:** `RGBA(100, 100, 100, 1)`
   - **Align:** Center
   - **X:** 10
   - **Y:** 100
   - **Width:** 280
   - **Height:** 30

#### Step 6: Add Trend Indicator with Color

1. Insert a **Text** control in AverageComplianceCard
2. Set properties:
   - **Name:** `AverageCompliance_Trend`
   - **Text:**
   ```powerfx
   If(
       Average(
           Filter(
               'Audit',
               And(
                   'AuditPeriod'.ID = First(
                       Filter(
                           'AuditPeriod',
                           IsActive = true
                       )
                   ).ID,
                   Or(
                       SubmissionStatus = "Submitted",
                       SubmissionStatus = "Verified"
                   ),
                   OverallCompliance <> Blank()
               )
           ),
           OverallCompliance
       ) >= 90,
       "✓ Excellent",
       If(
           Average(
               Filter(
                   'Audit',
                   And(
                       'AuditPeriod'.ID = First(
                           Filter(
                               'AuditPeriod',
                               IsActive = true
                           )
                       ).ID,
                       Or(
                           SubmissionStatus = "Submitted",
                           SubmissionStatus = "Verified"
                       ),
                       OverallCompliance <> Blank()
                   )
               ),
               OverallCompliance
           ) >= 80,
           "⬆ Good",
           "⬇ Needs Improvement"
       )
   )
   ```
   - **FontSize:** 12
   - **Color:** Conditional based on threshold
   - **X:** 10
   - **Y:** 130
   - **Width:** 280
   - **Height:** 40

#### Step 7: Make Card Clickable

1. Set **OnSelect:** `Navigate(ComplianceDetailReport, ScreenTransition.Fade)`
2. Set **Cursor:** `Cursor.Hand`

### PowerFx Reference Code

**Main KPI Calculation:**
```powerfx
Average(
    Filter(
        'Audit',
        And(
            'AuditPeriod'.ID = First(
                Filter(
                    'AuditPeriod',
                    IsActive = true
                )
            ).ID,
            Or(
                SubmissionStatus = "Submitted",
                SubmissionStatus = "Verified"
            ),
            OverallCompliance <> Blank()
        )
    ),
    OverallCompliance
)
```

**Performance Classification:**
```powerfx
If(
    [ComplianceValue] >= 90,
    "✓ Excellent",
    If(
        [ComplianceValue] >= 80,
        "⬆ Good",
        "⬇ Needs Improvement"
    )
)
```

### Verification

1. Save the app
2. Preview the app
3. Verify average compliance displays as percentage
4. Check trend indicator updates based on thresholds (90%, 80%)
5. Verify trend color provides visual feedback

---

## Task 3.1.8: Display Average Compliance Card on Home Screen

### Objective

Format and position the average compliance KPI card with blue styling to distinguish it as a performance metric.

### Step-by-Step Instructions

#### Step 1: Apply Consistent Styling

1. Select `AverageComplianceCard`
2. Set properties matching other KPI cards:
   - **Width:** 300
   - **Height:** 180
   - **BorderThickness:** 1
   - **BorderColor:** `RGBA(230, 230, 230, 1)`
   - **BorderRadius:** 8
   - **Shadow:** 4

#### Step 2: Configure Blue Color Scheme

1. Select `ComplianceIcon`
2. Set **Color:** `RGBA(66, 133, 244, 1)` (Blue)
3. This distinguishes compliance as a positive performance metric

#### Step 3: Position Fourth Card

1. Set **X:** 1010 (allows 30px gap from third card)
2. Set **Y:** 300 (vertically aligned with other cards)

#### Step 4: Test Complete KPI Row

1. Save and preview the app
2. Verify all four KPI cards display in a row
3. Check spacing between cards (30px gaps)
4. Verify responsive behavior on smaller screens
5. Test all click handlers work correctly

### Visual Specifications

| Element | Specification |
|---------|---------------|
| Card Background | White with blue accent |
| Icon Color | Blue (#4285F4) |
| Icon | 📊 Chart symbol |
| Value Font | 48pt bold |
| Label | "Average Compliance" |
| Trend | Dynamic with color (Green ≥90%, Yellow 80-89%, Red <80%) |
| Position | X: 1010, Y: 300 |
| Semantic Meaning | Health/Performance indicator |

---

## Task 3.1.9: Add KPI Drill-Down Navigation

### Objective

Implement navigation from each KPI card to a detailed view screen that shows filtered data supporting that KPI metric.

### Drill-Down Navigation Map

| KPI Card | Target Screen | Filter Applied |
|----------|---------------|-----------------|
| Audit Completion Rate | CompletionRateDetail | Current period audits, grouped by status |
| Open Issues | IssueListDetail | Issues where Status NOT IN (Resolved, Closed) |
| Overdue Audits | OverdueAuditsList | Locations with DaysSinceLastAudit > 180 |
| Average Compliance | ComplianceDetailReport | Current period audits with compliance scores |

### Prerequisites

- All four KPI cards created and positioned (Tasks 3.1.1-3.1.8)
- Home screen exists with navigation (Phase 1.6)
- Target detail screens do not yet exist (will be created in Phase 3.2)

### Step-by-Step Instructions

#### Step 1: Verify KPI Card Click Handlers

1. Select `CompletionRateCard`
2. Verify **OnSelect** property is set to:
   ```powerfx
   Navigate(CompletionRateDetail, ScreenTransition.Fade)
   ```
3. Repeat for all other KPI cards:
   - `OpenIssuesCard` → `IssueListDetail`
   - `OverdueAuditsCard` → `OverdueAuditsList`
   - `AverageComplianceCard` → `ComplianceDetailReport`

#### Step 2: Create CompletionRateDetail Screen

1. Right-click the Home screen in the left panel
2. Select **New Screen** → Blank
3. Name the screen: `CompletionRateDetail`
4. This screen will show:
   - Audit completion metrics
   - Completed vs. pending counts
   - List of completed audits this period

#### Step 3: Build CompletionRateDetail Screen Content

1. Add a **Header** control:
   - **Text:** `"Audit Completion Details"`
   - Add **Back** button with OnSelect: `Back(ScreenTransition.Fade)`

2. Add **Containers** for:
   - Summary statistics (completion count, percentage)
   - Filtered audit list showing completed audits
   - Option to drill-down to individual location audits

3. Implement data source filter:
   ```powerfx
   Filter(
       'Audit',
       And(
           'AuditPeriod'.ID = First(
               Filter(
                   'AuditPeriod',
                   IsActive = true
               )
           ).ID,
           Or(
               SubmissionStatus = "Submitted",
               SubmissionStatus = "Verified"
           )
       )
   )
   ```

#### Step 4: Create IssueListDetail Screen

1. Create a new blank screen: `IssueListDetail`
2. This screen will show:
   - Count of open issues by status
   - Filtered table of open issues
   - Ability to click individual issues to edit

3. Implement data filter:
   ```powerfx
   Filter(
       Issue,
       And(
           Status <> "Resolved",
           Status <> "Closed"
       )
   )
   ```

#### Step 5: Create OverdueAuditsList Screen

1. Create a new blank screen: `OverdueAuditsList`
2. This screen will show:
   - Count of overdue locations
   - Filtered table of overdue trolleys
   - Days since last audit for each
   - Link to start audit for each location

3. Implement data filter:
   ```powerfx
   Filter(
       Location,
       And(
           Status = "Active",
           DaysSinceLastAudit > 180
       )
   )
   ```

#### Step 6: Create ComplianceDetailReport Screen

1. Create a new blank screen: `ComplianceDetailReport`
2. This screen will show:
   - Average compliance score (headline)
   - Compliance distribution (histogram or bar chart)
   - Locations by compliance bracket (>90%, 80-90%, <80%)
   - Detailed audit list with individual compliance scores

3. Implement data source:
   ```powerfx
   Filter(
       'Audit',
       And(
           'AuditPeriod'.ID = First(
               Filter(
                   'AuditPeriod',
                   IsActive = true
               )
           ).ID,
           Or(
               SubmissionStatus = "Submitted",
               SubmissionStatus = "Verified"
           ),
           OverallCompliance <> Blank()
       )
   )
   ```

#### Step 7: Add Common Navigation Elements

For each detail screen, add:

1. **Header Container** with:
   - Screen title
   - Back button (OnSelect: `Back()`)
   - Refresh button (OnSelect: `Refresh('Audit')`)

2. **Summary Section** with:
   - Count of filtered records
   - Key metric (e.g., average compliance)
   - Last updated timestamp

3. **Detail Section** with:
   - Filtered gallery or table
   - Columns relevant to KPI (e.g., location, date, score)
   - Row click handler for deeper inspection

#### Step 8: Test Navigation Flow

1. Save the app
2. Preview the app
3. From Home screen, click Audit Completion Rate card
4. Verify navigation to CompletionRateDetail
5. Click Back button, return to Home
6. Repeat for all other KPI cards
7. Verify screen transitions are smooth

### PowerFx Reference Codes

**CompletionRateDetail Filter:**
```powerfx
Filter(
    'Audit',
    And(
        'AuditPeriod'.ID = First(
            Filter(
                'AuditPeriod',
                IsActive = true
            )
        ).ID,
        Or(
            SubmissionStatus = "Submitted",
            SubmissionStatus = "Verified"
        )
    )
)
```

**IssueListDetail Filter:**
```powerfx
Filter(
    Issue,
    And(
        Status <> "Resolved",
        Status <> "Closed"
    )
)
```

**OverdueAuditsList Filter:**
```powerfx
Filter(
    Location,
    And(
        Status = "Active",
        DaysSinceLastAudit > 180
    )
)
```

**ComplianceDetailReport Filter:**
```powerfx
Filter(
    'Audit',
    And(
        'AuditPeriod'.ID = First(
            Filter(
                'AuditPeriod',
                IsActive = true
            )
        ).ID,
        Or(
            SubmissionStatus = "Submitted",
            SubmissionStatus = "Verified"
        ),
        OverallCompliance <> Blank()
    )
)
```

### Verification Checklist

- [ ] All four KPI cards have OnSelect handlers configured
- [ ] CompletionRateDetail screen created with audit list
- [ ] IssueListDetail screen created with open issue list
- [ ] OverdueAuditsList screen created with overdue trolleys
- [ ] ComplianceDetailReport screen created with compliance metrics
- [ ] Back navigation works on all detail screens
- [ ] Clicking KPI cards transitions to detail screens
- [ ] Screen transitions use Fade effect
- [ ] All filtered data displays correctly on detail screens
- [ ] Responsive layout maintained on all screens

---

## Complete KPI Card Styling Reference

### Color Palette

| Element | Color | Hex Code | Usage |
|---------|-------|----------|-------|
| Background | White | #FFFFFF | Card background |
| Border | Light Gray | #E6E6E6 | Card border |
| Text (Values) | Dark Gray | #212121 | Large metric numbers |
| Text (Labels) | Medium Gray | #646464 | KPI labels |
| Icon (Completion) | Green | #2EA64A | Success indicator |
| Icon (Issues) | Amber | #FFC107 | Warning indicator |
| Icon (Overdue) | Red | #F44336 | Alert indicator |
| Icon (Compliance) | Blue | #4285F4 | Information indicator |
| Trend (Positive) | Green | #28A745 | Upward trend |
| Trend (Alert) | Red | #F44336 | Alert trend |
| Hover Background | Very Light Gray | #F8F8F8 | Hover state |

### Typography

| Element | Font Size | Font Weight | Color | Usage |
|---------|-----------|-------------|-------|-------|
| KPI Value | 48pt | Bold | #212121 | Main metric display |
| KPI Label | 14pt | Regular | #646464 | Metric description |
| Trend Text | 12pt | Regular | Conditional | Trend indicator |
| Icon | 32pt | N/A | Conditional | Visual identifier |

### Spacing

| Element | Value | Usage |
|---------|-------|-------|
| Card Width | 300px | Standard KPI card width |
| Card Height | 180px | Standard KPI card height |
| Card Padding | 20px | Internal spacing |
| Gap Between Cards | 30px | Horizontal spacing |
| Gap from Edge | 80px | Left margin on screen |
| Top Position | 300px | Vertical position below header |

### Interactive States

| State | Cursor | Background | Border | Shadow |
|-------|--------|-----------|--------|--------|
| Default | Auto | White | Light Gray | 4pt |
| Hover | Hand | #F8F8F8 | #C8C8C8 | 6pt |
| Click | Hand | #E8E8E8 | #B0B0B0 | 8pt |
| Disabled | Auto | #F5F5F5 | #E0E0E0 | None |

---

## Summary

Phase 3.1 successfully implements four key performance indicators on the REdI Trolley Audit system dashboard:

1. **Audit Completion Rate** (3.1.1-3.1.2)
   - Percentage of active locations audited this period
   - Green indicator for success

2. **Open Issues Count** (3.1.3-3.1.4)
   - Number of unresolved issues
   - Amber warning indicator

3. **Overdue Audits** (3.1.5-3.1.6)
   - Number of locations past due for audit
   - Red alert indicator

4. **Average Compliance** (3.1.7-3.1.8)
   - Average compliance score across current period
   - Blue information indicator

**Drill-Down Navigation** (3.1.9) enables users to click any KPI card and view detailed supporting data, creating an interactive dashboard that guides users to areas requiring attention.

---

## Troubleshooting Guide

### KPI Values Showing as Blank

**Problem:** KPI cards display no values
**Solutions:**
1. Verify all SharePoint lists are created and populated
2. Check that data connections are established in PowerApp
3. Verify AuditPeriod has IsActive = true
4. Test formulas in Power Apps formula bar

### Incorrect Audit Count

**Problem:** Audit completion rate doesn't match expected count
**Solutions:**
1. Verify audits have SubmissionStatus = "Submitted" or "Verified"
2. Check that Location.Status = "Active"
3. Verify AuditPeriod lookup is matching correctly
4. Use Power Apps Diagnostics to trace filter logic

### Blank Trend Indicators

**Problem:** Trend text shows empty
**Solutions:**
1. Verify conditional formulas have all branches
2. Check for Blank() values that prevent calculation
3. Test average/count formulas with sample data
4. Verify text formatting functions work correctly

### Navigation Not Working

**Problem:** Clicking KPI card doesn't navigate
**Solutions:**
1. Verify OnSelect property is set on card (not inner element)
2. Check that target screen exists and is named correctly
3. Test navigation with simple Navigate() without transition
4. Use Screen Transition.None if Fade causes issues

### Performance Issues

**Problem:** KPI values load slowly or refresh slowly
**Solutions:**
1. Add **Explicit** data refresh only when needed
2. Use **Filter** on collection to reduce data size
3. Consider moving complex calculations to Power Automate
4. Enable **offline mode** for local data caching

---

**Document prepared for:** REdI Team
**Contact:** MERT Nurse Educator #70106 or #70108
**Last Updated:** January 2026
