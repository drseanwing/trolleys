# Phase 2.3 Audit Entry Screens Implementation Guide

**RBWH Resuscitation Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 2.3 implements the core audit entry workflow across four sequential screens that capture all audit data before equipment checklist entry. This phase creates the user-facing forms where auditors select trolleys, document conditions, and record routine check counts. Data is stored in context variables throughout the workflow and submitted to SharePoint lists in Phase 2.5 (Audit Submission).

**Phase Scope:** Tasks 2.3.1 through 2.3.22
**Estimated Duration:** 13 hours
**Prerequisites:** Phase 1.6 must be complete (PowerApp foundation with navigation structure)

**Navigation Flow:**
```
Audit Selection Screen (2.3.1-2.3.4)
           ↓
Documentation Check Screen (2.3.5-2.3.9)
           ↓
Condition Check Screen (2.3.10-2.3.16)
           ↓
Routine Checks Screen (2.3.17-2.3.22)
           ↓
Equipment Checklist Screen (Phase 2.4)
           ↓
Review/Summary Screen (Phase 2.5)
```

---

## Context Variables and Data Structure

All audit entry screens use shared context variables to store data during the workflow. These variables are accessed across screens and ultimately submitted to create related SharePoint records.

### Main Context Variable: `AuditData`

Create this at app startup (OnStart property of App object):

```powerfx
Set(AuditData, {
    SelectedLocationId: Blank(),
    SelectedLocationName: "",
    LastAuditDate: Blank(),
    AuditType: "Comprehensive",

    // Documentation Check fields
    CheckRecordStatus: "None",
    GuidelinesStatus: "None",
    BLSPosterPresent: false,
    EquipmentListStatus: "None",

    // Condition Check fields
    IsClean: false,
    IsWorkingOrder: false,
    IssueDescription: "",
    RubberBandsPresent: false,
    O2TubingCorrect: false,
    InhaloCylinderOK: false,

    // Routine Checks fields
    OutsideCheckCount: 0,
    InsideCheckCount: 0,
    CheckCountNotAvailable: false,
    CheckCountNAReason: "",
    ExpectedOutsideCount: 0,
    ExpectedInsideCount: 0
});
```

---

## Task 2.3.1: Create Audit Selection Screen

### Objective

Build the initial screen where auditors begin an audit by selecting a trolley location, viewing recent audit history, and selecting the audit type (Comprehensive vs Spot Check).

### Prerequisites

- Phase 1.6 PowerApp foundation complete
- SharePoint Location list populated with 76 trolley locations
- AuditData context variable initialized

### Screen Layout Specifications

**Screen Name:** Screen_AuditSelection

**Dimensions:** 1366 x 768 (tablet) / responsive for phone

**Background Color:** #F5F5F5 (light gray)

**Layout Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Navigation Back Button | "New Audit" | Home Icon        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Section 1: Trolley Selection                                    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Select Trolley Location" (Label)                           │ │
│ │ [Search/Dropdown showing locations] (Combo Box)             │ │
│ │ Search displays: Department Name, Building, Level           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 2: Last Audit Information (when location selected)    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Last Audit Date: [value or "No previous audits"]            │ │
│ │ Days Since Last Audit: [value]                              │ │
│ │ Last Compliance Score: [value or "-"]                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 3: Audit Type Selection                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Audit Type" (Label)                                        │ │
│ │ (◉) Comprehensive  Detailed check of all trolley items      │ │
│ │ (○) Spot Check     Focused review of key items              │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│                        [Continue Button]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Header Section

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BackButton | Button | Text | "← Back" |
| BackButton | Button | OnSelect | `Back()` |
| BackButton | Button | Color | #CCCCCC |
| TitleLabel | Label | Text | "New Audit" |
| TitleLabel | Label | Font size | 24 |
| TitleLabel | Label | Font weight | Bold |
| HomeButton | Button | Icon | Home icon |
| HomeButton | Button | OnSelect | `Navigate(Screen_Home)` |

#### Section 1: Location Selection

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| LocationLabel | Label | Text | "Select Trolley Location" |
| LocationLabel | Label | Font size | 14 |
| LocationLabel | Label | Font weight | Bold |
| LocationCombo | Combo Box | Items | `Sort(Location_List, DepartmentName)` |
| LocationCombo | Combo Box | SearchFields | `["DepartmentName", "Building", "SpecificLocation"]` |
| LocationCombo | Combo Box | IsSearchable | true |
| LocationCombo | Combo Box | OnChange | See PowerFx section below |
| LocationCombo | Combo Box | SelectMultiple | false |
| LocationCombo | Combo Box | Width | 100% |
| LocationCombo | Combo Box | Height | 40px |

