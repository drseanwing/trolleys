# Phase 1.6 PowerApp Foundation Implementation Guide

**REdI Resuscitation Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 1.6 establishes the foundational PowerApp infrastructure for the REdI Trolley Audit system. This phase creates a canvas app with tablet/phone layouts, configures all SharePoint data connections, establishes the colour theme, builds core navigation, and creates the Home screen dashboard foundation.

**Phase Scope:** Tasks 1.6.1 through 1.6.6
**Estimated Duration:** 11 hours
**Prerequisites:** Phase 1.1-1.5 must be complete (all SharePoint lists created and populated)

---

## Task 1.6.1: Create New Canvas PowerApp with Tablet Layout

### Objective

Initialize a new Canvas PowerApp with tablet layout (1366x768) and enable phone layout support.

### Prerequisites

- Power Apps environment access with app creation permissions
- SharePoint site "REdI Trolley Audit" must exist (Task 1.1.1)

### Step-by-Step Instructions

#### Step 1: Create New App in Power Apps Studio

1. Navigate to https://make.powerapps.com
2. Sign in with your organizational account
3. In the left navigation, select **Create**
4. Click **Canvas app** under the "Start from blank" section
5. Name your app: `REdI_Trolley_Audit_App`
6. Choose **Tablet** as the format
7. Click **Create**

*Expected Result:* Power Apps Studio opens with a blank tablet-sized canvas

#### Step 2: Verify App Settings

1. Select **File** from the top menu
2. Select **App settings** from the left menu
3. Note the following details:
   - **App name:** REdI_Trolley_Audit_App
   - **App ID:** (auto-generated)
   - **Orientation:** Select **Portrait** (recommended for clinical use)
   - **Size:** Verify as **Tablet** (1366 x 768 px)

#### Step 3: Enable Phone Layout

1. In the **App settings** panel, locate the **Preview settings** section
2. Toggle **Enabled** on the Phone layout option
3. Select **Phone** from the layout dropdown to preview
4. Verify the layout adjusts appropriately
5. Return to **Tablet** view
6. Click **Save**

#### Step 4: Configure Basic App Properties

1. Go back to the main canvas
2. Select **File** → **Settings**
3. Under **Display**, set:
   - **Scale to fit:** ON (allows responsive design)
   - **Snap to grid:** ON (aids component alignment)

4. Under **Upcoming features**, verify:
   - **Formula bar syntax coloring:** ON
   - **Show names on components:** ON (helpful for troubleshooting)

5. Click **Save**

#### Step 5: Verify Canvas Configuration

1. The main canvas should now display:
   - Tablet size: 1366 x 768 pixels
   - Responsive layout indicators at screen edges
   - Grid alignment visible

### PowerFx Code

None required for this task (UI configuration only)

### Component Specifications

