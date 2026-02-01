# Phase 2.2 Trolley Management Flows Implementation Guide

**REdI Trolley Audit System**

Version: 1.0
Date: January 2026
Document Type: Step-by-Step Implementation Guide

---

## Overview

Phase 2.2 implements the Power Automate flows that handle trolley lifecycle management operations. These flows create, update, deactivate, and reactivate trolley location records, with comprehensive audit trail logging to the LocationChangeLog list. All flows integrate with PowerApp triggers and handle errors gracefully.

**Phase Scope:** Tasks 2.2.1 through 2.2.8
**Estimated Duration:** 12 hours
**Prerequisites:**
- Phase 1.4 (Location and LocationChangeLog lists created)
- Phase 1.6 (PowerApp foundation with data connections)
- Phase 2.1 (Trolley management screens created)

---

## LocationChangeLog Schema Reference

Before implementing flows, understand the LocationChangeLog structure:

```
LocationChangeLog List Fields:
- Title (Text, Required) - Auto-generated change reference (auto-populated by flow)
- Location (Lookup, Required) - Reference to Location record
- ChangeType (Choice, Required) - Created | Updated | Deactivated | Reactivated
- ChangeDateTime (DateTime, Required) - When change occurred
- ChangedBy (User, Required) - User who made the change
- FieldsChanged (Text, Optional) - Comma-separated list of field names
- OldValues (Note, Optional) - JSON object of previous values
- NewValues (Note, Optional) - JSON object of new values
- ChangeReason (Note, Optional) - User-provided reason (especially for deactivation)
```

---

## Task 2.2.1: Create Save New Trolley Flow

### Objective

Build a Power Automate flow triggered from the PowerApp that creates a new Location record with all provided attributes from the trolley creation form.

### Prerequisites

- Location SharePoint list created and configured
- PowerApp "Add New Trolley" screen completed (Task 2.1.12)
- User has edit permissions to Location list

### Flow Architecture

```
PowerApp (New Trolley Form)
          ↓
     Cloud Flow Trigger
          ↓
   Parse JSON Input
          ↓
   Create Location Item
          ↓
  Return Item ID to App
```

### Step-by-Step Implementation

#### Step 1: Create Cloud Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Instant cloud flow** (button-triggered)
3. Name the flow: `SaveNewTrolley_Flow`
4. Trigger: Select **PowerApps (V2)**
5. Click **Create**

#### Step 2: Configure PowerApp Trigger Input Parameters

In the PowerApp trigger, add the following inputs that will be sent from the PowerApp:

```
Input Name                    Type      Required
Department_Name              Text      Yes
DisplayName                  Text      Yes
ServiceLine_ID               Text      Yes
Building                     Text      Yes
Level                        Text      Yes
SpecificLocation             Text      No
TrolleyType                  Text      Yes
HasPaediatricBox             Toggle    No
DefibrillatorType            Text      Yes
OperatingHours               Text      Yes
Status                       Text      Yes (default: "Active")
Notes                        Text      No
```

#### Step 3: Add "Create Item" Action for Location

1. Click **Add action** and search for "SharePoint"
2. Select **Create item** (SharePoint connector)
3. Configure:
   - **Site Address:** Select the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **Title:**
     ```
     triggerOutputs()['body']['Department_Name']
     ```
   - **DisplayName:**
     ```
     triggerOutputs()['body']['DisplayName']
     ```
   - **ServiceLine (ID):**
     ```
     triggerOutputs()['body']['ServiceLine_ID']
     ```
   - **Building:**
     ```
     triggerOutputs()['body']['Building']
     ```
   - **Level:**
     ```
     triggerOutputs()['body']['Level']
     ```
   - **SpecificLocation:**
     ```
     triggerOutputs()['body']['SpecificLocation']
     ```
   - **TrolleyType:**
     ```
     triggerOutputs()['body']['TrolleyType']
     ```
   - **HasPaedBox (HasPaediatricBox):**
     ```
     triggerOutputs()['body']['HasPaediatricBox']
     ```
   - **DefibrillatorType:**
     ```
     triggerOutputs()['body']['DefibrillatorType']
     ```
   - **OperatingHours:**
     ```
     triggerOutputs()['body']['OperatingHours']
     ```
   - **Status:**
     ```
     triggerOutputs()['body']['Status']
     ```
   - **Notes:**
     ```
     triggerOutputs()['body']['Notes']
     ```

#### Step 4: Add Return Value Action

1. Click **Add action** and search for "Return"
2. Select **Return value (cloud flow)**
3. Set Output:
   ```text
   {
     "LocationId": @{body('Create_item')?['ID']},
     "LocationTitle": @{body('Create_item')?['Title']},
     "Status": "Success"
   }
   ```
   > Note: This is Power Automate expression syntax, not valid JSON.

#### Step 5: Add Error Handling (Try-Catch Pattern)

1. Wrap the "Create item" action in a **Scope** action named "Create_Location_Scope"
2. Add another **Scope** action after it named "Error_Handler"
3. In the flow, set the Error_Handler scope to run **When the previous step has failed**
4. Inside Error_Handler, add a **Compose** action:
   ```
   Name: ComposeErrorMessage
   Output: concat('Error creating trolley: ', string(trigger()['body']['Department_Name']),
            ' - ', body('Create_item')?['error']?['message'])
   ```

5. Add a **Send an email notification** action in the error handler:
   - **To:** MERT team distribution list or error notification address
   - **Subject:** "Trolley Creation Failed"
   - **Body:**
     ```
     Failed to create trolley: @{triggerOutputs()['body']['Department_Name']}

     Error: @{body('ComposeErrorMessage')}

     Time: @{utcNow()}
     User: @{triggerOutputs()['body']['CreatedBy']}
     ```

### PowerFx Code (PowerApp Integration)

In the PowerApp "Add New Trolley" screen, create a function to call this flow:

```powerfx
// Button "SaveTrolley" OnSelect event
If(
    Validate_TrolleyForm(),
    Launch_SaveNewTrolley_Flow(),
    Notify("Please fix validation errors before saving", NotificationType.Error)
);

// Function: Validate_TrolleyForm
Function Validate_TrolleyForm() As Boolean
    Return And(
        Not(IsBlank(Department_Name.Value)),
        Not(IsBlank(DisplayName.Value)),
        Not(IsBlank(ServiceLine_Lookup.Selected)),
        Not(IsBlank(Building_Dropdown.Selected)),
        Not(IsBlank(Level.Value)),
        Not(IsBlank(TrolleyType_Dropdown.Selected))
    )
End;

// Function: Launch_SaveNewTrolley_Flow
Function Launch_SaveNewTrolley_Flow()
    Set(
        varCreateLocationResult,
        'SaveNewTrolley_Flow'.Run(
            Department_Name.Value,
            DisplayName.Value,
            ServiceLine_Lookup.Selected.ID,
            Building_Dropdown.Value,
            Level.Value,
            SpecificLocation.Value,
            TrolleyType_Dropdown.Value,
            HasPaediatricBox.Value,
            DefibrillatorType_Dropdown.Value,
            OperatingHours_Dropdown.Value,
            "Active",
            Notes.Value
        )
    );

    If(
        varCreateLocationResult.Status = "Success",
        Notify("Trolley created successfully", NotificationType.Success);
        Set(varNewLocationId, varCreateLocationResult.LocationId);
        Navigate(Screen('LocationDetailsScreen'), ScreenTransition.Fade),
        Notify("Failed to create trolley: " & varCreateLocationResult.Error, NotificationType.Error)
    )
End;
```

### Flow Expression Reference

**Location Title (Department Name) - Must be Unique:**
```
triggerOutputs()['body']['Department_Name']
```

**ServiceLine Lookup ID:**
```
triggerOutputs()['body']['ServiceLine_ID']
```

**Current Timestamp:**
```
utcNow()
```

**Current User Information:**
```
triggerOutputs()['body']['CreatedBy']
```

### Testing Procedures

#### Test 1: Basic Trolley Creation
1. Open PowerApp and navigate to "Add New Trolley" screen
2. Enter test data:
   - Department Name: "ICU - New Trolley Test"
   - Display Name: "ICU-NEW-TEST"
   - Service Line: "Intensive Care"
   - Building: "James Mayne Building"
   - Level: "L3"
   - Trolley Type: "Standard"
   - Defibrillator: "LIFEPAK_1000_AED"
   - Operating Hours: "24_7"