#### Section 2: Last Audit Display

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| LastAuditContainer | Container | Visible | `AuditData.SelectedLocationId <> Blank()` |
| LastAuditContainer | Container | Background | #FFFFFF |
| LastAuditContainer | Container | Border | 1px solid #DDDDDD |
| LastAuditDateLabel | Label | Text | `"Last Audit Date: " & If(AuditData.LastAuditDate = Blank(), "No previous audits", Text(AuditData.LastAuditDate, "dd/mm/yyyy"))` |
| DaysSinceLabel | Label | Text | `"Days Since Last Audit: " & If(AuditData.LastAuditDate = Blank(), "-", Int((Now() - AuditData.LastAuditDate)/(1000*60*60*24)))` |
| ComplianceLabel | Label | Text | `"Last Compliance Score: " & If(AuditData.LastAuditDate = Blank(), "-", Text(LookUp(Location_List, ID = AuditData.SelectedLocationId).LastAuditCompliance, "0%"))` |

#### Section 3: Audit Type Selection

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| AuditTypeLabel | Label | Text | "Audit Type" |
| AuditTypeLabel | Label | Font weight | Bold |
| ComprehensiveRadio | Radio | Items | `["Comprehensive", "Spot Check"]` |
| ComprehensiveRadio | Radio | Default | "Comprehensive" |
| ComprehensiveRadio | Radio | OnChange | `Set(AuditData, {AuditData, AuditType: Self.Value})` |
| ComprehensiveRadio | Radio | Layout | Vertical |

#### Continue Button

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| ContinueButton | Button | Text | "Continue" |
| ContinueButton | Button | OnSelect | See validation logic below |
| ContinueButton | Button | Color | #2E7D32 (RBWH Green) |
| ContinueButton | Button | Font color | White |
| ContinueButton | Button | Height | 44px |
| ContinueButton | Button | Width | 200px |

### PowerFx Formulas

#### Task 2.3.2: Trolley Dropdown OnChange Handler

Implement searchable dropdown that populates AuditData when selection changes:

```powerfx
// LocationCombo OnChange property
If(
    !IsBlank(Self.Value),
    With(
        {
            selectedLocation: Self.Value,
            locationId: selectedLocation.ID,
            lastAudit: MaxEnumerateColumns(
                Filter(
                    Audit_List,
                    'Location/ID' = locationId &&
                    SubmissionStatus = "Submitted"
                ),
                StartedDateTime
            )
        },
        Set(AuditData, {
            AuditData,
            SelectedLocationId: locationId,
            SelectedLocationName: selectedLocation.DepartmentName,
            LastAuditDate: If(IsBlank(lastAudit), Blank(), lastAudit.StartedDateTime),
            ExpectedOutsideCount: selectedLocation.ExpectedOutsideChecks,
            ExpectedInsideCount: selectedLocation.ExpectedInsideChecks
        });
        // Reset other fields when location changes
        Set(AuditData, {
            AuditData,
            CheckRecordStatus: "None",
            GuidelinesStatus: "None",
            BLSPosterPresent: false,
            EquipmentListStatus: "None",
            IsClean: false,
            IsWorkingOrder: false,
            IssueDescription: "",
            RubberBandsPresent: false,
            O2TubingCorrect: false,
            InhaloCylinderOK: false,
            OutsideCheckCount: 0,
            InsideCheckCount: 0,
            CheckCountNotAvailable: false,
            CheckCountNAReason: ""
        })
    )
)
```

#### Task 2.3.3: Last Audit Info Display

Already implemented in component specifications above via label formulas. The display automatically updates based on AuditData.SelectedLocationId.

#### Task 2.3.4: Audit Type Selection Handler

```powerfx
// ComprehensiveRadio OnChange property
Set(AuditData, {
    AuditData,
    AuditType: Self.Value
});
```

#### Continue Button Validation

```powerfx
// ContinueButton OnSelect property
If(
    IsBlank(AuditData.SelectedLocationId),
    Notify("Please select a trolley location", NotificationType.Error),
    If(
        IsBlank(AuditData.AuditType),
        Notify("Please select an audit type", NotificationType.Error),
        Navigate(Screen_DocumentationCheck, ScreenTransition.Fade)
    )
)
```

### Data Binding

| Element | Data Source | Field Mapping |
|---------|-------------|----------------|
| LocationCombo Items | Location SharePoint list | Auto-generated by Combo Box |
| LocationCombo Display | DepartmentName + Building | Formatted in Item template |
| Last Audit Info | Audit_List + Location_List | Lookup by SelectedLocationId |

### Validation Rules