| Element | Specification |
|---------|---------------|
| Canvas Size | 1366 x 768 pixels |
| Layout Format | Tablet (Portrait) |
| Phone Support | Enabled, responsive scaling |
| Scale to Fit | Enabled |
| Snap to Grid | Enabled |
| Grid Spacing | 10 pixels |
| Background Color | White (#FFFFFF) |

### Verification Checklist

- [ ] App successfully created with name "REdI_Trolley_Audit_App"
- [ ] Tablet layout displays correctly (1366 x 768)
- [ ] Phone layout enabled and accessible from preview
- [ ] Orientation set to Portrait
- [ ] Scale to fit is enabled
- [ ] Snap to grid is enabled
- [ ] Canvas displays with white background
- [ ] App can be saved without errors

---

## Task 1.6.2: Configure App Data Connections

### Objective

Connect the PowerApp to all 10 SharePoint lists required for the audit system.

### Prerequisites

- Task 1.6.1 completed (app created)
- All Phase 1.2-1.5 SharePoint lists created and populated:
  - ServiceLine
  - EquipmentCategory
  - AuditPeriod
  - Equipment
  - Location
  - LocationChangeLog
  - Audit
  - AuditDocuments
  - AuditCondition
  - AuditChecks
  - (Optional: AuditEquipment for Phase 2)

- User must have read/write permissions to SharePoint site
- SharePoint site URL must be known (e.g., `https://yourtenant.sharepoint.com/sites/REdITrolleyAudit`)

### Step-by-Step Instructions

#### Step 1: Add SharePoint Connection to Power Apps

1. In Power Apps Studio, select **Data** in the left navigation panel
2. Click **Add data**
3. Search for **SharePoint**
4. Select the **SharePoint** connector
5. Click **Connect**
6. A dialog appears asking for the SharePoint site URL
7. Enter your SharePoint site URL: `https://yourtenant.sharepoint.com/sites/REdITrolleyAudit`
8. Click **Connect**

*Expected Result:* You see the SharePoint connector is now active with your site listed

#### Step 2: Add ServiceLine List

1. In the **Data** panel, click **Add data**
2. Your SharePoint site now appears in the list
3. Click on your SharePoint site
4. A list of available lists appears
5. Scroll down and select **ServiceLine**
6. Click **Add**

*Expected Result:* ServiceLine appears in your data sources

#### Step 3: Add Reference Data Lists (Repeat Steps)

Repeat the process for each of these reference lists. For each list:
1. Click **Add data** in the Data panel
2. Select your SharePoint site
3. Select the list name from the available lists
4. Click **Add**

Add these lists in order:
- **EquipmentCategory**
- **AuditPeriod**
- **Equipment**
- **Location**
- **LocationChangeLog**

*Expected Result:* All reference lists now appear in the Data panel

#### Step 4: Add Core Audit Lists

Repeat the process for the primary audit data lists:
- **Audit**
- **AuditDocuments**
- **AuditCondition**
- **AuditChecks**

#### Step 5: Verify All Connections

In the **Data** panel, you should now see all 10 lists:

```
✓ ServiceLine
✓ EquipmentCategory
✓ AuditPeriod
✓ Equipment
✓ Location
✓ LocationChangeLog
✓ Audit
✓ AuditDocuments
✓ AuditCondition
✓ AuditChecks
```

#### Step 6: Test Data Connection

To verify connections are working:

1. On the canvas, add a new **Gallery** control
2. In the formula bar, set its **Items** property to:
   ```powerfx
   ServiceLine
   ```
3. Verify the gallery populates with service line data
4. Delete this test gallery
5. Save the app

### PowerFx Code Examples

#### Test Formula for Each List

Use these formulas in test galleries or labels to verify connectivity:

```powerfx
// Test ServiceLine connection
CountRows(ServiceLine)

// Test Location connection with lookup
Filter(Location, ServiceLineId.Value = "your-service-line-id")

// Test Equipment with category
Filter(Equipment, CategoryId.Value = "your-category-id")

// Test Audit list
CountRows(Audit)
```

#### Collection Initialization (Optional - for offline support)

```powerfx
// In App.OnStart, create cached collections for reference data
ClearCollect(
    colServiceLines,
    ServiceLine
);

ClearCollect(
    colEquipmentCategories,
    EquipmentCategory
);

ClearCollect(
    colEquipment,
    Equipment
);

ClearCollect(
    colLocations,
    Location
);

ClearCollect(
    colAuditPeriods,
    AuditPeriod
);
```

### Connection String Reference

| List Name | Internal Name | Purpose |
|-----------|---------------|---------|
| ServiceLine | ServiceLine | Reference: organizational structure |
| EquipmentCategory | EquipmentCategory | Reference: trolley sections |
| AuditPeriod | AuditPeriod | Reference: current audit period config |
| Equipment | Equipment | Reference: master equipment list |
| Location | Location | Master: trolley locations |
| LocationChangeLog | LocationChangeLog | Historical: location changes |
| Audit | Audit | Primary: audit records |
| AuditDocuments | AuditDocuments | Child: documentation checks |
| AuditCondition | AuditCondition | Child: physical condition |
| AuditChecks | AuditChecks | Child: routine check counts |

### Verification Checklist

- [ ] SharePoint connection successfully added
- [ ] All 10 SharePoint lists visible in Data panel
- [ ] ServiceLine list contains 7 records
- [ ] Location list contains 76+ records
- [ ] Equipment list contains 89+ records
- [ ] EquipmentCategory list contains 8 records
- [ ] AuditPeriod list contains at least 1 current period
- [ ] Test gallery successfully displays data from ServiceLine
- [ ] No data connection errors appear
- [ ] App saved successfully

---

## Task 1.6.3: Create App Colour Theme

### Objective

Define colour variables aligned with REdI branding for consistent UI appearance throughout the app.

### Prerequisites

- Task 1.6.1 completed (app exists)
- Colour palette provided (REdI Brand Guidelines v1.0):
  - Primary: #1B3A5F (REdI Navy - Headers, backgrounds)
  - Accent: #E55B64 (REdI Coral - Primary brand, highlights)
  - Interactive: #2B9E9E (REdI Teal - Accents, interactive elements)
  - Background: #F5F5F5 (Light Grey)
  - Text Primary: #333333 (Dark Grey)
  - Text Secondary: #666666 (Medium Grey)

### Step-by-Step Instructions

#### Step 1: Create Theme Variables

1. In Power Apps Studio, select **File** → **Settings**
2. Select **Display** from the left menu
3. Note the colour palette section (this is for app-wide theme)
4. For more control, we'll create named colour variables instead

#### Step 2: Create Global Variables in App OnStart

1. Select the **App** object in the hierarchy
2. In the formula bar, select **OnStart** event
3. Enter the following formula to initialize all theme colours:

```powerfx
Set(PrimaryColor, RGBA(27, 58, 95, 1));
Set(AccentColor, RGBA(229, 91, 100, 1));
Set(InteractiveColor, RGBA(43, 158, 158, 1));
Set(BackgroundColor, RGBA(245, 245, 245, 1));
Set(TextPrimary, RGBA(51, 51, 51, 1));
Set(TextSecondary, RGBA(102, 102, 102, 1));
Set(BorderColor, RGBA(200, 200, 200, 1));
Set(ErrorColor, RGBA(220, 53, 69, 1));
Set(SuccessColor, RGBA(40, 167, 69, 1));
Set(WarningColor, RGBA(255, 193, 7, 1));
Set(InfoColor, RGBA(23, 162, 184, 1))
```

#### Step 3: Verify Global Variables

1. Save the app (Ctrl+S)
2. The app will automatically execute OnStart
3. Open **Power Apps Monitor** (Ctrl+Shift+I) to verify variables are created

#### Step 4: Document Colour System

Create a reference by adding comments to your OnStart:

```powerfx
// REdI Colour Theme - Initialized at app startup
// REdI Brand Guidelines v1.0 alignment

// Primary Branding Colours
Set(PrimaryColor, RGBA(27, 58, 95, 1));        // #1B3A5F REdI Navy
Set(AccentColor, RGBA(229, 91, 100, 1));       // #E55B64 REdI Coral
Set(InteractiveColor, RGBA(43, 158, 158, 1));  // #2B9E9E REdI Teal

// Secondary Colours
Set(LightTealColor, RGBA(141, 212, 212, 1));   // #8DD4D4 Light Teal
Set(LimeColor, RGBA(184, 204, 38, 1));         // #B8CC26 Lime Green
Set(SkyColor, RGBA(93, 173, 226, 1));          // #5DADE2 Sky Blue
Set(YellowColor, RGBA(244, 208, 63, 1));       // #F4D03F Warm Yellow

// Neutral Colours
Set(BackgroundColor, RGBA(245, 245, 245, 1));  // #F5F5F5 Light Grey
Set(TextPrimary, RGBA(51, 51, 51, 1));         // #333333 Dark Grey
Set(TextSecondary, RGBA(102, 102, 102, 1));    // #666666 Medium Grey
Set(BorderColor, RGBA(200, 200, 200, 1));      // #C8C8C8 Border Grey

// Semantic/Status Colours
Set(ErrorColor, RGBA(220, 53, 69, 1));         // #DC3545 Alert Red
Set(SuccessColor, RGBA(40, 167, 69, 1));       // #28A745 Success Green
Set(WarningColor, RGBA(255, 193, 7, 1));       // #FFC107 Warning Amber
Set(InfoColor, RGBA(23, 162, 184, 1));         // #17A2B8 Info Blue

// Typography (Montserrat font family)
Set(FontSizeH1, 40);       // 2.5rem
Set(FontSizeH2, 32);       // 2rem
Set(FontSizeH3, 24);       // 1.5rem
Set(FontSizeH4, 20);       // 1.25rem
Set(FontSizeBody, 16);     // 1rem
Set(FontSizeSmall, 14);    // 0.875rem
Set(FontSizeCaption, 12);  // 0.75rem
Set(FontWeightBold, 700);
Set(FontWeightSemiBold, 600);
Set(FontWeightMedium, 500);
Set(FontWeightNormal, 400)
```

#### Step 5: Apply Theme to Canvas Background

1. Select the main canvas (click blank area of screen)
2. In the **Fill** property (right panel), enter:
   ```powerfx
   BackgroundColor
   ```

#### Step 6: Create Theme Reference Documentation

Add a comment note in your app for future reference:

Create a new **Label** control temporarily:

1. Insert → **Label**
2. Set **Visible** to `false`
3. Set **Text** to:
```
"COLOUR THEME REFERENCE (REdI Brand Guidelines v1.0):
REdI Navy: #1B3A5F - Headers, Navigation, Backgrounds
REdI Coral: #E55B64 - Primary Brand, Buttons, Highlights
REdI Teal: #2B9E9E - Accents, Interactive Elements
Background: #F5F5F5 - Screen Background
Text Primary: #333333 - Headings, Body Text
Text Secondary: #666666 - Helper Text, Captions
Font: Montserrat (400, 500, 600, 700)"
```

4. Delete this label after noting colours

### PowerFx Code

Complete theme initialization formula for App.OnStart:

```powerfx
// REdI Trolley Audit System - Colour Theme Initialization
// Execute on app startup to define global colour variables
// Based on REdI Brand Guidelines v1.0

// Primary Branding (REdI - Resuscitation EDucation Initiative)
Set(PrimaryColor, RGBA(27, 58, 95, 1));        // #1B3A5F - REdI Navy (headers, backgrounds)
Set(AccentColor, RGBA(229, 91, 100, 1));       // #E55B64 - REdI Coral (primary brand, highlights)
Set(InteractiveColor, RGBA(43, 158, 158, 1));  // #2B9E9E - REdI Teal (accents, interactive)

// Secondary Colours
Set(LightTealColor, RGBA(141, 212, 212, 1));   // #8DD4D4 - Backgrounds, secondary elements
Set(LimeColor, RGBA(184, 204, 38, 1));         // #B8CC26 - Event branding, callouts
Set(SkyColor, RGBA(93, 173, 226, 1));          // #5DADE2 - Information, links
Set(YellowColor, RGBA(244, 208, 63, 1));       // #F4D03F - Warnings, highlights

// Neutral & Background
Set(BackgroundColor, RGBA(245, 245, 245, 1));  // #F5F5F5 - Page background
Set(TextPrimary, RGBA(51, 51, 51, 1));         // #333333 - Primary text
Set(TextSecondary, RGBA(102, 102, 102, 1));    // #666666 - Secondary text
Set(BorderColor, RGBA(200, 200, 200, 1));      // #C8C8C8 - Dividers & borders

// Semantic/Status Indicators (Clinical)
Set(ErrorColor, RGBA(220, 53, 69, 1));         // #DC3545 - Critical alerts, errors
Set(SuccessColor, RGBA(40, 167, 69, 1));       // #28A745 - Positive actions, completions
Set(WarningColor, RGBA(255, 193, 7, 1));       // #FFC107 - Caution, attention needed
Set(InfoColor, RGBA(23, 162, 184, 1));         // #17A2B8 - Informational content

// Typography (Montserrat type scale)
Set(FontSizeH1, 40);       // 2.5rem - Bold (700)
Set(FontSizeH2, 32);       // 2rem - SemiBold (600)
Set(FontSizeH3, 24);       // 1.5rem - SemiBold (600)
Set(FontSizeH4, 20);       // 1.25rem - Medium (500)
Set(FontSizeBody, 16);     // 1rem - Regular (400)
Set(FontSizeSmall, 14);    // 0.875rem - Regular (400)
Set(FontSizeCaption, 12);  // 0.75rem - Regular (400)
Set(FontWeightBold, 700);
Set(FontWeightSemiBold, 600);
Set(FontWeightMedium, 500);
Set(FontWeightNormal, 400)   // Regular text
```

### Component Specifications

| Colour Variable | Hex Code | RGB Values | Purpose |
|-----------------|----------|-----------|---------|
| PrimaryColor | #1B3A5F | 27,58,95 | REdI Navy - Headers, navigation, backgrounds |
| AccentColor | #E55B64 | 229,91,100 | REdI Coral - Primary brand, buttons, highlights |
| InteractiveColor | #2B9E9E | 43,158,158 | REdI Teal - Accents, interactive elements |
| LightTealColor | #8DD4D4 | 141,212,212 | Backgrounds, secondary elements |
| LimeColor | #B8CC26 | 184,204,38 | Event branding, callouts |
| SkyColor | #5DADE2 | 93,173,226 | Information, links |
| YellowColor | #F4D03F | 244,208,63 | Warnings, highlights |
| BackgroundColor | #F5F5F5 | 245,245,245 | Screen backgrounds, card backgrounds |
| TextPrimary | #333333 | 51,51,51 | Headings, body text |
| TextSecondary | #666666 | 102,102,102 | Helper text, captions, secondary info |
| BorderColor | #C8C8C8 | 200,200,200 | Dividers, borders, separator lines |
| ErrorColor | #DC3545 | 220,53,69 | Critical alerts, stop actions |
| SuccessColor | #28A745 | 40,167,69 | Positive actions, completions |
| WarningColor | #FFC107 | 255,193,7 | Caution, attention needed |
| InfoColor | #17A2B8 | 23,162,184 | Informational content |

### Verification Checklist

- [ ] App.OnStart contains all colour variable definitions
- [ ] All colour variables use RGBA format with correct values
- [ ] App executes OnStart without errors
- [ ] PowerApps Monitor confirms all variables are initialized
- [ ] Canvas background displays correct light grey colour
- [ ] No hardcoded colours in formula (all use variables)
- [ ] Theme colours saved as reference documentation
- [ ] App saves successfully with theme initialized

---

## Task 1.6.4: Create App Navigation Component

### Objective

Build a reusable navigation header component with REdI logo, app title, navigation menu, and current user display.

### Prerequisites

- Task 1.6.1-1.6.3 completed
- Colour theme variables initialized (Task 1.6.3)
- SharePoint connections configured (Task 1.6.2)
- Logo image file (redi-logo-primary-rgb.svg or redi-logo-reversed-rgb.svg for dark backgrounds)

### Step-by-Step Instructions

#### Step 1: Create Navigation Header Container

1. Insert a **Rectangle** shape to serve as the header background
2. Position it at the top of the canvas:
   - **X:** 0
   - **Y:** 0
   - **Width:** 1366
   - **Height:** 80
3. Set properties:
   - **Fill:** `PrimaryColor`
   - **BorderThickness:** 0
   - **ZIndex:** 100 (ensures it stays on top)

#### Step 2: Add Logo Component

1. Insert an **Image** control
2. Position it in the header:
   - **X:** 10
   - **Y:** 10
   - **Width:** 60
   - **Height:** 60
3. Set **Image** property to your logo file
4. Optional: Use a placeholder text if logo unavailable:
   - Delete the image
   - Add a **Label** with text "REdI"
   - Set fill color to `AccentColor`

#### Step 3: Add App Title

1. Insert a **Label** control for the app title
2. Position next to the logo:
   - **X:** 80
   - **Y:** 15
   - **Width:** 400
   - **Height:** 50
3. Set properties:
   - **Text:** "Trolley Audit System"
   - **Font:** Segoe UI, 28pt, Bold
   - **Color:** White
   - **Align:** Left
   - **VerticalAlign:** MiddleVertical

#### Step 4: Create Navigation Menu

1. Insert a **Horizontal Gallery** to create menu items dynamically
2. Position it in the header:
   - **X:** 500
   - **Y:** 25
   - **Width:** 400
   - **Height:** 40
3. Set the gallery's **Items** property to:
```powerfx
Table(
    {Label: "Home", Screen: "HomeScreen", Icon: "🏠"},
    {Label: "Trolleys", Screen: "TrolleysScreen", Icon: "🛒"},
    {Label: "Audit", Screen: "AuditScreen", Icon: "✓"},
    {Label: "Issues", Screen: "IssuesScreen", Icon: "⚠"},
    {Label: "Reports", Screen: "ReportsScreen", Icon: "📊"}
)
```

4. Inside the gallery, add a **Label** for each menu item:
   - **Text:** `ThisItem.Label`
   - **Font:** 12pt, Bold
   - **Color:** White
   - **Padding:** 10px horizontal
   - **Hover:** Set `Fill` to `AccentColor` with semi-transparency

#### Step 5: Add User Information Display

1. Insert a **Label** for the current user
2. Position on the right side of header:
   - **X:** 1000
   - **Y:** 25
   - **Width:** 350
   - **Height:** 40
3. Set properties:
   - **Text:** `"Welcome, " & User().FullName`
   - **Font:** 12pt
   - **Color:** White
   - **Align:** Right
   - **VerticalAlign:** MiddleVertical

#### Step 6: Add Current Date/Time Display (Optional)

1. Insert a **Label** below the user info
2. Position:
   - **X:** 1000
   - **Y:** 55
   - **Width:** 350
   - **Height:** 20
3. Set properties:
   - **Text:** `Text(Now(), "ddd, d mmmm yyyy")`
   - **Font:** 10pt
   - **Color:** White with 80% opacity
   - **Align:** Right

#### Step 7: Create Navigation Function

Add a helper collection to your App.OnStart for easier navigation:

```powerfx
ClearCollect(
    colNavigation,
    {
        Label: "Home",
        Screen: "HomeScreen",
        Icon: "🏠",
        Order: 1
    },
    {
        Label: "Trolleys",
        Screen: "TrolleysScreen",
        Icon: "🛒",
        Order: 2
    },
    {
        Label: "Audit",
        Screen: "AuditScreen",
        Icon: "✓",
        Order: 3
    },
    {
        Label: "Issues",
        Screen: "IssuesScreen",
        Icon: "⚠",
        Order: 4
    },
    {
        Label: "Reports",
        Screen: "ReportsScreen",
        Icon: "📊",
        Order: 5
    }
);
```

#### Step 8: Add Menu Click Handler

On each menu label in the gallery, add an **OnSelect** handler:

```powerfx
Navigate(Screen(ThisItem.Screen), ScreenTransition.Fade)
```

### PowerFx Code

Complete navigation header initialization:

```powerfx
// Add to App.OnStart after colour theme initialization

// Navigation Menu Structure
ClearCollect(
    colNavigationMenu,
    {
        Label: "Home",
        Screen: "HomeScreen",
        Icon: "🏠",
        Order: 1,
        Description: "Dashboard and KPIs"
    },
    {
        Label: "Trolleys",
        Screen: "TrolleysScreen",
        Icon: "🛒",
        Order: 2,
        Description: "View and manage trolleys"
    },
    {
        Label: "Audit",
        Screen: "AuditScreen",
        Icon: "✓",
        Order: 3,
        Description: "Start or review audits"
    },
    {
        Label: "Issues",
        Screen: "IssuesScreen",
        Icon: "⚠",
        Order: 4,
        Description: "Track maintenance issues"
    },
    {
        Label: "Reports",
        Screen: "ReportsScreen",
        Icon: "📊",
        Order: 5,
        Description: "View compliance reports"
    }
);

// Current User Variables
Set(CurrentUserName, User().FullName);
Set(CurrentUserEmail, User().Email);
Set(LoggedInTime, Now());
```

Navigation handler formula for menu items:

```powerfx
// OnSelect handler for menu label
If(
    ThisItem.Screen = "HomeScreen",
    Navigate(HomeScreen, ScreenTransition.Fade),
    ThisItem.Screen = "TrolleysScreen",
    Navigate(TrolleysScreen, ScreenTransition.Fade),
    ThisItem.Screen = "AuditScreen",
    Navigate(AuditScreen, ScreenTransition.Fade),
    ThisItem.Screen = "IssuesScreen",
    Navigate(IssuesScreen, ScreenTransition.Fade),
    ThisItem.Screen = "ReportsScreen",
    Navigate(ReportsScreen, ScreenTransition.Fade)
);
```

### Component Specifications

| Component | Property | Value |
|-----------|----------|-------|
| Header Rectangle | Width | 1366 |
| | Height | 80 |
| | Fill | PrimaryColor (#1B3A5F REdI Navy) |
| | ZIndex | 100 |
| Logo Image | Width | 60 |
| | Height | 60 |
| | Source | redi-logo-reversed-rgb.svg |
| App Title | Font | Montserrat, 28pt |
| | Font Weight | Bold (700) |
| | Text Color | White |
| Menu Gallery | Items | colNavigationMenu |
| | Columns | 5 |
| Menu Labels | Font | Montserrat, 12pt |
| | Font Weight | SemiBold (600) |
| | Text Color | White |
| | Hover Fill | AccentColor (#E55B64) at 80% |
| User Label | Font | Montserrat, 12pt |
| | Text Color | White |
| | Position | Right-aligned |

### Verification Checklist

- [ ] Header rectangle displays across full app width at top
- [ ] REdI logo or placeholder displays in header
- [ ] App title "Trolley Audit System" visible in header
- [ ] Navigation menu items display horizontally
- [ ] All 5 menu items visible: Home, Trolleys, Audit, Issues, Reports
- [ ] Current user name displays on right side of header
- [ ] Current date/time displays (optional, but recommended)
- [ ] Menu items change appearance on hover
- [ ] Clicking menu items navigates to correct screens (after screens are created)
- [ ] Header remains fixed when scrolling (ZIndex = 100)
- [ ] No horizontal scrollbar appears at 1366px width
- [ ] Logo and text colours are legible against navy background

---

## Task 1.6.5: Create Home Screen Layout

### Objective

Build the Home screen dashboard structure with sections for KPI cards, recent audits list, recent issues list, and quick action buttons.

### Prerequisites

- Task 1.6.1-1.6.4 completed
- Navigation component created
- All SharePoint lists connected
- Colour theme initialized

### Step-by-Step Instructions

#### Step 1: Create Base Screen Container

1. Create a new screen named "HomeScreen"
2. Set screen properties:
   - **Width:** 1366
   - **Height:** 768
   - **Fill:** `BackgroundColor`
   - **Orientation:** Portrait

#### Step 2: Add Navigation Header to Screen

1. Copy the navigation header from the previous canvas
2. Paste it onto HomeScreen at the top (Y: 0, Height: 80)
3. This creates a consistent header across all screens

#### Step 3: Add Main Content Container

1. Insert a **Rectangle** for the main content area:
   - **X:** 20
   - **Y:** 100
   - **Width:** 1326
   - **Height:** 650
   - **Fill:** White
   - **BorderColor:** `BorderColor`
   - **BorderThickness:** 1
   - **Radius:** 8px

#### Step 4: Create KPI Cards Section

1. Add a **Label** for section title:
   - **Text:** "Key Performance Indicators"
   - **Y:** 120
   - **Font Size:** 18pt, Bold
   - **Color:** `TextPrimary`

2. Create 4 KPI card rectangles in a horizontal row:
   - Each card dimensions:
     - **Width:** 300
     - **Height:** 120
     - **Fill:** White
     - **BorderColor:** `BorderColor`
     - **BorderThickness:** 1
     - **Radius:** 4px

   - Card positions (Y: 150):
     - Card 1: X: 30
     - Card 2: X: 350
     - Card 3: X: 670
     - Card 4: X: 990

3. Inside each card, add:
   - Large **Label** for the KPI value (48pt font)
   - Smaller **Label** for the KPI title (12pt font)

#### Step 5: Add "This Week's Audits" Section

1. Add a **Label** for section title:
   - **Text:** "This Week's Audits"
   - **Y:** 310
   - **Font Size:** 16pt, Bold
   - **Color:** `TextPrimary`

2. Create a **Gallery** to display audit list:
   - **X:** 30
   - **Y:** 340
   - **Width:** 620
   - **Height:** 300
   - **Items:** `Filter(Audit, IsBlank(CompletedDateTime))`

3. In the gallery, add:
   - **Label** for Location Name: `ThisItem.LocationId.DisplayName`
   - **Label** for Service Line: `ThisItem.LocationId.ServiceLineId.Name`
   - **Label** for Started Date: `Text(ThisItem.StartedDateTime, "ddd, d mmmm")`

#### Step 6: Add "Recent Issues" Section

1. Add a **Label** for section title (right column):
   - **Text:** "Recent Issues"
   - **Y:** 310
   - **X:** 700
   - **Font Size:** 16pt, Bold
   - **Color:** `TextPrimary`

2. Create a **Gallery** for issues list:
   - **X:** 700
   - **Y:** 340
   - **Width:** 620
   - **Height:** 300
   - **Items:** `Sort(Filter(Issue, Status <> "Closed"), DateCreated, Descending)`

3. In the gallery, add:
   - **Label** for Issue Number
   - **Label** for Title
   - **Label** for Severity (colour-coded)
   - **Label** for Age: `Text(DateDiff(Now(), DateCreated, Days)) & " days"`

#### Step 7: Add Quick Action Buttons

1. Add a horizontal row of action buttons at the bottom:
   - **Y:** 660
   - **X:** 30

2. Create buttons:
   - **Button 1:** "Start Audit"
     - Text: "Start Audit"
     - Fill: `PrimaryColor`
     - Text Color: White
     - OnSelect: `Navigate(AuditScreen)`

   - **Button 2:** "View Trolleys"
     - Text: "View Trolleys"
     - Fill: `InteractiveColor`
     - Text Color: White
     - OnSelect: `Navigate(TrolleysScreen)`

   - **Button 3:** "View Issues"
     - Text: "View Issues"
     - Fill: `AccentColor`
     - Text Color: White
     - OnSelect: `Navigate(IssuesScreen)`

   - **Button 4:** "View Reports"
     - Text: "View Reports"
     - Fill: `PrimaryColor`
     - Text Color: White
     - OnSelect: `Navigate(ReportsScreen)`

### PowerFx Code

Initialize Home screen data in screen OnVisible event:

```powerfx
// HomeScreen.OnVisible
// Load and calculate data when screen becomes visible

// Calculate KPI values for placeholder cards
Set(varAuditCompletionRate, "89%");
Set(varOpenIssuesCount, "12");
Set(varOverdueAudits, "3");
Set(varAvgComplianceScore, "87%");

// Load this week's incomplete audits
ClearCollect(
    colThisWeeksAudits,
    Filter(
        Audit,
        IsBlank(CompletedDateTime) And
        StartedDateTime >= Today() - 7
    )
);

// Load recent open issues (last 5)
ClearCollect(
    colRecentIssues,
    FirstN(
        Filter(
            Issue,
            Status <> "Closed"
        ),
        5
    )
)
```

Section title formula for dynamic content:

```powerfx
// For "This Week's Audits" label
Text(Today(), "dddd") & " - Week of " & Text(Today(), "d mmmm yyyy")

// For audits gallery items
Filter(
    Audit,
    And(
        IsBlank(CompletedDateTime),
        StartedDateTime >= Today() - 7,
        StartedDateTime <= Today() + 1
    )
)
```

Issue severity colour formula:

```powerfx
// In a label within the issues gallery
If(
    ThisItem.Severity = "Critical",
    ErrorColor,
    ThisItem.Severity = "High",
    AccentColor,
    ThisItem.Severity = "Medium",
    WarningColor,
    InfoColor
)
```

### Component Specifications

| Component | Purpose | Dimensions |
|-----------|---------|-----------|
| KPI Cards (4x) | Display key metrics | 300x120 each |
| This Week's Audits Gallery | List incomplete audits | 620x300 |
| Recent Issues Gallery | List open issues | 620x300 |
| Quick Action Buttons (4x) | Navigation shortcuts | 150x50 each |
| Main Container | Content area | 1326x650 |

### Layout Diagram

```
┌─────────────────────────────────────────────────────────┐
│         HEADER (Navigation Component)                    │
├─────────────────────────────────────────────────────────┤
│ Key Performance Indicators                               │
│ ┌─────────┬─────────┬─────────┬─────────┐               │
│ │  Card 1 │  Card 2 │  Card 3 │  Card 4 │               │
│ └─────────┴─────────┴─────────┴─────────┘               │
├──────────────────────┬──────────────────────┤            │
│                      │                      │            │
│  This Week's Audits  │   Recent Issues      │            │
│  Gallery             │   Gallery            │            │
│  (620x300)           │   (620x300)          │            │
│                      │                      │            │
├──────────────────────┴──────────────────────┤            │
│ Quick Actions: [Start Audit][View Trolleys]│            │
│              [View Issues] [View Reports]   │            │
└─────────────────────────────────────────────┘            │
```

### Verification Checklist

- [ ] HomeScreen created successfully
- [ ] Navigation header displays at top
- [ ] KPI section with title displays
- [ ] 4 KPI cards display in a row
- [ ] This Week's Audits section displays
- [ ] Audits gallery shows incomplete audits (or placeholder data)
- [ ] Recent Issues section displays
- [ ] Issues gallery shows open issues (or placeholder data)
- [ ] Quick action buttons display at bottom
- [ ] All buttons have correct background colours
- [ ] No layout overlaps or missing sections
- [ ] Screen scrolls smoothly if content exceeds viewport
- [ ] OnVisible event populates data without errors

---

## Task 1.6.6: Add Home Screen KPI Placeholders

### Objective

Create 4 KPI cards with placeholder calculations for:
1. Audit Completion Rate
2. Open Issues Count
3. Overdue Audits
4. Average Compliance Score

### Prerequisites

- Task 1.6.5 completed (Home screen layout)
- All SharePoint lists populated
- Data connections verified

### Step-by-Step Instructions

#### Step 1: Configure KPI Card 1 - Audit Completion Rate

1. Select the first KPI card (Card 1) from Task 1.6.5
2. Add a large **Label** inside for the metric value:
   - **Text:** `"89%"` (placeholder)
   - **Font Size:** 48pt, Bold
   - **Color:** `PrimaryColor`
   - **Align:** Center
   - **Y:** 10

3. Add a smaller **Label** below for the metric title:
   - **Text:** "Audit Completion Rate"
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`
   - **Align:** Center
   - **Y:** 65

4. Add a small **Icon/Shape** to indicate trend (optional):
   - Use an up arrow (↑) in `SuccessColor` if trend is positive
   - Position at top-right corner

**Formula for real calculation (Phase 3):**
```powerfx
// Phase 3: When Audit data is fully populated
Set(
    varAuditCompletionRate,
    Text(
        CountRows(
            Filter(
                Audit,
                SubmissionStatus = "Submitted"
            )
        ) / CountRows(Location),
        "0.0%"
    )
)
```

#### Step 2: Configure KPI Card 2 - Open Issues Count

1. Select the second KPI card (Card 2)
2. Add a large **Label** for the metric value:
   - **Text:** `"12"` (placeholder)
   - **Font Size:** 48pt, Bold
   - **Color:** `AccentColor`
   - **Align:** Center
   - **Y:** 10

3. Add a smaller **Label** for the metric title:
   - **Text:** "Open Issues"
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`
   - **Align:** Center
   - **Y:** 65

4. Optional: Add a trend indicator

**Formula for real calculation (Phase 2):**
```powerfx
// When Issue list is created
Set(
    varOpenIssuesCount,
    CountRows(
        Filter(
            Issue,
            Status <> "Closed" And Status <> "Resolved"
        )
    )
)
```

#### Step 3: Configure KPI Card 3 - Overdue Audits

1. Select the third KPI card (Card 3)
2. Add a large **Label** for the metric value:
   - **Text:** `"3"` (placeholder)
   - **Font Size:** 48pt, Bold
   - **Color:** `ErrorColor`
   - **Align:** Center
   - **Y:** 10

3. Add a smaller **Label** for the metric title:
   - **Text:** "Overdue Audits"
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`
   - **Align:** Center
   - **Y:** 65

4. Optional: Add a warning icon

**Formula for real calculation (Phase 2):**
```powerfx
// Count trolleys without audit in current period
Set(
    varOverdueAudits,
    CountRows(
        Filter(
            Location,
            IsBlank(LastAuditDate) Or
            DateDiff(Today(), LastAuditDate, Days) > 30
        )
    )
)
```

#### Step 4: Configure KPI Card 4 - Average Compliance Score

1. Select the fourth KPI card (Card 4)
2. Add a large **Label** for the metric value:
   - **Text:** `"87%"` (placeholder)
   - **Font Size:** 48pt, Bold
   - **Color:** `InteractiveColor`
   - **Align:** Center
   - **Y:** 10

3. Add a smaller **Label** for the metric title:
   - **Text:** "Avg Compliance"
   - **Font Size:** 12pt
   - **Color:** `TextSecondary`
   - **Align:** Center
   - **Y:** 65

4. Optional: Add a positive trend indicator

**Formula for real calculation (Phase 3):**
```powerfx
// Average compliance score of recent audits
Set(
    varAvgComplianceScore,
    Text(
        Average(
            Filter(
                Audit,
                SubmissionStatus = "Submitted"
            ),
            OverallCompliance
        ),
        "0.0%"
    )
)
```

#### Step 5: Make KPI Cards Interactive

1. Add an **OnSelect** event to each KPI card:

   **Card 1 (Completion Rate):**
   ```powerfx
   Navigate(ReportsScreen);
   Set(varReportFilter, "CompletionRate")
   ```

   **Card 2 (Open Issues):**
   ```powerfx
   Navigate(IssuesScreen);
   Set(varIssueFilter, "Open")
   ```

   **Card 3 (Overdue Audits):**
   ```powerfx
   Navigate(TrolleysScreen);
   Set(varTrolleyFilter, "Overdue")
   ```

   **Card 4 (Compliance Score):**
   ```powerfx
   Navigate(ReportsScreen);
   Set(varReportFilter, "Compliance")
   ```

#### Step 6: Add Card Styling for Interactivity

1. For each KPI card rectangle, add a **HoverFill** effect:
   - **HoverFill:** `RGBA(245, 245, 245, 1)` (light grey)
   - **Cursor:** `Pointer` (for all cards)

2. Optional: Add a subtle border highlight on hover:
   ```powerfx
   // In card's BorderThickness (optional)
   If(
       HoveringCard1,
       3,
       1
   )
   ```

#### Step 7: Add Card Loading States (Optional Enhancement)

Create a collection in HomeScreen.OnVisible to simulate loading:

```powerfx
// Temporary: Show loading placeholders while data loads
If(
    IsBlank(varAuditCompletionRate),
    "Loading...",
    varAuditCompletionRate
)
```

### PowerFx Code

Complete KPI initialization for HomeScreen.OnVisible:

```powerfx
// HomeScreen.OnVisible - Initialize KPI Variables
// These formulas calculate real values in Phase 3
// For now, they use placeholder values

// KPI 1: Audit Completion Rate (placeholder: 89%)
Set(
    varAuditCompletionRate,
    "89%"
    // Phase 3 formula:
    // Text(CountRows(Filter(Audit, SubmissionStatus = "Submitted")) / CountRows(Location), "0.0%")
);

// KPI 2: Open Issues Count (placeholder: 12)
Set(
    varOpenIssuesCount,
    "12"
    // Phase 2 formula:
    // CountRows(Filter(Issue, Status <> "Closed" And Status <> "Resolved"))
);

// KPI 3: Overdue Audits (placeholder: 3)
Set(
    varOverdueAudits,
    "3"
    // Phase 2 formula:
    // CountRows(Filter(Location, IsBlank(LastAuditDate) Or DateDiff(Today(), LastAuditDate, Days) > 30))
);

// KPI 4: Average Compliance Score (placeholder: 87%)
Set(
    varAvgComplianceScore,
    "87%"
    // Phase 3 formula:
    // Text(Average(Filter(Audit, SubmissionStatus = "Submitted"), OverallCompliance), "0.0%")
);
```

KPI card value display formula (for each card's label):

```powerfx
// Card 1 - Completion Rate
If(
    IsBlank(varAuditCompletionRate),
    "89%",
    varAuditCompletionRate
)

// Card 2 - Open Issues
If(
    IsBlank(varOpenIssuesCount),
    "12",
    varOpenIssuesCount
)

// Card 3 - Overdue Audits
If(
    IsBlank(varOverdueAudits),
    "3",
    varOverdueAudits
)

// Card 4 - Compliance Score
If(
    IsBlank(varAvgComplianceScore),
    "87%",
    varAvgComplianceScore
)
```

KPI card click handler (OnSelect for card rectangles):

```powerfx
// OnSelect event for each KPI card
If(
    ThisItem = Card1,
    Navigate(ReportsScreen),
    ThisItem = Card2,
    Navigate(IssuesScreen),
    ThisItem = Card3,
    Navigate(TrolleysScreen),
    Navigate(ReportsScreen)
)
```

### Component Specifications

| KPI Card | Title | Placeholder Value | Primary Colour | Linked Screen |
|----------|-------|-------------------|----------------|----|
| Card 1 | Audit Completion Rate | 89% | PrimaryColor | ReportsScreen |
| Card 2 | Open Issues Count | 12 | AccentColor | IssuesScreen |
| Card 3 | Overdue Audits | 3 | ErrorColor | TrolleysScreen |
| Card 4 | Avg Compliance Score | 87% | InteractiveColor | ReportsScreen |

### Verification Checklist

- [ ] KPI Card 1 displays "89%" for Audit Completion Rate
- [ ] KPI Card 2 displays "12" for Open Issues Count
- [ ] KPI Card 3 displays "3" for Overdue Audits
- [ ] KPI Card 4 displays "87%" for Average Compliance Score
- [ ] All cards have correct title labels
- [ ] Each metric value uses appropriate colour
- [ ] Cards are clickable (cursor changes to pointer on hover)
- [ ] Clicking each card navigates to correct screen
- [ ] KPI variables are initialized in HomeScreen.OnVisible
- [ ] No calculation errors appear in formula bar
- [ ] Cards align properly in 4-column layout
- [ ] All text is readable and properly aligned
- [ ] Placeholder values display correctly
- [ ] App saves without errors

---

## Phase 1.6 Completion Checklist

### Task 1.6.1: Canvas PowerApp Creation
- [ ] App successfully created with correct name
- [ ] Tablet layout (1366x768) configured
- [ ] Phone layout enabled and accessible
- [ ] Portrait orientation set
- [ ] Scale to fit and snap to grid enabled

### Task 1.6.2: Data Connections
- [ ] All 10 SharePoint lists connected
- [ ] No connection errors in Data panel
- [ ] Test gallery successfully displays data
- [ ] All lists show correct record counts
- [ ] Connection persists after app reload

### Task 1.6.3: Colour Theme
- [ ] All 11 colour variables initialized
- [ ] Colours match REdI design standards
- [ ] App.OnStart executes without errors
- [ ] Variables verified in Power Apps Monitor
- [ ] Canvas background displays correct colour

### Task 1.6.4: Navigation Component
- [ ] Header displays across full width
- [ ] Logo/REdI branding visible
- [ ] App title displays correctly
- [ ] 5 navigation menu items visible
- [ ] Current user name displays
- [ ] Menu items navigate to correct screens
- [ ] Header fixed position (ZIndex = 100)

### Task 1.6.5: Home Screen Layout
- [ ] HomeScreen created successfully
- [ ] Navigation header duplicated on screen
- [ ] KPI cards section displays
- [ ] 4 KPI cards in horizontal row
- [ ] "This Week's Audits" gallery displays
- [ ] "Recent Issues" gallery displays
- [ ] Quick action buttons display at bottom
- [ ] No overlapping components

### Task 1.6.6: KPI Placeholders
- [ ] Card 1: Audit Completion Rate (89%)
- [ ] Card 2: Open Issues (12)
- [ ] Card 3: Overdue Audits (3)
- [ ] Card 4: Avg Compliance (87%)
- [ ] All KPI values have correct colours
- [ ] Cards are interactive (clickable)
- [ ] KPI variables initialized in OnVisible
- [ ] All formulas calculate without errors

### General Quality Checks
- [ ] App name documented: REdI_Trolley_Audit_App
- [ ] All screens accessible from navigation
- [ ] No hardcoded colours (all use variables)
- [ ] No console errors or warnings
- [ ] App saves and publishes successfully
- [ ] App accessible to intended users

---

## Common Issues and Troubleshooting

### Issue: SharePoint Lists Not Appearing in Data Panel

**Symptoms:** Cannot see SharePoint lists in Data panel after connection

**Solutions:**
1. Verify you're connected to correct SharePoint site
2. Check user permissions on SharePoint site (must be at least Contributor)
3. Refresh the Data panel: Close and reopen Power Apps Studio
4. Verify lists were created in SharePoint (not just in project list)
5. Try removing and re-adding the SharePoint connection

### Issue: Colour Variables Not Applying to Controls

**Symptoms:** Components don't display assigned colours

**Solutions:**
1. Verify App.OnStart executes (check Power Apps Monitor)
2. Ensure formula uses exact variable name (case-sensitive in some cases)
3. Check that formula is in **Fill** property, not **Visible** or other properties
4. Restart the app (F5 or Reload)
5. Clear Power Apps cache (Settings → Clear app data)

### Issue: Navigation Menu Not Working

**Symptoms:** Clicking menu items doesn't navigate

**Solutions:**
1. Verify target screens exist (HomeScreen, TrolleysScreen, etc.)
2. Check screen names match exactly in Navigate formula
3. Verify OnSelect event is on correct control
4. Check that screens are enabled (not hidden)
5. Test with simpler navigation first: `Navigate(HomeScreen)`

### Issue: KPI Cards Not Displaying Values

**Symptoms:** Cards show blank or error values

**Solutions:**
1. Check variable initialization in OnVisible event
2. Verify formula syntax in label's Text property
3. Check for circular references in formulas
4. Use Power Apps Monitor to debug variable values
5. Simplify formula temporarily to test: `Set(varTest, "Test")`

### Issue: App Performance Slow or Unresponsive

**Symptoms:** App takes long time to load or responds slowly

**Solutions:**
1. Reduce number of rows loaded in galleries: Use `FirstN(List, 20)`
2. Defer data load: Load data only when needed, not on app startup
3. Minimize collection updates: Use filters instead of multiple collections
4. Check for circular formula references
5. Close other Power Apps tabs
6. Clear browser cache

---

## Next Steps

After completing Phase 1.6, proceed with:

### Phase 2.1: Trolley Management Screens (Tasks 2.1.1-2.1.18)
- Create Trolley List screen with filtering and sorting
- Build Trolley Detail screen with view/edit modes
- Implement trolley creation and deactivation workflows

### Phase 2.3: Audit Entry Screens (Tasks 2.3.1-2.3.22)
- Build audit selection screen
- Create documentation check screen
- Implement condition and equipment check screens

### Phase 2.5: Audit Submission (Tasks 2.5.1-2.5.15)
- Build review screen with compliance calculations
- Create submission and draft save flows

---

## Support and Reference

### Key Contacts

- **Power Apps Documentation:** https://docs.microsoft.com/power-apps/
- **SharePoint REST API:** https://docs.microsoft.com/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service
- **Power Automate:** https://docs.microsoft.com/power-automate/

### Related Documentation

- REdI Trolley Audit Task List: `RBWH_Trolley_Audit_Task_List.md`
- REdI Data Schema: `RBWH_Resuscitation_Trolley_Audit_Schema.md`
- SharePoint List Schemas: `sharepoint_schemas/` directory

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Documentation Team | Initial implementation guide |

---

**Document prepared for:** Royal Brisbane and Women's Hospital - MERT Program
**Document classification:** Internal - Implementation Guide
**Last updated:** January 2026