3. Click "Save Trolley"
4. Verify:
   - Flow executes without errors
   - Success notification displays
   - LocationChangeLog entry created (Task 2.2.2 will handle this)
   - User navigated to Location Details screen

#### Test 2: Duplicate Department Name Validation
1. Create trolley with name "Emergency - Main Corridor"
2. Attempt to create second trolley with same name
3. Verify:
   - PowerApp validation catches duplicate before flow execution
   - OR flow returns error if duplicate validation not in app

#### Test 3: Missing Required Fields
1. Leave "Department Name" blank
2. Click "Save Trolley"
3. Verify:
   - PowerApp validation prevents flow trigger
   - Error notification displays

#### Test 4: Special Characters in Fields
1. Enter department name with special characters: "ED-24/7 Resus (Main)"
2. Click "Save Trolley"
3. Verify:
   - Flow handles special characters correctly
   - Record created successfully in SharePoint

#### Test 5: Error Handling Path
1. Temporarily modify flow to force an error (e.g., invalid site address)
2. Attempt to create trolley
3. Verify:
   - Error handler executes
   - Email notification sent to MERT team
   - User receives error message in app

### Verification Checklist

- [ ] Flow created and named "SaveNewTrolley_Flow"
- [ ] PowerApp trigger configured with all input parameters
- [ ] Create Item action correctly maps all fields
- [ ] Return value action returns Location ID and status
- [ ] Error handler (Try-Catch pattern) implemented
- [ ] Error notification email configured
- [ ] PowerApp validation function prevents invalid submissions
- [ ] Flow successfully creates location in SharePoint
- [ ] Flow returns location ID to PowerApp
- [ ] All required fields enforced
- [ ] Special character handling verified
- [ ] Duplicate name detection working

---

## Task 2.2.2: Create Log New Trolley Change Flow

### Objective

Build a Power Automate flow triggered after trolley creation that logs the creation event to the LocationChangeLog with ChangeType "Created".

### Prerequisites

- SaveNewTrolley_Flow completed (Task 2.2.1)
- LocationChangeLog list created
- Location record successfully created

### Flow Architecture

```
SaveNewTrolley_Flow Completion
          ↓
  Log Creation Event Trigger
          ↓
  Generate Change Reference
          ↓
  Create LocationChangeLog Item
          ↓
      Flow Complete
```

### Step-by-Step Implementation

#### Step 1: Create Automated Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Automated cloud flow**
3. Name the flow: `LogNewTrolley_Flow`
4. Trigger: Search for and select **When an item is created** (SharePoint)
5. Click **Create**

#### Step 2: Configure SharePoint Trigger

1. In the trigger section:
   - **Site Address:** Select the REdI Trolley Audit SharePoint site
   - **List Name:** Location

#### Step 3: Add Condition to Check if New Item

Add a **Condition** to verify this is a new item (not an update):

```
Condition:
IF Status = "Active" AND Created date ≈ Current time (within last minute)
THEN: Proceed with logging
ELSE: Terminate (already logged by another action)
```

#### Step 4: Generate Change Reference ID

Add a **Compose** action to generate the change reference:

```
Name: GenerateChangeReference

Output:
concat('CHGLOC-', formatDateTime(utcNow(), 'yyyyMMdd'), '-', triggerBody()?['ID'])

Example Output: CHGLOC-20260125-47
```

#### Step 5: Create LocationChangeLog Entry

1. Click **Add action** and search for "SharePoint"
2. Select **Create item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** LocationChangeLog
   - **Title:**
     ```
     outputs('GenerateChangeReference')
     ```
   - **Location (ID):**
     ```
     triggerBody()?['ID']
     ```
   - **ChangeType:**
     ```
     Created
     ```
   - **ChangeDateTime:**
     ```
     utcNow()
     ```
   - **ChangedBy:**
     ```
     triggerBody()?['Author']['claims']['aud']
     ```
     (or use User Profile connector for better data)
   - **FieldsChanged:**
     ```
     Title,DisplayName,ServiceLine,Building,Level,SpecificLocation,TrolleyType,HasPaedBox,DefibrillatorType,OperatingHours,Status
     ```
   - **OldValues:**
     ```json
     {}
     ```
   - **NewValues:**
     ```json
     {
       "Title": "@{triggerBody()?['Title']}",
       "DisplayName": "@{triggerBody()?['DisplayName']}",
       "Building": "@{triggerBody()?['Building']}",
       "Level": "@{triggerBody()?['Level']}",
       "SpecificLocation": "@{triggerBody()?['SpecificLocation']}",
       "TrolleyType": "@{triggerBody()?['TrolleyType']}",
       "HasPaedBox": "@{triggerBody()?['HasPaedBox']}",
       "DefibrillatorType": "@{triggerBody()?['DefibrillatorType']}",
       "OperatingHours": "@{triggerBody()?['OperatingHours']}",
       "Status": "@{triggerBody()?['Status']}"
     }
     ```
   - **ChangeReason:**
     ```
     New trolley location created
     ```

#### Step 6: Add Error Handling

1. Add a **Scope** action named "LogChangeLog_Scope" wrapping the Create item action
2. Add an error-handling **Scope** with this condition:
   ```
   Expression: result('LogChangeLog_Scope')?['status'] == 'Failed'
   ```
3. Inside error scope, add **Send email** to notify MERT of logging failure

#### Step 7: Add Completion Action (Optional)

Add a **Compose** action for audit logging:

```
Name: LogFlowCompletion

Output:
concat('Successfully logged trolley creation for ', triggerBody()?['Title'],
       ' at ', utcNow())
```

### Flow Expression Reference

**Change Reference Format:**
```
concat('CHGLOC-', formatDateTime(utcNow(), 'yyyyMMdd'), '-', triggerBody()?['ID'])
```

**JSON NewValues (Complete):**
```json
{
  "Title": "@{triggerBody()?['Title']}",
  "DisplayName": "@{triggerBody()?['DisplayName']}",
  "ServiceLineId": "@{triggerBody()?['ServiceLineId']['value']}",
  "Building": "@{triggerBody()?['Building']}",
  "Level": "@{triggerBody()?['Level']}",
  "TrolleyType": "@{triggerBody()?['TrolleyType']}",
  "HasPaedBox": "@{triggerBody()?['HasPaedBox']}",
  "DefibrillatorType": "@{triggerBody()?['DefibrillatorType']}",
  "OperatingHours": "@{triggerBody()?['OperatingHours']}",
  "Status": "@{triggerBody()?['Status']}"
}
```

**Current User (User Profile approach):**
```
user('userupn')?['mail']
```

### Testing Procedures

#### Test 1: Automatic Log Entry on Creation
1. Complete Test 1 from Task 2.2.1 (create new trolley via PowerApp)
2. Wait 5-10 seconds for flow to trigger
3. Verify in LocationChangeLog list:
   - New entry created with ChangeType "Created"
   - Change Reference auto-generated correctly
   - ChangeDateTime matches creation time
   - Location lookup populated correctly
   - NewValues JSON contains all trolley attributes
   - OldValues JSON is empty {}

#### Test 2: Change Reference Format
1. Create new trolley
2. Check LocationChangeLog entry Title field
3. Verify format matches: CHGLOC-YYYYMMDD-{ID}

#### Test 3: User Information Capture
1. Create new trolley
2. Verify ChangedBy field shows correct user who created trolley

#### Test 4: Flow Execution on Manual Creation
1. Navigate to SharePoint Location list directly
2. Create item manually (not through PowerApp)
3. Verify:
   - LocationChangeLog entry created automatically
   - ChangeType "Created" assigned
   - NewValues captured correctly

#### Test 5: Error Handling
1. Disconnect the SharePoint connector temporarily
2. Create new trolley via PowerApp
3. Verify:
   - Error handler executes
   - Email notification sent
   - Location still created (separate from this flow)

### Verification Checklist

- [ ] Flow created and named "LogNewTrolley_Flow"
- [ ] SharePoint trigger configured for Location list
- [ ] Change reference generated in correct format (CHGLOC-YYYYMMDD-ID)
- [ ] LocationChangeLog entry created automatically
- [ ] ChangeType set to "Created"
- [ ] ChangeDateTime populated correctly
- [ ] ChangedBy captures current user
- [ ] NewValues JSON contains all trolley fields
- [ ] OldValues JSON is empty for creation
- [ ] FieldsChanged lists all fields separated by commas
- [ ] Error handler sends notification on failure
- [ ] Flow triggers within 10 seconds of location creation
- [ ] Manual creation in SharePoint also triggers log entry

