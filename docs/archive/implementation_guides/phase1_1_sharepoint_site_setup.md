# REdI Trolley Audit System
## Phase 1.1 SharePoint Site Setup Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 1.1.1 - 1.1.4

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Prerequisites](#prerequisites)
3. [Task 1.1.1: Create SharePoint Site](#task-111-create-sharepoint-site)
4. [Task 1.1.2: Configure Site Permissions](#task-112-configure-site-permissions)
5. [Task 1.1.3: Create Site Navigation](#task-113-create-site-navigation)
6. [Task 1.1.4: Configure Site Branding](#task-114-configure-site-branding)
7. [Verification Checklist](#verification-checklist)
8. [Troubleshooting](#troubleshooting)

---

## Executive Summary

This guide provides step-by-step instructions for setting up the SharePoint Online site infrastructure for the REdI Trolley Audit system. Phase 1.1 establishes the foundation upon which all audit data lists, PowerApp, and reporting will be built.

### What You'll Complete

| Task | Objective | Time | Dependency |
|------|-----------|------|-----------|
| 1.1.1 | Provision SharePoint site with standard settings | 1 hour | None |
| 1.1.2 | Configure role-based access control (RBAC) | 2 hours | 1.1.1 |
| 1.1.3 | Build navigation structure for key lists | 1 hour | 1.1.1 |
| 1.1.4 | Apply REdI branding elements | 1 hour | 1.1.1 |

**Total Duration:** Approximately 5 hours of implementation work

### Site Overview

By the end of Phase 1.1, you will have:
- **Provisioned site:** REdI Trolley Audit
- **User groups:** Owners, Members, Visitors
- **Navigation menu:** Home, Trolley Locations, Equipment, Audits, Issues, Reports
- **Branding:** REdI colour scheme applied
- **Ready for:** Phase 1.2 (Reference Data Lists)

---

## Prerequisites

### Required Access & Permissions

- **Office 365 Admin Access** - To approve new site creation
- **SharePoint Administrator** - To configure site permissions and branding
- **Microsoft 365 tenant** - With SharePoint Online capability
- **Power Platform environment** - Configured for this organization

### Required Information

Before starting, gather:

1. **Organizational Details**
   - Organization name: Resuscitation EDucation Initiative (REdI)
   - Department contact: REdI Team, Workforce Development & Education Unit
   - Approval manager name and email

2. **Branding Assets**
   - Organisation logo (PNG/SVG, max 500KB)
   - Colour codes:
     - REdI Navy: #1B3A5F (Headers, primary text, backgrounds)
     - REdI Teal: #2B9E9E (Accents, interactive elements)
     - REdI Coral: #E55B64 (Primary brand, highlights)
     - Text colour: #333333 (Dark grey)

3. **User Groups** (collect from your IT contact)
   - MERT Educators email list (for Owners)
   - NUM/Ward Managers email list (for Members)
   - Clinical Staff email list (for Visitors - read-only)

### Microsoft 365 Service Requirements

- SharePoint Online (included in most enterprise licenses)
- Power Automate (included in most enterprise licenses)
- Power Apps (included in most enterprise licenses)
- Office 365 Groups
- Exchange Online (for mail notifications)

---

# Task 1.1.1: Create SharePoint Site

## Objective
Provision a new SharePoint Team Site named "REdI Trolley Audit" with appropriate storage, features, and initial configuration.

## Step-by-Step Instructions

### Step 1: Access SharePoint Admin Center

**Action:** Navigate to SharePoint Admin Center

```
1. Go to https://yourtenant-admin.sharepoint.com
2. Sign in with your Microsoft 365 admin account
3. From the left sidebar, click "Sites" > "Active Sites"
```

**Expected Result:** You see a list of existing SharePoint sites

**Screenshot Placeholder:** [Admin Center - Active Sites View]

---

### Step 2: Create New Site

**Action:** Initiate site creation

```
1. Click the "+ Create" button at the top
2. Select "Team Site"
3. Choose "Create modern site"
```

**Screenshot Placeholder:** [Create Site Dialog - Template Selection]

---

### Step 3: Configure Site Information

**Action:** Enter site details

**Form Fields to Complete:**

| Field | Value | Required |
|-------|-------|----------|
| **Site Name** | REdI Trolley Audit | Yes |
| **Site Description** | Resuscitation trolley audit system for Royal Brisbane and Women's Hospital | No |
| **Site Address (URL)** | /sites/REdITrolleyAudit | Yes |
| **Classification** | Internal | Yes |
| **Time Zone** | (UTC+10:00) Brisbane | Yes |
| **Language** | English | Yes |
| **Owner Email** | [MERT Lead educator email] | Yes |

**Example Completion:**

```
Site Name: REdI Trolley Audit
Site Address: REdITrolleyAudit
Owner: mert.lead@rbwh.qld.gov.au
Time Zone: (UTC+10:00) Brisbane
Language: English
```

**Screenshot Placeholder:** [Site Configuration Form - All Fields Populated]

---

### Step 4: Advanced Settings

**Action:** Configure storage and additional options

**Required Settings:**

| Setting | Configuration | Reason |
|---------|---------------|--------|
| **Storage Quota** | 100 GB | Adequate for audit records, documents, and historical data |
| **Allow external sharing** | Only with verified external users | Security compliance |
| **Default Sharing Link Type** | Internal | Restrict to REdI users only |
| **Team Site Default Privacy** | Private | Controlled access via groups |

**Steps:**

```
1. Under "Advanced Settings" section
2. Set Storage quota: 100 GB (slider or text input)
3. External sharing: "Only with verified external users"
4. Default sharing: "Internal"
5. Leave all other settings at default
```

**Screenshot Placeholder:** [Advanced Settings Configuration]

---

### Step 5: Review & Create

**Action:** Verify all settings and create site

**Pre-Creation Checklist:**

- [ ] Site name: "REdI Trolley Audit"
- [ ] URL is clean: REdITrolleyAudit (no spaces/special characters)
- [ ] Owner email is valid and belongs to MERT educator
- [ ] Time zone: Brisbane (UTC+10:00)
- [ ] Language: English
- [ ] Storage: 100 GB
- [ ] Sharing set to Internal

**Steps:**

```
1. Review all entered information
2. Click "Create"
3. Wait 2-5 minutes for site provisioning
```

**Expected Result:**
- Confirmation message appears
- Site appears in Active Sites list
- Site can be accessed via URL: https://yourtenant.sharepoint.com/sites/REdITrolleyAudit

**Screenshot Placeholder:** [Site Creation Confirmation]

---

### Step 6: Verify Site Creation

**Action:** Access and verify the new site

**Steps:**

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Wait for initial site rendering (may take a few seconds)
3. Verify you can:
   - Access the home page
   - See the site name in the header
   - Access site settings (gear icon > Site Settings)
```

**Verification Points:**

- [ ] Site loads without errors
- [ ] Site URL is correct: /sites/REdITrolleyAudit
- [ ] Site name displays as "REdI Trolley Audit"
- [ ] Home page has placeholder content
- [ ] Navigation is visible

**Screenshot Placeholder:** [Newly Created Site - Home Page]

---

### Step 7: Enable Required Site Features

**Action:** Activate necessary SharePoint features

**Steps:**

```
1. From site home page, click gear icon (Settings)
2. Select "Site Settings"
3. Go to "Site collection features"
4. Verify these are ENABLED:
   - SharePoint Server Publishing Infrastructure
   - Search Results Web Part
   - Power Apps Support
```

**Expected Result:** All required features are active

**Screenshot Placeholder:** [Site Features List]

---

## Configuration Summary for Task 1.1.1

| Item | Value | Status |
|------|-------|--------|
| Site Name | REdI Trolley Audit | ✓ Created |
| Site URL | /sites/REdITrolleyAudit | ✓ Created |
| Owner | [MERT Lead] | ✓ Set |
| Storage | 100 GB | ✓ Configured |
| Time Zone | Brisbane (UTC+10:00) | ✓ Set |
| Language | English | ✓ Set |
| External Sharing | Only verified external users | ✓ Configured |

**Next Step:** Proceed to Task 1.1.2 (Configure Site Permissions)

---

# Task 1.1.2: Configure Site Permissions

## Objective
Establish role-based access control with three permission levels: Owners (MERT Educators), Members (NUM/Ward Managers), and Visitors (Auditors - read-only).

## Overview

This task creates three Office 365 Groups that will control access to the SharePoint site and all its lists. Permissions will be assigned at both the site and list levels.

### Permission Model

```
┌─────────────────────────────────────────────────────────────┐
│                    REdI Trolley Audit Site                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │ OWNERS (MERT)   │  │ MEMBERS (NUMs)   │  │ VISITORS   │ │
│  │                 │  │                  │  │ (Auditors) │ │
│  │ Full Control    │  │ Contribute       │  │ Read Only  │ │
│  │ - Create lists  │  │ - Edit audits    │  │ - View    │ │
│  │ - Manage perms  │  │ - Log issues     │  │ - Reports │ │
│  │ - Settings      │  │ - View items     │  │           │ │
│  └─────────────────┘  └──────────────────┘  └────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Step-by-Step Instructions

### Step 1: Navigate to Site Permissions

**Action:** Access SharePoint Site Settings

**Steps:**

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Click gear icon (Settings) top right
3. Select "Site Settings"
4. Under "Users and Permissions" section, click "Site permissions"
```

**Expected Result:** You see current permission groups and sharing settings

**Screenshot Placeholder:** [Site Settings - Permissions Section]

---

### Step 2: Create MERT Educators Owner Group

**Action:** Create first permission group for site owners

**Steps:**

```
1. From "Site permissions" page, click "Grant permissions" or "+ New Group"
2. Select "Create a new group"
3. Fill in group details:
   - Name: REdI Trolley Audit - Owners
   - Description: MERT Educators with full site control
   - Permission Level: Full Control
4. Add members:
   - Search for each MERT educator by email
   - Click "Add" for each person
```

**Group Details:**

| Property | Value |
|----------|-------|
| **Name** | REdI Trolley Audit - Owners |
| **Email** | rbwhtrolleyaudit-owners@yourtenant.onmicrosoft.com |
| **Permission Level** | Full Control |
| **Members** | [List of MERT educators] |

**Members to Add:**
```
- Primary MERT Educator
- Secondary MERT Educator
- MERT Coordinator (if applicable)
- IT Support contact (optional)

Note: Get exact email addresses from your IT contact
```

**Screenshot Placeholder:** [Create New Group Dialog - Owners]

---

### Step 3: Create NUM/Ward Managers Member Group

**Action:** Create second permission group for site members

**Steps:**

```
1. Click "+ New Group" again
2. Fill in group details:
   - Name: REdI Trolley Audit - Members
   - Description: NUM and Ward Managers - can edit audits and manage issues
   - Permission Level: Contribute
3. Add members:
   - Search for each NUM by email
   - Search for each Ward Manager by email
   - Click "Add" for each person
```

**Group Details:**

| Property | Value |
|----------|-------|
| **Name** | REdI Trolley Audit - Members |
| **Email** | rbwhtrolleyaudit-members@yourtenant.onmicrosoft.com |
| **Permission Level** | Contribute |
| **Members** | [List of NUMs and Ward Managers] |

**Typical Members:**
```
- NUM 7A North
- NUM 8A South
- NUM 9B West
- NUM CCU
- NUM ICU
- Ward Managers (x12-15)

Note: Get email list from your Nursing Leadership contact
```

**Permission Details - Contribute Level:**

| Action | Allowed |
|--------|---------|
| View site content | ✓ |
| Add/Edit items | ✓ |
| Delete own items | ✓ |
| Create lists | ✗ |
| Delete lists | ✗ |
| Change site permissions | ✗ |

**Screenshot Placeholder:** [Create New Group Dialog - Members]

---

### Step 4: Create Auditors Visitor Group

**Action:** Create third permission group for read-only access

**Steps:**

```
1. Click "+ New Group" again
2. Fill in group details:
   - Name: REdI Trolley Audit - Visitors
   - Description: Clinical staff - Auditors and assessors (read-only access)
   - Permission Level: Read
3. Add members:
   - Search for each clinical auditor by email
   - Search for clinical staff who need report access
   - Click "Add" for each person
```

**Group Details:**

| Property | Value |
|----------|-------|
| **Name** | REdI Trolley Audit - Visitors |
| **Email** | rbwhtrolleyaudit-visitors@yourtenant.onmicrosoft.com |
| **Permission Level** | Read |
| **Members** | [List of clinical auditors/staff] |

**Typical Members:**
```
- Clinical nurses (multiple wards)
- Doctors who conduct audits
- Pharmacy staff (if viewing reports)
- Allied health (if required)

Note: Can add ~50-100 users. Start with core group.
```

**Permission Details - Read Level:**

| Action | Allowed |
|--------|---------|
| View site content | ✓ |
| View items | ✓ |
| Download reports | ✓ |
| Add/Edit items | ✗ |
| Delete items | ✗ |
| Create lists | ✗ |

**Screenshot Placeholder:** [Create New Group Dialog - Visitors]

---

### Step 5: Verify All Groups Created

**Action:** Confirm all three groups are visible

**Steps:**

```
1. From Site Settings > Site Permissions
2. Look for "Quick Launch" or group list showing:
   - REdI Trolley Audit - Owners
   - REdI Trolley Audit - Members
   - REdI Trolley Audit - Visitors
3. Click each group to verify member count
```

**Verification Points:**

- [ ] Owners group created with Full Control
- [ ] Members group created with Contribute
- [ ] Visitors group created with Read
- [ ] All groups visible in Site Settings
- [ ] All members added to respective groups

**Screenshot Placeholder:** [All Groups Visible in Site Settings]

---

### Step 6: Configure List-Level Permissions

**Action:** Set up specific list permissions for future lists

**Background:** When Phase 1.2 lists are created, they will inherit site permissions. However, some specialized lists may need additional restrictions.

**Steps:**

```
1. Create a reference document noting:
   - Lists that use default site permissions: Most (inherited)
   - Lists with custom permissions: None initially

2. Document for Phase 1.2:
   "All Phase 1.2 reference data lists (ServiceLine,
    EquipmentCategory, AuditPeriod) inherit site
    permissions with no additional restrictions."
```

**Screenshot Placeholder:** [List Permissions Settings - Ready for Phase 1.2]

---

### Step 7: Test Permissions

**Action:** Verify permission groups work correctly

**Testing Steps:**

```
1. Log out and log in as MERT educator (Owners group)
   - Verify can access site settings
   - Verify can create lists

2. Log out and log in as NUM (Members group)
   - Verify can access site
   - Verify cannot access site settings
   - Verify can view content

3. Log out and log in as clinical auditor (Visitors group)
   - Verify can access site
   - Verify can view reports (when available)
   - Verify cannot edit items
   - Verify cannot access settings
```

**Expected Results:**

| User Role | Site Access | List Edit | Settings | Create Lists |
|-----------|-------------|-----------|----------|--------------|
| MERT (Owner) | ✓ | ✓ | ✓ | ✓ |
| NUM (Member) | ✓ | ✓ | ✗ | ✗ |
| Auditor (Visitor) | ✓ | ✗ | ✗ | ✗ |

**Screenshot Placeholder:** [Testing - Member User Attempting Edit]

---

## Configuration Summary for Task 1.1.2

| Group Name | Permission Level | Members | Status |
|-----------|-----------------|---------|--------|
| REdI Trolley Audit - Owners | Full Control | [Count: _] | ✓ Created |
| REdI Trolley Audit - Members | Contribute | [Count: _] | ✓ Created |
| REdI Trolley Audit - Visitors | Read | [Count: _] | ✓ Created |

**Documentation to Save:**

Create a file named `site_permissions_audit.txt` documenting:

```
Site: REdI Trolley Audit
Created: [Date]
Groups created: 3
Total users: [Count]

Group 1: REdI Trolley Audit - Owners
- Email: rbwhtrolleyaudit-owners@yourtenant.onmicrosoft.com
- Members: [List names]

Group 2: REdI Trolley Audit - Members
- Email: rbwhtrolleyaudit-members@yourtenant.onmicrosoft.com
- Members: [List names]

Group 3: REdI Trolley Audit - Visitors
- Email: rbwhtrolleyaudit-visitors@yourtenant.onmicrosoft.com
- Members: [List names]

Permission testing completed: [Date]
All groups verified: [Yes/No]
```

**Next Step:** Proceed to Task 1.1.3 (Create Site Navigation)

---

# Task 1.1.3: Create Site Navigation

## Objective
Build a clear, intuitive site navigation structure that guides users to key lists and features.

## Navigation Strategy

The site will use a hierarchical menu structure adapted to mobile and desktop views:

```
Home (Site Home)
├── Trolley Locations (Audit Resources)
│   ├── Equipment Master List
│   └── Service Lines
├── Audits (Audit Management)
│   ├── Run Audit
│   └── Audit History
├── Issues (Issue Management)
│   ├── Open Issues
│   └── Issue Reports
└── Reports (Reporting)
    ├── Compliance Dashboard
    └── Audit Reports
```

## Step-by-Step Instructions

### Step 1: Access Site Navigation Settings

**Action:** Navigate to site navigation configuration

**Steps:**

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Click gear icon (Settings)
3. Select "Edit site information"
4. Look for "Appearance" or "Navigation" section
5. Or use: Site Settings > Navigation Elements
```

**Expected Result:** Site navigation settings appear

**Screenshot Placeholder:** [Navigation Settings Interface]

---

### Step 2: Configure Header Navigation

**Action:** Set up top navigation bar

**Navigation Items to Create:**

| Menu Item | Target | Icon | Display |
|-----------|--------|------|---------|
| Home | Site Home | Home | Always |
| Trolley Locations | [Link to location data] | Map | Show |
| Equipment | Equipment list | Box | Show |
| Audits | Audit list | Clipboard | Show |
| Issues | Issues list | Alert | Show |
| Reports | Reports library | Report | Show |

**Steps:**

```
1. Under "Navigation" section, click "Edit Navigation"
2. Add items in order (or use drag-drop if available):

   Item 1 - Trolley Locations
   - Title: Trolley Locations
   - Type: Link
   - URL: /sites/REdITrolleyAudit/Lists/Location
   - Display: In menu

   Item 2 - Equipment
   - Title: Equipment
   - Type: Link
   - URL: /sites/REdITrolleyAudit/Lists/Equipment
   - Display: In menu

   Item 3 - Audits
   - Title: Audits
   - Type: Link
   - URL: /sites/REdITrolleyAudit/Lists/Audit
   - Display: In menu

   Item 4 - Issues
   - Title: Issues
   - Type: Link
   - URL: /sites/REdITrolleyAudit/Lists/Issue
   - Display: In menu

   Item 5 - Reports
   - Title: Reports
   - Type: Link
   - URL: [To be completed in Phase 3]
   - Display: In menu
```

**Note:** List URLs will be available after Phase 1.2-1.5 list creation. For now, create the navigation structure.

**Screenshot Placeholder:** [Navigation Items Configuration]

---

### Step 3: Set Home Page Navigation

**Action:** Configure home page quick links

**Steps:**

```
1. Go to Site Home page
2. Edit the home page (if in edit mode)
3. Add "Quick Links" web part
4. Configure quick link buttons:
```

**Quick Links Web Part Configuration:**

```
Link 1:
- Title: Run Audit
- Icon: Clipboard
- Description: Start a new trolley audit
- URL: [PowerApp or form URL - Phase 1.6]

Link 2:
- Title: View Locations
- Icon: Map Pin
- Description: Browse all trolley locations
- URL: /sites/REdITrolleyAudit/Lists/Location

Link 3:
- Title: Manage Issues
- Icon: Alert
- Description: View and manage open issues
- URL: /sites/REdITrolleyAudit/Lists/Issue

Link 4:
- Title: Audit Reports
- Icon: Chart
- Description: View compliance reports
- URL: [Reports URL - Phase 3]

Link 5:
- Title: Equipment Master
- Icon: Package
- Description: View all equipment items
- URL: /sites/REdITrolleyAudit/Lists/Equipment
```

**Screenshot Placeholder:** [Home Page with Quick Links]

---

### Step 4: Create Navigation Breadcrumb

**Action:** Set up breadcrumb for list pages

**Note:** SharePoint Modern sites automatically show breadcrumbs. Verify:

```
1. Navigate to each list page (will exist after Phase 1.2)
2. Verify breadcrumb shows:
   Home > [Site Name] > [List Name]
3. Breadcrumb items should be clickable
```

**Expected Result:** Breadcrumb appears on all list pages

**Screenshot Placeholder:** [List Page Breadcrumb Example]

---

### Step 5: Configure Mobile Navigation

**Action:** Ensure navigation works on mobile devices

**Steps:**

```
1. Test on mobile device or use browser mobile emulator:
   - Press F12 (Developer Tools)
   - Click device toggle (phone icon)
   - Select iPhone or Android device

2. Verify:
   - Hamburger menu appears on mobile
   - All navigation items are accessible
   - Menu is readable on small screen
   - No horizontal scrolling required

3. Test all navigation links on mobile
   - Should not get "page not found"
   - Should load correctly on mobile
```

**Mobile Navigation Best Practices:**

- [ ] Hamburger menu implemented for small screens
- [ ] Touch targets are at least 44x44 pixels
- [ ] No horizontal scrolling required
- [ ] All links open correctly
- [ ] Forms are mobile-friendly

**Screenshot Placeholder:** [Mobile Navigation - Hamburger Menu]

---

### Step 6: Create Navigation Documentation

**Action:** Document the navigation structure

**Create File:** `site_navigation_guide.md`

```markdown
# REdI Trolley Audit Site Navigation Guide

## Main Navigation Structure

### Top Menu Bar
1. **Home** - Dashboard and system overview
2. **Trolley Locations** - Manage and view trolley locations
3. **Equipment** - Master equipment list
4. **Audits** - Conduct and view audits
5. **Issues** - Track and manage issues
6. **Reports** - View compliance reports

### Home Page Quick Links
- Run Audit - Start a new audit
- View Locations - Browse trolleys
- Manage Issues - View open issues
- Audit Reports - View reports
- Equipment Master - View equipment

### List URLs
- Home: /sites/REdITrolleyAudit
- Locations: /sites/REdITrolleyAudit/Lists/Location
- Equipment: /sites/REdITrolleyAudit/Lists/Equipment
- Audits: /sites/REdITrolleyAudit/Lists/Audit
- Issues: /sites/REdITrolleyAudit/Lists/Issue
- Reports: [Phase 3]

### User Access by Role
- **MERT Educators**: Full access to all navigation items
- **NUMs/Managers**: Access to all items, no settings
- **Auditors**: Access to Audit, Issues, Reports; read-only others

```

**Screenshot Placeholder:** [Documentation File Created]

---

## Configuration Summary for Task 1.1.3

| Item | Configuration | Status |
|------|---------------|--------|
| Top Navigation Menu | 5 main items configured | ✓ Ready |
| Quick Links | 5 quick action links | ✓ Ready |
| Breadcrumb Navigation | Automatic (SharePoint) | ✓ Working |
| Mobile Navigation | Hamburger menu tested | ✓ Working |
| Documentation | Navigation guide created | ✓ Complete |

**Pending Items (Complete in Later Phases):**

- [ ] Phase 1.2: Update navigation links to actual list URLs
- [ ] Phase 1.6: Add Run Audit link to PowerApp
- [ ] Phase 3: Add Reports link to Power BI

**Next Step:** Proceed to Task 1.1.4 (Configure Site Branding)

---

# Task 1.1.4: Configure Site Branding

## Objective
Apply REdI (Resuscitation EDucation Initiative) branding to the SharePoint site, including colours, logo, and theme.

## Branding Specifications

### Colour Scheme

**REdI Brand Colours:**

```
REdI Navy:          #1B3A5F
                    RGB(27, 58, 95)
                    Used for: Headers, primary text, backgrounds

REdI Coral:         #E55B64
                    RGB(229, 91, 100)
                    Used for: Primary brand, highlights, buttons

REdI Teal:          #2B9E9E
                    RGB(43, 158, 158)
                    Used for: Accents, interactive elements

Dark Grey:          #333333
                    RGB(51, 51, 51)
                    Used for: Body text, borders

Light Grey:         #F5F5F5
                    RGB(245, 245, 245)
                    Used for: Backgrounds

White:              #FFFFFF
                    Used for: Page backgrounds
```

**Visual Reference:**

```
┌─────────────────────────────────────┐
│ ■ #1B3A5F REdI Navy                 │
│ ■ #E55B64 REdI Coral                │
│ ■ #2B9E9E REdI Teal                 │
│ ■ #333333 Dark Grey (Text)          │
│ ■ #F5F5F5 Light Grey (Background)   │
│ ■ #FFFFFF White                     │
└─────────────────────────────────────┘
```

### Logo Requirements

**Size & Format:**
- Recommended size: 200x50 pixels (4:1 ratio)
- Format: SVG preferred, PNG with transparent background
- Maximum file size: 500 KB
- File name: redi-logo-primary-rgb.svg (or redi-logo-primary-rgb.png)
- Minimum digital size: 100px width

---

## Step-by-Step Instructions

### Step 1: Access Site Branding Settings

**Action:** Navigate to theme and branding configuration

**Steps:**

```
1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Click gear icon (Settings) top right
3. Select "Site Settings"
4. Under "Design" or "Site Appearance" section:
   - Click "Change the look" or "Theme"
5. If not visible, try:
   - Settings > Appearance > Theme
```

**Expected Result:** Theme selection interface appears

**Screenshot Placeholder:** [Site Settings - Theme Options]

---

### Step 2: Upload Organization Logo

**Action:** Upload REdI logo to site

**Steps:**

```
1. From Theme settings, locate "Site Logo" section
2. Click "Upload new logo"
3. Browse and select: redi-logo-primary-rgb.svg (or .png)
4. Verify logo displays correctly
5. Adjust positioning if needed:
   - Top left (typical)
   - Logo should align with header
   - Maintain clear space equal to height of "E" on all sides
```

**Logo Specifications Checklist:**

- [ ] File: redi-logo-primary-rgb.svg or redi-logo-primary-rgb.png
- [ ] Size: 200x50 pixels minimum (or similar 4:1 ratio)
- [ ] Background: Transparent
- [ ] Clarity: Readable at 32 pixel height (100px minimum width)
- [ ] File size: < 500 KB

**Screenshot Placeholder:** [Logo Upload - Position Preview]

---

### Step 3: Select or Create Theme

**Action:** Configure site colour theme

**Option A: Use Built-in Theme (Quickest)**

```
1. If "Theme" page is shown:
2. Look for a dark blue or navy theme
3. Click to preview
4. Modify theme colours to REdI palette:
   - Primary: #1B3A5F (REdI Navy)
   - Accent: #E55B64 (REdI Coral)
   - Secondary: #2B9E9E (REdI Teal)
   - Text: #333333
```

**Option B: Create Custom Theme (Recommended)**

**Steps:**

```
1. From Theme settings, click "Create custom theme"
   or "+ New Theme"

2. Theme Name: REdI Trolley Audit

3. Configure Colours:
```

**Colour Configuration:**

| Theme Element | Hex Code | RGB | Notes |
|---------------|----------|-----|-------|
| Primary (Dominant colour) | #1B3A5F | 27,58,95 | REdI Navy |
| Secondary (Accent) | #E55B64 | 229,91,100 | REdI Coral - primary brand |
| Tertiary (Interactive) | #2B9E9E | 43,158,158 | REdI Teal - accents |
| Text (Neutral dark) | #333333 | 51,51,51 | Dark grey for readability |
| Background | #FFFFFF | 255,255,255 | White page background |
| Neutral (Light) | #F5F5F5 | 245,245,245 | Light grey for sections |

**Steps to Configure Each Colour:**

```
1. Click "Primary Colour"
   - Enter: #1B3A5F (REdI Navy)
   - Click OK/Apply

2. Click "Secondary Colour" or "Accent"
   - Enter: #E55B64 (REdI Coral)
   - Click OK/Apply

3. Click "Text Colour"
   - Enter: #333333
   - Click OK/Apply

4. Leave Navigation colour as default (will use primary)

5. Click "Create" or "Save Theme"
```

**Screenshot Placeholder:** [Custom Theme Configuration - All Colours Set]

---

### Step 4: Configure Header Styling

**Action:** Customize header layout and appearance

**Steps:**

```
1. From Site Settings, find "Header" or "Logo"
2. Configure:
   - Logo alignment: Left
   - Header style: Minimal (removes redundant info)
   - Site title position: Below logo
   - Site title: REdI Trolley Audit
```

**Header Configuration Checklist:**

- [ ] Logo displays in top left
- [ ] Site title reads "REdI Trolley Audit"
- [ ] Header background uses REdI Navy (#1B3A5F)
- [ ] Search bar is visible
- [ ] No horizontal scrolling

**Screenshot Placeholder:** [Header Configuration - Logo and Title Positioned]

---

### Step 5: Apply Theme to Site

**Action:** Activate the theme across the entire site

**Steps:**

```
1. From Theme settings, confirm your custom theme
2. Click "Apply" or "Save and Apply"
3. Wait 30-60 seconds for theme to apply
4. Refresh the page (Ctrl+F5 or Cmd+Shift+R)
5. Verify changes appear across site
```

**Expected Results After Application:**

- [ ] Header background is REdI Navy (#1B3A5F)
- [ ] Buttons show REdI Coral (#E55B64) on hover
- [ ] Text is dark grey (#333333)
- [ ] Logo visible in top left
- [ ] Site title shows "REdI Trolley Audit"

**Screenshot Placeholder:** [Site After Theme Applied - Header with Branding]

---

### Step 6: Configure Footer

**Action:** Add organization footer with contact information

**Steps:**

```
1. Go to Site Settings > "Footer" or "Custom Footer"
2. Add footer content:

Footer Text:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Resuscitation EDucation Initiative (REdI)
Workforce Development & Education Unit
Royal Brisbane & Women's Hospital

For support: redi@health.qld.gov.au
Last updated: [System-generated date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. Click Save
```

**Footer Configuration:**

| Setting | Value |
|---------|-------|
| Background colour | #F5F5F5 (Light grey) |
| Text colour | #333333 (Dark grey) |
| Font size | 12px |
| Content | Contact info + REdI details |
| Display | On all pages |

**Screenshot Placeholder:** [Site Footer Configuration]

---

### Step 7: Test Branding Across All Pages

**Action:** Verify branding appears correctly throughout site

**Testing Pages:**

```
1. Home Page
   - Logo visible? ✓
   - Header blue? ✓
   - Theme applied? ✓

2. When lists are created (Phase 1.2+):
   - Test on ServiceLine list page
   - Test on Equipment list page
   - Test on Location list page

3. Mobile View
   - Hamburger menu visible? ✓
   - Logo responsive? ✓
   - Colours correct on mobile? ✓

4. Different Browsers
   - Chrome
   - Edge
   - Safari (if available)
```

**Cross-Browser Testing Checklist:**

| Browser | Logo OK | Colours OK | Mobile OK |
|---------|---------|-----------|-----------|
| Chrome | ✓ | ✓ | ✓ |
| Edge | ✓ | ✓ | ✓ |
| Safari | ✓ | ✓ | ✓ |
| Firefox | ✓ | ✓ | ✓ |

**Screenshot Placeholder:** [Site Home - Full Branding Applied]

---

### Step 8: Document Branding Configuration

**Action:** Save branding specifications for future reference

**Create File:** `branding_configuration.txt`

```
REdI Trolley Audit Site - Branding Configuration
=================================================

Site: REdI Trolley Audit
URL: /sites/REdITrolleyAudit
Date Configured: [Date]
Configured By: [Your Name]

COLOUR SCHEME (REdI Brand Guidelines v1.0)
──────────────────────────────────────────
REdI Navy:          #1B3A5F (RGB 27, 58, 95)
REdI Coral:         #E55B64 (RGB 229, 91, 100)
REdI Teal:          #2B9E9E (RGB 43, 158, 158)
Text Dark:          #333333 (RGB 51, 51, 51)
Background Light:   #F5F5F5 (RGB 245, 245, 245)
Background White:   #FFFFFF (RGB 255, 255, 255)

TYPOGRAPHY
──────────
Primary Font: Montserrat (400, 500, 600, 700)
Display Font: Bebas Neue
Fallback: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif

LOGO
────
File: redi-logo-primary-rgb.svg
Size: 200x50 pixels minimum (100px width minimum digital)
Format: SVG preferred, PNG with transparent background
Location: Site header, top left
Status: Uploaded and active

HEADER CONFIGURATION
───────────────────
Site Title: REdI Trolley Audit
Logo Position: Left
Header Style: Minimal
Background: REdI Navy (#1B3A5F)
Search Bar: Enabled

FOOTER CONFIGURATION
───────────────────
Status: Configured
Content: REdI contact details
Background: Light Grey (#F5F5F5)

THEME
─────
Theme Name: REdI Trolley Audit
Type: Custom
Status: Applied to entire site

TESTING RESULTS
───────────────
Desktop: PASS ✓
Mobile: PASS ✓
Cross-browser: PASS ✓
All pages: PASS ✓

NEXT STEPS (Phase 1.2+)
──────────────────────
- Monitor branding consistency across new lists
- Verify theme persists after list creation
- Test branding in PowerApp (Phase 1.6)
- Verify in Power BI reports (Phase 3)
```

**Screenshot Placeholder:** [Configuration Document Saved]

---

## Configuration Summary for Task 1.1.4

| Item | Configuration | Status |
|------|---------------|--------|
| Logo Upload | redi-logo-primary-rgb.svg | ✓ Uploaded |
| Primary Colour | #1B3A5F (REdI Navy) | ✓ Applied |
| Accent Colour | #E55B64 (REdI Coral) | ✓ Applied |
| Interactive Colour | #2B9E9E (REdI Teal) | ✓ Applied |
| Text Colour | #333333 (Dark Grey) | ✓ Applied |
| Header Style | Minimal with logo left | ✓ Configured |
| Footer | REdI contact details | ✓ Configured |
| Theme Name | REdI Trolley Audit | ✓ Created |
| Typography | Montserrat / Bebas Neue | ✓ Applied |
| Cross-browser Testing | All major browsers | ✓ Passed |

---

## Post-Implementation Notes

### Branding Refresh Schedule

Consider these updates during the project:

```
Immediate (Now):         Complete Phase 1.1 branding
Phase 1.6 (PowerApp):    Match app theme to site
Phase 2 (Forms):         Apply theme to issue forms
Phase 3 (Reports):       Apply theme to Power BI
Phase 4 (Training):      Show branding in training videos
```

### Branding Maintenance

To maintain consistency:

1. **Use standard colours** when creating flows and apps
2. **Apply theme** to all new lists/views
3. **Test on mobile** regularly
4. **Document changes** to branding configuration
5. **Annual review** of colour accessibility

### Accessibility Considerations

The chosen colour palette meets:

- ✓ WCAG 2.1 Level AA contrast ratios
- ✓ 4.5:1 text contrast minimum
- ✓ Colour-blind friendly (no pure red/green)
- ✓ Mobile high-contrast mode compatible

---

# Verification Checklist

## Phase 1.1 Completion Verification

Use this comprehensive checklist to verify all Phase 1.1 tasks are complete.

### Task 1.1.1: Create SharePoint Site

**Site Creation**
- [ ] Site name: "REdI Trolley Audit"
- [ ] Site URL: /sites/REdITrolleyAudit
- [ ] Site accessible at: https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
- [ ] Time zone: Brisbane (UTC+10:00)
- [ ] Storage quota: 100 GB
- [ ] Language: English
- [ ] Site features enabled: SharePoint Publishing, Power Apps Support

**Site Access**
- [ ] Site home page loads without errors
- [ ] Navigation works correctly
- [ ] Search functionality available
- [ ] No 404 or access denied errors

---

### Task 1.1.2: Configure Site Permissions

**Group Creation**
- [ ] Group 1: "REdI Trolley Audit - Owners" (Full Control)
- [ ] Group 2: "REdI Trolley Audit - Members" (Contribute)
- [ ] Group 3: "REdI Trolley Audit - Visitors" (Read)

**Member Assignment**
- [ ] MERT educators added to Owners group: ___ members
- [ ] NUMs/Ward Managers added to Members group: ___ members
- [ ] Clinical auditors added to Visitors group: ___ members
- [ ] All members can log in with O365 accounts

**Permission Testing**
- [ ] Owners can access settings ✓
- [ ] Owners can create lists ✓
- [ ] Members can edit items ✓
- [ ] Members cannot access settings ✓
- [ ] Visitors can view items ✓
- [ ] Visitors cannot edit items ✓

**Group Email Addresses**
- [ ] rbwhtrolleyaudit-owners@yourtenant.onmicrosoft.com (Working)
- [ ] rbwhtrolleyaudit-members@yourtenant.onmicrosoft.com (Working)
- [ ] rbwhtrolleyaudit-visitors@yourtenant.onmicrosoft.com (Working)

---

### Task 1.1.3: Create Site Navigation

**Navigation Structure**
- [ ] Home link configured
- [ ] Trolley Locations link configured
- [ ] Equipment link configured
- [ ] Audits link configured
- [ ] Issues link configured
- [ ] Reports link configured

**Quick Links**
- [ ] Run Audit quick link visible on home
- [ ] View Locations quick link visible
- [ ] Manage Issues quick link visible
- [ ] Reports quick link visible
- [ ] Equipment Master quick link visible

**Navigation Functionality**
- [ ] All menu items clickable
- [ ] All links work (or gracefully handle Phase 1.2+ lists)
- [ ] Breadcrumb appears on list pages
- [ ] Mobile hamburger menu works
- [ ] No horizontal scrolling on mobile

**Documentation**
- [ ] Navigation guide document created
- [ ] List URLs documented
- [ ] User access by role documented

---

### Task 1.1.4: Configure Site Branding

**Colours Applied**
- [ ] REdI Navy (#1B3A5F) in header
- [ ] REdI Coral (#E55B64) in buttons/highlights
- [ ] REdI Teal (#2B9E9E) in accents/interactive elements
- [ ] Dark grey (#333333) for text
- [ ] Light grey (#F5F5F5) in backgrounds

**Logo Configuration**
- [ ] REdI logo uploaded
- [ ] Logo visible in header, top left
- [ ] Logo responsive on mobile
- [ ] Logo size appropriate (200x50 or similar, 100px min width)

**Header & Footer**
- [ ] Header shows site title: "REdI Trolley Audit"
- [ ] Header background is REdI Navy
- [ ] Footer displays contact information
- [ ] Footer background is light grey

**Cross-Browser Testing**
- [ ] Chrome: Branding displays correctly ✓
- [ ] Edge: Branding displays correctly ✓
- [ ] Safari: Branding displays correctly ✓
- [ ] Firefox: Branding displays correctly ✓

**Mobile Branding**
- [ ] Logo visible on mobile
- [ ] Colours correct on mobile
- [ ] Theme applies to mobile view
- [ ] No scaling issues

**Documentation**
- [ ] Branding configuration document created
- [ ] Colour codes documented
- [ ] Logo file saved
- [ ] Theme settings recorded

---

## Overall Site Health Check

**Functionality**
- [ ] All features working without errors
- [ ] Site performance acceptable (< 3 seconds load time)
- [ ] No permission-related errors
- [ ] Site renders correctly on all devices

**Security**
- [ ] External sharing: "Only verified external users"
- [ ] Default sharing: "Internal"
- [ ] All groups have appropriate permission levels
- [ ] No over-permissioned users

**Documentation**
- [ ] Site setup procedures documented
- [ ] Permissions documented
- [ ] Navigation documented
- [ ] Branding specifications documented

---

# Troubleshooting

## Common Issues and Solutions

### Issue: Site Creation Fails or Takes Too Long

**Symptoms:**
- Site creation wizard hangs
- Error message appears during creation
- Site doesn't appear in Active Sites list

**Solutions:**

```
1. Check permissions:
   - Verify you have Office 365 admin access
   - Try with a different admin account
   - Check if organization allows site creation

2. Check quotas:
   - Verify organization hasn't hit site quota
   - Check storage not exceeded
   - Try with different storage value (50 GB instead of 100 GB)

3. Try again:
   - Clear browser cache (Ctrl+Shift+Delete)
   - Try in private/incognito window
   - Wait 15 minutes and retry
   - Try different browser

4. Contact support:
   - If issue persists, contact Microsoft 365 admin
   - Provide site name, attempted URL, error messages
```

**Verification:** Site appears in Admin Center > Active Sites and loads correctly

---

### Issue: Permission Groups Not Created or Empty

**Symptoms:**
- Groups don't appear in Site Settings
- Groups appear but no members
- Cannot add members to group
- "User not found" when adding members

**Solutions:**

```
1. Verify user emails:
   - Ensure email addresses are correct
   - Check for typos (common: missing domain)
   - Verify users are in your organization
   - Try email format: firstname.lastname@yourtenant.onmicrosoft.com

2. Check user activation:
   - Verify users have Office 365 licenses assigned
   - Ensure users have accessed portal at least once
   - Check for inactive/blocked accounts

3. Create groups differently:
   - Try creating via Azure AD instead of SharePoint
   - Use Microsoft 365 admin center > Groups
   - Wait 24 hours for group sync

4. Manually add members:
   - Instead of adding during group creation,
     create empty group then add members after
   - Try adding one user at a time
   - Verify each user added successfully

5. Contact IT:
   - If persistent, check with IT department
   - Verify account creation workflow
   - Ensure O365 tenant properly configured
```

**Verification:** All three groups created with correct member counts

---

### Issue: Branding Not Applying or Looks Wrong

**Symptoms:**
- Theme changes don't appear
- Logo not visible
- Colours different than specified
- Mobile branding looks broken

**Solutions:**

```
1. Force refresh:
   - Hard refresh page: Ctrl+Shift+R (or Cmd+Shift+R Mac)
   - Clear browser cache entirely
   - Logout and login again
   - Try in private/incognito window

2. Check logo upload:
   - Verify logo file format: PNG with transparency
   - Check file size: < 500 KB
   - Verify file actually uploaded (check URL)
   - Try re-uploading if file looks corrupted

3. Verify colour codes:
   - Use colour picker to check hex codes
   - Confirm #1B3A5F is REdI Navy (not #005fad)
   - Try one colour at a time
   - Verify browser colour support (hex vs RGB)

4. Check browser compatibility:
   - Try different browser
   - Clear extensions that might override styles
   - Disable dark mode if enabled
   - Test in different device

5. Wait for propagation:
   - Theme changes can take 5-10 minutes
   - Wait and refresh again
   - Check on different device
   - Check at different time
```

**Verification:** Site header shows correct colours, logo visible, consistent on all devices

---

### Issue: Navigation Links Lead to 404 or Blank Pages

**Symptoms:**
- Clicking menu items shows "Page not found"
- Links point to non-existent lists
- Navigation items don't work
- Breadcrumb broken

**Solutions:**

```
1. Wait for Phase 1.2:
   - Lists don't exist yet in Phase 1.1
   - Navigation links will be created in Phase 1.2
   - For now, document the list URLs
   - Update navigation when lists created

2. Verify current navigation:
   - Home link should work: /sites/REdITrolleyAudit
   - Test other existing pages
   - Quick links to future lists are fine (as placeholders)

3. Fix broken links:
   - Replace non-existent URLs with # for now
   - Update all links in Phase 1.2 when lists created
   - Use relative URLs: /sites/REdITrolleyAudit/Lists/[ListName]
   - Test each link after list creation

4. Clear cache:
   - Hard refresh browser
   - Clear CDN cache if applicable
   - Wait for navigation to refresh
```

**Verification:** Home page loads, navigation menu visible, links functional or appropriately marked as "Coming Soon"

---

### Issue: Mobile Menu Doesn't Work

**Symptoms:**
- Hamburger menu not visible on mobile
- Menu doesn't open when tapped
- Mobile layout looks wrong
- Page unreadable on phone

**Solutions:**

```
1. Check mobile view:
   - Press F12 (Developer Tools)
   - Click device toggle (looks like phone)
   - Select "iPhone" or "Android"
   - Rotate device to test portrait/landscape

2. Verify SharePoint Modern experience:
   - Ensure using SharePoint Modern (not Classic)
   - Modern automatically includes mobile menu
   - If Classic, consider migrating to Modern

3. Test on actual device:
   - Use real phone to test
   - Try different phone (iOS/Android)
   - Check screen orientation
   - Test on mobile data (not just WiFi)

4. Clear mobile cache:
   - Close and reopen browser
   - Clear browser app data
   - Try different browser app
   - Restart phone

5. Check accessibility settings:
   - Some phone settings affect rendering
   - Disable zoom if enabled
   - Check text size settings
   - Try default phone settings
```

**Verification:** Mobile menu hamburger icon visible, opens when tapped, all items accessible and readable

---

### Issue: Users Can't Access Site

**Symptoms:**
- "Access Denied" error
- Site shows but can't open documents
- Users not in groups can't access
- Permission inheritance broken

**Solutions:**

```
1. Verify user is in correct group:
   - Check Site Settings > Site Permissions
   - Find user in Groups list
   - Confirm correct permission level
   - Add to group if missing

2. Check permission inheritance:
   - Site Settings > List Permissions
   - Ensure lists inherit from site
   - Reset permissions if modified
   - Check for unique permissions blocking access

3. Verify user account:
   - User must have Office 365 license
   - User must be in organization
   - User must have email activated
   - Try with different user to test

4. Clear permissions cache:
   - Have user logout completely
   - Wait 15 minutes
   - User login again
   - Permissions may take time to propagate

5. Try manual fix:
   - Remove user from group
   - Wait 5 minutes
   - Re-add user to group
   - User logout/login again
```

**Verification:** All group members can access site, no permission errors, access level matches group assignment

---

## Performance Issues

### Site Loading Slowly

**Symptoms:**
- Pages take > 5 seconds to load
- Navigation sluggish
- Lists slow to open

**Solutions:**

```
1. Check network:
   - Test internet speed: www.speedtest.net
   - Try wired connection if on WiFi
   - Try different network
   - Check bandwidth usage

2. Browser optimization:
   - Clear cache and cookies
   - Disable extensions
   - Update browser to latest
   - Try different browser

3. SharePoint optimization:
   - Minimize number of items in views (Phase 1.2)
   - Use efficient search
   - Avoid heavy customizations
   - Contact your IT department

4. Check time of day:
   - Try during off-peak hours
   - Tenant might be overloaded
   - Try again later
   - Monitor pattern over time
```

**Verification:** Site home page loads in < 3 seconds, list pages in < 5 seconds

---

## Getting Help

### Internal Support Resources

| Issue Type | Contact | Response Time |
|-----------|---------|----------------|
| SharePoint access | Your IT Help Desk | 1-2 hours |
| Account/Licensing | O365 Admin | 2-4 hours |
| Site permission | Site Owner | 1 hour |
| MERT Support | MERT Coordinator | Same day |

### Information to Provide When Getting Help

```
1. Error Message
   - What exactly does it say?
   - Full error code if shown
   - Screenshot if possible

2. User Information
   - Your email address
   - Group membership
   - When access worked last (if applicable)

3. Environment
   - Browser name and version
   - Device type (desktop/mobile/tablet)
   - Operating system (Windows/Mac/iOS/Android)
   - Network type (corporate/home/mobile)

4. Reproduction Steps
   - What were you trying to do?
   - Exact steps to reproduce problem
   - Did you try anything to fix it?
   - Does problem occur consistently?

5. Screenshots
   - Full screen showing error
   - Browser address bar showing URL
   - Any relevant details visible
```

---

# Summary

You have successfully completed Phase 1.1 - SharePoint Site Setup for the REdI Trolley Audit system.

## What Was Accomplished

✓ **Task 1.1.1** - Provisioned SharePoint site "REdI Trolley Audit"
✓ **Task 1.1.2** - Configured 3-tier permission model (Owners, Members, Visitors)
✓ **Task 1.1.3** - Created intuitive navigation menu structure
✓ **Task 1.1.4** - Applied REdI branding

## Key Artefacts Created

1. **SharePoint Site**
   - URL: /sites/REdITrolleyAudit
   - 100 GB storage allocated
   - Modern experience enabled

2. **Permission Groups**
   - REdI Trolley Audit - Owners (Full Control)
   - REdI Trolley Audit - Members (Contribute)
   - REdI Trolley Audit - Visitors (Read)

3. **Navigation Structure**
   - 5 main menu items
   - 5 quick action links
   - Mobile-responsive design

4. **Brand Identity**
   - REdI brand colours applied
   - Logo uploaded and positioned
   - Consistent theme across site

5. **Documentation**
   - Site navigation guide
   - Branding specifications
   - Permission assignment record

## Next Steps

Phase 1.2 begins the creation of reference data lists:
- ServiceLine list (7 items)
- EquipmentCategory list (8 items)
- AuditPeriod list (initial configuration)

### Phase 1.2 will use this site as its foundation.

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Lead | | | |
| SharePoint Admin | | | |
| MERT Educator | | | |
| IT Approver | | | |

---

**Document Version:** 1.0
**Last Updated:** January 2026
**Status:** APPROVED FOR IMPLEMENTATION

For questions or updates, contact the MERT Coordination Team.

---

*End of Phase 1.1 Implementation Guide*