- Location selection required before continue
- Audit type must be selected (defaults to Comprehensive)
- If no previous audits exist, last audit fields display "No previous audits" / "-"

### Error Handling

```powerfx
// Add to app OnError property for global error catching
If(
    IsError(result),
    Notify(
        "Error loading audit selection: " & FirstError.Message,
        NotificationType.Error
    )
)
```

---

## Task 2.3.5-2.3.9: Create Documentation Check Screen

### Objective

Build the second step of the audit workflow where auditors verify the presence and status of four key documentation items: Check Record, Checking Guidelines, BLS Poster, and Equipment List.

### Prerequisites

- Screen_AuditSelection complete
- AuditData context variable with SelectedLocationId populated

### Screen Layout Specifications

**Screen Name:** Screen_DocumentationCheck

**Background Color:** #F5F5F5

**Layout Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Back Button | "Documentation Check" | Progress (Step 1/4)│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "Selected Location: [Location Name]" (context info)            │
│                                                                 │
│ Section 1: Check Record Status                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Check Record Present" (Label)                              │ │
│ │ (○) Current    (○) Old    (○) None                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 2: Checking Guidelines Status                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Checking Guidelines Present" (Label)                       │ │
│ │ (○) Current    (○) Old    (○) None                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 3: BLS Poster Toggle                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "BLS Poster Present" (Label)                                │ │
│ │ Toggle: [YES/NO]                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 4: Equipment List Status                               │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Equipment List Present" (Label)                            │ │
│ │ (○) Current    (○) Old    (○) None                           │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│              [Back] [Continue to Condition Check]              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Header Section

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BackButton | Button | Text | "← Back" |
| BackButton | Button | OnSelect | `Navigate(Screen_AuditSelection, ScreenTransition.Fade)` |
| TitleLabel | Label | Text | "Documentation Check" |
| TitleLabel | Label | Font size | 24 |
| ProgressLabel | Label | Text | "Step 1 of 4" |
| ProgressLabel | Label | Font size | 12 |
| ProgressLabel | Label | Color | #666666 |

#### Location Context

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| ContextLabel | Label | Text | `"Selected Location: " & AuditData.SelectedLocationName` |
| ContextLabel | Label | Font size | 14 |
| ContextLabel | Label | Color | #333333 |

#### Section 1: Check Record Status

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| CheckRecordLabel | Label | Text | "Check Record Present" |
| CheckRecordLabel | Label | Font weight | Bold |
| CheckRecordRadio | Radio | Items | `["Current", "Old", "None"]` |
| CheckRecordRadio | Radio | Default | AuditData.CheckRecordStatus |
| CheckRecordRadio | Radio | OnChange | `Set(AuditData, {AuditData, CheckRecordStatus: Self.Value})` |
| CheckRecordRadio | Radio | Layout | Horizontal |

#### Section 2: Guidelines Status

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| GuidelinesLabel | Label | Text | "Checking Guidelines Present" |
| GuidelinesLabel | Label | Font weight | Bold |
| GuidelinesRadio | Radio | Items | `["Current", "Old", "None"]` |
| GuidelinesRadio | Radio | Default | AuditData.GuidelinesStatus |
| GuidelinesRadio | Radio | OnChange | `Set(AuditData, {AuditData, GuidelinesStatus: Self.Value})` |
| GuidelinesRadio | Radio | Layout | Horizontal |

#### Section 3: BLS Poster Toggle (Task 2.3.8)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BLSLabel | Label | Text | "BLS Poster Present" |
| BLSLabel | Label | Font weight | Bold |
| BLSToggle | Toggle | Default | AuditData.BLSPosterPresent |
| BLSToggle | Toggle | OnChange | `Set(AuditData, {AuditData, BLSPosterPresent: Self.Value})` |
| BLSToggle | Toggle | OnText | "Yes" |
| BLSToggle | Toggle | OffText | "No" |

#### Section 4: Equipment List Status (Task 2.3.9)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| EquipmentListLabel | Label | Text | "Equipment List Present" |
| EquipmentListLabel | Label | Font weight | Bold |
| EquipmentListRadio | Radio | Items | `["Current", "Old", "None"]` |
| EquipmentListRadio | Radio | Default | AuditData.EquipmentListStatus |
| EquipmentListRadio | Radio | OnChange | `Set(AuditData, {AuditData, EquipmentListStatus: Self.Value})` |
| EquipmentListRadio | Radio | Layout | Horizontal |

#### Navigation Buttons

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BackButton2 | Button | Text | "Back" |
| BackButton2 | Button | OnSelect | `Navigate(Screen_AuditSelection, ScreenTransition.Fade)` |
| BackButton2 | Button | Color | #CCCCCC |
| ContinueButton | Button | Text | "Continue to Condition Check" |
| ContinueButton | Button | OnSelect | `Navigate(Screen_ConditionCheck, ScreenTransition.Fade)` |
| ContinueButton | Button | Color | #2E7D32 |