---

## Task 2.2.3: Create Update Trolley Flow

### Objective

Build a Power Automate flow triggered from the PowerApp that updates an existing Location record with modified attributes (e.g., building, level, trolley type changes).

### Prerequisites

- Location record exists
- PowerApp "Trolley Detail" edit mode screen completed (Task 2.1.10)
- User has edit permissions to Location list

### Flow Architecture

```
PowerApp (Edit Trolley Form)
          ↓
  Cloud Flow Trigger (Update)
          ↓
  Parse JSON Input
          ↓
  Update Location Item
          ↓
 Return Update Status
```

### Step-by-Step Implementation

#### Step 1: Create Cloud Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Instant cloud flow** (button-triggered)
3. Name the flow: `UpdateTrolley_Flow`
4. Trigger: Select **PowerApps (V2)**
5. Click **Create**

#### Step 2: Configure PowerApp Trigger Input Parameters

Add the following inputs:

```
Input Name                    Type      Required
LocationId                   Text      Yes (ID of location to update)
Department_Name              Text      Yes
DisplayName                  Text      Yes
ServiceLine_ID               Text      Yes
Building                     Text      Yes
Level                        Text      Yes
SpecificLocation             Text      No
TrolleyType                  Text      Yes
HasPaediatricBox             Toggle    No
DefibrillatorType            Text      Yes
OperatingHours               Text      Yes
Notes                        Text      No
```

#### Step 3: Get Current Location Item (Before Update)

Add an action to retrieve the current Location item before updating:

1. Click **Add action** and search for "SharePoint"
2. Select **Get item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerOutputs()['body']['LocationId']
     ```
4. Rename this action to "GetCurrentLocation"

#### Step 4: Create Object for Old Values

Add a **Compose** action to capture old values:

```
Name: OldValuesCompose

Output:
{
  "Title": "@{body('GetCurrentLocation')?['Title']}",
  "DisplayName": "@{body('GetCurrentLocation')?['DisplayName']}",
  "Building": "@{body('GetCurrentLocation')?['Building']}",
  "Level": "@{body('GetCurrentLocation')?['Level']}",
  "SpecificLocation": "@{body('GetCurrentLocation')?['SpecificLocation']}",
  "TrolleyType": "@{body('GetCurrentLocation')?['TrolleyType']}",
  "HasPaedBox": "@{body('GetCurrentLocation')?['HasPaedBox']}",
  "DefibrillatorType": "@{body('GetCurrentLocation')?['DefibrillatorType']}",
  "OperatingHours": "@{body('GetCurrentLocation')?['OperatingHours']}"
}
```

#### Step 5: Update Location Item

1. Click **Add action** and search for "SharePoint"
2. Select **Update item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerOutputs()['body']['LocationId']
     ```
   - **Title:**
     ```
     triggerOutputs()['body']['Department_Name']
     ```
   - **DisplayName:**
     ```
     triggerOutputs()['body']['DisplayName']
     ```
   - **Building:**
     ```
     triggerOutputs()['body']['Building']
     ```
   - **Level:**
     ```
     triggerOutputs()['body']['Level']
     ```
   - **SpecificLocation:**
     ```
     triggerOutputs()['body']['SpecificLocation']
     ```
   - **TrolleyType:**
     ```
     triggerOutputs()['body']['TrolleyType']
     ```
   - **HasPaedBox:**
     ```
     triggerOutputs()['body']['HasPaediatricBox']
     ```
   - **DefibrillatorType:**
     ```
     triggerOutputs()['body']['DefibrillatorType']
     ```
   - **OperatingHours:**
     ```
     triggerOutputs()['body']['OperatingHours']
     ```
   - **Notes:**
     ```
     triggerOutputs()['body']['Notes']
     ```
4. Rename this action to "UpdateLocation"

#### Step 6: Create Object for New Values

Add another **Compose** action:

```
Name: NewValuesCompose

Output:
{
  "Title": "@{triggerOutputs()['body']['Department_Name']}",
  "DisplayName": "@{triggerOutputs()['body']['DisplayName']}",
  "Building": "@{triggerOutputs()['body']['Building']}",
  "Level": "@{triggerOutputs()['body']['Level']}",
  "SpecificLocation": "@{triggerOutputs()['body']['SpecificLocation']}",
  "TrolleyType": "@{triggerOutputs()['body']['TrolleyType']}",
  "HasPaedBox": "@{triggerOutputs()['body']['HasPaediatricBox']}",
  "DefibrillatorType": "@{triggerOutputs()['body']['DefibrillatorType']}",
  "OperatingHours": "@{triggerOutputs()['body']['OperatingHours']}"
}
```

#### Step 7: Determine Changed Fields

Add a **Compose** action to identify which fields changed:

```
Name: ChangedFieldsList

Expression: (use a complex expression to compare old vs new values)

// This is a simplified example - in practice, use a larger expression:
if(
  equals(body('GetCurrentLocation')?['Title'], triggerOutputs()['body']['Department_Name']),
  '',
  'Title'
)
```

For this task, you can simplify by using:

```
Building;Level;SpecificLocation;TrolleyType;DefibrillatorType;OperatingHours;HasPaedBox
(Note: In Task 2.2.4, we'll implement more sophisticated change detection)
```

#### Step 8: Return Success Status

Add a **Return value** action:

```json
{
  "LocationId": "@{triggerOutputs()['body']['LocationId']}",
  "Status": "Updated",
  "OldValues": "@{outputs('OldValuesCompose')}",
  "NewValues": "@{outputs('NewValuesCompose')}"
}
```

#### Step 9: Add Error Handling

Wrap the Update action in a **Scope** and add error handler:

```
Scope Name: UpdateScope

Error Handler (when UpdateScope fails):
- Send email with error details
- Return error status to PowerApp
```

### PowerFx Code (PowerApp Integration)

In the PowerApp "Trolley Detail" screen edit mode:

```powerfx
// Button "SaveChanges" OnSelect event
If(
    Validate_EditTrolleyForm(),
    Launch_UpdateTrolley_Flow(),
    Notify("Please fix validation errors before saving", NotificationType.Error)
);

// Function: Launch_UpdateTrolley_Flow
Function Launch_UpdateTrolley_Flow()
    Set(
        varUpdateResult,
        'UpdateTrolley_Flow'.Run(
            varCurrentLocationId,
            TrolleyTitle_Edit.Value,
            DisplayName_Edit.Value,
            ServiceLine_Lookup_Edit.Selected.ID,
            Building_Dropdown_Edit.Value,
            Level_Edit.Value,
            SpecificLocation_Edit.Value,
            TrolleyType_Dropdown_Edit.Value,
            HasPaediatricBox_Edit.Value,
            DefibrillatorType_Dropdown_Edit.Value,
            OperatingHours_Dropdown_Edit.Value,
            Notes_Edit.Value
        )
    );

    If(
        varUpdateResult.Status = "Updated",
        Notify("Trolley updated successfully", NotificationType.Success);
        // Trigger log flow to record the change (Task 2.2.4)
        Refresh(Location);
        Set(varEditMode, false),
        Notify("Failed to update trolley", NotificationType.Error)
    )
End;
```

### Testing Procedures

#### Test 1: Basic Trolley Update
1. Open PowerApp and navigate to existing trolley
2. Change fields:
   - Building: "Ned Hanlon Building"
   - Level: "Ground"
   - Notes: "Updated for new location"
3. Click "Save Changes"
4. Verify:
   - Flow executes successfully
   - Success notification displays
   - LocationChangeLog entry created (Task 2.2.4)
   - Changes visible in SharePoint

#### Test 2: Update with Optional Fields
1. Open trolley with blank SpecificLocation
2. Add value: "Bay 3, Room 412"
3. Update trolley
4. Verify:
   - Optional fields handled correctly
   - LocationChangeLog shows field change

#### Test 3: No Changes Scenario
1. Open trolley detail
2. Don't make any changes
3. Click "Save Changes"
4. Verify:
   - Update still succeeds (no-op)
   - LocationChangeLog entry created (or optional check)

#### Test 4: Concurrent Updates
1. Open same trolley in two browser windows
2. Edit different fields in each window
3. Save from window 1, then window 2
4. Verify:
   - Last update wins (standard SharePoint behavior)
   - LocationChangeLog captures both updates

#### Test 5: Error Handling
1. Modify flow to use invalid Location ID
2. Attempt update
3. Verify:
   - Error handler executes
   - Email notification sent
   - Error returned to PowerApp

