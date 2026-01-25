# RBWH Trolley Audit System
## Phase 4.4 Deployment Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 4.4.1 - 4.4.8

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Task 4.4.1: User Guide Document](#task-441-user-guide-document)
3. [Task 4.4.2: Admin Guide Document](#task-442-admin-guide-document)
4. [Task 4.4.3-4.4.4: Training Videos](#task-443-444-training-videos)
5. [Task 4.4.5-4.4.6: Training Sessions](#task-445-446-training-sessions)
6. [Task 4.4.7: Production Permissions](#task-447-production-permissions)
7. [Task 4.4.8: Go-Live Deployment](#task-448-go-live-deployment)
8. [Appendices](#appendices)

---

## Executive Summary

Phase 4.4 is the final phase of the RBWH Trolley Audit system implementation. This phase transitions the fully-tested system from development to production, ensuring users are trained, permissions are properly configured, and support infrastructure is in place.

### Key Objectives

- Create comprehensive documentation for end users and administrators
- Deliver training through videos and live sessions
- Configure production-grade permissions and access controls
- Execute controlled go-live deployment
- Establish post-go-live monitoring and support

### Timeline & Resources

| Task | Duration | Resource |
|------|----------|----------|
| 4.4.1 - User Guide | 8 hours | Technical Writer |
| 4.4.2 - Admin Guide | 4 hours | System Administrator + Technical Writer |
| 4.4.3 - Auditor Video | 4 hours | Training Coordinator + Screen Recording |
| 4.4.4 - Manager Video | 3 hours | Training Coordinator + Screen Recording |
| 4.4.5 - Auditor Training | 4 hours | Training Coordinator + 2 facilitators |
| 4.4.6 - Manager Training | 3 hours | Training Coordinator + facilitator |
| 4.4.7 - Production Permissions | 2 hours | System Administrator |
| 4.4.8 - Go-Live Deployment | 2 hours | Project Lead + System Administrator |
| **Total** | **30 hours** | Cross-functional team |

### Success Criteria

- 100% of auditors complete training
- 100% of managers/educators complete training
- Zero critical issues in production
- All users with appropriate permissions assigned
- All test accounts and data cleaned up
- Support team responsive within 4 business hours

---

## Task 4.4.1: User Guide Document

**Objective:** Create comprehensive end-user documentation for auditors completing trolley audits.

**Dependency:** 4.3.10 (Testing complete)
**Duration:** 8 hours
**Owner:** Technical Writer + MERT Educators

### Document Structure

The User Guide should be created as both a PDF and web-based document in SharePoint. Follow this structure:

#### 1.1 Document Metadata

```markdown
RBWH Trolley Audit System - User Guide for Auditors
Version: 1.0
Date: [Current Date]
Audience: Clinical Staff (Auditors)
Last Updated: [Date]
Next Review: [6 months from now]
```

#### 1.2 Table of Contents & Navigation

```
1. Getting Started
2. System Access & Login
3. Completing an Audit (Step-by-Step)
4. Common Questions (FAQ)
5. Troubleshooting
6. Keyboard Shortcuts & Tips
7. Support Contacts
```

---

### 1. Getting Started Section

**Purpose:** Orient new users quickly.

```markdown
## 1. Getting Started

### What is the RBWH Trolley Audit System?

The RBWH Trolley Audit System is a mobile-friendly PowerApp that enables:
- Rapid completion of trolley audits (typically 15-20 minutes per trolley)
- Standardized audit data collection across all departments
- Real-time compliance tracking
- Issue reporting integrated into the system

### Key Benefits
- **For Auditors:** Simple workflow, timer functionality, offline capability
- **For Departments:** Automatic compliance tracking, immediate issue escalation
- **For Management:** Visibility into audit status and equipment compliance

### Before You Start
- Ensure you have a smartphone or tablet (iPad/Android recommended)
- Connect to WiFi or mobile network (internet required for submission)
- Notify your manager you will be conducting audits
- Have access to the trolley location being audited

### Time Required
- Comprehensive Audit: 15-20 minutes per trolley
- Spot Check Audit: 10-12 minutes per trolley
```

---

### 2. System Access & Login Section

**Purpose:** Enable users to access the application.

```markdown
## 2. System Access & Login

### Step 1: Download the PowerApps Mobile App

1. Open your smartphone app store (Apple App Store or Google Play Store)
2. Search for "Power Apps"
3. Download the official Microsoft Power Apps app
4. Install the app on your device

### Step 2: Launch the Application

1. Open the Power Apps app
2. Tap "Sign In"
3. Enter your RBWH email address (firstname.lastname@rbwh.org.au)
4. Enter your RBWH password
5. If prompted, choose "Accept" for app permissions
6. Select "RBWH Trolley Audit" from your available apps
7. Tap "Open App"

### Step 3: Verify Access

Once the app loads, you should see:
- RBWH Trolley Audit logo at the top
- "Home" screen with 4 main buttons
- Current date and time
- Your name in the top-right corner

**Troubleshooting Access Issues:**
- **"App not found" message:** Contact your IT Support (see Section 7)
- **"Invalid credentials" message:** Verify your email and password are correct
- **App won't load:** Check internet connection, try closing and reopening

### Offline Mode (Available)

If you're in an area without WiFi or mobile signal:
1. The app will automatically save your audit in offline mode
2. Complete your audit as normal
3. When you reconnect to internet, tap "Sync" to submit
4. The app will notify when sync is complete

**Note:** Offline mode requires you to have accessed the app at least once while connected.
```

---

### 3. Completing an Audit (Step-by-Step) Section

**Purpose:** Detailed walkthrough of the entire audit workflow.

```markdown
## 3. Completing an Audit (Step-by-Step)

### Overview

Every audit follows this 6-step workflow:

```
Step 1: Select Trolley → Step 2: Documentation → Step 3: Condition →
Step 4: Routine Checks → Step 5: Equipment → Step 6: Review & Submit
```

### Step 1: Select Trolley to Audit

**Screen: "Select Trolley"**

1. Tap the "Start New Audit" button on the Home screen
2. You'll see the "Select Trolley" screen
3. In the dropdown labeled "Which trolley are you auditing?", tap to open
4. **Type the trolley location** (e.g., "ICU Bay 1" or "ED Resus 2")
5. Matching locations will appear - tap to select
   - **Tip:** You can search by department name, building, or room number
   - **Example searches:** "Surgery", "Building 3", "Ward"
6. Once selected, the screen shows:
   - Trolley location name
   - Last audit date (when this trolley was last audited)
   - Audit type options

**Selecting Audit Type:**
- **Comprehensive Audit:** Full checklist (check all sections below)
  - Use for: Annual audits, when requested by manager
  - Time: 15-20 minutes
- **Spot Check Audit:** Focused checklist (equipment and condition only)
  - Use for: Weekly random audits, follow-up on issues
  - Time: 10-12 minutes

7. Select your audit type and tap "Next"

**Troubleshooting Step 1:**
- **"Can't find my trolley":**
  - Try searching by building or department name
  - Contact your manager with the trolley location details
  - Contact IT Support (see Section 7)
- **"Wrong trolley appeared":**
  - Verify the location matches before proceeding
  - If incorrect, select "Back" and search again

---

### Step 2: Documentation Check (Comprehensive Only)

**Screen: "Documentation"**

This step verifies that required audit documentation is available at the trolley location.

**Question 1: Check Record Present**
- Options: "Yes - current version", "Yes - old version", "No"
- What to look for:
  - **Current version:** Today's date or recent (within 3 months)
  - **Old version:** More than 3 months old but still present
  - **No:** No check record visible at trolley
- Enter your finding and move on

**Question 2: Checking Guidelines Present**
- Options: "Yes - current version", "Yes - old version", "No"
- What to look for:
  - **Current version:** Latest audit guidelines (usually printed poster)
  - **Old version:** Guidelines but outdated or worn
  - **No:** No guidelines present
- Enter your finding and move on

**Question 3: BLS Poster Present**
- Options: "Yes", "No"
- What to look for:
  - BLS (Basic Life Support) poster, typically laminated
  - Can be mounted on trolley or nearby wall
  - Usually color-coded with step numbers

**Question 4: Equipment List Present**
- Options: "Yes - current", "Yes - old", "No"
- What to look for:
  - Printed equipment list showing expected quantities
  - Usually attached to trolley or in nearby folder
  - Should match the equipment you'll check in Step 5

8. After answering all 4 questions, tap "Next"

**Troubleshooting Step 2:**
- **"I'm not sure if documentation is current":**
  - Check the printed date
  - Compare to the electronic equipment list
  - If unsure, select "Old version" rather than "Current"

---

### Step 3: Trolley Condition Check

**Screen: "Trolley Condition"**

This step assesses the physical condition of the trolley itself.

**Question 1: Trolley Clean**
- Options: "Yes", "No"
- What to check:
  - Surface dirt, stains, or buildup
  - Interior cleanliness (drawers, crevices)
  - Any visible contamination or damage
- **Action if No:** Describe issue in the text field that appears
- **Example:** "Sticky residue on top drawer handle"

**Question 2: Working Order**
- Options: "Yes", "No"
- What to check:
  - Drawers open and close smoothly
  - Wheels roll freely
  - Handles and locks function
  - No visible damage or broken components
- **Action if No:** A text field appears to enter issue details
- **Example:** "Bottom drawer won't open - appears stuck"

**Question 3: Rubber Bands Present**
- Options: "Yes", "No"
- What to check:
  - Rubber bands holding equipment in place
  - Usually wrapped around drawers or handle
  - Should prevent shifting during transport

**Question 4: O2 Tubing Correct**
- Options: "Yes", "No"
- What to check:
  - Oxygen tubing connected to cylinder (if present)
  - No kinks, damage, or disconnections
  - Tubing length appropriate

**Question 5: INHALO Cylinder (if present)**
- Options: "Not Applicable", "Yes (Good Pressure)", "No (Low/Empty)"
- What to check:
  - INHALO cylinder pressure gauge
  - Should show "full" or needle in green zone
  - Not applicable if trolley doesn't carry INHALO

9. After all questions, tap "Next"

**Troubleshooting Step 3:**
- **"I'm not sure if O2 tubing is 'correct'":**
  - Check that it's connected and not kinked
  - Ensure it leads to the oxygen cylinder
  - If you're unsure, select "No" and note concerns
- **"There are multiple issues":**
  - Select "No" for the relevant question
  - Describe all issues in the text field
  - Example: "Tubing kinked near base, connection loose"

---

### Step 4: Routine Checks

**Screen: "Routine Checks"**

This step captures data about regular maintenance checks performed by ward staff.

**Question 1: Outside Check Count**
- What this means: Daily checks performed outside the trolley
- Expected count: Calculated based on working days since last audit
- **Example:** If last audit was 5 working days ago, expected = 5
- Enter the actual count observed
- **Tip:** Check the trolley for a check sheet or tally marks

**Question 2: Inside Check Count**
- What this means: Weekly checks performed on contents inside drawers
- Expected count: Calculated based on weeks since last audit
- **Example:** If last audit was 2 weeks ago, expected = 2
- Enter the actual count observed

**Question 3: Checks Not Available**
- Options: "Yes", "No"
- Use "Yes" if: Check records are missing, damaged, or unavailable
- If "Yes" is selected, a text field appears
- **Example reasons to enter:** "Ward on leave", "Check sheet lost", "New trolley"

10. After entering values, tap "Next"

**Troubleshooting Step 4:**
- **"I can't find the check count":**
  - Look for a paper sheet attached to trolley
  - Check clipboards nearby
  - Ask ward staff - they maintain these records
  - If unavailable, select "Checks Not Available" and explain
- **"What counts as a valid check?":**
  - Written mark (tally, date, initials) by ward staff
  - Must show date or day (to verify recency)
  - Single entry per day/week minimum

---

### Step 5: Equipment Checklist

**Screen: "Equipment Checklist"**

This is the main checklist - verifying that all required equipment is present in the correct quantities.

**Understanding the Screen Layout:**

1. **Category Headers** (Expandable sections)
   - "Top of Trolley"
   - "Drawer 1: Airway Management"
   - "Drawer 2: Breathing"
   - "Drawer 3: Circulation"
   - "Drawer 4: Drugs"
   - "Side of Trolley"
   - "Back of Trolley"
   - "Paediatric Box" (if applicable)

2. **For Each Equipment Item:**
   - Item name and expected quantity
   - **Text showing:** "Expected: 3 units"
   - Input field for "Quantity Found"
   - Notes field (optional)

**Completing the Equipment Checklist:**

11. For each item visible:
    - Verify the equipment is present
    - Enter the actual quantity you find
    - **Tip:** Leave "Quantity Found" blank if item is completely missing
    - Add notes if quantity differs from expected
    - **Example notes:** "Found 2 instead of 3", "Old stock", "Expired 6/2024"

12. Items highlighted in RED indicate:
    - Quantity below expected
    - Required equipment for this trolley type
    - Needs attention

13. Items highlighted in ORANGE indicate:
    - Quantity below expected
    - But acceptable (e.g., consumables depleted)
    - Note for future restocking

14. Tap each category header to expand/collapse sections
    - **Tip:** Use this to navigate large lists
    - Collapsed categories are "sticky" (stay collapsed if you go back)

**Special Cases:**

- **Paediatric Equipment (if visible):**
  - Only check if trolley has paediatric capability
  - Usually 6-8 specialized paediatric items
  - Quantities typically 1-2 units

- **Defibrillator Pads:**
  - Your trolley has specific defibrillator type
  - Only correct pads will be shown
  - Examples: "Adult Pads" or "Paediatric Pads"

15. After reviewing all items, tap "Next"

**Troubleshooting Step 5:**
- **"Item quantity doesn't match - should I enter 0 or actual count?":**
  - Always enter the actual quantity you find
  - Enter 0 if item is completely missing
  - Add notes explaining discrepancy
- **"Some items are locked in drawers":**
  - Carefully open drawers and count items
  - Ensure drawers are returned to original state
  - If drawer is damaged and can't open, note this
- **"Quantity field is showing red - is this a problem?":**
  - Red indicates shortage vs. expected quantity
  - Complete the audit - managers will review
  - If critical item (like airway equipment) is missing, notify your manager immediately
- **"I can't find an item":**
  - Search thoroughly in labeled sections
  - Check under wrappers or packaging
  - If still not found, enter 0
  - Add note explaining where you searched

---

### Step 6: Review & Submit

**Screen: "Review"**

This screen shows a summary of your entire audit before final submission.

**Review Checklist:**

16. Review each section:
    - Verify all responses are correct
    - Check that red-highlighted items are intentional (if any)
    - Confirm your name is shown as the auditor

17. If you need to change something:
    - Tap "Edit" button next to the section
    - Make corrections
    - Tap "Save" to return to review screen

18. Final submission options:
    - **"Submit Audit"** - Completes and submits the audit
      - Use this when you're confident in all entries
      - Audit data is sent to management
      - You'll receive confirmation
    - **"Save as Draft"** - Saves without submitting
      - Use if you need to complete later
      - You can resume from the same point
      - Managers won't see draft audits
    - **"Cancel"** - Discard without saving
      - All data will be lost
      - You'll be asked to confirm

19. Tap "Submit Audit" when ready

**After Submission:**

20. You'll see a confirmation message:
    - "Audit successfully submitted"
    - Confirmation email sent to your email address
    - Timestamp of submission
    - You can now start another audit or exit

**Troubleshooting Step 6:**
- **"I submitted but didn't see confirmation":**
  - Check your email (including Spam folder)
  - Go to Home screen and look for submitted audit
  - Contact IT Support if not visible after 1 hour
- **"I found an error after submitting":**
  - Managers will review; don't worry
  - Contact your manager to report the error
  - For critical errors, contact IT Support (see Section 7)
- **"Audit won't submit - error message appeared":**
  - Check internet connection
  - Ensure all required fields are filled
  - Try "Save as Draft" first, then submit later
  - Contact IT Support if problem persists

---

### 4. Common Questions (FAQ)

**Purpose:** Quick reference for frequently asked questions.

```markdown
## 4. Frequently Asked Questions (FAQ)

### Audit Workflow & Process

**Q: How long does an audit typically take?**
A: Comprehensive audits: 15-20 minutes
Spot check audits: 10-12 minutes
Times may vary based on trolley complexity and documentation availability.

**Q: Can I save my audit and complete it later?**
A: Yes! Tap "Save as Draft" on the Review screen. You can resume anytime from the saved point.

**Q: What if I make a mistake on a question - can I go back?**
A: Yes. On the Review screen, tap "Edit" next to the section you want to change. Make corrections and tap "Save".

**Q: Do I need internet to complete an audit?**
A: For submitting, yes. However, the app supports offline mode - complete your audit offline, then submit when connected.

**Q: What if I don't know an answer to a question?**
A: Do your best to assess fairly. If truly unsure, select "No" and add a note explaining. Managers will review.

**Q: Can other people see my audit before it's submitted?**
A: No. Only you and management can see your draft. Once submitted, it's visible to relevant managers.

---

### Equipment & Trolley Questions

**Q: What's the difference between "Expected" and "Quantity Found"?**
A: "Expected" = quantity this trolley should have (based on trolley type)
"Quantity Found" = what you actually count during the audit

**Q: Should I count expired items?**
A: Count them, then note "expired" in the Notes field. They shouldn't be there but flagging them helps with cleanup.

**Q: What if a drawer is stuck and I can't open it?**
A: Document this in the trolley condition section. Don't force it - note "Bottom drawer stuck" and let management know.

**Q: How do I know if my trolley has a paediatric box?**
A: You would know - your department either has paediatric services or doesn't. The trolley location should have this configured.

---

### Submission & Data

**Q: What happens after I submit an audit?**
A: Your data is stored in our system. Management reviews it, equipment issues are escalated, and managers track audit status.

**Q: Can I edit an audit after submitting?**
A: No, submitted audits are locked. Contact your manager if you need to report a correction.

**Q: Who can see my audit?**
A: Your manager, MERT educators, and IT administrators. Your individual responses aren't shared with clinical staff.

**Q: How long is my audit data kept?**
A: Minimum 2 years for compliance tracking. Longer if required by audit regulations.

---

### Technical Questions

**Q: The app is very slow - what should I do?**
A: First, check your WiFi/mobile connection signal strength. If problem persists:
1. Close the app completely
2. Wait 30 seconds
3. Reopen the app
4. Try again

**Q: I keep getting logged out - why?**
A: For security, you may be logged out after inactivity. Simply log back in with your email/password.

**Q: Can I use the app on a computer instead of tablet?**
A: Yes - Power Apps works on desktop browsers (Chrome, Edge, Safari). Visit powerapp.rbwh.org.au and log in.

**Q: What if I lose WiFi connection mid-audit?**
A: If offline mode is enabled, your audit saves automatically. When you reconnect, it will sync. Resume where you left off.

---

### General Questions

**Q: Why is this system needed instead of the old Microsoft Forms?**
A: The new system offers:
- Better mobile experience
- Real-time data collection
- Equipment-level detail (not just "yes/no" for all items)
- Automatic compliance tracking
- Integration with issue management

**Q: How often will audits be required?**
A: All trolleys: at least 1 comprehensive audit per calendar year
Spot checks: randomly selected trolleys weekly (10 trolleys/week)

**Q: What if I disagree with a trolley's compliance score?**
A: Speak with your manager. MERT educators review all scores and can adjust if needed.

**Q: Can I audit a trolley from another department?**
A: Only if you're authorized. Search for the trolley - you'll only see those you're permitted to audit.
```

---

### 5. Troubleshooting

**Purpose:** Structured problem-solving guidance.

```markdown
## 5. Troubleshooting Guide

### Issue: "App Won't Load"

**Symptoms:**
- App opens but shows blank screen
- App closes immediately after opening
- Loading spinner appears indefinitely

**Solutions (in order):**
1. Check internet connection
   - Open web browser and verify WiFi works
   - If on mobile, try both WiFi and cellular
2. Close app completely (don't just minimize)
   - Double-click home button (iPhone) or use recent apps (Android)
   - Swipe up on Power Apps to close
3. Wait 30 seconds, reopen app
4. If still not working, restart device:
   - Power off device completely
   - Wait 10 seconds
   - Power on and reopen app
5. If problem persists, contact IT Support

---

### Issue: "Can't Find Trolley I'm Looking For"

**Symptoms:**
- Trolley not appearing in dropdown
- Dropdown shows "No matches"
- Wrong trolley appearing

**Solutions:**
1. Try different search terms:
   - Search by room number (e.g., "ICU 3")
   - Search by department (e.g., "Surgery")
   - Search by building (e.g., "Building 3")
2. Verify trolley location name:
   - Ask your manager for official location name
   - Check facility map or location list
   - Search using exact official name
3. Check if trolley is active:
   - Some trolleys may be deactivated/archived
   - Contact manager if trolley should be active
4. Verify you have permission:
   - Not all auditors can audit all locations
   - Contact manager or IT Support for access

---

### Issue: "Equipment Quantities Don't Match"

**Symptoms:**
- Items highlighted in red (shortage)
- Items missing entirely
- More items than expected

**What this likely means:**
- Equipment has been used/consumed (normal)
- Equipment needs restocking (manager will see this)
- Equipment is damaged/expired (should be removed)
- Items were never fully stocked (report to manager)

**What to do:**
1. Enter actual count you find (not expected count)
2. Add note explaining discrepancy
3. If critical item missing (airway equipment, defib pads):
   - Notify your manager immediately
   - Don't wait for system to catch it
4. Complete the audit normally
5. Managers will review and prioritize restocking

---

### Issue: "Audit Won't Submit"

**Symptoms:**
- Submit button is greyed out
- "Submission failed" error message
- Audit appears to submit but no confirmation

**Solutions:**
1. Verify internet connection
   - Check WiFi or mobile signal strength
   - Try opening a web browser to confirm internet works
2. Fill all required fields:
   - Go back to Review screen
   - Tap "Edit" for any incomplete sections
   - Ensure all questions are answered
3. Save as draft first:
   - Tap "Save as Draft"
   - Wait for confirmation
   - Try submitting again
4. Wait and retry:
   - Sometimes submission just needs time
   - Wait 5 minutes, then try again
5. If still failing:
   - Save as draft for now
   - Contact IT Support (see Section 7)
   - Provide the draft audit details

---

### Issue: "Offline Mode Not Working"

**Symptoms:**
- App requires internet even though offline was mentioned
- Audit doesn't sync after reconnecting

**What to know:**
- Offline mode requires at least one prior login while connected
- Offline mode may need to be specifically enabled
- New installations may not have offline capability

**Solutions:**
1. If first time using app:
   - Complete one audit while connected to internet
   - This enables offline mode for future sessions
2. Check if app is truly offline:
   - Look for "Offline Mode" indicator (usually shows as banner)
   - Check internet settings - are you actually disconnected?
3. After reconnecting:
   - Open app
   - Look for "Sync" button or notification
   - Tap to sync offline audits
4. If sync fails:
   - Ensure you're connected to internet
   - Close app and reopen
   - Try sync again

---

### Issue: "Login Problems - Can't Access System"

**Symptoms:**
- "Invalid credentials" message
- Account locked after multiple login attempts
- "You don't have permission" message

**Solutions for "Invalid Credentials":**
1. Verify your email address:
   - Should be firstname.lastname@rbwh.org.au
   - Check that CAPS LOCK is not on
   - Try entering email in lowercase
2. Reset your password:
   - On login screen, tap "Forgot Password"
   - Follow password reset flow
   - Use new password to login
3. Contact IT if you:
   - Aren't sure of your email
   - Can't reset password
   - Receive "Account Locked" message

**Solutions for "No Permission":**
1. Verify you're in the correct group:
   - Contact your manager
   - Confirm you're authorized to audit
   - Request access if needed
2. Confirm correct tenant:
   - You should see "RBWH" or hospital name
   - Not a different organization's account
3. If recently granted access:
   - Access changes take up to 2 hours to process
   - Wait 2 hours, log out completely, log back in
   - Clear browser cache if using web version

---

### Issue: "My Edits Didn't Save"

**Symptoms:**
- Made changes on Review screen but they disappeared
- Returned to section and old data is still there

**What likely happened:**
- You tapped "Back" instead of "Save" after editing
- App crashed before saving
- Session was interrupted

**Solutions:**
1. If still on Review screen:
   - Tap "Edit" for the section again
   - Re-enter your corrections
   - Tap "Save" this time (not "Back")
2. If you already moved past:
   - You may need to restart the audit
   - Tap "Start New Audit" and go through process again
   - Or contact IT Support to recover your draft

---

## Section 6: Keyboard Shortcuts & Tips

```markdown
### Tablet & Desktop Shortcuts

| Action | Shortcut |
|--------|----------|
| Move to next question | Tab key or down arrow |
| Move to previous question | Shift+Tab or up arrow |
| Open/Close category section | Enter key or spacebar |
| Submit form | Ctrl+Enter or Cmd+Enter |
| Exit without saving | Esc key |

### General Tips for Faster Auditing

1. **Use search efficiently:**
   - Type partial name (e.g., "ICU" instead of full location)
   - Search terms are auto-complete enabled

2. **For equipment checklist:**
   - Categories remember collapse state between audits
   - Use this to quickly move through sections

3. **For offline use:**
   - Download facility map before going offline
   - Take screenshot of expected equipment quantities
   - Makes auditing easier without live references

4. **For common items:**
   - System remembers your recent audits
   - Quickly retry recent trolley location
```

---

## Section 7: Support Contacts

```markdown
## 7. Support Contacts & Getting Help

### IT Support (Technical Issues)
**Email:** it.support@rbwh.org.au
**Phone:** +61 7 3636 [Support Number]
**Hours:** Monday-Friday, 8am-5pm
**Response Time:** 4 business hours for issues, 24 hours for inquiries

**Best for:**
- App won't load or keeps crashing
- Login problems
- Internet/connection issues
- Permission/access problems
- Device-specific problems

**What to include in your email:**
- Device type (iPad, iPhone, Android tablet, etc.)
- App version (check in app Settings)
- When problem started
- Steps you took to try to fix it
- Audit location name if relevant

---

### MERT Educators (Process Questions)
**Email:** mert@rbwh.org.au
**Office:** Building X, Room X
**Hours:** Monday-Friday, 8:30am-4:30pm

**Best for:**
- Questions about audit requirements
- Issues with trolley compliance score
- Disagreement with audit findings
- New trolley locations or equipment changes
- Policy questions about audit process

---

### Your Direct Manager (Department-Specific)
**When to contact:**
- You can't find your trolley
- You don't have permission to audit certain trolleys
- You need time to complete audits
- Department has specific audit scheduling

---

### Online Resources

**Power Apps Help Center:**
https://powerapps.microsoft.com/en-us/support/

**RBWH SharePoint Help:**
https://sharepoint.rbwh.org.au/sites/it-support

**System Status Page:**
https://rbwh.powerplatform.com/status
```

---

### Document Footer

```markdown
---

**Document Version:** 1.0
**Last Updated:** [Current Date]
**Next Review Date:** [6 months]
**Maintained by:** Technical Writing Team
**Approved by:** MERT Educators, IT Administration

For feedback or corrections to this guide, contact: mert@rbwh.org.au

---
```

---

## Task 4.4.2: Admin Guide Document

**Objective:** Create comprehensive administrator documentation covering MERT Educator and IT Administrator roles.

**Dependency:** 4.3.10 (Testing complete)
**Duration:** 4 hours
**Owner:** System Administrator + Technical Writer

### Document Structure

The Admin Guide should cover two distinct audiences within a single document using clear section headers.

#### 2.1 Document Metadata

```markdown
RBWH Trolley Audit System - Administrator Guide
Version: 1.0
Date: [Current Date]
Audience: MERT Educators, IT Administrators
Last Updated: [Date]
Next Review: [6 months from now]
```

---

### Section A: MERT Educator Guide

**Purpose:** Enable educators to manage audit process, review data, and manage issues.

```markdown
## Part A: MERT Educator Guide

### A.1 Overview & Responsibilities

As a MERT Educator, you have several responsibilities in the system:

| Responsibility | Description | Frequency |
|----------------|-------------|-----------|
| Audit Oversight | Review submitted audits for quality and completeness | Daily/Weekly |
| Issue Management | Review and triage reported issues | Daily |
| Random Selection | Generate/review weekly random audit selections | Weekly |
| Reporting | Monitor compliance trends, generate reports | Weekly/Monthly |
| User Support | Answer process questions, handle escalations | As needed |
| Configuration | Add new trolleys, update equipment lists | As needed |

### A.2 Accessing the System

**Via PowerApp (Primary Method):**
1. Open Power Apps app on tablet/phone
2. Sign in with RBWH credentials
3. Select "RBWH Trolley Audit" app
4. You'll see Home screen with admin options

**Via Web Browser (For Reporting):**
1. Navigate to https://app.powerbi.com/
2. Sign in with RBWH credentials
3. Select "RBWH Trolley Audit Reports" workspace
4. View dashboards and reports

**Via SharePoint (For Data Management):**
1. Navigate to https://rbwh.sharepoint.com/sites/RBWHTrolleyAudit
2. Sign in with RBWH credentials
3. Access individual lists for manual data management if needed

---

### A.3 Daily: Reviewing Submitted Audits

**Purpose:** Quality assurance and issue identification.

**Accessing Submitted Audits:**
1. Open RBWH Trolley Audit app (PowerApp)
2. From Home screen, tap "View Audits"
3. You'll see list of all recent audits

**Filter Options:**
- Filter by date range (today, this week, this month)
- Filter by trolley location
- Filter by service line
- Filter by compliance score
- Sort by submission date (newest first)

**Reviewing Individual Audit:**
1. Tap audit entry to open detail view
2. Screen shows:
   - Trolley location and audit date
   - Auditor name and submission time
   - Compliance score (overall percentage)
   - All questions and answers
   - Any notes or comments
   - Issues flagged during audit

**Quality Checks to Perform:**
- ✓ Auditor name is recognizable (not blank)
- ✓ Audit date is recent (not from 2 weeks ago)
- ✓ All sections completed (no blanks unless noted)
- ✓ Equipment quantities are reasonable (not random numbers)
- ✓ Notes are clear if items are missing/expired
- ✓ Condition issues properly documented

**If Audit Looks Incomplete:**
1. Contact the auditor directly
2. Ask them to resubmit with corrections
3. Do not approve questionable audits
4. Document the issue for training purposes

**If Critical Issues Found:**
- Equipment missing: Escalate to manager immediately
- Trolley not working: Deactivate until repairs made
- Process questions: Reach out to auditor for clarification

---

### A.4 Weekly: Random Audit Selection

**Purpose:** Generate the weekly list of 10 trolleys to audit.

**Automated Generation (Recommended):**
1. System generates automatically every Monday 8am
2. You'll receive email notification
3. Selection is based on:
   - Trolleys not audited in 6+ months (high priority)
   - Even distribution across service lines
   - Avoidance of same trolley twice in 4 weeks

**Manual Generation (If Needed):**
1. Open app and go to "Admin" section
2. Tap "Generate Random Selection"
3. Choose generation date
4. System calculates priority scores
5. Review generated list before confirming
6. Once confirmed, auditors see list on Home screen

**Selection Review Checklist:**
- ✓ 10 trolleys are selected
- ✓ At least 30% are due for comprehensive audit
- ✓ No trolley selected more than once per month
- ✓ Trolleys distributed across service lines
- ✓ No inactive/deactivated trolleys included

**If Selection Looks Wrong:**
1. Check audit history of selected trolleys
2. If error found, manually adjust by:
   - Removing incorrectly selected trolley
   - Manually adding appropriate alternative
3. Communicate any changes to team

---

### A.5 Issue Management Workflow

**Purpose:** Track issues from identification through resolution.

**Accessing Issues:**
1. Open app and select "View Issues"
2. Default shows open (unresolved) issues
3. Filter options:
   - By status (Open, In Progress, Resolved, Closed)
   - By severity (Critical, High, Medium, Low)
   - By location
   - By assigned to

**Issue Status Workflow:**

```
Reported (New) → Assigned → In Progress → Pending Verification → Resolved → Closed
```

**Reviewing New Issues:**
1. Sort issues by submission date (newest first)
2. Read issue summary and description
3. Determine initial severity:
   - **Critical:** Safety risk, missing critical equipment
   - **High:** Major equipment missing, trolley non-functional
   - **Medium:** Minor equipment shortage, documentation issues
   - **Low:** Documentation formatting, duplicate entry

**Assigning Issues:**
1. Tap issue to open detail view
2. Tap "Assign" button
3. Select which manager/staff member should handle
4. Add assignment note if needed
5. Assignment notification sent automatically

**Monitoring Issue Resolution:**
1. Access issue detail page
2. View all corrective actions taken
3. Check dates and notes for each action
4. Follow-up audit may be scheduled
5. Once resolved by manager, mark as "Resolved"
6. After verification, close issue

**Manager Escalation:**
1. If issue not addressed within SLA (varies by severity):
   - Critical: 24 hours
   - High: 3 days
   - Medium: 5 days
   - Low: 10 days
2. System can auto-escalate or send reminder
3. You can manually escalate if needed:
   - Open issue
   - Tap "Escalate"
   - Add escalation note
   - Notify next-level manager

---

### A.6 Monthly: Compliance Reporting

**Purpose:** Track system-wide compliance trends.

**Accessing Reports:**
1. Navigate to Power BI workspace
2. Select "Trolley Audit Dashboard"
3. View real-time compliance metrics

**Key Metrics to Monitor:**

| Metric | Meaning | Target |
|--------|---------|--------|
| Audit Completion Rate | % of trolleys audited in last 12 months | 100% |
| Average Compliance Score | Mean compliance across all trolleys | >90% |
| Overdue Trolleys | Count of trolleys past audit due date | <5% |
| Open Issues | Total unresolved issues | <20 |
| Average Issue Age | Days since average issue reported | <10 days |

**Report Visualization Examples:**
- **Compliance Trend:** Line chart showing monthly average scores
- **Service Line Comparison:** Bar chart comparing service lines
- **Building Comparison:** Map showing compliance by location
- **Equipment Deficiency:** Table of most commonly missing items
- **Issue Aging:** Chart showing how long issues remain open

**Interpreting Low Compliance:**
1. Click metric to drill down
2. Identify trolleys with lowest scores
3. Analyze what equipment/conditions are problematic
4. Determine if:
   - Issue is system-wide (new equipment not stocked)
   - Location-specific (one trolley not maintained)
   - Process issue (auditors not counting correctly)
5. Take corrective action

**Monthly Board Report:**
1. Generate report with:
   - Overall compliance metric
   - Key issues and status
   - Equipment deficiency summary
   - Recommendations for next month
2. Present to leadership as needed

---

### A.7 Trolley Management

**Purpose:** Add new trolleys, update configurations, or deactivate trolleys.

**Adding a New Trolley Location:**
1. Open app and go to "Admin" section
2. Tap "Manage Trolleys" → "Add New"
3. Enter required information:
   - **Department/Location Name:** "ICU Bay 3" or "ED Resus 2"
   - **Service Line:** Select from dropdown
   - **Building:** Select location
   - **Trolley Type:** Standard or Pediatric
   - **Defibrillator Type:** (if applicable)
4. Optional fields:
   - Operating hours (if trolley only operates certain times)
   - Special notes (e.g., "Mobile trolley")
   - Equipment customizations
5. Tap "Save"
6. New trolley appears in auditor dropdown

**Updating Trolley Configuration:**
1. Open app, go to "Manage Trolleys"
2. Find trolley by name/location
3. Tap to open detail view
4. Update fields as needed:
   - Change service line (if dept transferred)
   - Update operating hours
   - Modify equipment profile
5. Tap "Save" to apply changes

**Deactivating a Trolley:**
1. Open app, go to "Manage Trolleys"
2. Find trolley in list
3. Tap "Deactivate" button
4. Provide reason (archived, moved, etc.)
5. Confirm deactivation
6. Trolley no longer appears in auditor selections
7. Historical data is retained (not deleted)

**Reactivating a Trolley:**
1. Open "Manage Trolleys" and filter for "Inactive"
2. Find trolley to reactivate
3. Tap "Reactivate" button
4. Trolley returns to active status
5. Appears again in auditor selections

---

### A.8 Handling Common Questions

**Q: A manager says equipment qty is wrong - how do I fix it?**
A:
1. Review the equipment master list for that trolley type
2. Verify the expected quantity (may need to check with supplier/pharmacy)
3. If expected quantity is wrong, update Equipment Master List
4. You can add a note to the trolley explaining discrepancy
5. Next audit cycle will use new expected quantity

**Q: Auditor submitted audit with missing equipment - what now?**
A:
1. Review audit details to confirm items really missing
2. Contact the auditor to double-check
3. If confirmed missing, escalate to nurse manager
4. Nurse manager coordinates restocking with CELS/Pharmacy
5. Manager marks trolley as "restocking in progress"
6. Spot check audit scheduled after restocking

**Q: One location won't show up in the dropdown for auditors****
A:
1. Check if trolley is "inactive" (it wouldn't show)
2. Reactivate if needed
3. Verify trolley name matches exactly (typos prevent matching)
4. Check if service line is correctly assigned
5. Wait 5 minutes and try again (system may need refresh)

**Q: How do I know if an auditor is trained?**
A:
1. Pull system user log (ask IT admin)
2. Look for login activity from user
3. Check submission history (have they submitted audits?)
4. If no activity: send reminder, offer additional training
5. Don't grant access until confident in competence

```

---

### Section B: IT Administrator Guide

**Purpose:** Enable IT staff to manage permissions, system configuration, and troubleshooting.

```markdown
## Part B: IT Administrator Guide

### B.1 System Architecture Overview

**Component Architecture:**

```
┌─────────────────────────────────────────────────┐
│           End User Layer (PowerApp)              │
│   - Auditor Interface (Tablet/Phone)            │
│   - Manager Dashboard (Web)                      │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────┴────────────────────────────────┐
│   Data Layer (SharePoint Lists)                  │
│   - Location list (76 trolleys)                  │
│   - Audit records (detailed responses)           │
│   - Issue tracking                               │
│   - Equipment master                             │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────┴────────────────────────────────┐
│   Automation Layer (Power Automate Flows)       │
│   - Submit audit flow (creates records)          │
│   - Issue notification flows                     │
│   - Random selection generation                  │
│   - Weekly scheduled flows                       │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────┴────────────────────────────────┐
│   Reporting Layer (Power BI)                    │
│   - Real-time dashboards                         │
│   - Compliance reports                           │
│   - Trend analysis                               │
└─────────────────────────────────────────────────┘
```

**Key Components:**

| Component | Location | Purpose |
|-----------|----------|---------|
| PowerApp Canvas | Power Platform environment | User interface |
| SharePoint Lists | Tenant SharePoint | Data storage |
| Power Automate Flows | Cloud flows | Business logic automation |
| Power BI Workspace | Power BI Service | Reporting & analytics |

---

### B.2 Permission & Security Model

**Azure AD Groups (Recommended):**

```
rbwh-trolley-auditors@rbwh.org.au
├── All staff with audit responsibility
├── About 50-60 users
└── Can submit audits, view own submissions

rbwh-trolley-managers@rbwh.org.au
├── NUM, Ward Managers, Service Directors
├── About 20-30 users
└── Can view audits, manage issues, access reports

rbwh-trolley-educators@rbwh.org.au
├── MERT Educators only
├── About 3-5 users
└── Can view all data, generate reports, configure system

rbwh-trolley-admins@rbwh.org.au
├── IT Administrators
├── 1-2 users
└── Can manage permissions, system config, troubleshoot
```

**SharePoint List Permissions:**

| List | Auditors | Managers | Educators | Admins |
|------|----------|----------|-----------|--------|
| Location (Trolley list) | Read | Read | Read/Write | Read/Write |
| Audit (Submissions) | Create/Edit Own | Read All | Read All | All |
| Issue (Problems reported) | Create | Read/Edit | Read/Edit All | All |
| Equipment (Master list) | Read | Read | Read/Write | Read/Write |
| AuditPeriod | Read | Read | Read/Write | Read/Write |

**PowerApp Permissions:**

```
RBWH Trolley Audit App (Canvas)
├── Auditor Role
│   ├── Can access: Audit entry screens, personal submissions
│   ├── Cannot access: Admin screens, user management
│   └── Default role for most users
├── Manager Role
│   ├── Can access: Issue management, audit review, reports
│   └── Cannot access: System configuration, user admin
└── Admin Role
    ├── Can access: All screens, settings, configuration
    └── Limited to MERT educators
```

---

### B.3 Permission Configuration Steps

**Initial Setup (First Time):**

1. **Create Azure AD Security Groups:**
   ```powershell
   # Using Azure AD PowerShell
   New-AzureADGroup -DisplayName "rbwh-trolley-auditors" `
     -MailNickname "rbwh-trolley-auditors" `
     -SecurityEnabled $true `
     -MailEnabled $false

   # Repeat for managers, educators, admins
   ```

2. **Add Users to Groups:**
   ```powershell
   # Add auditor user
   Add-AzureADGroupMember -ObjectId (Get-AzureADGroup `
     -Filter "DisplayName eq 'rbwh-trolley-auditors'").ObjectId `
     -RefObjectId (Get-AzureADUser -Filter "userPrincipalName eq 'user@rbwh.org.au'").ObjectId
   ```

3. **Grant SharePoint List Access:**
   - Open SharePoint site settings
   - Go to "Site Permissions"
   - Add groups with appropriate permission levels:
     - Auditors: "Edit" (can create/edit own items)
     - Managers: "Edit" (can view all items)
     - Educators: "Full Control" (can modify all)

4. **Configure PowerApp Access:**
   - Open Power Apps admin center
   - Select app "RBWH Trolley Audit"
   - Go to "Share" settings
   - Add security groups with appropriate roles
   - Configure role-based security via Power Fx formulas

**Ongoing Maintenance:**

1. **Adding New Auditor:**
   - Add user email to "rbwh-trolley-auditors" group
   - Send welcome email with link to app
   - Allow 1-2 hours for permissions to propagate
   - User should be able to log in and see app

2. **Promoting Manager to Educator:**
   - Remove from "rbwh-trolley-managers" group
   - Add to "rbwh-trolley-educators" group
   - Admin screens will appear on next login

3. **Removing User (Off-boarding):**
   - Remove from all trolley system groups
   - Remove from PowerApp share list
   - Within 24 hours, user loses access

---

### B.4 Troubleshooting Permission Issues

**Issue: User can't see the app**

Diagnosis:
1. Verify user is added to security group
2. Check if group membership propagated (can take 2 hours)
3. Verify user's license includes Power Apps
4. Confirm PowerApp is shared with the user's group

Solution:
```powershell
# Check group membership
$group = Get-AzureADGroup -Filter "DisplayName eq 'rbwh-trolley-auditors'"
Get-AzureADGroupMember -ObjectId $group.ObjectId |
  Where-Object {$_.UserPrincipalName -eq "user@rbwh.org.au"}

# If empty, add user:
Add-AzureADGroupMember -ObjectId $group.ObjectId `
  -RefObjectId (Get-AzureADUser -Filter "userPrincipalName eq 'user@rbwh.org.au'").ObjectId

# Wait 2 hours, then have user retry
```

**Issue: User can see app but can't access data**

Diagnosis:
1. User has right app access but no SharePoint permissions
2. User is in wrong group for their role
3. User's license doesn't include SharePoint

Solution:
```powershell
# Verify SharePoint list permissions
$site = Get-PnPWeb
Get-PnPList -Identity "Audit" | Get-PnPRoleAssignment |
  Where-Object {$_.Member -like "*auditors*"}

# Add group to list if missing
$group = Get-PnPGroup -Identity "rbwh-trolley-auditors"
Set-PnPListPermission -Identity "Audit" `
  -Group $group -AddRole "Edit"
```

**Issue: Manager sees audit data they shouldn't**

Diagnosis:
1. Manager is in wrong group (educators instead of managers)
2. PowerApp security formula has a logic error
3. SharePoint list view not properly filtered

Solution:
1. Verify group membership
2. Review PowerApp user role formulas
3. Check SharePoint views - ensure managers see filtered data only

---

### B.5 Backup & Data Management

**Regular Backups:**

1. **SharePoint Lists (Automatic):**
   - Microsoft handles automated backups
   - Point-in-time restore available 30 days
   - No action required

2. **Manual Backup (Recommended):**
   ```powershell
   # Export audit data to CSV monthly
   $list = Get-PnPList -Identity "Audit"
   Get-PnPListItem -List $list | Export-Csv `
     -Path "C:\Backups\Audit_$(Get-Date -Format 'yyyy-MM-dd').csv"
   ```

3. **Power BI Workspace:**
   - Export reports to PDF monthly
   - Save workspace configuration
   - Store in secure file share

**Data Retention Policies:**

| Data Type | Retention | Notes |
|-----------|-----------|-------|
| Audit Records | 7 years | Minimum compliance requirement |
| Issue Records | 7 years | Linked to audit records |
| Equipment Data | 3 years | Reference data can be archived |
| User Logs | 1 year | Compliance requirement |

**Data Deletion (When Needed):**

```powershell
# Delete older records (e.g., 2015 audit period)
$list = Get-PnPList -Identity "Audit"
$items = Get-PnPListItem -List $list `
  -Query '<View><Query><Where><Lt>
    <FieldRef Name="Created"/>
    <Value Type="DateTime">2015-12-31</Value>
  </Lt></Where></Query></View>'
$items | ForEach-Object { Remove-PnPListItem -List $list -Identity $_.Id }
```

---

### B.6 Monitoring & Health

**System Health Checks (Weekly):**

1. **Power Automate Flows:**
   ```
   - Check that scheduled flows completed successfully
   - Look for failed flow runs
   - If fails >5%, investigate error messages
   ```

2. **PowerApp Performance:**
   ```
   - Monitor app response time (should be <2 sec for load)
   - Check for crashes in analytics
   - If issues, clear app cache or rebuild
   ```

3. **SharePoint Performance:**
   ```
   - Verify lists are accessible
   - Check for large items or corrupted data
   - Confirm calculated columns are updating
   ```

4. **Data Quality:**
   ```
   - Spot check 5-10 recent audit submissions
   - Verify data makes sense and is complete
   - Flag unusual patterns for review
   ```

**Performance Optimization:**

- **Large List Issues:** If Audit list exceeds 5,000 items, enable indexed columns
- **Slow PowerApp:** Clear browser cache, check for complex formulas
- **Flow Timeout:** Break large flows into smaller flows, use child flows
- **Query Efficiency:** Index Location and ServiceLine lookups

---

### B.7 System Configuration

**Configuration Settings Location:**

All system settings are stored in a configuration item in SharePoint:
- List: "SystemConfiguration"
- Item: "AppConfig"

**Common Configurations:**

```
AuditDueDateDays: 365
  Purpose: Days until audit is overdue
  Example: "365" means audits older than 365 days are overdue

RandomSelectionCount: 10
  Purpose: How many trolleys selected each week
  Example: "10" means select 10 trolleys weekly

PriorityWeight_MonthsSinceAudit: 2.0
  Purpose: How much to weight "months without audit" in priority algorithm
  Example: "2.0" = double weight for old audits

CriticalEquipmentList: Airway kit, Ambu bag, Defib pads
  Purpose: Items flagged as critical
  Example: Missing these triggers high severity issue
```

**Modifying Configuration:**

1. Navigate to SharePoint site
2. Open "SystemConfiguration" list
3. Click "AppConfig" item
4. Edit field and click Save
5. Changes take effect immediately

---

### B.8 Handling Test Data & Go-Live

**Pre-Go-Live:**

1. **Identify Test Accounts:**
   ```powershell
   # List all test user accounts
   Get-AzureADUser | Where-Object {$_.DisplayName -like "*test*"}
   ```

2. **Remove Test Data:**
   ```powershell
   # Delete test audit submissions
   $list = Get-PnPList -Identity "Audit"
   $testItems = Get-PnPListItem -List $list `
     -Query '<View><Query><Where><Contains>
       <FieldRef Name="AuditorName"/>
       <Value Type="Text">test</Value>
     </Contains></Where></Query></View>'
   $testItems | ForEach-Object {
     Remove-PnPListItem -List $list -Identity $_.Id
   }
   ```

3. **Verify No Test Accounts in Production:**
   ```powershell
   # Check group membership
   $groups = @("rbwh-trolley-auditors", "rbwh-trolley-managers",
               "rbwh-trolley-educators")
   foreach ($grp in $groups) {
     Write-Host "Checking $grp..."
     $group = Get-AzureADGroup -Filter "DisplayName eq '$grp'"
     Get-AzureADGroupMember -ObjectId $group.ObjectId |
       Where-Object {$_.DisplayName -like "*test*"} |
       Format-Table DisplayName, UserPrincipalName
   }
   ```

4. **Reset All Passwords:**
   - Production users change passwords
   - Ensures test password not used in production

**Post-Go-Live:**

1. **Monitor First Week:**
   - Check daily for errors
   - Monitor Power Automate flows
   - Respond quickly to support requests

2. **Performance Baseline:**
   - Record app load time
   - Note flow execution times
   - Document expected metrics

3. **User Feedback Loop:**
   - Collect user feedback via survey
   - Address critical issues immediately
   - Document enhancement requests

---

### B.9 Disaster Recovery

**If System Goes Down:**

**Phase 1: Immediate Response (First 30 min)**

1. Identify scope:
   - Is PowerApp unavailable?
   - Are SharePoint lists accessible?
   - Can users access reporting?

2. Communicate to users:
   - Post message in Teams
   - Send email if Teams down
   - Provide status updates every 30 minutes

3. Engage support:
   - Contact Microsoft Support (if Azure/O365 issue)
   - Contact IT leadership
   - Document time issue started

**Phase 2: Recovery (Within 2 hours)**

1. Check service status:
   - https://status.office365.com
   - Check Power Platform status page

2. If Microsoft service issue:
   - Wait for Microsoft to resolve
   - No action needed on your end
   - Provide users status updates

3. If local issue (PowerApp or configuration):
   - Check Power Automate logs for failed flows
   - Review recent changes
   - Attempt rollback if recent change made

**Phase 3: Restoration**

1. Verify all components working:
   - Users can log in
   - Users can submit audits
   - Power Automate flows processing
   - Reports loading

2. Check data integrity:
   - Recent submissions saved correctly
   - No data loss
   - Flows didn't skip or duplicate

3. Document incident:
   - What failed, when, for how long
   - Root cause
   - Steps to prevent recurrence
   - Post-incident review

```

---

### Document Footer

```markdown
---

**Document Version:** 1.0
**Last Updated:** [Current Date]
**Next Review Date:** [6 months]
**Maintained by:** IT Administration + MERT Educators
**Approved by:** IT Director, MERT Lead Educator

For feedback or corrections to this guide, contact: it.support@rbwh.org.au

---
```

---

## Task 4.4.3-4.4.4: Training Videos

**Objectives:** Create video recordings to train users on system functionality.

**Duration:** 4 hours (auditor) + 3 hours (manager) = 7 hours total
**Deliverables:** Two MP4 videos for on-demand viewing

### Video 4.4.3: Auditor Training Video (15-20 minutes)

**Production Specifications:**

| Aspect | Specification |
|--------|---------------|
| Duration | 15-20 minutes |
| Format | MP4, 1080p minimum, 60 fps |
| Audio | Stereo, 128 kbps minimum |
| Captions | Embedded SRT file (English) |
| Screen Recording | 1920x1080 minimum resolution |
| Hosting | SharePoint document library + YouTube (if approved) |

**Script Outline - Auditor Training Video**

```markdown
## VIDEO SCRIPT: Auditor Training (16 minutes)

### SEGMENT 1: INTRODUCTION (1 minute)

[VISUAL: Title slide with RBWH branding]

NARRATOR: "Welcome to the RBWH Trolley Audit System training for auditors.
This video will walk you through completing your first audit from start to finish.
By the end, you'll know exactly what to do when you open the app."

[VISUAL: Show 3 key benefits on screen]

NARRATOR: "Three key things you'll learn today:
1. How to access the app and log in
2. How to complete each audit section step-by-step
3. How to review and submit your audit"

---

### SEGMENT 2: ACCESS & LOGIN (2 minutes)

[VISUAL: Screen recording - App store screen]

NARRATOR: "First, you need to install the Power Apps app from your device's app store.
Search for 'Power Apps' and download the official Microsoft app."

[VISUAL: Show app icon]

NARRATOR: "Once installed, open the app and you'll see a login screen.
Enter your RBWH email address - that's firstname dot lastname at RBWH dot org dot au"

[VISUAL: Demonstrate login with test account]

NARRATOR: "Enter your RBWH network password, then accept the permissions.
You'll see your available apps - select RBWH Trolley Audit."

[VISUAL: App loading]

NARRATOR: "The app will load. This usually takes 30-45 seconds on first launch.
You'll see the Home screen once it's ready."

---

### SEGMENT 3: HOME SCREEN OVERVIEW (1 minute)

[VISUAL: Screen recording - Home screen]

NARRATOR: "Here's the Home screen. At the top, you'll see RBWH logo and your name.
Below that are four main buttons."

[VISUAL: Highlight each button]

NARRATOR: "The big blue button labeled 'Start New Audit' - that's where you begin an audit.
'View My Audits' shows audits you've already submitted.
'This Week's Random Audits' shows which trolleys you should audit this week.
And 'Help' takes you to documentation if you get stuck."

[VISUAL: Highlight Start New Audit button]

NARRATOR: "To begin an audit, tap 'Start New Audit'."

---

### SEGMENT 4: AUDIT WORKFLOW - TROLLEY SELECTION (3 minutes)

[VISUAL: Screen recording - Trolley selection screen]

NARRATOR: "You're now on the 'Select Trolley' screen. Here you'll pick which trolley to audit.
Tap the dropdown that says 'Which trolley are you auditing?'"

[VISUAL: Demonstrate typing in dropdown]

NARRATOR: "You can search by trolley location name, building, or department.
Let me search for ICU Bay 1."

[VISUAL: Show search results appearing]

NARRATOR: "See how the app is filtering results as I type?
Find your trolley and tap it to select it."

[VISUAL: Select trolley]

NARRATOR: "Great! Now you see some information about this trolley.
Notice it says 'Last audited on [date]' - this tells you when the trolley was last audited.
Below that, you choose your audit type."

[VISUAL: Highlight audit type options]

NARRATOR: "For a full audit, select 'Comprehensive'.
This checks documentation, equipment, condition - everything.
For a quick check, select 'Spot Check'.
Most weekly audits will be spot checks, but comprehensive audits might be requested."

[VISUAL: Select audit type]

NARRATOR: "Once you've selected your trolley and audit type, tap the 'Next' button."

---

### SEGMENT 5: AUDIT WORKFLOW - DOCUMENTATION (3 minutes)

[VISUAL: Screen recording - Documentation screen]

NARRATOR: "You're now on the Documentation screen.
This step only appears for comprehensive audits.
Here you're checking that required documents are available at the trolley."

[VISUAL: Highlight first question]

NARRATOR: "First question: 'Is the Check Record present?'
The Check Record is a sheet that documents previous audits.
You have three options:
- Yes, current version (printed recently, within 3 months)
- Yes, old version (present but older than 3 months)
- No (not visible at the trolley)"

[VISUAL: Show example of check record]

NARRATOR: "Look for a check record at the trolley location.
If you find one with today's date or a recent date, select 'Yes, current version'.
If it's old or you can't find one, select the appropriate option."

[VISUAL: Move to next question]

NARRATOR: "Second question: 'Checking guidelines present?'
This is a poster or printed sheet showing how to audit the trolley correctly.
Again, you're looking for current vs. old vs. not present."

[VISUAL: Demonstrate answering]

NARRATOR: "Third question: 'BLS Poster Present?'
BLS stands for Basic Life Support. Look for a poster with step-by-step CPR instructions.
It's usually laminated and color-coded. Simple yes or no."

[VISUAL: Show typical BLS poster]

NARRATOR: "Finally: 'Equipment List Present?'
This is a printed or posted list showing what equipment should be on the trolley.
Again, current version, old version, or not present."

[VISUAL: Demonstrate completing all]

NARRATOR: "Once you've answered all four documentation questions, tap 'Next'
to move to the Trolley Condition screen."

---

### SEGMENT 6: AUDIT WORKFLOW - TROLLEY CONDITION (3 minutes)

[VISUAL: Screen recording - Trolley Condition screen]

NARRATOR: "Now you're assessing the physical condition of the trolley itself.
This includes cleanliness, whether it works properly, and condition of attachments."

[VISUAL: Highlight first question]

NARRATOR: "First: 'Is the trolley clean?'
Look for dirt, stains, sticky spots, or any visible contamination.
If it's clean, select yes. If it needs cleaning, select no.
A text box will appear asking for details - describe what you see."

[VISUAL: Demonstrate yes response]

NARRATOR: "Second: 'Is trolley in working order?'
Open and close all drawers to confirm they move smoothly.
Check that wheels roll freely, handles work, nothing is broken.
If everything works, select yes. If something is broken, select no and describe it."

[VISUAL: Show checking drawer movement]

NARRATOR: "Third: 'Are rubber bands present?'
These hold equipment in place during transport.
Look for rubber bands around drawers or handle. Yes or no?"

[VISUAL: Highlight rubber bands on physical trolley]

NARRATOR: "Fourth: 'Is O2 tubing correct?'
Check if oxygen tubing is connected properly to the oxygen cylinder.
It shouldn't be kinked or disconnected. Yes or no?"

[VISUAL: Show oxygen connection]

NARRATOR: "Finally: 'INHALO cylinder' - this only applies if your trolley carries this equipment.
Look at the cylinder pressure gauge. Is it showing good pressure?
Select 'Not Applicable' if your trolley doesn't carry INHALO."

[VISUAL: Show INHALO gauge]

NARRATOR: "Once you've assessed trolley condition, tap 'Next' to continue."

---

### SEGMENT 7: AUDIT WORKFLOW - ROUTINE CHECKS (2 minutes)

[VISUAL: Screen recording - Routine Checks screen]

NARRATOR: "The Routine Checks screen shows how often ward staff are checking this trolley.
The app calculates how many checks you'd EXPECT based on time since the last audit.
You enter how many you actually found."

[VISUAL: Highlight first field]

NARRATOR: "First field: 'Outside check count' - these are daily checks done on the outside.
The app shows 'Expected: 5' - meaning since the last audit, there should be 5 daily checks.
Look for a check sheet, paper tally, or marks on a clipboard.
Count how many checks are documented and enter that number."

[VISUAL: Show example check sheet]

NARRATOR: "Second field: 'Inside check count' - weekly checks of equipment inside.
The app shows 'Expected: 2' - so you'd expect 2 entries since last audit.
Count what you actually see and enter that number."

[VISUAL: Demonstrate entering numbers]

NARRATOR: "If you can't find the check sheet or it's unavailable,
select the 'Checks Not Available' checkbox and briefly explain why -
for example, 'Staff on leave' or 'Check sheet lost'."

[VISUAL: Show checkbox option]

NARRATOR: "This helps managers understand if the trolley wasn't being checked properly.
Once you've entered check counts, tap 'Next' to go to the Equipment Checklist."

---

### SEGMENT 8: AUDIT WORKFLOW - EQUIPMENT (4 minutes)

[VISUAL: Screen recording - Equipment Checklist screen]

NARRATOR: "Here's the main Equipment Checklist - the most important part of your audit.
This is where you verify that all equipment is present in correct quantities.
The screen is organized by category to help you stay organized."

[VISUAL: Show category headers]

NARRATOR: "You'll see sections like 'Top of Trolley', 'Drawer 1: Airway',
'Drawer 2: Breathing', and so on. Tap a category to expand it."

[VISUAL: Expand Top of Trolley category]

NARRATOR: "Inside each category, you see a list of equipment items.
For each item, there's a quantity field showing what you EXPECT,
and an input field showing 'Quantity Found'."

[VISUAL: Highlight one equipment row]

NARRATOR: "Here's an example: 'Ambu Bag - Expected 2 units'.
You need to actually count the Ambu bags in this trolley and enter what you find.
The app shows 'Expected: 2', so if you find 2, enter 2. If you find 1, enter 1."

[VISUAL: Demonstrate counting in drawer]

NARRATOR: "If you find the correct quantity, the row stays neutral colored.
If you find fewer than expected, the row turns yellow or red -
that's OK, just enter the actual number you find."

[VISUAL: Show color coding examples]

NARRATOR: "If an item is completely missing, leave the quantity field blank or enter 0.
There's also a Notes field where you can explain - for example, 'Found 1 expired, 1 good'."

[VISUAL: Show notes field]

NARRATOR: "Important tip: The app is intelligent about your trolley.
If your trolley doesn't have a paediatric box, those items won't show up.
If your trolley has a specific defibrillator type, only the matching pads will show."

[VISUAL: Show filtered equipment list]

NARRATOR: "Go through each category and enter quantities for all visible items.
Remember: enter the ACTUAL quantity you find, not what you hope is there.
The numbers help managers know what needs restocking."

[VISUAL: Demonstrate moving through multiple items]

NARRATOR: "Once you've gone through all equipment items, tap 'Next'
to see the Review and Submit screen."

---

### SEGMENT 9: AUDIT WORKFLOW - REVIEW & SUBMIT (2 minutes)

[VISUAL: Screen recording - Review screen]

NARRATOR: "Now you're on the Review screen. This shows a summary of your entire audit
before you submit. Take a moment to scan through and verify everything looks right."

[VISUAL: Show scrolling through review]

NARRATOR: "You'll see each section summarized:
- Your trolley selection
- Documentation findings
- Condition assessment
- Routine check counts
- Equipment checklist with all your entries"

[VISUAL: Highlight different sections as mentioned]

NARRATOR: "If you notice something wrong, tap the 'Edit' button next to that section.
You'll go back to fix it, then return to this review."

[VISUAL: Demonstrate edit button]

NARRATOR: "At the bottom, you have three options:
'Submit Audit' to send your audit to management,
'Save as Draft' to save without submitting (useful if you need to finish later),
or 'Cancel' to discard without saving."

[VISUAL: Highlight buttons]

NARRATOR: "Once everything looks good, tap 'Submit Audit'."

[VISUAL: Show submission processing]

NARRATOR: "The app will process and submit your audit.
You'll see a confirmation message and an email will be sent confirming your submission.
Your audit is now complete!"

---

### SEGMENT 10: NEXT STEPS & SUPPORT (1 minute)

[VISUAL: Back to home screen]

NARRATOR: "Congratulations! You've successfully completed an audit.
Now you can see 'View My Audits' to see your submissions,
or 'Start New Audit' to audit the next trolley."

[VISUAL: Show menu options]

NARRATOR: "If you get stuck at any point:
- The 'Help' menu has answers to common questions
- Tap 'Support Contacts' for phone numbers and emails
- If you need technical help, contact IT Support
- If you have audit process questions, contact MERT Educators"

[VISUAL: Show support contact options]

NARRATOR: "That's it! You're ready to audit trolleys using the new system.
Thank you for keeping RBWH resuscitation trolleys audit-ready and compliant."

[VISUAL: Closing slide with branding]

END OF VIDEO
```

---

### Video 4.4.4: Manager Training Video (10-15 minutes)

**Script Outline - Manager Training Video**

```markdown
## VIDEO SCRIPT: Manager Training (13 minutes)

### SEGMENT 1: INTRODUCTION (1 minute)

[VISUAL: Title slide - Manager/Educator Edition]

NARRATOR: "Welcome to the RBWH Trolley Audit System training for managers and educators.
This video shows you how to access audit data, review submissions,
manage issues, and generate reports."

[VISUAL: Show 4 key responsibilities]

NARRATOR: "You'll learn:
1. How to access the manager dashboard
2. How to review auditor submissions
3. How to manage issues and corrective actions
4. How to access compliance reports"

---

### SEGMENT 2: ACCESS & LOGIN (1 minute)

[VISUAL: Show login process on desktop browser]

NARRATOR: "As a manager, you have two ways to access the system.
First, you can use the mobile app just like auditors.
Open Power Apps, select RBWH Trolley Audit, and you'll see manager options."

[VISUAL: Show app with manager menu]

NARRATOR: "Second, and most useful for managers, is web access.
Open a web browser and navigate to the app.powerbi.com site.
Log in with your RBWH credentials."

[VISUAL: Show Power BI login]

NARRATOR: "Once logged in, you'll see access to reports and dashboards
showing your department's audit data."

---

### SEGMENT 3: REVIEWING AUDIT SUBMISSIONS (3 minutes)

[VISUAL: Screen recording - Audit list view]

NARRATOR: "From the manager menu in the PowerApp,
select 'View Audits' to see all audit submissions."

[VISUAL: Show audit list loading]

NARRATOR: "Here you see all recent audits from your service line or assigned trolleys.
Each row shows the trolley location, audit date, auditor name, and compliance score."

[VISUAL: Highlight columns]

NARRATOR: "You can filter the list by date range, trolley, or compliance score.
For example, filter to show only audits from this week, or only audits with low scores."

[VISUAL: Demonstrate filtering]

NARRATOR: "Click on any audit to see full details."

[VISUAL: Open sample audit]

NARRATOR: "Here you see every question and the auditor's response.
You can verify the audit looks complete and reasonable.
If something looks wrong - like a critical item missing -
you can follow up with the auditor."

[VISUAL: Show reviewing audit details]

NARRATOR: "Notice at the bottom there's a 'Compliance Score: 87%'
This is calculated automatically based on equipment found vs. expected.
If you disagree with a score, you can contact MERT educators."

[VISUAL: Highlight compliance score]

NARRATOR: "Key things to look for when reviewing:
1. Auditor name is someone you recognize
2. Audit date is recent, not from weeks ago
3. All sections are completed (no blanks)
4. Equipment quantities seem reasonable
5. Any flagged issues are documented"

[VISUAL: Checklist appears on screen]

---

### SEGMENT 4: MANAGING ISSUES (3 minutes)

[VISUAL: Screen recording - Issue list view]

NARRATOR: "From the manager menu, select 'View Issues' to see problems reported
during audits that need action."

[VISUAL: Show issue list]

NARRATOR: "Each issue shows:
- Issue title and description
- Severity level (Critical, High, Medium, Low)
- Location it affects
- Who it's assigned to
- Days since reported"

[VISUAL: Highlight each column]

NARRATOR: "Filter by status to see 'Open' issues that need action.
Critical and High severity issues need immediate attention."

[VISUAL: Show filtering to Critical only]

NARRATOR: "Click an issue to open the detail view."

[VISUAL: Open issue detail]

NARRATOR: "Here you see the full description of the problem.
Below that are 'Corrective Actions' - steps your team is taking to fix it.
And comments from the team discussing the issue."

[VISUAL: Show actions and comments section]

NARRATOR: "As manager, you can:
1. Add corrective actions - what will be done and by when
2. Add comments explaining the situation
3. Mark as resolved once fixed
4. Close the issue once verified"

[VISUAL: Show action buttons]

NARRATOR: "System tracks response times:
- Critical issues: should be addressed within 24 hours
- High issues: within 3 days
- Medium issues: within 5 days
- Low issues: within 10 days

If an issue is aging and no action taken, it will escalate automatically."

[VISUAL: Show escalation warning]

NARRATOR: "Best practice: review issues daily, assign actions immediately,
and update status as work progresses."

---

### SEGMENT 5: COMPLIANCE REPORTS (2.5 minutes)

[VISUAL: Screen recording - Power BI dashboard]

NARRATOR: "To see compliance data and trends, navigate to Power BI reports.
Click 'Reports' on the manager menu or go directly to powerbi.com."

[VISUAL: Show Power BI loading]

NARRATOR: "You'll see several dashboards. Let me show you the main ones."

[VISUAL: Highlight main dashboard]

NARRATOR: "The 'Trolley Audit Dashboard' shows overall metrics:
- Audit Completion Rate: percentage of trolleys audited recently
- Average Compliance Score: average equipment compliance
- Overdue Trolleys: how many haven't been audited in 365 days
- Open Issues: number of unresolved problems"

[VISUAL: Show each KPI card]

NARRATOR: "Below that are visual charts:
This 'Compliance Trend' line chart shows how compliance is changing over time.
If the line is going up, good! If down, there's a problem to investigate."

[VISUAL: Highlight trend chart]

NARRATOR: "The 'Service Line Comparison' bar chart shows which departments
are doing well with compliance and which need help."

[VISUAL: Show bar chart]

NARRATOR: "The 'Equipment Deficiency' table shows the most commonly missing items.
If you see the same item repeatedly missing, coordinate with CELS/Pharmacy
to ensure it's being stocked."

[VISUAL: Show table]

NARRATOR: "You can click any metric to drill down and see details.
For example, click 'Overdue Trolleys' to see exactly which trolleys
need audits in the next week."

[VISUAL: Demonstrate drill-down]

---

### SEGMENT 6: GENERATING RANDOM AUDITS (2 minutes)

[VISUAL: Screen recording - Random selection screen]

NARRATOR: "MERT educators generate the weekly random selection of trolleys to audit.
But as a manager, you'll see the 'This Week's Audits' list in the app."

[VISUAL: Show selection list]

NARRATOR: "This tells you which 10 trolleys should be spot-checked this week.
You use this to assign audit work to your staff."

[VISUAL: Highlight trolley list]

NARRATOR: "As auditors complete audits from the random selection,
you'll see the 'Completed' count go up.
By week end, ideally all 10 are completed."

[VISUAL: Show completion progress]

NARRATOR: "If an audit isn't completed by Friday, follow up with the assigned auditor
to ensure it gets done."

---

### SEGMENT 7: COMMON MANAGER TASKS (2 minutes)

[VISUAL: Screen recording - Various screens]

NARRATOR: "Here are common things managers do in the system:"

[VISUAL: Show 5 task boxes]

NARRATOR: "1. Add New Trolley: If your department gets a new resuscitation trolley,
you (or an educator) can add it to the system so it appears in the audit list."

NARRATOR: "2. Update Trolley Info: If location moves or equipment configuration changes,
update the trolley record so audits are relevant."

NARRATOR: "3. Manage Compliance by Equipment: If you notice an item is consistently missing,
coordinate with the right department to ensure restocking."

NARRATOR: "4. Track Issue Resolution: Monitor that corrective actions are completed
and issues are properly closed."

NARRATOR: "5. Verify Audit Quality: Spot-check audits from new auditors to ensure
they're filling out the form correctly."

---

### SEGMENT 8: SUPPORT & QUESTIONS (1 minute)

[VISUAL: Support contact information on screen]

NARRATOR: "If you have questions about the system process:
Contact MERT Educators at mert@rbwh.org.au"

NARRATOR: "If you have technical issues:
Contact IT Support at it.support@rbwh.org.au"

NARRATOR: "If you're unsure about audit findings or compliance scores:
Reach out to MERT educators - they review audits and can explain findings."

[VISUAL: Contact info displayed]

NARRATOR: "You're ready to use the new system to track trolley compliance
and keep your department's audit status current. Thank you!"

[VISUAL: Closing slide]

END OF VIDEO
```

---

## Task 4.4.5-4.4.6: Training Sessions

**Objectives:** Conduct live training sessions for auditors and managers.

**Delivery Method:** Live Zoom/Teams sessions with hands-on practice

### Training Session 4.4.5: Auditor Training Session (2 hours)

**Session Agenda**

```markdown
## AUDITOR TRAINING SESSION AGENDA
Date: [TBD]
Time: 2 hours
Location: [Zoom/Teams link]
Attendees: ~50 auditors across all service lines

### Agenda Breakdown:

**0:00-0:05 (5 min) - Welcome & Housekeeping**
- Welcome participants
- Agenda overview
- Zoom controls tour (mute, chat, raise hand)
- Q&A protocol: chat for questions during, unmute to ask live

**0:05-0:15 (10 min) - System Overview**
- What is the new trolley audit system?
- Why we're replacing Microsoft Forms
- Key benefits for auditors vs. old system
- Timeline and deployment plan

**0:15-0:30 (15 min) - System Access**
- Download Power Apps app (demo on screen)
- Login with RBWH credentials
- What if login fails? (troubleshooting)
- Resetting passwords
- Show what Home screen looks like
- Ask: "Can everyone see the home screen?"

**0:30-0:50 (20 min) - Completing an Audit (Live Demo)**
- Live walkthrough of complete audit
- Presenter screen shares their device
- Step 1: Select trolley
  - Show search functionality
  - Demonstrate multiple search methods
  - Show last audit date display
- Step 2: Documentation (if comprehensive)
  - Point out each question
  - Explain what to look for
- Step 3: Trolley condition
  - Show physical examples (photos/video)
  - Explain yes/no decisions
- Step 4: Routine checks
  - Explain expected vs. found
- Step 5: Equipment
  - Show category accordion
  - Demonstrate entering quantities
  - Show color coding
  - Explain what red/yellow means
- Step 6: Review
  - Show review screen layout
  - Show edit buttons
  - Explain submit vs. save draft

**0:50-1:10 (20 min) - Hands-On Practice**
- Participants attempt first audit
- Facilitators available for help (breakout rooms if needed)
- "Dummy" trolley to practice with
- Do NOT submit - just complete draft
- Facilitators circulate via breakout rooms

**1:10-1:20 (10 min) - Break & Troubleshooting**
- Answer questions from practice
- Address common issues
- "I couldn't find the trolley..."
- "What if I made a mistake?"
- "Can I save and continue later?"

**1:20-1:40 (20 min) - Common Questions & Edge Cases**
- Q: How long does an audit actually take?
- Q: What if equipment is expired?
- Q: What if a drawer is stuck?
- Q: Can I use my personal phone?
- Q: What if I'm in an area without WiFi?
- Q: How do I know which trolley to audit?
- Q: What happens after I submit?

**1:40-1:50 (10 min) - Support & Going Live**
- Support contacts (phone, email)
- When to contact IT vs. MERT educators
- Going live date
- First few weeks will have active support

**1:50-2:00 (10 min) - Wrap-up & Feedback**
- Open Q&A - unmute and ask anything
- Feedback survey (link in chat)
- "Thank you" and confirmation of system launch date
- Recording will be available for those who need to watch later

### Training Materials Provided:
- PowerPoint slides (emailed before training)
- User Guide PDF (as reference during session)
- Dummy trolley location for practice
- Troubleshooting guide (quick reference)
- Support contact sheet
```

---

### Training Session 4.4.6: Manager Training Session (1.5 hours)

**Session Agenda**

```markdown
## MANAGER TRAINING SESSION AGENDA
Date: [TBD]
Time: 1.5 hours
Location: [Zoom/Teams link]
Attendees: ~20-25 managers/educators/directors

### Agenda Breakdown:

**0:00-0:05 (5 min) - Welcome**
- Welcome managers and educators
- Agenda overview
- Q&A protocol

**0:05-0:15 (10 min) - System Overview for Managers**
- Why the new system matters for management
- What's changing from Microsoft Forms
- Key manager responsibilities:
  - Reviewing audits
  - Managing issues
  - Using reports
  - Staff training/oversight
- Timeline

**0:15-0:30 (15 min) - Reviewing Audit Data**
- How to access submissions
- Audit list view and filtering
- Opening and reviewing individual audits
- What to look for in audit quality
- Demo: "This audit looks good" vs. "this one has issues"
- Where to find compliance scores
- How scores are calculated

**0:30-0:50 (20 min) - Issue Management Workflow**
- Where issues appear in the system
- Issue status workflow (New → Assigned → In Progress → Resolved → Closed)
- Creating/assigning corrective actions
- Adding comments
- Response time expectations
- Escalation process
- Demo: Managing an example issue from start to close

**0:50-1:10 (20 min) - Reports & Compliance Dashboards**
- Accessing Power BI reports
- Reading the main dashboard
  - Audit completion rate
  - Average compliance score
  - Overdue trolleys
  - Open issues
- Understanding trend charts
- Filtering reports by date range, service line
- Drilling into details
- How to use data for:
  - Identifying problem areas
  - Tracking progress
  - Reporting to leadership

**1:10-1:20 (10 min) - Common Manager Questions**
- Q: What if we disagree with a compliance score?
- Q: Equipment is missing - what's the next step?
- Q: How often should I review audits?
- Q: How do I know if an auditor is doing it right?
- Q: Can I edit an audit after submission?
- Q: What if there's a critical safety issue?

**1:20-1:30 (10 min) - Support & Going Live**
- Support process for issues
- Training your team on their responsibilities
- Going live date and timeline
- First week support will be active
- Encouraging early adoption

**1:30-1:35 (5 min) - Wrap-up**
- Feedback survey
- Recording will be available
- "Thank you" and confirmation of launch

### Training Materials Provided:
- PowerPoint slides (manager version)
- Admin Guide excerpt (PDF for reference)
- Dashboard walkthrough guide
- Sample issue workflow document
- Support contact information
```

---

## Task 4.4.7: Production Permissions

**Objective:** Configure final production-grade RBAC and verify access controls.

**Duration:** 2 hours
**Owner:** System Administrator

### Permissions Configuration Checklist

```markdown
## PRODUCTION PERMISSIONS CONFIGURATION

### Phase 1: Pre-Production Review (30 min)

**Audit Current State:**

- [ ] List all current users in system
- [ ] Verify each user has appropriate role
- [ ] Identify and remove test accounts
- [ ] Document final user counts per role:
  - Auditors: ___ users
  - Managers: ___ users
  - Educators: ___ users
  - Admins: ___ users

**Identify Test/Training Data:**

- [ ] Find all test audit records (created during development)
- [ ] Locate test trolley locations
- [ ] Identify dummy data in lists
- [ ] Document cleanup scope

---

### Phase 2: Clean Up Test Data (30 min)

**Remove Test Accounts:**

1. Access Azure AD:
   ```
   Connect to Azure AD > Users & Groups
   ```
2. Identify test accounts:
   - Names containing "test", "demo", "training"
   - Emails with @test, @training suffix
   - Disabled accounts still in groups
3. Remove from all trolley groups:
   ```
   For each test account:
   - Remove from rbwh-trolley-auditors
   - Remove from rbwh-trolley-managers
   - Remove from rbwh-trolley-educators
   - Remove from rbwh-trolley-admins
   ```
4. Verify removal completed
   - [ ] No test accounts in any group
   - [ ] No test account logins in last 24 hours

**Delete Test Data from SharePoint:**

1. Access SharePoint site
2. Go to "Audit" list
3. Filter for test records:
   - Created before [go-live date]
   - With test auditor names
4. Delete test records:
   ```
   Select all test records > Delete
   Confirm: "Yes, permanently delete"
   ```
5. Verify deletion:
   - [ ] Audit list has only production data
   - [ ] All test submissions removed

**Archive Test Trolleys:**

1. Go to Location list
2. Identify test/dummy trolley entries
3. For each:
   - Edit and mark as "Archived"
   - Note in description: "Archived [date] - test record"
4. Verify:
   - [ ] No test trolleys in active list
   - [ ] Test trolleys no longer appear in auditor selections

---

### Phase 3: Configure Production Permissions (45 min)

**Azure AD Security Groups:**

Verify final group configuration:

```
rbwh-trolley-auditors@rbwh.org.au (50-60 members expected)
  Members:
    - All clinical staff authorized to conduct audits
    - Ward nurses, senior nurses, clinical educators
  Verify: [ ] All correct, [ ] No test accounts

rbwh-trolley-managers@rbwh.org.au (20-30 members expected)
  Members:
    - NUM (Nurse Unit Managers)
    - Ward managers
    - Service directors
    - MERT educators who review audits
  Verify: [ ] All correct, [ ] No test accounts

rbwh-trolley-educators@rbwh.org.au (3-5 members expected)
  Members:
    - MERT Lead Educator
    - MERT educators with admin responsibilities
  Verify: [ ] All correct

rbwh-trolley-admins@rbwh.org.au (1-2 members expected)
  Members:
    - IT administrator for trolley system
    - IT manager (backup)
  Verify: [ ] All correct
```

**SharePoint List Permissions:**

For each list in the SharePoint site:

```
Location List
  - rbwh-trolley-auditors: [Edit] - can submit audits, read locations
  - rbwh-trolley-managers: [Edit] - can edit, view all
  - rbwh-trolley-educators: [Full Control]
  - rbwh-trolley-admins: [Full Control]

Audit List
  - rbwh-trolley-auditors: [Create/Edit Own] - can create, edit own, read
  - rbwh-trolley-managers: [Edit] - view all, read/edit
  - rbwh-trolley-educators: [Full Control]
  - rbwh-trolley-admins: [Full Control]

Issue List
  - rbwh-trolley-managers: [Edit] - can manage issues
  - rbwh-trolley-educators: [Full Control]
  - rbwh-trolley-admins: [Full Control]

Equipment List
  - rbwh-trolley-auditors: [Read] - view only
  - rbwh-trolley-managers: [Read] - view only
  - rbwh-trolley-educators: [Edit] - can modify equipment list
  - rbwh-trolley-admins: [Full Control]
```

**PowerApp Share Settings:**

1. Open Power Apps admin center
2. Select "RBWH Trolley Audit" app
3. Go to "Share" section
4. Configure sharing:
   - rbwh-trolley-auditors: [User] role → can run app only
   - rbwh-trolley-managers: [User] role → can run app + view reports
   - rbwh-trolley-educators: [Co-owner] role → can edit app + admin
   - rbwh-trolley-admins: [Owner] role → full control

**Power Automate Flows:**

1. Verify all flows owned by service account (not personal)
2. All flows set to "Production" environment (not test)
3. Flow sharing configured correctly:
   - Run-only access for auditors (can trigger audit submit)
   - Run + edit for managers (can trigger issue actions)
   - Full control for educators/admins

---

### Phase 4: Security Verification (15 min)

**Verify Access Controls Are Working:**

Test each role:

```
TEST 1: Auditor Account
  - Can access PowerApp ✓
  - Can start new audit ✓
  - Can see only permitted trolleys ✓
  - Cannot access Admin screens ✗
  - Cannot view other auditors' drafts ✗

TEST 2: Manager Account
  - Can access PowerApp ✓
  - Can view all audits ✓
  - Can create/edit issues ✓
  - Cannot delete audit records ✗
  - Cannot edit PowerApp ✗

TEST 3: Educator Account
  - Can access all features ✓
  - Can edit trolley configuration ✓
  - Can modify equipment list ✓
  - Can view system settings ✓

TEST 4: Admin Account
  - Can access all features ✓
  - Can modify all data ✓
  - Can edit flows and configurations ✓
```

**Document Test Results:**

- [ ] All role access tests passed
- [ ] No unauthorized access observed
- [ ] Security boundaries working correctly

---

### Phase 5: Final Verification Checklist (15 min)

Before going live, verify:

- [ ] All production user accounts have correct permissions
- [ ] No test accounts exist in production
- [ ] No test data remains in SharePoint lists
- [ ] All security groups have final member count
- [ ] PowerApp role-based security configured
- [ ] Power Automate flows in production environment
- [ ] Backup of configuration completed
- [ ] Disaster recovery documentation updated
- [ ] Password policy configured (if applicable)
- [ ] MFA enabled for admin accounts
- [ ] Audit logging enabled for compliance

---

### Phase 6: Documentation & Handoff (15 min)

**Create Production Documentation:**

1. Final permission matrix document:
   ```
   - User role definitions
   - Permission levels by role
   - SharePoint access matrix
   - PowerApp access matrix
   ```

2. Emergency access procedures:
   ```
   - What to do if admin account locked
   - How to add new user urgently
   - Emergency permission elevation process
   ```

3. Ongoing maintenance checklist:
   ```
   - Monthly: Review user access
   - Quarterly: Audit permissions against current staff list
   - Annually: Security review
   ```

**Sign-Off:**

- [ ] IT Director approves final permissions
- [ ] MERT Lead Educator approves user roles
- [ ] Project Lead signs off on security review
- [ ] Document filed in project repository

---

### Rollback Procedure

If critical permission issues discovered immediately after go-live:

1. Identify affected users/role
2. Determine if issue affects data integrity or security
3. If critical:
   - Temporarily restrict access for affected role
   - Notify affected users
   - Fix permission configuration
   - Test fix
   - Re-enable access
4. If non-critical:
   - Schedule fix for next business day
   - Document workaround
   - Implement fix after hours

---
```

---

## Task 4.4.8: Go-Live Deployment

**Objective:** Execute controlled production deployment with monitoring and support.

**Duration:** 2 hours (launch window) + 1 week post-go-live support
**Owner:** Project Lead + System Administrator + Support Team

### Pre-Go-Live Checklist (48 hours before launch)

```markdown
## PRE-GO-LIVE DEPLOYMENT CHECKLIST

### 24 Hours Before Go-Live

**System Readiness:**
- [ ] All training videos completed and uploaded
- [ ] All documentation finalized and published
- [ ] Production permissions configured and tested
- [ ] No test data remains in production lists
- [ ] Power Automate flows verified working
- [ ] Power BI reports loaded with current data
- [ ] Backups completed

**Communication Sent:**
- [ ] Go-live announcement email to all users
  - What's launching
  - When it launches
  - How to access
  - Support contacts
  - Link to training materials
- [ ] Manager briefing completed
  - Their roles and responsibilities
  - What to expect first week
- [ ] IT Support briefed
  - Common issues to expect
  - How to help auditors
  - Escalation path

**Contingency Prepared:**
- [ ] Rollback plan documented
- [ ] Emergency contact list prepared
- [ ] Escalation procedures defined
- [ ] Incident response team identified

---

### Go-Live Day - Launch Window (2 hours)

**T-30 minutes (Preparation):**
- [ ] All systems verified online and working
- [ ] Support team online and ready
- [ ] Project lead in main communication channel
- [ ] Send final reminder email to users

**T-00 (System Go-Live):**

1. **Final Verification (5 min):**
   - PowerApp accessible to all users
   - SharePoint lists responding
   - Power Automate flows triggering
   - Power BI reports loading
   - No error messages

2. **Send Go-Live Announcement (5 min):**
   ```
   Email Subject: "RBWH Trolley Audit System is Now Live!"

   Body:
   "The new RBWH Trolley Audit System is now live.

   How to access:
   - Open Power Apps app on your phone/tablet
   - Or visit [PowerApp URL] on computer
   - Log in with your RBWH email

   First steps:
   1. Watch the training video (15 min)
   2. Contact your manager for your first trolley to audit
   3. Complete your first audit

   Support:
   - Questions? Contact [email]
   - Technical issues? Call [phone]

   We're excited to launch this system!"
   ```

3. **Monitor Activity (remaining time):**
   - Watch for user logins
   - Monitor for error messages
   - Track submitted audits
   - Ready to help with questions

**T+1 hour (Status Check):**
- [ ] First audits being submitted successfully
- [ ] Users able to login without issues
- [ ] No critical errors reported
- [ ] System performing normally

**T+2 hours (Handoff to Support):**
- If all working: transition to 24/7 support mode
- If issues: activate incident response plan

---

### Rollback Criteria

**Deploy rollback if ANY of:**
- System unable to accept new audits (database errors)
- Data corruption detected
- Security breach detected
- More than 20% of users unable to access
- Critical data loss

**Rollback Process:**
1. Notify all users immediately: "System maintenance in progress"
2. Revert to last backup (typically 1 hour before issue)
3. Investigate root cause
4. Fix issue
5. Re-deploy with testing
6. Notify users when resumed

---

### Communication Plan - First Week

**Day 1 (Launch Day) - Hourly Updates:**
- 9:00am: System live, users start connecting
- 10:00am: Status: [numbers of audits submitted], all working smoothly
- 12:00pm: Status: [more numbers], minor questions answered, system stable
- 3:00pm: Status: [end of day numbers], overall successful launch

**Day 2-5 - Daily Standup:**
- 8:30am: "Good morning! System status: [brief summary]"
  - Number of audits submitted yesterday
  - Any issues reported/resolved
  - Reminder about support contacts
  - Encouragement to try first audit if not done

**Day 7 (One Week) - Launch Retrospective:**
- Send thank you email to all participants
- Share statistics: "X audits submitted, Y users trained"
- Announce: "Moving to standard support - only critical issues"
- Provide feedback survey link

---

### Support Contact Setup

**First Week Support Team:**

```
Role: Primary Support Line
Contact: [Phone number]
Hours: 7:00am - 6:00pm (first week)
Handles: All user questions and technical issues

Role: Secondary Support (Escalation)
Contact: [Backup phone/email]
Hours: 7:00am - 6:00pm
Handles: Complex issues, rollback decisions

Role: IT Infrastructure
Contact: [Email]
Hours: 24/7 on-call
Handles: System down scenarios, database issues

Role: MERT Educators
Contact: [Email]
Hours: 8:30am - 4:30pm
Handles: Process questions, audit interpretation
```

**Support Response Times:**

| Severity | Response Time | Resolution Time |
|----------|---------------|-----------------|
| Critical (system down) | 15 minutes | 1 hour |
| High (many users affected) | 30 minutes | 2 hours |
| Medium (some users affected) | 1 hour | 4 hours |
| Low (single user issue) | 2 hours | 8 hours |

---

### Post-Go-Live Monitoring

**Hour 1-4 (Active Monitoring):**
- Monitor system logs every 15 minutes
- Watch email support channel
- Be ready for immediate intervention
- Have all team members available

**Day 1 (End of Day Review):**
- Total audits submitted: ___
- Total users accessed: ___
- Critical issues: ___
- Major issues: ___
- Minor issues: ___
- System uptime: ___ %

**Week 1 Daily Review:**
- Audit submission trends (should increase daily)
- Error rates (should be <1%)
- Support tickets (trend and resolution)
- User feedback (sentiment)

**Week 2+ (Standard Monitoring):**
- Weekly system health check
- Monthly usage statistics
- Quarterly performance review

---

### First Week Support Scripts

**When auditor calls: "The app won't load"**

Script:
1. "Hi! Let's get you up and running. First, can you tell me what device you're using - iPad, iPhone, or Android?"
2. "Are you on WiFi or mobile data?"
3. "Try closing the app completely and reopening it. If that doesn't work, restart your device."
4. "If you're still seeing issues, we might need to clear the app cache. Here's how..."

**When manager calls: "I can't see audit submissions"**

Script:
1. "Let me help! Are you accessing via the mobile app or web browser?"
2. "From the home screen, tap 'View Audits' or go to the Reports section"
3. "You might need to filter by date or service line. Try clearing filters first"
4. "If you're still not seeing data, it may need 5 minutes to sync. Try refreshing"

**When auditor asks: "What do I do if I find critical equipment missing?"**

Script:
1. "Great question! Enter 0 (or leave blank) for the missing quantity"
2. "In the audit notes, briefly explain: 'Critical item [name] not found'"
3. "When you submit, this automatically escalates to your manager"
4. "Don't wait - also notify your manager directly that equipment is missing"
5. "The system will track this as an issue"

---

### Success Metrics (Track During First Week)

| Metric | Target | Actual |
|--------|--------|--------|
| System uptime | 99.5% | ___% |
| Audit submissions | 20+ per day | ___ |
| User login rate | 60%+ of staff | __% |
| Average response time | <5 min | ___ |
| Critical issues | 0 | ___ |
| User satisfaction | 80%+ positive | __% |

---

### Transition to Standard Operations (End of Week 1)

By end of week 1:
- [ ] All critical issues resolved
- [ ] First batch of audits submitted
- [ ] Users comfortable with system
- [ ] Support team confident in operation

**Actions:**
1. Reduce support team size (if needed)
2. Move support hours to business hours only
3. Begin routine weekly monitoring
4. Schedule first full week review meeting
5. Update communications - moving to standard support

---

### Post-Go-Live Issues & Resolution Log

Template for tracking issues during first week:

```
Issue #1:
  Date/Time: [when reported]
  Severity: [Critical/High/Medium/Low]
  Description: [what went wrong]
  Users Affected: [count]
  Status: [Open/In Progress/Resolved]
  Resolution: [what was done]
  Time to Resolve: [duration]

[Repeat for each issue]
```

---
```

---

## Appendices

### Appendix A: Glossary of Terms

```markdown
## Glossary

**Audit:** The process of checking a resuscitation trolley for compliance with equipment, condition, and documentation standards.

**Auditor:** Clinical staff member authorized to conduct trolley audits.

**Compliance Score:** Percentage calculated based on equipment found vs. expected quantities. Formula: (Equipment OK / Total Expected) × 100

**Corrective Action:** Specific action taken to resolve an issue (e.g., "restock missing equipment by Friday").

**Defibrillator (Defib):** Emergency equipment used to restore heart rhythm. Different types have different pads (adult vs. pediatric).

**Draft Audit:** Incomplete audit saved without submission. Can be resumed later.

**Issue:** Problem identified during audit (missing equipment, broken drawer, etc.) that requires action.

**Spot Check:** Quick audit focusing on equipment and condition, omitting documentation checks.

**Comprehensive Audit:** Full audit including all sections (documentation, condition, checks, equipment).

**Trolley Location:** Specific physical location of a resuscitation trolley (e.g., "ICU Bay 3", "ED Resus Area").

**Service Line:** Organizational grouping (e.g., Medical Services, Surgical Services, Critical Care).
```

---

### Appendix B: Sample Training Email

```markdown
Subject: RBWH Trolley Audit System - Training & Launch

Dear RBWH Clinical Staff,

We're excited to announce the launch of the new RBWH Trolley Audit System!

WHAT'S LAUNCHING
A new mobile app that makes trolley audits faster, easier, and more detailed.
Instead of Microsoft Forms, you'll use a purpose-built PowerApp on tablet or phone.

WHY THIS IS BETTER
- Faster: Complete audits in 10-20 minutes (vs. 30+ with forms)
- Easier: Guided workflow with search and filtering
- Better data: Track equipment item-by-item (not just "yes/no")
- Real-time reporting: Managers see data immediately
- Mobile-first: Works great on tablets

WHEN IT LAUNCHES
[Date] at 9:00 AM

WHAT YOU NEED TO DO

1. WATCH THE TRAINING VIDEO (15 minutes)
   Link: [Training Video URL]
   or see "RBWH Trolley Audit - Auditor Training" in SharePoint

2. DOWNLOAD THE POWER APPS APP
   Search "Power Apps" in your device's app store
   Download the official Microsoft app

3. ATTEND TRAINING SESSION (Optional but recommended)
   Date: [Training Date]
   Time: [Training Time]
   Link: [Zoom/Teams link]
   This is a live walk-through - great for seeing it in action

4. START AUDITING
   After launch, your manager will assign trolleys to audit
   Open the app, log in, and start your first audit

HOW TO GET HELP

- Questions about the system?
  Email: mert@rbwh.org.au

- Technical issues?
  Email: it.support@rbwh.org.au
  Phone: [Support number]
  First week: 7am-6pm daily
  After first week: 8:30am-4:30pm business hours

- Can't download the app?
  Contact your IT department for app installation support

FREQUENTLY ASKED QUESTIONS

Q: Do I need a new phone or tablet?
A: No! The app works on existing devices (iPad, iPhone, Android tablets)

Q: What if I don't have a tablet?
A: You can also use a laptop/computer via web browser

Q: Will my old audits transfer?
A: Yes - historical data has been imported so you can see trends

Q: What if I need to complete an audit but don't have internet?
A: The app supports offline mode - you can audit offline and sync when connected

Q: Do I still use Microsoft Forms?
A: No - the old system is being replaced by this new app

MORE INFORMATION

Full training materials: [SharePoint link]
User Guide: [PDF link]
FAQ: [Link]
System Demo Video: [Video link]

We know change can feel like a lot, but we've made this system super user-friendly.
The first audit takes a little longer (20-30 min) as you learn the flow,
but by your second audit you'll be flying through it in 12-15 minutes!

Thank you for your patience during this transition. We're committed to making
this system support your work, not complicate it. Your feedback is valuable -
please share suggestions with your manager or MERT educators.

Looking forward to seeing you audit!

RBWH Medical Education & Simulation Team
```

---

### Appendix C: Sample Manager Launch Email

```markdown
Subject: Manager Launch Brief - Trolley Audit System Goes Live [Date]

Dear Managers,

The new RBWH Trolley Audit System launches [Date]. Here's what you need to know and do.

YOUR RESPONSIBILITIES

Starting [Date], you'll manage the trolley audit process through this system:

1. ENSURE YOUR TEAM IS TRAINED
   - Share training video link: [URL]
   - Encourage attendance at live training: [Date/Time]
   - Answer basic questions about the process

2. MONITOR AUDIT SUBMISSIONS
   - Review audits submitted by your team
   - Flag quality issues with auditors
   - Respond to equipment shortage alerts

3. MANAGE ISSUES & CORRECTIVE ACTIONS
   - Issues appear automatically when problems are flagged
   - You assign corrective actions to address them
   - Track progress until resolved
   - Target: High severity within 3 days, Medium within 5 days

4. USE DATA & REPORTS
   - Access reports to monitor compliance trends
   - Use data to identify problem areas
   - Report metrics to your leadership

YOUR FIRST WEEK

Week of [Date]:
- Monday AM: System goes live
- Mon-Fri: Users submit first audits
- Watch for: Questions, technical issues (support team handling these)
- Your role: Encourage uptake, watch for quality issues, start managing issues

TRAINING FOR YOU

Attend Manager Training Session:
- Date: [Date]
- Time: [Time]
- Duration: 90 minutes
- Content: Reviewing audits, managing issues, reading reports
- Link: [Zoom/Teams link]

Self-Training (Optional):
- Watch Manager Training Video: [URL]
- Read Admin Guide excerpt: [PDF]
- Explore Reports: [Power BI link]

KEY INFORMATION

New System Features:
- Equipment tracked item-by-item (not just "yes/no")
- Spot check audits (10-min quick version)
- Issue management with corrective actions
- Real-time compliance dashboard
- Weekly random audit selection

What's NOT Changing:
- Audit requirements (still need annual comprehensive audit per trolley)
- Equipment lists (same equipment expected)
- Service line groupings
- Your oversight and accountability

FIRST WEEK SUPPORT

If you need help:
- Process questions: Contact MERT Educators (mert@rbwh.org.au)
- Technical issues: Contact IT Support (it.support@rbwh.org.au)
- Questions about reports: Contact MERT Educators

We'll have extended support hours the first week (7am-6pm daily).

COMMUNICATION

You'll receive daily updates:
- Mon-Fri first week: 8am status email
- Week 2: Less frequent updates
- Week 3+: Standard ongoing monitoring

ACTION ITEMS FOR YOU

- [ ] Watch Manager Training Video (15 min)
- [ ] Attend Training Session [Date] (optional but recommended)
- [ ] Share training video link with your team
- [ ] Encourage team to complete training before launch day
- [ ] Prepare to answer "What's this new system?" questions
- [ ] Access the system yourself the first day to explore

THANK YOU

We're transitioning to a better system that will help us track compliance,
identify issues quickly, and improve our trolley management.
Your support of this change is crucial to its success.

Questions? Reach out to MERT educators or IT support.

Best regards,
Project Leadership Team
```

---

### Appendix D: Success Metrics Dashboard

```markdown
## Post-Go-Live Metrics to Track

### Daily Metrics (Track for first 2 weeks)

| Metric | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 |
|--------|-------|-------|-------|-------|-------|
| System uptime | ___% | ___% | ___% | ___% | ___% |
| Audits submitted | ___ | ___ | ___ | ___ | ___ |
| Unique users | ___ | ___ | ___ | ___ | ___ |
| Support tickets | ___ | ___ | ___ | ___ | ___ |
| Critical issues | ___ | ___ | ___ | ___ | ___ |

### Weekly Metrics (Track for first month)

| Week | Audits | Users | Avg Compliance | Issues Logged | Issues Resolved |
|------|--------|-------|----------------|---------------|-----------------|
| Week 1 | ___ | ___% | __% | ___ | ___ |
| Week 2 | ___ | ___% | __% | ___ | ___ |
| Week 3 | ___ | ___% | __% | ___ | ___ |
| Week 4 | ___ | ___% | __% | ___ | ___ |

### User Adoption Metrics

- [ ] 60%+ of auditors have submitted at least 1 audit (by end of week 1)
- [ ] 80%+ of auditors have submitted at least 1 audit (by end of week 2)
- [ ] 100% of assigned auditors trained (by end of week 1)
- [ ] Average audit time stabilizes at 12-15 min (by week 2)

### Quality Metrics

- [ ] 95%+ of audits have all fields completed
- [ ] <1% of audits require resubmission
- [ ] 100% of critical issues escalated to manager
- [ ] 80%+ of issues resolved within SLA

---
```

---

## Document Control & Closure

**Document Version:** 1.0
**Status:** Final - Ready for Implementation
**Approved by:** [Project Lead], [MERT Lead Educator], [IT Director]
**Effective Date:** [Go-Live Date]
**Next Review Date:** [6 months post-go-live]

**Document Location:**
`\\DOCKERSERVER\Public\Downloads\trolleys\trolleys\implementation_guides\phase4_4_deployment.md`

**Maintenance Notes:**
- Update with actual dates and contact information 48 hours before go-live
- Keep links current (training videos, SharePoint URLs)
- Update metrics daily during first week of go-live
- Schedule post-go-live retrospective for 2 weeks after launch

---

*End of Phase 4.4 Deployment Implementation Guide*