### PowerFx Formulas

#### Task 2.3.6: Check Record Status Radio Handler

```powerfx
// CheckRecordRadio OnChange property
Set(AuditData, {
    AuditData,
    CheckRecordStatus: Self.Value
})
```

#### Task 2.3.7: Guidelines Status Radio Handler

```powerfx
// GuidelinesRadio OnChange property
Set(AuditData, {
    AuditData,
    GuidelinesStatus: Self.Value
})
```

#### Task 2.3.8: BLS Poster Toggle Handler

```powerfx
// BLSToggle OnChange property
Set(AuditData, {
    AuditData,
    BLSPosterPresent: Self.Value
})
```

#### Task 2.3.9: Equipment List Status Radio Handler

```powerfx
// EquipmentListRadio OnChange property
Set(AuditData, {
    AuditData,
    EquipmentListStatus: Self.Value
})
```

### Data Binding

All data is stored in AuditData context variable and displayed via formulas. No direct SharePoint connections needed at this stage.

---

## Task 2.3.10-2.3.16: Create Condition Check Screen

### Objective

Build the third step of the audit workflow where auditors verify the physical condition of the trolley including cleanliness, working order, and specific equipment condition checks (rubber bands, O2 tubing, INHALO cylinder).

### Prerequisites

- Screen_DocumentationCheck complete
- AuditData context variable with documentation data populated

### Screen Layout Specifications

**Screen Name:** Screen_ConditionCheck

**Background Color:** #F5F5F5

**Layout Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Back Button | "Physical Condition Check" | (Step 2/4)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "Selected Location: [Location Name]" (context info)            │
│                                                                 │
│ Section 1: Cleanliness                                         │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Is the trolley clean?" (Label)                             │ │
│ │ Toggle: [YES/NO]                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 2: Working Order                                       │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Is the trolley in working order?" (Label)                  │ │
│ │ Toggle: [YES/NO]                                            │ │
│ │                                                             │ │
│ │ [Conditionally shown if NO selected]                        │ │
│ │ "Describe any issues:" (Label)                              │ │
│ │ [Multi-line text field for issue description]               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 3: Rubber Bands                                        │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Are rubber bands present and in use?" (Label)              │ │
│ │ Toggle: [YES/NO]                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 4: O2 Tubing                                           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Is O2 tubing correct type and condition?" (Label)          │ │
│ │ Toggle: [YES/NO]                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 5: INHALO Cylinder                                     │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "INHALO cylinder has correct pressure?" (Label)             │ │
│ │ Toggle: [YES/NO]                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│              [Back] [Continue to Routine Checks]               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Header Section

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BackButton | Button | Text | "← Back" |
| BackButton | Button | OnSelect | `Navigate(Screen_DocumentationCheck, ScreenTransition.Fade)` |
| TitleLabel | Label | Text | "Physical Condition Check" |
| TitleLabel | Label | Font size | 24 |
| ProgressLabel | Label | Text | "Step 2 of 4" |

#### Section 1: Cleanliness Toggle (Task 2.3.11)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| CleanLabel | Label | Text | "Is the trolley clean?" |
| CleanLabel | Label | Font weight | Bold |
| CleanToggle | Toggle | Default | AuditData.IsClean |
| CleanToggle | Toggle | OnChange | `Set(AuditData, {AuditData, IsClean: Self.Value})` |
| CleanToggle | Toggle | OnText | "Yes" |
| CleanToggle | Toggle | OffText | "No" |

#### Section 2: Working Order (Task 2.3.12-2.3.13)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| WorkingLabel | Label | Text | "Is the trolley in working order?" |
| WorkingLabel | Label | Font weight | Bold |
| WorkingToggle | Toggle | Default | AuditData.IsWorkingOrder |
| WorkingToggle | Toggle | OnChange | `Set(AuditData, {AuditData, IsWorkingOrder: Self.Value})` |
| WorkingToggle | Toggle | OnText | "Yes" |
| WorkingToggle | Toggle | OffText | "No" |
| IssueLabel | Label | Text | "Describe any issues:" |
| IssueLabel | Label | Visible | `!AuditData.IsWorkingOrder` |
| IssueLabel | Label | Font weight | Bold |
| IssueTextInput | Text input | Visible | `!AuditData.IsWorkingOrder` |
| IssueTextInput | Text input | Default | AuditData.IssueDescription |
| IssueTextInput | Text input | OnChange | `Set(AuditData, {AuditData, IssueDescription: Self.Value})` |
| IssueTextInput | Text input | Mode | MultiLine |
| IssueTextInput | Text input | Height | 100px |
| IssueTextInput | Text input | Placeholder | "Enter details about the issue..." |