### Verification Checklist

- [ ] Flow created and named "UpdateTrolley_Flow"
- [ ] PowerApp trigger includes LocationId input
- [ ] GetCurrentLocation retrieves item before update
- [ ] OldValuesCompose captures pre-update state
- [ ] UpdateLocation action correctly updates all fields
- [ ] NewValuesCompose captures post-update state
- [ ] ChangedFieldsList identifies modified fields
- [ ] Return value includes old/new values
- [ ] Error handler implemented
- [ ] PowerApp successfully calls flow
- [ ] Flow returns status to PowerApp
- [ ] Changes reflected in SharePoint
- [ ] Optional fields handled correctly
- [ ] Concurrent update handling verified

---

## Task 2.2.4: Create Log Trolley Update Flow

### Objective

Build a Power Automate flow triggered after trolley update that logs the modification event to LocationChangeLog with ChangeType "Updated", capturing both old and new values for all changed fields.

### Prerequisites

- UpdateTrolley_Flow completed (Task 2.2.3)
- LocationChangeLog list created
- Location record successfully updated

### Flow Architecture

```
UpdateTrolley_Flow Completion
          ↓
  Log Update Event Trigger
          ↓
  Compare Old vs New Values
          ↓
  Identify Changed Fields
          ↓
  Create LocationChangeLog Entry
          ↓
      Flow Complete
```

### Step-by-Step Implementation

#### Step 1: Create Automated Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Automated cloud flow**
3. Name the flow: `LogTrolleyUpdate_Flow`
4. Trigger: Select **When an item is modified** (SharePoint)
5. Click **Create**

#### Step 2: Configure SharePoint Trigger

In the trigger section:
- **Site Address:** the REdI Trolley Audit SharePoint site
- **List Name:** Location

#### Step 3: Add Condition to Exclude Creation Events

Add a **Condition** to ensure we only log updates, not creations:

```
Condition:
IF DateTimeCreated != LastModified (within 1 minute)
THEN: This is an update, proceed
ELSE: This is a creation, skip (handled by Task 2.2.2)
```

Expression format:
```
not(equals(triggerBody()?['Created'], triggerBody()?['Modified']))
```

#### Step 4: Get Previous Version of Item

Add an action to retrieve the previous version:

1. Click **Add action** and search for "SharePoint"
2. Select **Get item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerBody()?['ID']
     ```
4. Rename to "GetPreviousVersion"

Note: This gets the current version. To get the true previous version, you would need to use SharePoint version history API or maintain a separate history log.

#### Step 5: Generate Change Reference

Add a **Compose** action:

```
Name: GenerateChangeReference

Output:
concat('CHGLOC-', formatDateTime(utcNow(), 'yyyyMMdd'), '-', triggerBody()?['ID'])
```

#### Step 6: Build Old Values Object

This is complex since we need to compare with stored state. For this implementation, we'll capture the current values as "old" and require manual intervention for precise change detection. A better approach uses a separate tracking flow, but for Phase 2.2, we'll use available data:

Add a **Compose** action:

```
Name: OldValuesCompose

Output:
{
  "Title": "@{body('GetPreviousVersion')?['Title']}",
  "DisplayName": "@{body('GetPreviousVersion')?['DisplayName']}",
  "Building": "@{body('GetPreviousVersion')?['Building']}",
  "Level": "@{body('GetPreviousVersion')?['Level']}",
  "TrolleyType": "@{body('GetPreviousVersion')?['TrolleyType']}"
}
```

#### Step 7: Build New Values Object

Add another **Compose** action:

```
Name: NewValuesCompose

Output:
{
  "Title": "@{triggerBody()?['Title']}",
  "DisplayName": "@{triggerBody()?['DisplayName']}",
  "Building": "@{triggerBody()?['Building']}",
  "Level": "@{triggerBody()?['Level']}",
  "TrolleyType": "@{triggerBody()?['TrolleyType']}"
}
```

#### Step 8: Identify Changed Fields

Add a **Compose** action using complex expressions:

```
Name: IdentifyChangedFields

Output: (This requires multiple conditions - simplified below)

// Simplified: Build a string of changed fields
if(
  not(equals(body('GetPreviousVersion')?['Title'], triggerBody()?['Title'])),
  'Title;',
  ''
)
+
if(
  not(equals(body('GetPreviousVersion')?['Building'], triggerBody()?['Building'])),
  'Building;',
  ''
)
+
if(
  not(equals(body('GetPreviousVersion')?['Level'], triggerBody()?['Level'])),
  'Level;',
  ''
)
+ 'etc...'
```

In practice, you can use a simplified version that lists common fields changed and let the detailed view be in OldValues/NewValues JSON.

#### Step 9: Create LocationChangeLog Entry

1. Click **Add action** and search for "SharePoint"
2. Select **Create item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** LocationChangeLog
   - **Title:**
     ```
     outputs('GenerateChangeReference')
     ```
   - **Location (ID):**
     ```
     triggerBody()?['ID']
     ```
   - **ChangeType:**
     ```
     Updated
     ```
   - **ChangeDateTime:**
     ```
     utcNow()
     ```
   - **ChangedBy:**
     ```
     triggerBody()?['Editor']['claims']['aud']
     ```
   - **FieldsChanged:**
     ```
     outputs('IdentifyChangedFields')
     ```
   - **OldValues:**
     ```
     outputs('OldValuesCompose')
     ```
   - **NewValues:**
     ```
     outputs('NewValuesCompose')
     ```
   - **ChangeReason:**
     ```
     (leave blank or use a reason from the update payload if available)
     ```

#### Step 10: Add Error Handling

Wrap the Create LocationChangeLog action in a **Scope**:

```
Scope Name: LogUpdateScope

If LogUpdateScope fails:
- Send email notification to MERT
- Log error to SharePoint diagnostics list (optional)
```

### Flow Expression Reference

**Compare Two Fields for Equality:**
```
equals(body('GetPreviousVersion')?['Building'], triggerBody()?['Building'])
```

**Concatenate Multiple Field Changes:**
```
concat(
  if(not(equals(old_value, new_value)), 'FieldName;', ''),
  if(not(equals(old_value, new_value)), 'FieldName;', '')
)
```

**Extract Modified By User:**
```
triggerBody()?['Editor']['email']
```

### Testing Procedures

#### Test 1: Update Single Field
1. Open trolley in PowerApp
2. Change Building field only
3. Save
4. Verify in LocationChangeLog:
   - ChangeType = "Updated"
   - FieldsChanged includes "Building"
   - OldValues shows previous building
   - NewValues shows new building
   - Other fields show old values in both (unchanged)

#### Test 2: Update Multiple Fields
1. Change Building, Level, and TrolleyType
2. Save
3. Verify in LocationChangeLog:
   - FieldsChanged lists all three changed fields
   - OldValues and NewValues show all fields
   - Only changed fields differ

#### Test 3: Update with No Actual Changes
1. Open trolley
2. Don't make changes
3. Save
4. Verify:
   - LocationChangeLog entry may be created (depends on implementation)
   - Or entry not created if "no changes" detected

#### Test 4: Rapid Successive Updates
1. Update trolley three times in quick succession (within 1 minute)
2. Verify in LocationChangeLog:
   - All three update events logged separately
   - Each has correct change reference
   - Each shows appropriate old/new values

#### Test 5: Update with Special Characters
1. Change a field to include special characters
2. Save
3. Verify:
   - JSON in OldValues/NewValues properly escaped
   - No truncation of special characters

### Verification Checklist

- [ ] Flow created and named "LogTrolleyUpdate_Flow"
- [ ] SharePoint trigger configured for Location list
- [ ] Condition excludes creation events
- [ ] GetPreviousVersion retrieves correct item
- [ ] Change reference generated correctly
- [ ] OldValuesCompose captures pre-update state
- [ ] NewValuesCompose captures post-update state
- [ ] IdentifyChangedFields lists modified fields
- [ ] LocationChangeLog entry created with ChangeType "Updated"
- [ ] ChangedBy captures user who made update
- [ ] OldValues and NewValues JSON properly formatted
- [ ] Error handler sends notification on failure
- [ ] Flow triggers within 30 seconds of update
- [ ] All changed fields correctly identified

---

## Task 2.2.5: Create Deactivate Trolley Flow

### Objective

Build a Power Automate flow triggered from the PowerApp that sets a Location's Status to "Inactive" and captures the deactivation reason provided by the user.

### Prerequisites

- Location record exists
- PowerApp "Deactivate Trolley" dialog completed (Task 2.1.15)
- User has edit permissions to Location list

### Flow Architecture

```
PowerApp (Deactivate Dialog)
          ↓
  Cloud Flow Trigger
          ↓
  Capture Deactivation Reason
          ↓
  Set Status to Inactive
          ↓
  Record Decommission Date
          ↓
  Return Status
