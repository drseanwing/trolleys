# REdI Trolley Audit System
## Phase 4.2 Advanced Features Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 4.2.1 - 4.2.8

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Prerequisites](#prerequisites)
3. [Task 4.2.1-4.2.2: Offline Mode](#task-421-422-offline-mode)
4. [Task 4.2.3-4.2.5: Custom Equipment per Location](#task-423-425-custom-equipment-per-location)
5. [Task 4.2.6: Follow-up Audit Workflow](#task-426-follow-up-audit-workflow)
6. [Task 4.2.7-4.2.8: Photo Attachments](#task-427-428-photo-attachments)
7. [Testing Procedures](#testing-procedures)
8. [Troubleshooting](#troubleshooting)

---

## Executive Summary

Phase 4.2 implements advanced features that enhance the audit system's capability and user experience:

| Feature | Purpose | Impact |
|---------|---------|--------|
| Offline Mode | Enable audit entry without internet | Supports clinical areas with poor connectivity |
| Custom Equipment | Per-location equipment overrides | Handles trolley variations across campus |
| Follow-up Audits | Verification workflow for resolved issues | Ensures accountability for corrections |
| Photo Attachments | Evidence capture during audits | Documents condition and issues |

**Total Estimated Duration:** 15 hours
**Skill Level Required:** Intermediate to Advanced PowerApps/Power Automate

---

## Prerequisites

### Required Completion
- Phase 1.1-1.5: SharePoint site, lists, and seed data
- Phase 1.6: PowerApp foundation and data connections
- Phase 2.1-2.8: Core audit workflows and screens
- All data connections must be active and tested

### Required Access & Permissions
- Power Apps environment with offline sync capability
- SharePoint Administrator to create new lists
- Power Automate flow creation permissions
- Azure Storage (for photo storage, if not using SharePoint)

### Required Knowledge
- PowerApps offline mode configuration
- Power Automate workflow design
- Camera/media picker controls
- Document library setup in SharePoint

---

## Task 4.2.1-4.2.2: Offline Mode

### Objective

Enable PowerApp offline sync settings so auditors can capture audit data in areas with poor or no internet connectivity, with automatic sync on reconnection.

### Step 1: Create LocationEquipment List (Prerequisite for 4.2.3)

First, create the LocationEquipment list that stores per-location equipment customizations.

**Navigate to SharePoint Site:**

1. Go to https://yourtenant.sharepoint.com/sites/REdITrolleyAudit
2. Select **Settings** (gear icon) → **Site contents**
3. Click **+ New** → **List**
4. Name: `LocationEquipment`
5. Click **Create**

**Add Columns:**

1. Click **+ Add column**
2. Create each column with these settings:

| Column Name | Type | Required | Notes |
|------------|------|----------|-------|
| Location | Lookup | Yes | Points to Location list |
| Equipment | Lookup | Yes | Points to Equipment list |
| CustomQuantity | Number | No | Override standard quantity |
| IsExcluded | Yes/No | No | Hide this item from checklist |
| EffectiveDate | Date | Yes | When override starts |
| Notes | Multiple lines | No | Reason for customization |

**Configure Lookups:**

For the **Location** column:
- Type: Lookup
- Get information from: Location
- In this column: Title (or DepartmentName if using that)

For the **Equipment** column:
- Type: Lookup
- Get information from: Equipment
- In this column: ItemName

### Step 2: Enable Offline Sync in PowerApp

**Open the Audit App in Edit Mode:**

1. Navigate to https://make.powerapps.com
2. Open **REdI_Trolley_Audit_App**
3. Click **Edit**

**Enable Offline Settings:**

1. From top menu, select **File** → **Settings**
2. Scroll to **Offline data**
3. Toggle **Enable offline support** to **ON**

**Configure Data Tables for Offline Sync:**

1. From top menu, select **Data** → **Connectors**
2. Find **SharePoint** connector
3. For each list, toggle to enable offline:
   - Location
   - Equipment
   - EquipmentCategory
   - Audit (optional - for read-only sync)
   - AuditEquipment (optional)
   - AuditDocuments (optional)

**Configuration Details:**

| List | Cache Mode | Priority | Notes |
|------|-----------|----------|-------|
| Location | Full | High | Master reference data |
| Equipment | Full | High | Equipment lookup |
| EquipmentCategory | Full | High | Category grouping |
| Audit | Incremental | Medium | Draft audits only |
| AuditEquipment | Incremental | Medium | Equipment responses |
| AuditDocuments | Incremental | Low | Documentation responses |

### Step 3: Configure Offline Collections

**Create Local Collections for Caching:**

In PowerApp, add this formula to the **App OnStart**:

```powershell
// Load reference data into offline collections
ClearCollect(
    colLocations,
    Refresh(Location)
);
ClearCollect(
    colEquipment,
    Refresh(Equipment)
);
ClearCollect(
    colCategories,
    Refresh(EquipmentCategory)
);

// Set offline indicator variable
Set(varIsOnline, Connection.Connected)
```

### Step 4: Update Audit Screens for Offline Mode

**Location Selection Screen:**

Replace the dropdown formula with offline-aware version:

```powershell
// Use local collection when offline
If(
    varIsOnline,
    Location,
    colLocations
)
```

**Equipment Checklist Screen:**

Add offline sync status to the screen:

1. Add a text label showing:
   ```powershell
   If(
       varIsOnline,
       "Online - Changes sync immediately",
       "Offline mode - Will sync when connected"
   )
   ```

2. Add a sync button (visible when offline):
   ```powershell
   Visible: Not(varIsOnline)
   OnSelect: RefreshAll(); Notify("Syncing data...")
   ```

### Step 5: Test Offline Functionality

**Simulate Offline Mode:**

1. Open PowerApp in browser
2. Open Developer Tools (F12)
3. Go to **Network** tab
4. Toggle **Offline** checkbox

**Test Data Entry:**

1. With offline mode active:
   - Navigate to audit entry
   - Create draft audit
   - Fill in responses
   - Try to submit (should show queued message)

2. Verify offline data persists:
   - Refresh browser (Ctrl+F5)
   - Draft should still be visible

3. Restore connection:
   - Toggle offline OFF in Network tab
   - Sync button should trigger
   - Verify draft syncs to SharePoint

**Expected Results:**

- [ ] App loads with offline collections
- [ ] Audit entry works without internet
- [ ] Data persists after browser refresh
- [ ] Sync completes on reconnection
- [ ] No data loss during sync

### Step 6: Configure Conflict Resolution

**When offline changes conflict with online updates:**

Add this logic to the audit submission flow:

```powershell
// Check for conflicts before submission
If(
    IsBlank(Lookup(Audit, AuditId = ThisRecord.AuditId)),
    // No conflict - submit normally
    SubmitForm(frmAudit),
    // Conflict detected
    Notify(
        "This audit was modified elsewhere. Please review changes.",
        Warning
    )
)
```

**Conflict Resolution Flow in Power Automate:**

1. Create new flow: **Handle Audit Conflicts**
2. Trigger: When offline app sync completes
3. Actions:
   - Check if modification timestamp differs
   - If conflict: send notification to auditor
   - Log conflict to AuditConflictLog table
   - Display resolution options:
     - Keep my changes
     - Accept their changes
     - Manual merge

---

## Task 4.2.3-4.2.5: Custom Equipment per Location

### Objective

Allow each location to customize which equipment items are required, with optional quantity overrides.

### Step 1: Review LocationEquipment List

The LocationEquipment list was created in 4.2.1. Verify structure:

**SharePoint List Columns:**
- Location (Lookup to Location)
- Equipment (Lookup to Equipment)
- CustomQuantity (Number, optional)
- IsExcluded (Yes/No, to hide items)
- EffectiveDate (Date)
- Notes (Text explanation)

**Add Sample Data:**

1. Go to LocationEquipment list
2. Add test records:

| Location | Equipment | CustomQuantity | IsExcluded | Notes |
|----------|-----------|-----------------|-----------|-------|
| 7A North | Adrenaline 1:1000 | 3 | No | Increased for high acuity area |
| Cardiac Cath Lab | Amiodarone 100mg | 2 | No | Cardiac-specific requirement |
| Mental Health Ward | Restraint equipment | (blank) | Yes | Not applicable for this area |

### Step 2: Create Equipment Customization Screen in PowerApp

**Add New Screen:**

1. In Power Apps Studio, click **New screen** → **Blank**
2. Name it: `EquipmentCustomizationScreen`

**Add Screen Components:**

```
Screen Layout:
├── Header: "Equipment Customization"
├── Location Dropdown (Auto-populated)
├── Filter Buttons: All / Included / Excluded
├── Data Table:
│   ├── Equipment Name
│   ├── Standard Quantity
│   ├── Custom Quantity (edit box)
│   ├── Is Excluded (toggle)
│   └── Action buttons (Save/Cancel)
└── Save All button
```

**Create Header Section:**

1. Add **Combo box** for location selection:
   - Items: `Sort(Filter(Location, IsActive=true), DepartmentName)`
   - Display Value: `DepartmentName`
   - Search enabled: Yes

2. Add instructional text label:
   ```
   "Select a location to customize its equipment requirements.
   Excluded items will not appear in audits. Custom quantities
   override standard amounts."
   ```

### Step 3: Build Equipment Customization Data Table

**Create Filtered Equipment List:**

1. Add **Gallery** control (vertical)
2. Set Items formula:

```powershell
// Show equipment with customization status
AddColumns(
    Filter(
        Equipment,
        IsActive = true
    ),
    "LocationCustomization",
    LookUp(
        LocationEquipment,
        Equipment.EquipmentId = Equipment.EquipmentId
        And Location.LocationId = cmbLocation.Selected.LocationId
    ),
    "CustomQty",
    If(
        IsBlank(LocationCustomization.CustomQuantity),
        Equipment.StandardQuantity,
        LocationEquipment.CustomQuantity
    ),
    "IsExcluded",
    If(
        IsBlank(LocationCustomization),
        false,
        LocationCustomization.IsExcluded
    )
)
```

**Add Gallery Layout:**

For each item in the gallery:

```
Template:
├── Equipment Name (Label)
├── Category (Label)
├── Standard Qty: [StandardQuantity] (Label)
├── Custom Qty: [TextInput] - editable
├── Excluded (Toggle)
└── Modified indicator (Icon)
```

### Step 4: Add Save Functionality

**Create Save Location Record Flow:**

1. In Power Automate, create flow: **Update Equipment Customization**
2. Trigger: Manual trigger from PowerApp

**Flow Steps:**

```
Action 1: Apply to each Equipment record
├── For each item in selectedEquipment array
│
├── Check if LocationEquipment record exists
│   Condition: If LocationId + EquipmentId match
│
├── If exists: Update LocationEquipment
│   └── Set: CustomQuantity, IsExcluded, ModifiedDate
│
└── If not exists: Create new LocationEquipment
    └── Set: Location, Equipment, CustomQuantity, EffectiveDate, IsExcluded
```

**PowerApp Button OnSelect:**

```powershell
// Collect changes
ClearCollect(
    colEquipmentChanges,
    Gallery1.AllItems
);

// Call Power Automate flow
UpdateEquipmentCustomization.Run(
    cmbLocation.Selected.LocationId,
    colEquipmentChanges
);

// Notify user
Notify("Equipment customization saved", Success)
```

### Step 5: Update Equipment Checklist Screen

**Modify Audit Equipment Checklist:**

Replace the equipment list formula to use LocationEquipment:

```powershell
// Get equipment, applying location customizations
AddColumns(
    Filter(
        Equipment,
        IsActive = true
        And (
            IsPaediatric = false
            Or varCurrentAudit.Location.HasPaedBox = true
        )
    ),
    "IsIncluded",
    Not(
        IsBlank(
            LookUp(
                LocationEquipment,
                Equipment.EquipmentId = Equipment.EquipmentId
                And Location.LocationId = varCurrentAudit.LocationId
                And IsExcluded = true
            )
        )
    ),
    "CustomQuantity",
    If(
        IsBlank(
            LookUp(
                LocationEquipment,
                Equipment.EquipmentId = Equipment.EquipmentId
                And Location.LocationId = varCurrentAudit.LocationId
            ).CustomQuantity
        ),
        Equipment.StandardQuantity,
        LookUp(
            LocationEquipment,
            Equipment.EquipmentId = Equipment.EquipmentId
            And Location.LocationId = varCurrentAudit.LocationId
        ).CustomQuantity
    )
)
```

**Filter to Show Only Included Items:**

```powershell
// In Gallery Items property
Filter(
    <<above formula>>,
    IsIncluded = true
)
```

**Update Quantity Expected Display:**

```powershell
// Show custom quantity instead of standard
"Expected: " & Text(ThisRecord.CustomQuantity, "0")
```

---

## Task 4.2.6: Follow-up Audit Workflow

### Objective

When an issue is marked as Resolved, prompt for a verification audit and link it to the original issue.

### Step 1: Create Follow-Up Audit Tracking List

**Create SharePoint List:**

1. Go to site contents
2. Create new list: `FollowUpAudit`

**Add Columns:**

| Column Name | Type | Required | Notes |
|------------|------|----------|-------|
| OriginalAuditId | Lookup | Yes | Links to initial audit |
| IssueId | Lookup | Yes | Links to issue being verified |
| Location | Lookup | Yes | Same location as original |
| ScheduledDate | Date | Yes | When verification planned |
| CompletedDate | Date | No | When verification done |
| Status | Choice | Yes | Scheduled/In Progress/Completed/Deferred |
| VerificationResult | Choice | No | Issue Resolved/Issue Recurs/Issue Escalated |
| VerificationNotes | Multiple lines | No | Findings from follow-up |
| VerifiedBy | Person | No | Who conducted verification |

### Step 2: Add Follow-Up Trigger to Issue Management

**Modify Issue Detail Screen:**

1. On Issue detail, find "Mark Resolved" button
2. Update OnSelect formula:

```powershell
// Update issue status
Patch(
    Issue,
    ThisRecord,
    {Status: "Resolved"}
);

// Show follow-up dialog
Set(varShowFollowUpDialog, true)
```

### Step 3: Create Follow-Up Scheduling Dialog

**Add Dialog Screen:**

1. New screen: `FollowUpScheduleDialog`
2. Add components:

```
Dialog Layout:
├── Title: "Schedule Follow-Up Audit"
├── Explanation text:
│   "A follow-up audit will verify that this issue
│    has been properly resolved. Schedule it now
│    or defer for later scheduling."
├── Date picker: "Verification Date"
├── Priority dropdown: Immediate/This Week/Within 2 Weeks
├── Notes field: Optional notes for auditor
├── Buttons:
│   ├── Schedule Now
│   ├── Defer
│   └── Cancel
```

**Schedule Button OnSelect:**

```powershell
// Create FollowUpAudit record
Patch(
    FollowUpAudit,
    Defaults(FollowUpAudit),
    {
        OriginalAuditId: varCurrentAudit.AuditId,
        IssueId: ThisRecord.IssueId,
        Location: ThisRecord.Location,
        ScheduledDate: dtFollowUpDate.Value,
        Status: "Scheduled",
        VerificationNotes: txtFollowUpNotes.Value
    }
);

// Navigate back to issue
Navigate(IssueDetailScreen, ScreenTransition.Pop);
Notify("Follow-up audit scheduled", Success)
```

### Step 4: Create Follow-Up Audit Entry Screen

**Add Screen:** `FollowUpAuditScreen`

This screen is similar to Equipment Checklist but simplified:

```
Screen Layout:
├── Header: "Follow-Up Audit Verification"
├── Original Issue Summary
│   ├── Issue Title
│   ├── Original Finding
│   └── Issue Number
├── Verification Status Buttons:
│   ├── "Issue Resolved" (green)
│   ├── "Issue Recurs" (red)
│   └── "Escalate" (orange)
├── Verification Notes (text area)
├── Evidence section (for photos - see 4.2.7)
└── Complete button
```

**Verification Result OnSelect:**

```powershell
// For "Issue Resolved"
Patch(
    FollowUpAudit,
    varFollowUpRecord,
    {
        Status: "Completed",
        VerificationResult: "Issue Resolved",
        VerificationNotes: txtNotes.Value,
        VerifiedBy: User().Email,
        CompletedDate: Now()
    }
);

// Update related issue
Patch(
    Issue,
    LookUp(Issue, IssueId = varFollowUpRecord.IssueId),
    {Status: "Closed"}
);

Notify("Follow-up audit completed", Success)
```

### Step 5: Add Follow-Up Dashboard

**Create Follow-Up Audit List Screen:**

Add new screen showing pending follow-ups:

```
Screen Layout:
├── Filter options:
│   ├── Status (All/Scheduled/Overdue)
│   ├── Priority
│   └── Location
├── Gallery showing follow-ups:
│   ├── Issue Title
│   ├── Location
│   ├── Scheduled Date (highlight if overdue)
│   ├── Status badge
│   └── Action button (Start Verification)
└── Summary: X scheduled, Y completed, Z overdue
```

**Gallery Items Formula:**

```powershell
Filter(
    AddColumns(
        FollowUpAudit,
        "IsOverdue",
        And(
            ScheduledDate < Today(),
            Status <> "Completed"
        ),
        "DaysUntilDue",
        DateDiff(Today(), ScheduledDate)
    ),
    Status = "Scheduled"
)
```

---

## Task 4.2.7-4.2.8: Photo Attachments

### Objective

Enable photo capture during audits and store images in SharePoint document library.

### Step 1: Create AuditPhotos Document Library

**Create SharePoint Document Library:**

1. Go to site home
2. Click **+ New** → **Document library**
3. Name: `AuditPhotos`
4. Click **Create**

**Add Metadata Columns:**

1. Go to library settings
2. Add columns:

| Column Name | Type | Notes |
|------------|------|-------|
| AuditId | Single line text | For filtering |
| ItemId | Single line text | Equipment or trolley section |
| PhotoType | Choice | Equipment/Condition/Issue/General |
| CapturedDateTime | Date/Time | When taken |
| Description | Multiple lines | What photo shows |

### Step 2: Add Camera Control to Audit Screens

**Add Camera Control to Equipment Checklist Screen:**

1. On Equipment Checklist screen, add **Camera** control:
   - Property: `Photo_Camera1`
   - Size: 100x100 pixels
   - Visible for each equipment item

2. Add **Image** control to display captured photo:
   - Property: `Image_Equipment`
   - Image source: `Photo_Camera1.Photo`

**Add Photo Buttons:**

For each equipment row:

1. Add **Camera icon** button:
   ```
   Text: "📷"
   OnSelect:
   Set(varSelectedEquipmentId, ThisRecord.EquipmentId);
   Notify("Click camera icon to capture photo")
   ```

2. Add **Delete photo** button:
   ```
   Text: "✕"
   OnSelect:
   Set(varEquipmentPhotos[ThisRecord.EquipmentId], Blank());
   Notify("Photo deleted")
   ```

### Step 3: Create Photo Storage Table

**Add Table to Store Photo References:**

In Power Automate, create a SharePoint list: `AuditPhotoReferences`

| Column | Type | Purpose |
|--------|------|---------|
| AuditId | Lookup | Links to audit |
| ItemId | Text | Equipment or section ID |
| PhotoURL | Hyperlink | URL to photo in library |
| PhotoType | Choice | Equipment/Condition/Issue |
| Description | Text | What photo documents |
| CapturedDate | Date/Time | When photo taken |

### Step 4: Create Upload Photo Flow

**New Power Automate Flow:** `Upload Audit Photo`

**Trigger:** Manual (called from PowerApp)

**Inputs:**

```
- AuditId (string)
- ItemId (string)
- PhotoType (string)
- PhotoBase64 (string - base64 encoded image)
- Description (string)
```

**Flow Actions:**

```
Action 1: Create file in AuditPhotos library
├── Location: /sites/REdITrolleyAudit/AuditPhotos
├── File name:
│   @{triggerBody()['AuditId']}_
│   @{triggerBody()['ItemId']}_
│   @{utcNow('yyyyMMdd_HHmmss')}.jpg
└── File content: @triggerBody()['PhotoBase64']

Action 2: Create AuditPhotoReferences record
├── AuditId: @triggerBody()['AuditId']
├── ItemId: @triggerBody()['ItemId']
├── PhotoURL: @outputs('Create_file')['id']
├── PhotoType: @triggerBody()['PhotoType']
├── Description: @triggerBody()['Description']
└── CapturedDate: @utcNow()

Action 3: Return photo URL to PowerApp
└── Return: @outputs('Create_file')['webUrl']
```

### Step 5: Integrate Photo Upload into PowerApp

**Add Upload Button to Equipment Item:**

```powershell
OnSelect:
If(
    IsBlank(Photo_Camera1.Photo),
    Notify("Please capture a photo first", Warning),
    UploadAuditPhoto.Run(
        varCurrentAudit.AuditId,
        ThisRecord.EquipmentId,
        "Equipment",
        ImageData(Photo_Camera1.Photo, "image/jpeg"),
        txtPhotoDescription.Value
    )
);
Notify("Photo uploading...");
```

**Photo Upload Feedback:**

```powershell
// Show upload status
If(
    UploadAuditPhoto.IsRunning,
    Notify("Uploading photo...", Information),
    If(
        UploadAuditPhoto.IsSuccessful,
        Notify("Photo saved", Success),
        Notify("Photo upload failed", Error)
    )
)
```

### Step 6: Display Photos in Issue Detail Screen

**Add Photo Gallery to Issue Detail:**

1. Add **Gallery** control for photos
2. Items formula:

```powershell
Filter(
    AuditPhotoReferences,
    AuditId = varCurrentIssue.AuditId
)
```

**Gallery Template:**

```
├── Photo image (from PhotoURL)
├── Type label (PhotoType)
├── Description label
├── Captured date label
└── Delete button
```

**Photo Display:**

```powershell
// Show photo with metadata
Image:
    Value: @ThisRecord.PhotoURL

Below image:
    Text(ThisRecord.CapturedDate, "dd/mm/yyyy hh:mm")
    & " - " & ThisRecord.PhotoType
```

### Step 7: Add Condition Photos to Audit

**Add Trolley Condition Photo Section:**

On Condition Check screen, add:

```
Section: "Trolley Condition Evidence"
├── Instructions: "Take photos of any issues found"
├── Camera control (size 200x200)
├── Photo type dropdown:
│   ├── General trolley
│   ├── Wheels/base
│   ├── Handle
│   ├── Locks
│   └── Other
├── Description text field
└── Upload button (uses same UploadAuditPhoto flow)
```

---

## Testing Procedures

### Offline Mode Testing (4.2.1-4.2.2)

**Test Plan:**

1. **Offline Collection Loading**
   - Verify collections populate on app start
   - Check collection row count matches SharePoint lists
   - Confirm data refreshes after login

2. **Offline Data Entry**
   - Enable offline mode in browser dev tools
   - Create new draft audit
   - Verify all screens work without network
   - Fill complete audit form
   - Check data persists after browser refresh

3. **Conflict Resolution**
   - Create audit offline
   - Modify same audit online (different window)
   - Reconnect offline browser
   - Verify conflict detection triggers
   - Test resolution options

4. **Sync Verification**
   - Turn offline mode off
   - Click sync button
   - Verify data appears in SharePoint
   - Check audit timestamp in list

**Expected Results:**

- [ ] All reference data available offline
- [ ] Can complete full audit without network
- [ ] Data persists and syncs correctly
- [ ] Conflicts detected and resolved
- [ ] No data loss during sync

### Custom Equipment Testing (4.2.3-4.2.5)

**Test Plan:**

1. **Equipment Customization**
   - Open Equipment Customization screen
   - Select test location
   - Modify custom quantity for item
   - Toggle item excluded
   - Save changes
   - Verify LocationEquipment record created

2. **Audit Uses Custom Equipment**
   - Start audit for location with customization
   - View equipment checklist
   - Verify excluded items hidden
   - Verify custom quantity shown instead of standard
   - Add response for item

3. **Multiple Locations**
   - Customize equipment for Location A
   - Customize differently for Location B
   - Start audits for each
   - Verify each sees correct customizations
   - Modify customizations
   - Verify new audits use updated values

**Expected Results:**

- [ ] Customizations save correctly
- [ ] Audits reflect location-specific equipment
- [ ] Excluded items don't appear in checklist
- [ ] Custom quantities used in calculations
- [ ] Changes don't affect other locations

### Follow-Up Audit Testing (4.2.6)

**Test Plan:**

1. **Follow-Up Scheduling**
   - Create and submit audit
   - Create issue with findings
   - Mark issue as Resolved
   - Follow-up dialog appears
   - Schedule follow-up audit
   - Verify FollowUpAudit record created

2. **Follow-Up Audit Entry**
   - View follow-up audit list
   - Start follow-up audit
   - Select "Issue Resolved"
   - Add verification notes
   - Submit follow-up
   - Verify original issue status changed to Closed
   - Verify FollowUpAudit marked Completed

3. **Overdue Tracking**
   - Create follow-up audit with past date
   - Check dashboard shows as overdue
   - Verify visual indicator (red/warning)
   - Complete overdue follow-up
   - Verify status updates

**Expected Results:**

- [ ] Follow-up audits created on issue resolution
- [ ] Can conduct verification audit
- [ ] Issue status updates based on result
- [ ] Overdue audits flagged
- [ ] Complete audit trail maintained

### Photo Attachment Testing (4.2.7-4.2.8)

**Test Plan:**

1. **Photo Capture and Upload**
   - Open audit equipment screen
   - Take photo using camera control
   - Photo displays in preview
   - Click upload
   - Verify photo appears in AuditPhotos library
   - Check file named correctly
   - Verify metadata saved

2. **Photo Display in Issue**
   - Create issue during audit
   - Attach photos to issue items
   - View issue detail
   - Photos display in gallery
   - Click photo to view full size
   - Verify timestamp and description show

3. **Multiple Photo Types**
   - Capture equipment photo
   - Capture condition photo
   - Capture issue photo
   - Filter by photo type
   - Verify each type displays correctly

4. **Photo Management**
   - Delete photo from list
   - Verify deletion confirmed
   - Confirm removed from library
   - Re-upload photo
   - Verify new version has fresh timestamp

**Expected Results:**

- [ ] Photos capture successfully
- [ ] Files upload to SharePoint library
- [ ] Metadata correct and searchable
- [ ] Photos display in issue details
- [ ] Photo filtering works
- [ ] Delete and re-upload functions work

---

## Troubleshooting

### Offline Mode Issues

**Problem: Offline collections don't populate**

*Solutions:*
1. Check data connections are active
2. Verify OnStart formula in PowerApp
3. Ensure lists aren't empty
4. Check user permissions to lists
5. Try manual refresh of collections

**Problem: Offline changes don't sync on reconnect**

*Solutions:*
1. Check network connectivity
2. Click sync button manually
3. Check for sync errors in Power Automate
4. Verify no data validation errors
5. Check SharePoint list isn't locked

**Problem: Conflicts occur during sync**

*Solutions:*
1. Add timestamp columns to track updates
2. Implement last-write-wins strategy
3. Create conflict resolution UI
4. Log all conflicts for review
5. Notify user of conflicts immediately

### Custom Equipment Issues

**Problem: Customizations don't appear in audit**

*Solutions:*
1. Verify LocationEquipment records created
2. Check Location and Equipment lookups resolve
3. Refresh PowerApp data connections
4. Test formula in formula bar
5. Check IsExcluded logic inverted

**Problem: Custom quantities not calculated**

*Solutions:*
1. Verify CustomQuantity column populated
2. Check lookup is returning correct record
3. Test formula with sample data
4. Verify data types (number, not text)
5. Add debugging label to show values

### Follow-Up Audit Issues

**Problem: Follow-up dialog doesn't appear**

*Solutions:*
1. Check Set(varShowFollowUpDialog, true) executes
2. Verify dialog screen exists
3. Check Visible property on dialog
4. Test button OnSelect formula
5. Review Power Automate flow status

**Problem: Follow-up audits don't create**

*Solutions:*
1. Check Power Automate flow has run permission
2. Verify FollowUpAudit list exists
3. Check all lookup columns configure correctly
4. Review flow run history for errors
5. Test flow with sample input

### Photo Attachment Issues

**Problem: Camera control doesn't work**

*Solutions:*
1. Verify camera permissions granted
2. Check device has camera hardware
3. Test in mobile or tablet device
4. Check camera control visible on screen
5. Try alternative: file picker for photos

**Problem: Photos don't upload to SharePoint**

*Solutions:*
1. Check AuditPhotos library exists
2. Verify user has write permissions
3. Check file size limit (shouldn't exceed 100MB)
4. Verify flow has SharePoint connector permission
5. Test file naming convention works

**Problem: Photo URLs invalid**

*Solutions:*
1. Check AuditPhotos library accessible
2. Verify file permissions include view access
3. Test URL directly in browser
4. Check sharing settings on library
5. Regenerate photo files with correct naming

---

## Configuration Checklist

### Pre-Implementation

- [ ] All Phase 1-3 tasks complete
- [ ] PowerApp data connections active
- [ ] SharePoint lists verified
- [ ] Power Automate connector permissions configured
- [ ] Team informed of new features

### Offline Mode (4.2.1-4.2.2)

- [ ] Offline support enabled in PowerApp settings
- [ ] Reference data tables selected for cache
- [ ] App OnStart formula includes ClearCollect
- [ ] Offline collections tested
- [ ] Conflict resolution logic implemented
- [ ] Sync tested on reconnection

### Custom Equipment (4.2.3-4.2.5)

- [ ] LocationEquipment list created
- [ ] Equipment Customization screen built
- [ ] Sample customizations created
- [ ] Equipment checklist formula updated
- [ ] Excluded items hidden from checklist
- [ ] Custom quantities displayed correctly

### Follow-Up Audits (4.2.6)

- [ ] FollowUpAudit list created
- [ ] Follow-up trigger added to issue resolution
- [ ] Follow-up scheduling dialog created
- [ ] Follow-up audit screen built
- [ ] Verification results update issue status
- [ ] Dashboard shows pending follow-ups

### Photo Attachments (4.2.7-4.2.8)

- [ ] AuditPhotos library created with metadata columns
- [ ] Camera controls added to audit screens
- [ ] Photo upload flow created
- [ ] Photo URL storage configured
- [ ] Photos display in issue details
- [ ] File naming convention working

### Final Verification

- [ ] All features tested per procedures above
- [ ] No errors in Power Automate flows
- [ ] offline mode syncs properly
- [ ] Custom equipment appears in audits
- [ ] Follow-up audits created automatically
- [ ] Photos upload and display correctly
- [ ] Documentation updated
- [ ] Team trained on new features

---

## Sign-Off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Technical Lead | | | |
| Power Apps Developer | | | |
| MERT Educator | | | |
| IT Approver | | | |

---

**Document Version:** 1.0
**Last Updated:** January 2026
**Status:** APPROVED FOR IMPLEMENTATION

For questions, contact the MERT Technical Coordination Team.

---

*End of Phase 4.2 Advanced Features Implementation Guide*