#### Section 3: Rubber Bands Toggle (Task 2.3.14)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| RubberLabel | Label | Text | "Are rubber bands present and in use?" |
| RubberLabel | Label | Font weight | Bold |
| RubberToggle | Toggle | Default | AuditData.RubberBandsPresent |
| RubberToggle | Toggle | OnChange | `Set(AuditData, {AuditData, RubberBandsPresent: Self.Value})` |
| RubberToggle | Toggle | OnText | "Yes" |
| RubberToggle | Toggle | OffText | "No" |

#### Section 4: O2 Tubing Toggle (Task 2.3.15)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| O2Label | Label | Text | "Is O2 tubing correct type and condition?" |
| O2Label | Label | Font weight | Bold |
| O2Toggle | Toggle | Default | AuditData.O2TubingCorrect |
| O2Toggle | Toggle | OnChange | `Set(AuditData, {AuditData, O2TubingCorrect: Self.Value})` |
| O2Toggle | Toggle | OnText | "Yes" |
| O2Toggle | Toggle | OffText | "No" |

#### Section 5: INHALO Cylinder Toggle (Task 2.3.16)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| InhaloLabel | Label | Text | "INHALO cylinder has correct pressure?" |
| InhaloLabel | Label | Font weight | Bold |
| InhaloToggle | Toggle | Default | AuditData.InhaloCylinderOK |
| InhaloToggle | Toggle | OnChange | `Set(AuditData, {AuditData, InhaloCylinderOK: Self.Value})` |
| InhaloToggle | Toggle | OnText | "Yes" |
| InhaloToggle | Toggle | OffText | "No" |

### PowerFx Formulas

#### Task 2.3.11: Cleanliness Toggle Handler

```powerfx
// CleanToggle OnChange property
Set(AuditData, {
    AuditData,
    IsClean: Self.Value
})
```

#### Task 2.3.12: Working Order Toggle Handler

```powerfx
// WorkingToggle OnChange property
Set(AuditData, {
    AuditData,
    IsWorkingOrder: Self.Value
})
```

#### Task 2.3.13: Issue Description Conditional Field

```powerfx
// IssueLabel Visible property
!AuditData.IsWorkingOrder

// IssueTextInput Visible property
!AuditData.IsWorkingOrder

// IssueTextInput OnChange property
Set(AuditData, {
    AuditData,
    IssueDescription: Self.Value
})

// Clear issue description when working order is set to Yes
// Add to WorkingToggle OnChange:
If(
    Self.Value,
    Set(AuditData, {AuditData, IssueDescription: ""})
)
```

#### Task 2.3.14: Rubber Bands Toggle Handler

```powerfx
// RubberToggle OnChange property
Set(AuditData, {
    AuditData,
    RubberBandsPresent: Self.Value
})
```

#### Task 2.3.15: O2 Tubing Toggle Handler

```powerfx
// O2Toggle OnChange property
Set(AuditData, {
    AuditData,
    O2TubingCorrect: Self.Value
})
```

#### Task 2.3.16: INHALO Cylinder Toggle Handler

```powerfx
// InhaloToggle OnChange property
Set(AuditData, {
    AuditData,
    InhaloCylinderOK: Self.Value
})
```

### Data Binding

All data stored in AuditData context variable. Issue description field conditionally shown/hidden based on IsWorkingOrder toggle state.

---

## Task 2.3.17-2.3.22: Create Routine Checks Screen

### Objective

Build the fourth and final step before equipment checklist where auditors enter the number of outside (daily) and inside (weekly) checks performed, with handling for unavailable data and display of expected check counts.

### Prerequisites

- Screen_ConditionCheck complete
- AuditData context variable with condition data populated
- Location record includes ExpectedOutsideChecks and ExpectedInsideChecks values

### Screen Layout Specifications

**Screen Name:** Screen_RoutineChecks

**Background Color:** #F5F5F5

**Layout Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Back Button | "Routine Checks" | (Step 3/4)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "Selected Location: [Location Name]" (context info)            │
│                                                                 │
│ Section 1: Expected Check Counts                               │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Expected Outside (Daily) Checks: [value]"                  │ │
│ │ "Expected Inside (Weekly) Checks: [value]"                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 2: Check Availability Toggle (Task 2.3.20)            │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Check records available?" (Label)                          │ │
│ │ Toggle: [YES/NO]                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 3: Check Count Entry (shown if records available)      │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Outside (Daily) Check Count" (Label)                       │ │
│ │ [Numeric input field] / [Expected: value]                   │ │
│ │                                                             │ │
│ │ "Inside (Weekly) Check Count" (Label)                       │ │
│ │ [Numeric input field] / [Expected: value]                   │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Section 4: Not Available Reason (shown if records not available)│
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ "Reason records not available:" (Label)                     │ │
│ │ [Multi-line text field for reason]                          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│              [Back] [Continue to Equipment Check]              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Specifications