```

### Step-by-Step Implementation

#### Step 1: Create Cloud Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Instant cloud flow** (button-triggered)
3. Name the flow: `DeactivateTrolley_Flow`
4. Trigger: Select **PowerApps (V2)**
5. Click **Create**

#### Step 2: Configure PowerApp Trigger Input Parameters

Add the following inputs:

```
Input Name                    Type      Required
LocationId                   Text      Yes
DeactivationReason           Text      Yes
```

#### Step 3: Get Current Location Item

Add an action to retrieve the location:

1. Click **Add action** and search for "SharePoint"
2. Select **Get item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerOutputs()['body']['LocationId']
     ```
4. Rename to "GetCurrentLocation"

#### Step 4: Update Location - Set Inactive

1. Click **Add action** and search for "SharePoint"
2. Select **Update item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerOutputs()['body']['LocationId']
     ```
   - **Status:**
     ```
     Inactive
     ```
   - **DecommissionedDate:**
     ```
     utcNow()
     ```
   - **Notes:**
     ```
     concat(
       'DEACTIVATED ',
       formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm'),
       ' - Reason: ',
       triggerOutputs()['body']['DeactivationReason'],
       ' - ',
       body('GetCurrentLocation')?['Notes']
     )
     ```

Note: The Notes field is appended with deactivation info to maintain history.

#### Step 5: Return Success Status

Add a **Return value** action:

```json
{
  "LocationId": "@{triggerOutputs()['body']['LocationId']}",
  "Status": "Deactivated",
  "DeactivationDate": "@{utcNow()}",
  "DeactivationReason": "@{triggerOutputs()['body']['DeactivationReason']}"
}
```

#### Step 6: Add Confirmation Email

Add a **Send an email notification** action:

```
To: MERT team distribution list
Subject: Trolley Deactivated - @{body('GetCurrentLocation')?['Title']}
Body:
Trolley Location: @{body('GetCurrentLocation')?['Title']}
Service Line: @{body('GetCurrentLocation')?['ServiceLine']['DisplayValue']}
Building: @{body('GetCurrentLocation')?['Building']}
Deactivation Reason: @{triggerOutputs()['body']['DeactivationReason']}
Deactivated By: @{User().FullName}
Date: @{utcNow()}
```

#### Step 7: Add Error Handling

Wrap the Update action in a **Scope** named "DeactivateScope":

```
Error Handler:
- Send email to MERT with error details
- Return error status to PowerApp
```

### PowerFx Code (PowerApp Integration)

In the PowerApp "Trolley Detail" screen, in the Deactivate button's OnSelect:

```powerfx
// Launch deactivation with reason dialog
Set(varShowDeactivateDialog, true);

// In Deactivation Dialog - Submit button OnSelect
If(
    Not(IsBlank(DeactivationReason_Input.Value)),
    Launch_DeactivateTrolley_Flow(),
    Notify("Please provide a deactivation reason", NotificationType.Error)
);

// Function: Launch_DeactivateTrolley_Flow
Function Launch_DeactivateTrolley_Flow()
    Set(
        varDeactivateResult,
        'DeactivateTrolley_Flow'.Run(
            varCurrentLocationId,
            DeactivationReason_Input.Value
        )
    );

    If(
        varDeactivateResult.Status = "Deactivated",
        Notify(
            "Trolley deactivated successfully. Reason: " &
            varDeactivateResult.DeactivationReason,
            NotificationType.Success
        );
        Refresh(Location);
        Set(varShowDeactivateDialog, false);
        Navigate(TrolleysScreen, ScreenTransition.Fade),
        Notify("Failed to deactivate trolley", NotificationType.Error)
    )
End;
```

### Testing Procedures

#### Test 1: Deactivate with Reason
1. Open PowerApp and navigate to active trolley
2. Click "Deactivate Trolley"
3. Enter reason: "Relocated to different site"
4. Confirm
5. Verify:
   - Flow executes successfully
   - Status changed to "Inactive" in SharePoint
   - DecommissionedDate set to current date
   - Notes updated with deactivation info
   - Confirmation email sent to MERT
   - LocationChangeLog entry created (Task 2.2.6)

#### Test 2: Deactivate Without Reason
1. Click "Deactivate Trolley"
2. Leave reason blank
3. Click "Confirm"
4. Verify:
   - Validation prevents flow execution
   - Error notification displays

#### Test 3: Deactivation Reason Preserved in Notes
1. Deactivate trolley with reason: "Equipment failure, awaiting repair"
2. Re-open trolley in SharePoint
3. Verify Notes field contains:
   - Original notes (if any)
   - "DEACTIVATED" timestamp
   - Deactivation reason

#### Test 4: Verify Status Change in UI
1. Deactivate trolley via PowerApp
2. Verify trolley removed from "Active Trolleys" view
3. Verify trolley appears in "Inactive Trolleys" view (if available)

#### Test 5: Error Handling
1. Modify flow to use invalid LocationId
2. Attempt deactivation
3. Verify:
   - Error handler executes
   - Email notification sent
   - Error returned to PowerApp

### Verification Checklist

- [ ] Flow created and named "DeactivateTrolley_Flow"
- [ ] PowerApp trigger includes LocationId and DeactivationReason
- [ ] GetCurrentLocation retrieves correct item
- [ ] UpdateLocation sets Status to "Inactive"
- [ ] DecommissionedDate set to current date
- [ ] Deactivation reason appended to Notes
- [ ] Return value includes deactivation date and reason
- [ ] Confirmation email sent to MERT
- [ ] Email includes trolley name and reason
- [ ] Error handler implemented
- [ ] PowerApp validation prevents empty reason
- [ ] Status change visible in SharePoint
- [ ] LocationChangeLog entry created

---

## Task 2.2.6: Create Log Deactivation Flow

### Objective

Build a Power Automate flow triggered after trolley deactivation that logs the event to LocationChangeLog with ChangeType "Deactivated" and captures the deactivation reason.

### Prerequisites

- DeactivateTrolley_Flow completed (Task 2.2.5)
- LocationChangeLog list created
- Location Status successfully changed to "Inactive"

### Flow Architecture

```
DeactivateTrolley_Flow Completion
          ↓
  Log Deactivation Event Trigger
          ↓
  Generate Change Reference
          ↓
  Create LocationChangeLog Entry
          ↓
  Notify Supervisors
          ↓
      Flow Complete
```

### Step-by-Step Implementation

#### Step 1: Create Automated Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Automated cloud flow**
3. Name the flow: `LogDeactivation_Flow`
4. Trigger: Select **When an item is modified** (SharePoint)
5. Click **Create**

#### Step 2: Configure SharePoint Trigger

In the trigger section:
- **Site Address:** the REdI Trolley Audit SharePoint site
- **List Name:** Location

#### Step 3: Add Condition for Status Change to Inactive

Add a **Condition**:

```
IF Status = "Inactive" AND Status != Previous Status
THEN: Log deactivation
ELSE: Terminate flow
```

Expression:
```
equals(triggerBody()?['Status'], 'Inactive')
```

#### Step 4: Get Previous Version for Comparison

Add a **Get item** action to retrieve the location:

```
Site Address: the REdI Trolley Audit SharePoint site
List Name: Location
ID: triggerBody()?['ID']
```

Note: This gets current state; for true previous state, additional logic needed.

#### Step 5: Generate Change Reference

Add a **Compose** action:

```
Name: GenerateChangeReference

Output:
concat('CHGLOC-', formatDateTime(utcNow(), 'yyyyMMdd'), '-', triggerBody()?['ID'])
```

#### Step 6: Extract Deactivation Reason from Notes

Add a **Compose** action to parse deactivation reason:

```
Name: ExtractDeactivationReason

Output: (Extract text after "Reason: " in Notes field)

// This is a simplified extraction
substring(
  triggerBody()?['Notes'],
  indexOf(triggerBody()?['Notes'], 'Reason: ') + 8,
  indexOf(triggerBody()?['Notes'], ' - ') - indexOf(triggerBody()?['Notes'], 'Reason: ') - 8
)
```

#### Step 7: Build Old Values Object

Add a **Compose** action:

```
Name: OldValuesCompose

Output:
{
  "Status": "Active",
  "Title": "@{triggerBody()?['Title']}",
  "DecommissionedDate": ""
}
```

#### Step 8: Build New Values Object

Add a **Compose** action:

```
Name: NewValuesCompose

Output:
{
  "Status": "Inactive",
  "Title": "@{triggerBody()?['Title']}",
  "DecommissionedDate": "@{triggerBody()?['DecommissionedDate']}"
}
```

#### Step 9: Create LocationChangeLog Entry

1. Click **Add action** and search for "SharePoint"
2. Select **Create item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** LocationChangeLog
   - **Title:**
     ```
     outputs('GenerateChangeReference')
     ```
   - **Location (ID):**
     ```
     triggerBody()?['ID']
     ```
   - **ChangeType:**
     ```
     Deactivated
     ```
   - **ChangeDateTime:**
     ```
     utcNow()
     ```
   - **ChangedBy:**
     ```
     triggerBody()?['Editor']['email']
     ```
   - **FieldsChanged:**
     ```
     Status;DecommissionedDate
     ```
   - **OldValues:**
     ```
     outputs('OldValuesCompose')
     ```
   - **NewValues:**
     ```
     outputs('NewValuesCompose')
     ```
   - **ChangeReason:**
     ```
     outputs('ExtractDeactivationReason')
     ```

#### Step 10: Send Notification to Service Line Manager

Add an **Send an email notification** action:

```
To: (Service Line Manager - from Location lookup)
Subject: Trolley Deactivated - @{triggerBody()?['Title']}
Body:
The following trolley location has been deactivated:

Department: @{triggerBody()?['Title']}
Service Line: @{triggerBody()?['ServiceLineId']['DisplayValue']}
Building: @{triggerBody()?['Building']}
Level: @{triggerBody()?['Level']}

Deactivation Date: @{triggerBody()?['DecommissionedDate']}
Deactivation Reason: @{outputs('ExtractDeactivationReason')}
Deactivated By: @{triggerBody()?['Editor']['DisplayName']}

Please update your records accordingly.
```

#### Step 11: Add Error Handling

Wrap the Create LocationChangeLog action in a **Scope**:

```
If logging fails:
- Send error notification
- Log error details
```

### Testing Procedures

#### Test 1: Log Deactivation Event
1. Deactivate trolley via PowerApp (Task 2.2.5)
2. Wait 10-15 seconds
3. Verify in LocationChangeLog:
   - New entry with ChangeType "Deactivated"
   - Change Reference auto-generated
   - ChangeDateTime matches deactivation
   - ChangedBy shows user who deactivated
   - ChangeReason contains deactivation reason from notes
   - OldValues shows Status: "Active"
   - NewValues shows Status: "Inactive"

#### Test 2: Email Notification
1. Deactivate trolley with reason: "Under maintenance"
2. Verify email sent to:
   - Service Line manager (if available)
   - Or MERT team distribution list
3. Email contains:
   - Trolley name, service line, building
   - Deactivation reason
   - User who deactivated

#### Test 3: Manual Deactivation in SharePoint
1. Open Location list in SharePoint
2. Manually change Status to "Inactive"
3. Verify:
   - LogDeactivation_Flow triggers
   - LocationChangeLog entry created
   - Email sent

#### Test 4: Deactivation Reason with Special Characters
1. Deactivate with reason: "Equipment failure: pump needs O/H & calibration"
2. Verify:
   - Reason extracted and stored correctly
   - JSON properly escaped in ChangeReason field

#### Test 5: Error Handling
1. Temporarily disconnect SharePoint connector
2. Deactivate trolley
3. Verify:
   - Error handler executes
   - Notification sent
   - Trolley still deactivated (separate from this flow)

### Verification Checklist

- [ ] Flow created and named "LogDeactivation_Flow"
- [ ] SharePoint trigger configured for Location list
- [ ] Condition correctly detects Status change to "Inactive"
- [ ] Change reference generated in correct format
- [ ] Deactivation reason extracted from Notes
- [ ] LocationChangeLog entry created with ChangeType "Deactivated"
- [ ] ChangedBy captures user who deactivated
- [ ] OldValues shows Status as "Active"
- [ ] NewValues shows Status as "Inactive"
- [ ] ChangeReason contains deactivation reason
- [ ] Email notification sent to Service Line manager
- [ ] Email includes all required information
- [ ] Error handler sends notification on failure
- [ ] Flow triggers within 30 seconds of deactivation
- [ ] Manual deactivation in SharePoint also triggers logging

---

## Task 2.2.7: Create Reactivate Trolley Flow

### Objective

Build a Power Automate flow triggered from the PowerApp that sets a Location's Status back to "Active".

### Prerequisites

- Location record exists with Status "Inactive"
- PowerApp "Reactivate Trolley" dialog completed (Task 2.1.16)
- User has edit permissions to Location list

### Flow Architecture

```
PowerApp (Reactivate Dialog)
          ↓
  Cloud Flow Trigger
          ↓
  Set Status to Active
          ↓
  Clear DecommissionedDate
          ↓
  Return Status
```

### Step-by-Step Implementation

#### Step 1: Create Cloud Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Instant cloud flow** (button-triggered)
3. Name the flow: `ReactivateTrolley_Flow`
4. Trigger: Select **PowerApps (V2)**
5. Click **Create**

#### Step 2: Configure PowerApp Trigger Input Parameters

Add the following inputs:

```
Input Name                    Type      Required
LocationId                   Text      Yes
```

#### Step 3: Get Current Location Item

Add an action to retrieve the location:

1. Click **Add action** and search for "SharePoint"
2. Select **Get item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerOutputs()['body']['LocationId']
     ```
4. Rename to "GetCurrentLocation"

#### Step 4: Update Location - Set Active

1. Click **Add action** and search for "SharePoint"
2. Select **Update item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** Location
   - **ID:**
     ```
     triggerOutputs()['body']['LocationId']
     ```
   - **Status:**
     ```
     Active
     ```
   - **DecommissionedDate:**
     ```
     (leave blank or set to null using dynamic content)
     ```

#### Step 5: Return Success Status

Add a **Return value** action:

```json
{
  "LocationId": "@{triggerOutputs()['body']['LocationId']}",
  "Status": "Reactivated",
  "ReactivationDate": "@{utcNow()}"
}
```

#### Step 6: Add Confirmation Email

Add a **Send an email notification** action:

```
To: MERT team distribution list
Subject: Trolley Reactivated - @{body('GetCurrentLocation')?['Title']}
Body:
Trolley Location: @{body('GetCurrentLocation')?['Title']}
Service Line: @{body('GetCurrentLocation')?['ServiceLine']['DisplayValue']}
Building: @{body('GetCurrentLocation')?['Building']}
Reactivation Date: @{utcNow()}
Reactivated By: @{User().FullName}
```

#### Step 7: Add Error Handling

Wrap the Update action in a **Scope** named "ReactivateScope":

```
Error Handler:
- Send email to MERT with error details
- Return error status to PowerApp
```

### PowerFx Code (PowerApp Integration)

In the PowerApp "Trolley Detail" screen, in the Reactivate button's OnSelect:

```powerfx
// Launch reactivation confirmation dialog
Set(varShowReactivateDialog, true);

// In Reactivation Dialog - Confirm button OnSelect
If(
    varCurrentLocationStatus = "Inactive",
    Launch_ReactivateTrolley_Flow(),
    Notify("Only inactive trolleys can be reactivated", NotificationType.Error)
);

// Function: Launch_ReactivateTrolley_Flow
Function Launch_ReactivateTrolley_Flow()
    Set(
        varReactivateResult,
        'ReactivateTrolley_Flow'.Run(
            varCurrentLocationId
        )
    );

    If(
        varReactivateResult.Status = "Reactivated",
        Notify(
            "Trolley reactivated successfully",
            NotificationType.Success
        );
        Refresh(Location);
        Set(varShowReactivateDialog, false);
        Navigate(TrolleysScreen, ScreenTransition.Fade),
        Notify("Failed to reactivate trolley", NotificationType.Error)
    )
End;
```

### Testing Procedures

#### Test 1: Reactivate Inactive Trolley
1. Open PowerApp and navigate to inactive trolley
2. Click "Reactivate Trolley"
3. Confirm reactivation
4. Verify:
   - Flow executes successfully
   - Status changed to "Active" in SharePoint
   - DecommissionedDate cleared
   - Confirmation email sent to MERT
   - LocationChangeLog entry created (Task 2.2.8)