#### Header Section

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BackButton | Button | Text | "← Back" |
| BackButton | Button | OnSelect | `Navigate(Screen_ConditionCheck, ScreenTransition.Fade)` |
| TitleLabel | Label | Text | "Routine Checks" |
| TitleLabel | Label | Font size | 24 |
| ProgressLabel | Label | Text | "Step 3 of 4" |

#### Section 1: Expected Check Counts (Task 2.3.22)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| ExpectedOutsideLabel | Label | Text | `"Expected Outside (Daily) Checks: " & Text(AuditData.ExpectedOutsideCount, "0")` |
| ExpectedOutsideLabel | Label | Font size | 14 |
| ExpectedOutsideLabel | Label | Color | #333333 |
| ExpectedInsideLabel | Label | Text | `"Expected Inside (Weekly) Checks: " & Text(AuditData.ExpectedInsideCount, "0")` |
| ExpectedInsideLabel | Label | Font size | 14 |
| ExpectedInsideLabel | Label | Color | #333333 |

#### Section 2: Check Availability Toggle (Task 2.3.20)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| AvailableLabel | Label | Text | "Check records available?" |
| AvailableLabel | Label | Font weight | Bold |
| AvailableToggle | Toggle | Default | `!AuditData.CheckCountNotAvailable` |
| AvailableToggle | Toggle | OnChange | `Set(AuditData, {AuditData, CheckCountNotAvailable: !Self.Value})` |
| AvailableToggle | Toggle | OnText | "Yes" |
| AvailableToggle | Toggle | OffText | "No" |

#### Section 3: Check Count Entry (Task 2.3.18-2.3.19)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| OutsideLabel | Label | Text | "Outside (Daily) Check Count" |
| OutsideLabel | Label | Font weight | Bold |
| OutsideLabel | Label | Visible | `!AuditData.CheckCountNotAvailable` |
| OutsideInput | Text input | Type | Number |
| OutsideInput | Text input | Default | AuditData.OutsideCheckCount |
| OutsideInput | Text input | OnChange | `Set(AuditData, {AuditData, OutsideCheckCount: Value(Self.Value)})` |
| OutsideInput | Text input | Visible | `!AuditData.CheckCountNotAvailable` |
| OutsideInput | Text input | Width | 100px |
| OutsideHelper | Label | Text | `"/ Expected: " & Text(AuditData.ExpectedOutsideCount, "0")` |
| OutsideHelper | Label | Font size | 12 |
| OutsideHelper | Label | Color | #666666 |
| OutsideHelper | Label | Visible | `!AuditData.CheckCountNotAvailable` |
| InsideLabel | Label | Text | "Inside (Weekly) Check Count" |
| InsideLabel | Label | Font weight | Bold |
| InsideLabel | Label | Visible | `!AuditData.CheckCountNotAvailable` |
| InsideInput | Text input | Type | Number |
| InsideInput | Text input | Default | AuditData.InsideCheckCount |
| InsideInput | Text input | OnChange | `Set(AuditData, {AuditData, InsideCheckCount: Value(Self.Value)})` |
| InsideInput | Text input | Visible | `!AuditData.CheckCountNotAvailable` |
| InsideInput | Text input | Width | 100px |
| InsideHelper | Label | Text | `"/ Expected: " & Text(AuditData.ExpectedInsideCount, "0")` |
| InsideHelper | Label | Font size | 12 |
| InsideHelper | Label | Color | #666666 |
| InsideHelper | Label | Visible | `!AuditData.CheckCountNotAvailable` |

#### Section 4: Not Available Reason (Task 2.3.21)

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| ReasonLabel | Label | Text | "Reason records not available:" |
| ReasonLabel | Label | Font weight | Bold |
| ReasonLabel | Label | Visible | `AuditData.CheckCountNotAvailable` |
| ReasonInput | Text input | Visible | `AuditData.CheckCountNotAvailable` |
| ReasonInput | Text input | Default | AuditData.CheckCountNAReason |
| ReasonInput | Text input | OnChange | `Set(AuditData, {AuditData, CheckCountNAReason: Self.Value})` |
| ReasonInput | Text input | Mode | MultiLine |
| ReasonInput | Text input | Height | 100px |
| ReasonInput | Text input | Placeholder | "Enter reason why records are not available..." |