#### Test 2: Prevent Reactivation of Active Trolley
1. Open active trolley
2. Verify "Reactivate" button is disabled or hidden
3. Or if button visible, clicking should show error message

#### Test 3: Reactivation Makes Trolley Visible in Active View
1. Reactivate trolley via PowerApp
2. Navigate to Location list "Active Trolleys" view
3. Verify trolley now appears in active view

#### Test 4: Email Notification Content
1. Reactivate trolley
2. Verify email received contains:
   - Trolley name
   - Service line and building
   - Reactivation date
   - User who reactivated

#### Test 5: Error Handling
1. Modify flow to use invalid LocationId
2. Attempt reactivation
3. Verify:
   - Error handler executes
   - Email notification sent
   - Error returned to PowerApp

### Verification Checklist

- [ ] Flow created and named "ReactivateTrolley_Flow"
- [ ] PowerApp trigger includes LocationId
- [ ] GetCurrentLocation retrieves correct item
- [ ] UpdateLocation sets Status to "Active"
- [ ] DecommissionedDate cleared
- [ ] Return value includes reactivation date
- [ ] Confirmation email sent to MERT
- [ ] Email includes trolley name and date
- [ ] Error handler implemented
- [ ] PowerApp prevents reactivation of active trolleys
- [ ] Status change visible in SharePoint
- [ ] LocationChangeLog entry created

---

## Task 2.2.8: Create Log Reactivation Flow

### Objective

Build a Power Automate flow triggered after trolley reactivation that logs the event to LocationChangeLog with ChangeType "Reactivated".

### Prerequisites

- ReactivateTrolley_Flow completed (Task 2.2.7)
- LocationChangeLog list created
- Location Status successfully changed to "Active"

### Flow Architecture

```
ReactivateTrolley_Flow Completion
          ↓
  Log Reactivation Event Trigger
          ↓
  Generate Change Reference
          ↓
  Create LocationChangeLog Entry
          ↓
  Notify Supervisors
          ↓
      Flow Complete
```

### Step-by-Step Implementation

#### Step 1: Create Automated Flow in Power Automate

1. Navigate to https://make.powerautomate.com
2. Click **Create** → **Cloud flow** → **Automated cloud flow**
3. Name the flow: `LogReactivation_Flow`
4. Trigger: Select **When an item is modified** (SharePoint)
5. Click **Create**

#### Step 2: Configure SharePoint Trigger

In the trigger section:
- **Site Address:** the REdI Trolley Audit SharePoint site
- **List Name:** Location

#### Step 3: Add Condition for Status Change to Active

Add a **Condition**:

```
IF Status = "Active" AND Previous Status = "Inactive"
THEN: Log reactivation
ELSE: Terminate flow
```

Expression:
```
equals(triggerBody()?['Status'], 'Active')
```

#### Step 4: Get Location Details

Add a **Get item** action:

```
Site Address: the REdI Trolley Audit SharePoint site
List Name: Location
ID: triggerBody()?['ID']
```

#### Step 5: Generate Change Reference

Add a **Compose** action:

```
Name: GenerateChangeReference

Output:
concat('CHGLOC-', formatDateTime(utcNow(), 'yyyyMMdd'), '-', triggerBody()?['ID'])
```

#### Step 6: Build Old Values Object

Add a **Compose** action:

```
Name: OldValuesCompose

Output:
{
  "Status": "Inactive",
  "Title": "@{triggerBody()?['Title']}",
  "DecommissionedDate": "@{triggerBody()?['DecommissionedDate']}"
}
```

#### Step 7: Build New Values Object

Add a **Compose** action:

```
Name: NewValuesCompose

Output:
{
  "Status": "Active",
  "Title": "@{triggerBody()?['Title']}",
  "DecommissionedDate": ""
}
```

#### Step 8: Create LocationChangeLog Entry

1. Click **Add action** and search for "SharePoint"
2. Select **Create item**
3. Configure:
   - **Site Address:** the REdI Trolley Audit SharePoint site
   - **List Name:** LocationChangeLog
   - **Title:**
     ```
     outputs('GenerateChangeReference')
     ```
   - **Location (ID):**
     ```
     triggerBody()?['ID']
     ```
   - **ChangeType:**
     ```
     Reactivated
     ```
   - **ChangeDateTime:**
     ```
     utcNow()
     ```
   - **ChangedBy:**
     ```
     triggerBody()?['Editor']['email']
     ```
   - **FieldsChanged:**
     ```
     Status;DecommissionedDate
     ```
   - **OldValues:**
     ```
     outputs('OldValuesCompose')
     ```
   - **NewValues:**
     ```
     outputs('NewValuesCompose')
     ```
   - **ChangeReason:**
     ```
     Trolley location reactivated
     ```

#### Step 9: Send Notification to Service Line Manager

Add an **Send an email notification** action:

```
To: (Service Line Manager from Location)
Subject: Trolley Reactivated - @{triggerBody()?['Title']}
Body:
The following trolley location has been reactivated:

Department: @{triggerBody()?['Title']}
Service Line: @{triggerBody()?['ServiceLineId']['DisplayValue']}
Building: @{triggerBody()?['Building']}
Level: @{triggerBody()?['Level']}

Reactivation Date: @{utcNow()}
Reactivated By: @{triggerBody()?['Editor']['DisplayName']}

This location is now available for audits.
```

#### Step 10: Add Error Handling

Wrap the Create LocationChangeLog action in a **Scope**:

```
If logging fails:
- Send error notification
- Log error details
```

### Testing Procedures

#### Test 1: Log Reactivation Event
1. Reactivate trolley via PowerApp (Task 2.2.7)
2. Wait 10-15 seconds
3. Verify in LocationChangeLog:
   - New entry with ChangeType "Reactivated"
   - Change Reference auto-generated
   - ChangeDateTime matches reactivation time
   - ChangedBy shows user who reactivated
   - OldValues shows Status: "Inactive"
   - NewValues shows Status: "Active"
   - DecommissionedDate cleared in NewValues

#### Test 2: Email Notification
1. Reactivate trolley
2. Verify email sent to:
   - Service Line manager (if available)
   - Or MERT team distribution list
3. Email contains:
   - Trolley name, service line, building
   - Reactivation date and time
   - User who reactivated

#### Test 3: Manual Reactivation in SharePoint
1. Open Location list in SharePoint
2. Manually change Status to "Active" on inactive trolley
3. Verify:
   - LogReactivation_Flow triggers
   - LocationChangeLog entry created
   - Email sent

#### Test 4: LocationChangeLog Audit Trail
1. Deactivate trolley (creates entry with ChangeType "Deactivated")
2. Reactivate trolley (creates entry with ChangeType "Reactivated")
3. View LocationChangeLog for this trolley
4. Verify audit trail shows:
   - Deactivation event first
   - Reactivation event second
   - Both with timestamps and users

#### Test 5: Error Handling
1. Temporarily disconnect SharePoint connector
2. Reactivate trolley
3. Verify:
   - Error handler executes
   - Notification sent
   - Trolley still reactivated (separate from this flow)

### Verification Checklist

- [ ] Flow created and named "LogReactivation_Flow"
- [ ] SharePoint trigger configured for Location list
- [ ] Condition correctly detects Status change to "Active"
- [ ] Change reference generated in correct format
- [ ] LocationChangeLog entry created with ChangeType "Reactivated"
- [ ] ChangedBy captures user who reactivated
- [ ] OldValues shows Status as "Inactive"
- [ ] NewValues shows Status as "Active"
- [ ] DecommissionedDate cleared in NewValues
- [ ] Email notification sent to Service Line manager
- [ ] Email includes all required information
- [ ] Error handler sends notification on failure
- [ ] Flow triggers within 30 seconds of reactivation
- [ ] Manual reactivation in SharePoint also triggers logging
- [ ] Complete audit trail visible in LocationChangeLog

---

## Phase 2.2 Completion Checklist

### Task 2.2.1: Save New Trolley Flow
- [ ] Flow created and named "SaveNewTrolley_Flow"
- [ ] PowerApp trigger configured with all inputs
- [ ] Create Location item action correctly mapped
- [ ] Return value includes Location ID
- [ ] Error handler implemented
- [ ] PowerApp validation prevents invalid submissions
- [ ] All required fields enforced