#### Navigation Buttons

| Component | Type | Property | Value |
|-----------|------|----------|-------|
| BackButton2 | Button | Text | "Back" |
| BackButton2 | Button | OnSelect | `Navigate(Screen_ConditionCheck, ScreenTransition.Fade)` |
| ContinueButton | Button | Text | "Continue to Equipment Check" |
| ContinueButton | Button | OnSelect | See validation logic below |
| ContinueButton | Button | Color | #2E7D32 |

### PowerFx Formulas

#### Task 2.3.18: Outside Check Count Input Handler

```powerfx
// OutsideInput OnChange property
Set(AuditData, {
    AuditData,
    OutsideCheckCount: Value(Self.Value)
})
```

#### Task 2.3.19: Inside Check Count Input Handler

```powerfx
// InsideInput OnChange property
Set(AuditData, {
    AuditData,
    InsideCheckCount: Value(Self.Value)
})
```

#### Task 2.3.20: Check Availability Toggle Handler

```powerfx
// AvailableToggle OnChange property
Set(AuditData, {
    AuditData,
    CheckCountNotAvailable: !Self.Value
});

// When toggling to "No Available" (CheckCountNotAvailable = true),
// clear the count fields
If(
    !Self.Value,
    Set(AuditData, {
        AuditData,
        OutsideCheckCount: 0,
        InsideCheckCount: 0
    })
)
```

#### Task 2.3.21: Not Available Reason Field Handler

```powerfx
// ReasonInput OnChange property
Set(AuditData, {
    AuditData,
    CheckCountNAReason: Self.Value
})
```

#### Task 2.3.22: Display Expected Check Counts

Already implemented in Section 1 labels with formulas:

```powerfx
// ExpectedOutsideLabel Text property
"Expected Outside (Daily) Checks: " & Text(AuditData.ExpectedOutsideCount, "0")

// ExpectedInsideLabel Text property
"Expected Inside (Weekly) Checks: " & Text(AuditData.ExpectedInsideCount, "0")
```

These values are populated from Location record when trolley is selected in Screen_AuditSelection.

#### Continue Button Validation

```powerfx
// ContinueButton OnSelect property
If(
    AuditData.CheckCountNotAvailable,
    If(
        IsBlank(AuditData.CheckCountNAReason) || Len(AuditData.CheckCountNAReason) = 0,
        Notify("Please provide reason why records are not available", NotificationType.Error),
        Navigate(Screen_EquipmentCheck, ScreenTransition.Fade)
    ),
    If(
        IsBlank(AuditData.OutsideCheckCount) || IsBlank(AuditData.InsideCheckCount),
        Notify("Please enter both check count values", NotificationType.Error),
        If(
            AuditData.OutsideCheckCount < 0 || AuditData.InsideCheckCount < 0,
            Notify("Check counts cannot be negative", NotificationType.Error),
            Navigate(Screen_EquipmentCheck, ScreenTransition.Fade)
        )
    )
)
```

### Data Binding

| Element | Data Source | Field Mapping |
|---------|-------------|----------------|
| Expected check counts | AuditData context | Set when location selected |
| Check availability | AuditData context | CheckCountNotAvailable |
| Outside/Inside counts | AuditData context | OutsideCheckCount / InsideCheckCount |
| Reason field | AuditData context | CheckCountNAReason |

### Validation Rules

- If records available: both count fields must be filled and non-negative
- If records unavailable: reason field must be populated with explanation
- Expected values are display-only, calculated from Location master data
- Invalid numeric input prevented by field type

---

## Integration Points

### Between Screens

1. **Screen_AuditSelection → Screen_DocumentationCheck**
   - Passes: SelectedLocationId, SelectedLocationName, AuditType, expected check counts
   - Validates: Location selected, audit type chosen

2. **Screen_DocumentationCheck → Screen_ConditionCheck**
   - Passes: All documentation check responses (4 fields)
   - Validates: No validation required (all fields have defaults)

3. **Screen_ConditionCheck → Screen_RoutineChecks**
   - Passes: All condition check responses (6 fields)
   - Validates: No validation required

4. **Screen_RoutineChecks → Screen_EquipmentCheck (Phase 2.4)**
   - Passes: Complete AuditData context with all fields filled
   - Validates: Check counts valid (or NA reason provided)

### To Phase 2.5 Review Screen

The complete AuditData context is passed to Screen_Review where:
- All responses are displayed in summary format
- Compliance scores are calculated
- Data is formatted for SharePoint submission

---

## Context Variable Full Structure Reference