### Task 2.2.2: Log New Trolley Change Flow
- [ ] Flow created and named "LogNewTrolley_Flow"
- [ ] SharePoint trigger configured for Location list
- [ ] Change reference generated in correct format
- [ ] LocationChangeLog entry created automatically
- [ ] ChangeType set to "Created"
- [ ] NewValues JSON populated correctly
- [ ] OldValues JSON empty for creation
- [ ] Error handler implemented

### Task 2.2.3: Update Trolley Flow
- [ ] Flow created and named "UpdateTrolley_Flow"
- [ ] PowerApp trigger includes LocationId
- [ ] GetCurrentLocation retrieves item before update
- [ ] OldValuesCompose captures pre-update state
- [ ] UpdateLocation correctly updates all fields
- [ ] NewValuesCompose captures post-update state
- [ ] Return value includes status
- [ ] Error handler implemented

### Task 2.2.4: Log Trolley Update Flow
- [ ] Flow created and named "LogTrolleyUpdate_Flow"
- [ ] SharePoint trigger configured for Location list
- [ ] Condition excludes creation events
- [ ] IdentifyChangedFields lists modified fields
- [ ] LocationChangeLog entry created with ChangeType "Updated"
- [ ] OldValues and NewValues JSON properly formatted
- [ ] Error handler implemented

### Task 2.2.5: Deactivate Trolley Flow
- [ ] Flow created and named "DeactivateTrolley_Flow"
- [ ] PowerApp trigger includes LocationId and DeactivationReason
- [ ] UpdateLocation sets Status to "Inactive"
- [ ] DecommissionedDate set to current date
- [ ] Deactivation reason appended to Notes
- [ ] Confirmation email sent to MERT
- [ ] Error handler implemented

### Task 2.2.6: Log Deactivation Flow
- [ ] Flow created and named "LogDeactivation_Flow"
- [ ] Condition detects Status change to "Inactive"
- [ ] LocationChangeLog entry created with ChangeType "Deactivated"
- [ ] ChangeReason contains deactivation reason
- [ ] Email sent to Service Line manager
- [ ] Error handler implemented

### Task 2.2.7: Reactivate Trolley Flow
- [ ] Flow created and named "ReactivateTrolley_Flow"
- [ ] PowerApp trigger includes LocationId
- [ ] UpdateLocation sets Status to "Active"
- [ ] DecommissionedDate cleared
- [ ] Confirmation email sent to MERT
- [ ] Error handler implemented

### Task 2.2.8: Log Reactivation Flow
- [ ] Flow created and named "LogReactivation_Flow"
- [ ] Condition detects Status change to "Active"
- [ ] LocationChangeLog entry created with ChangeType "Reactivated"
- [ ] OldValues shows Status as "Inactive"
- [ ] NewValues shows Status as "Active"
- [ ] Email sent to Service Line manager
- [ ] Error handler implemented

### End-to-End Testing
- [ ] Create new trolley and verify complete flow (Tasks 2.2.1-2.2.2)
- [ ] Update trolley and verify complete flow (Tasks 2.2.3-2.2.4)
- [ ] Deactivate trolley and verify complete flow (Tasks 2.2.5-2.2.6)
- [ ] Reactivate trolley and verify complete flow (Tasks 2.2.7-2.2.8)
- [ ] Verify LocationChangeLog audit trail shows all changes
- [ ] Verify all emails sent to appropriate recipients
- [ ] Verify error handling path works correctly

---

## Common Issues and Troubleshooting

### Issue: Flow Not Triggering from PowerApp

**Symptoms:** Click button in PowerApp but flow doesn't execute

**Solutions:**
1. Verify flow name matches exactly in PowerApp
2. Confirm flow is saved and published (not in draft status)
3. Check flow connector is authorized
4. Verify PowerApp has correct flow input parameters
5. Check browser console for errors (F12 developer tools)
6. Test flow manually from Power Automate first

### Issue: LocationChangeLog Entry Not Created

**Symptoms:** Flow executes but no entry in LocationChangeLog

**Solutions:**
1. Verify LocationChangeLog list exists and has correct name
2. Check SharePoint site address is correct
3. Confirm user has permissions to create items
4. Verify all required fields are populated in Create item action
5. Check for error in flow execution history
6. Manually create test entry to verify list functionality

### Issue: JSON Parsing Errors in OldValues/NewValues

**Symptoms:** JSON fields show malformed data or errors

**Solutions:**
1. Use JSON string encoding for special characters
2. Verify field values don't contain unescaped quotes
3. Use proper JSON object structure with proper commas
4. Test expressions in Power Automate designer first
5. Wrap expressions in json() function if needed

### Issue: Duplicate LocationChangeLog Entries

**Symptoms:** Multiple entries created for single trolley change

**Solutions:**
1. Add condition to check if entry already exists before creating
2. Implement "created or modified" vs "only modified" logic
3. Add delay between check and create to prevent race conditions
4. Review flow trigger conditions for duplicate execution

### Issue: Email Notifications Not Sending

**Symptoms:** Flow completes but email not received

**Solutions:**
1. Verify email address is correct
2. Check spam/junk folder
3. Verify user has permissions to send emails
4. Test with known good email address first
5. Check flow execution history for email action errors
6. Verify email connector is authorized

### Issue: User Information Not Captured Correctly

**Symptoms:** ChangedBy field shows incorrect user or system account

**Solutions:**
1. Use User Profile connector instead of trigger body claim
2. Add User() function if available
3. Configure Office 365 Users connector
4. Verify current user context in flow
5. Test in different browsers/clients

---

## Flow Implementation Checklist Summary

| Task | Flow Name | Trigger Type | Primary Action | ChangeLog Entry | Testing Status |
|------|-----------|--------------|-----------------|-----------------|---|
| 2.2.1 | SaveNewTrolley_Flow | PowerApp Button | Create Location | (Task 2.2.2) | Pending |
| 2.2.2 | LogNewTrolley_Flow | Item Created | Create ChangeLog | Created | Pending |
| 2.2.3 | UpdateTrolley_Flow | PowerApp Button | Update Location | (Task 2.2.4) | Pending |
| 2.2.4 | LogTrolleyUpdate_Flow | Item Modified | Create ChangeLog | Updated | Pending |
| 2.2.5 | DeactivateTrolley_Flow | PowerApp Button | Set Inactive | (Task 2.2.6) | Pending |
| 2.2.6 | LogDeactivation_Flow | Item Modified | Create ChangeLog | Deactivated | Pending |
| 2.2.7 | ReactivateTrolley_Flow | PowerApp Button | Set Active | (Task 2.2.8) | Pending |
| 2.2.8 | LogReactivation_Flow | Item Modified | Create ChangeLog | Reactivated | Pending |

---

## Next Steps

After completing Phase 2.2, proceed with:

### Phase 2.3: Audit Entry Screens (Tasks 2.3.1-2.3.22)
- Build audit selection screen
- Create documentation check screens
- Implement condition and equipment check screens

### Phase 2.5: Audit Submission (Tasks 2.5.1-2.5.15)
- Build review screen with compliance calculations
- Create Submit Audit flow to save all audit data
- Implement draft save functionality

### Phase 2.8: Issue Workflow Flows (Tasks 2.8.1-2.8.11)
- Build issue creation and assignment flows
- Implement issue resolution tracking
- Create escalation workflows

---

## Support and Reference

### Key Documentation

- REdI Trolley Audit Task List: `RBWH_Trolley_Audit_Task_List.md`
- Phase 1.6 PowerApp Foundation: `phase1_6_powerapp_foundation.md`
- SharePoint Location Schema: `sharepoint_schemas/Location.json`
- SharePoint LocationChangeLog Schema: `sharepoint_schemas/LocationChangeLog.json`

### External Resources

- Power Automate Documentation: https://docs.microsoft.com/power-automate/
- Power Apps Documentation: https://docs.microsoft.com/power-apps/
- SharePoint REST API: https://docs.microsoft.com/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service
- PowerFx Language Reference: https://docs.microsoft.com/power-platform/power-fx/

### MERT Contact Information

- **MERT Coordinator:** [Contact details to be updated]
- **IT Support:** [Contact details to be updated]
- **Documentation Lead:** [Contact details to be updated]

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Documentation Team | Initial implementation guide for Phase 2.2 |

---

**Document prepared for:** Royal Brisbane and Women's Hospital - MERT Program
**Document classification:** Internal - Implementation Guide
**Last updated:** January 2026
**Status:** Ready for Implementation