At end of Phase 2.3 (before equipment screen), AuditData contains:

```powerfx
{
    // Audit Selection
    SelectedLocationId: [GUID],
    SelectedLocationName: "Department Name",
    LastAuditDate: [DateTime],
    AuditType: "Comprehensive" | "SpotCheck",

    // Documentation Check
    CheckRecordStatus: "Current" | "Old" | "None",
    GuidelinesStatus: "Current" | "Old" | "None",
    BLSPosterPresent: [Boolean],
    EquipmentListStatus: "Current" | "Old" | "None",

    // Condition Check
    IsClean: [Boolean],
    IsWorkingOrder: [Boolean],
    IssueDescription: [Text],
    RubberBandsPresent: [Boolean],
    O2TubingCorrect: [Boolean],
    InhaloCylinderOK: [Boolean],

    // Routine Checks
    OutsideCheckCount: [Number],
    InsideCheckCount: [Number],
    CheckCountNotAvailable: [Boolean],
    CheckCountNAReason: [Text],
    ExpectedOutsideCount: [Number],
    ExpectedInsideCount: [Number]
}
```

---

## Screen Summary Table

| Screen Name | Task ID | Purpose | Duration | Status |
|-------------|---------|---------|----------|--------|
| Screen_AuditSelection | 2.3.1-2.3.4 | Select trolley and audit type | 2 hours | Design template provided |
| Screen_DocumentationCheck | 2.3.5-2.3.9 | Verify documentation | 3 hours | Design template provided |
| Screen_ConditionCheck | 2.3.10-2.3.16 | Check physical condition | 3 hours | Design template provided |
| Screen_RoutineChecks | 2.3.17-2.3.22 | Enter check counts | 2 hours | Design template provided |

**Total Phase 2.3 Estimated Duration:** 13 hours

---

## Testing Checklist

Before moving to Phase 2.4 Equipment Checklist, verify:

- [ ] All four screens display correctly in tablet and phone layouts
- [ ] Navigation back/forward works between all screens
- [ ] Trolley dropdown search filters by department name, building, level
- [ ] Last audit date and compliance display correctly when trolley selected
- [ ] Audit type radio defaults to Comprehensive
- [ ] All radio button and toggle selections update AuditData correctly
- [ ] Issue description field shows/hides based on working order toggle
- [ ] Expected check counts display from Location record
- [ ] Check availability toggle shows/hides count entry vs reason fields
- [ ] Continue button validations trigger appropriate error messages
- [ ] Numeric input fields reject non-numeric entries
- [ ] All AuditData values persist when navigating back/forward
- [ ] Context labels correctly display selected location name on each screen

---

## Troubleshooting Guide

### Issue: Trolley dropdown not showing any locations

**Solution:** Verify Location_List data connection is configured in app and contains records. Check Location list in SharePoint has been populated with seed data.

### Issue: Last audit date not displaying

**Solution:** Ensure Audit_List has submitted audits for selected location. Check date format formula matches your regional settings.

### Issue: Expected check counts showing as 0 or blank

**Solution:** Verify Location records include ExpectedOutsideChecks and ExpectedInsideChecks column values in SharePoint. These must be populated for calculations to work.

### Issue: Issue description field not appearing when toggle set to "No"

**Solution:** Verify WorkingToggle OnChange formula includes logic to set IsWorkingOrder to false when toggled. Check IssueTextInput Visible property formula uses `!AuditData.IsWorkingOrder`.

### Issue: Reason field not appearing when check availability set to "No"

**Solution:** Check AvailableToggle formula correctly sets CheckCountNotAvailable to opposite of toggle value. Verify ReasonInput Visible property uses `AuditData.CheckCountNotAvailable`.

---

## Related Phases and Tasks

**Dependency Chain:**
- Phase 1.6: PowerApp Foundation (prerequisite)
- Phase 2.4: Equipment Checklist (follows this phase)
- Phase 2.5: Audit Submission (uses AuditData from this phase)

**Cross-References:**
- Trolley data model: See RBWH_Resuscitation_Trolley_Audit_Schema.md
- Audit list schema: See sharepoint_schemas/Audit.json
- Equipment list schema: See sharepoint_schemas/Equipment.json

---

## Additional Resources

- PowerFx documentation: https://learn.microsoft.com/en-us/power-platform/power-fx/reference
- Power Apps canvas app best practices: https://learn.microsoft.com/en-us/power-apps/guidance/planning/introduction
- Combo box control: https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-combo-box

---

*End of Phase 2.3 Implementation Guide*

**Document Version:** 1.0
**Last Updated:** January 2026
**Next Phase:** 2.4 Equipment Checklist
