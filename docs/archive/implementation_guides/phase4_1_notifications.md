# REdI Trolley Audit System
## Phase 4.1 Notifications Implementation Guide

**Document Version:** 1.0
**Date:** January 2026
**Status:** Ready for Implementation
**Tasks Covered:** 4.1.1 - 4.1.10

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Prerequisites](#prerequisites)
3. [Email Template Design Specifications](#email-template-design-specifications)
4. [Task 4.1.1-4.1.2: Audit Submission Confirmation](#task-411-412-audit-submission-confirmation)
5. [Task 4.1.3-4.1.4: Critical Issue Alert](#task-413-414-critical-issue-alert)
6. [Task 4.1.5-4.1.6: Issue Assignment Notification](#task-415-416-issue-assignment-notification)
7. [Task 4.1.7-4.1.8: Weekly Selection Announcement](#task-417-418-weekly-selection-announcement)
8. [Task 4.1.9: Overdue Audit Reminder](#task-419-overdue-audit-reminder)
9. [Task 4.1.10: Issue Escalation Workflow](#task-4110-issue-escalation-workflow)
10. [Verification Checklist](#verification-checklist)
11. [Troubleshooting](#troubleshooting)

---

## Executive Summary

This guide provides step-by-step instructions for implementing Phase 4.1 Notifications, a critical component of the REdI Trolley Audit system that keeps stakeholders informed of audit submissions, critical issues, assignments, and escalations through automated email notifications and scheduled maintenance flows.

### What You'll Complete

| Task | Objective | Time | Dependency |
|------|-----------|------|-----------|
| 4.1.1-4.1.2 | Audit Submission Confirmation email + flow | 3 hours | 2.5.8 (Submit Audit flow) |
| 4.1.3-4.1.4 | Critical Issue Alert email + flow | 4 hours | 2.8.1 (Save New Issue flow) |
| 4.1.5-4.1.6 | Issue Assignment Notification email + flow | 3 hours | 2.8.3 (Assign Issue flow) |
| 4.1.7-4.1.8 | Weekly Selection Announcement email + flow | 3 hours | 2.9.15 (Generate Selection flow) |
| 4.1.9 | Overdue Audit Reminder scheduled flow | 4 hours | 3.1.5 (Overdue audits KPI) |
| 4.1.10 | Issue Escalation scheduled flow | 5 hours | 2.8.11 (Escalate Issue flow) |

**Total Duration:** Approximately 22 hours of implementation work

### Notifications Overview

By the end of Phase 4.1, you will have:
- **5 HTML email templates** designed with REdI branding
- **4 transactional flows** triggered by audit/issue events
- **2 scheduled flows** running daily for overdue reminders and escalations
- **Recipient logic** ensuring correct people receive notifications
- **Complete email branding** with REdI colour scheme

---

## Prerequisites

### Required Access & Permissions

- **Power Automate** - License with cloud flow creation capability
- **Exchange Online** - For sending emails
- **SharePoint Administrator** - To access SharePoint lists
- **Power Automate Admin** - To configure scheduled flows
- **MERT Educator access** - To test notification workflows

### Required Information

Before starting, gather:

1. **REdI Branding Assets**
   - REdI logo (PNG, recommended 150x60 pixels, <100KB)
   - Primary colour: #1B3A5F (REdI blue)
   - Secondary colour: #2B9E9E (REdI green)
   - Footer text colour: #666666 (Medium grey)

2. **SharePoint Site Details**
   - Site URL: https://[yourtenant].sharepoint.com/sites/REdITrolleyAudit
   - Environment name (for Power Automate connections)

3. **Notification Recipients**
   - MERT Educator email addresses (for escalations, critical alerts)
   - Ward Manager/NUM email templates (dynamic - will pull from Location/ServiceLine)
   - Generic system notification email address (for testing)

4. **List Names and Columns**
   - Audit list with: AuditorEmail, OverallCompliance, Location lookup, CompletedDateTime
   - Issue list with: AssignedTo, Severity, LocationId, ReportedDate, Status
   - Location list with: ServiceLine lookup, ContactEmail
   - ServiceLine list with: ContactEmail

### Power Automate Environment Setup

Before creating flows:

1. **Ensure Power Automate connections exist:**
   - SharePoint (to your site)
   - Office 365 Outlook (for sending emails)
   - HTTP (for any dynamic content needs)

2. **Configure send-as account:**
   - Use a shared mailbox or service account for notifications
   - Recommended address: trolleyaudit@rbwh.com.au (or your organization standard)
   - Email subject will include "[REdI Trolley Audit System]" prefix

3. **List field dependencies:**
   - Ensure all referenced columns exist in SharePoint lists
   - Lookups are configured correctly before flow creation

---

## Email Template Design Specifications

### General Design Standards

All email templates follow this structure and branding:

**Header Section:**
```
┌─────────────────────────────────────────────────────────┐
│  [REdI LOGO]  REdI Trolley Audit System                │
│                                                         │
│  Primary colour: #1B3A5F (used for header background)  │
│  Text colour: White (#FFFFFF)                          │
└─────────────────────────────────────────────────────────┘
```

**Body Section:**
- Font: Segoe UI or Calibri, 14px for body text
- Line height: 1.5 for readability
- Colour scheme: #333333 (text), #F5F5F5 (subtle backgrounds)
- Key information: #1B3A5F (highlighting)

**Footer Section:**
```
┌─────────────────────────────────────────────────────────┐
│  ─────────────────────────────────────────────────────  │
│  This is an automated message from the REdI Trolley    │
│  Audit System. Do not reply to this email.             │
│  Contact your MERT Educator for assistance.            │
│                                                         │
│  [© REdI 2026]                                         │
└─────────────────────────────────────────────────────────┘
```

### Email Template Best Practices

1. **HTML-based templates** - Use responsive design that works on mobile/desktop
2. **Accessibility** - Include alt text for images, high contrast text
3. **Subject lines** - Clear, scannable, include action item when applicable
4. **Call-to-actions** - Use button links (not plain text links) with clear labels
5. **Unsubscribe** - Include footer with "Manage notification preferences" option
6. **Email width** - Design for 600px fixed width (standard email client width)

---

## Task 4.1.1-4.1.2: Audit Submission Confirmation

### Task 4.1.1: Create Audit Submission Email Template

**Objective:** Design an HTML email template that confirms audit submission with compliance score breakdown.

#### Step 1: Email Template Design

**Subject Line:** `[REdI Trolley Audit] Submission Confirmed - {Location} - {Compliance}%`

**Template Variables:**
```
{AuditorName}        - Person who submitted audit
{Location}           - Trolley location name
{SubmissionDateTime} - When audit was submitted
{OverallCompliance}  - Overall compliance percentage (0-100)
{DocumentScore}      - Documentation subscore (0-100)
{EquipmentScore}     - Equipment subscore (0-100)
{ConditionScore}     - Condition subscore (0-100)
{CheckScore}         - Routine checks subscore (0-100) [optional]
{IssuesFound}        - Count of issues found
{CriticalIssues}     - Count of critical issues
{FollowUpRequired}   - "Yes" or "No"
{FollowUpDueDate}    - Date if follow-up required
{AuditId}            - Audit record ID (for linking)
```

#### Step 2: HTML Email Template Structure

Create the following HTML template (save as reference for Power Automate):

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audit Submission Confirmation</title>
    <style type="text/css">
        body {
            font-family: 'Segoe UI', Calibri, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #F5F5F5;
        }
        .email-container {
            width: 600px;
            margin: 20px auto;
            background-color: #FFFFFF;
            border-collapse: collapse;
        }
        .header {
            background-color: #1B3A5F;
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: bold;
        }
        .header p {
            margin: 5px 0 0 0;
            font-size: 13px;
            opacity: 0.9;
        }
        .content {
            padding: 30px 20px;
            color: #333333;
        }
        .greeting {
            font-size: 16px;
            margin-bottom: 20px;
        }
        .confirmation-box {
            background-color: #E8F4F8;
            border-left: 4px solid #1B3A5F;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .confirmation-box h3 {
            margin: 0 0 10px 0;
            color: #1B3A5F;
            font-size: 16px;
        }
        .confirmation-box p {
            margin: 5px 0;
            font-size: 14px;
        }
        .scores-table {
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
            background-color: #F9F9F9;
        }
        .scores-table th {
            background-color: #E8E8E8;
            color: #333333;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid #CCCCCC;
        }
        .scores-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #E8E8E8;
        }
        .score-label {
            color: #666666;
            font-size: 14px;
        }
        .score-value {
            color: #1B3A5F;
            font-weight: bold;
            font-size: 16px;
        }
        .overall-score {
            background-color: #E8F4F8;
            font-weight: bold;
            font-size: 16px;
        }
        .overall-score .score-value {
            font-size: 20px;
        }
        .status-critical {
            color: #D32F2F;
        }
        .status-warning {
            color: #F57F17;
        }
        .status-good {
            color: #388E3C;
        }
        .action-required {
            background-color: #FFF3E0;
            border-left: 4px solid #F57F17;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .action-required h3 {
            margin: 0 0 10px 0;
            color: #F57F17;
            font-size: 16px;
        }
        .button {
            background-color: #1B3A5F;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 20px 0;
            font-weight: bold;
        }
        .footer {
            background-color: #F5F5F5;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666666;
            border-top: 1px solid #E0E0E0;
        }
        .footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <table class="email-container">
        <tr>
            <td class="header">
                <h1>REdI Trolley Audit System</h1>
                <p>Audit Submission Confirmed</p>
            </td>
        </tr>
        <tr>
            <td class="content">
                <p class="greeting">Hi {AuditorName},</p>

                <p>Your audit submission for <strong>{Location}</strong> has been successfully received and processed.</p>

                <div class="confirmation-box">
                    <h3>Submission Details</h3>
                    <p><strong>Location:</strong> {Location}</p>
                    <p><strong>Submitted:</strong> {SubmissionDateTime}</p>
                    <p><strong>Submission ID:</strong> {AuditId}</p>
                </div>

                <h3>Compliance Score Breakdown</h3>
                <table class="scores-table">
                    <tr>
                        <th>Category</th>
                        <th>Score</th>
                        <th>Status</th>
                    </tr>
                    <tr>
                        <td class="score-label">Documentation</td>
                        <td class="score-value">{DocumentScore}%</td>
                        <td>
                            <span class="status-good" style="display: inline-block;">
                                {DocumentScore >= 80 ? '✓' : '⚠'}
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td class="score-label">Equipment</td>
                        <td class="score-value">{EquipmentScore}%</td>
                        <td>
                            <span class="{EquipmentScore >= 95 ? 'status-good' : 'status-warning'}"
                                  style="display: inline-block;">
                                {EquipmentScore >= 95 ? '✓' : '⚠'}
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td class="score-label">Condition</td>
                        <td class="score-value">{ConditionScore}%</td>
                        <td>
                            <span class="status-good" style="display: inline-block;">
                                {ConditionScore >= 80 ? '✓' : '⚠'}
                            </span>
                        </td>
                    </tr>
                    {CheckScore !== null ? (
                        <tr>
                            <td class="score-label">Routine Checks</td>
                            <td class="score-value">{CheckScore}%</td>
                            <td>
                                <span class="{CheckScore >= 75 ? 'status-good' : 'status-warning'}"
                                      style="display: inline-block;">
                                    {CheckScore >= 75 ? '✓' : '⚠'}
                                </span>
                            </td>
                        </tr>
                    ) : ('')}
                    <tr class="overall-score">
                        <td class="score-label">OVERALL COMPLIANCE</td>
                        <td class="score-value">{OverallCompliance}%</td>
                        <td>
                            <span class="{OverallCompliance >= 80 ? 'status-good' : 'status-critical'}"
                                  style="display: inline-block;">
                                {OverallCompliance >= 80 ? '✓ Compliant' : '✗ Below Target'}
                            </span>
                        </td>
                    </tr>
                </table>

                <h3>Issues Reported</h3>
                <p>
                    <strong>Total Issues Found:</strong> {IssuesFound}
                    <br/>
                    <strong>Critical Issues:</strong>
                    <span class="{CriticalIssues > 0 ? 'status-critical' : 'status-good'}">
                        {CriticalIssues}
                    </span>
                </p>

                {FollowUpRequired === 'Yes' ? (
                    <div class="action-required">
                        <h3>Follow-Up Audit Required</h3>
                        <p>Based on compliance score below 80%, a follow-up audit is required.</p>
                        <p><strong>Due Date:</strong> {FollowUpDueDate}</p>
                        <p>This will be scheduled through the MERT team.</p>
                    </div>
                ) : ('')}

                {CriticalIssues > 0 ? (
                    <div class="action-required">
                        <h3>Critical Issues Require Immediate Attention</h3>
                        <p>Critical issues have been identified and notifications sent to the appropriate teams.</p>
                        <p>Please contact your MERT Educator immediately to coordinate resolution.</p>
                    </div>
                ) : ('')}

                <p><a href="{AppLink}/audit/{AuditId}" class="button">View Full Audit Details</a></p>

                <p>If you have questions about this submission or the compliance scores, please contact your MERT Educator.</p>
            </td>
        </tr>
        <tr>
            <td class="footer">
                <p>This is an automated message from the REdI Trolley Audit System.</p>
                <p>Do not reply to this email. Contact your MERT Educator for assistance.</p>
                <p>&copy; REdI 2026</p>
                <p><a href="{PreferencesLink}">Manage Notification Preferences</a></p>
            </td>
        </tr>
    </table>
</body>
</html>
```

#### Step 3: Create Email Template in Power Automate

1. Open **Power Automate** → Navigate to **Cloud flows** → **Instant cloud flows**
2. Create a **New flow** called `Email Template - Audit Submission`
3. Add a manual trigger (for testing the template)
4. Add an **Outlook** → **Send an email (V2)** action
5. Configure the following:

| Field | Value |
|-------|-------|
| **To** | {AuditorEmail} |
| **Subject** | `[REdI Trolley Audit] Submission Confirmed - {Location} - {OverallCompliance}%` |
| **Body** | [Paste HTML template above] |
| **IsHtml** | Yes (toggle) |

**Important:** Replace all `{variable}` placeholders with Power Automate dynamic content:
- Use `body('Get_Audit_Record')['AuditorEmail']` for dynamic values
- Use Power Automate expressions for conditional formatting
- Test with sample data first

---

### Task 4.1.2: Add Submission Confirmation to Audit Submit Flow

**Objective:** Integrate the email template into the existing "Submit Audit" flow (Task 2.5.8).

#### Step 1: Locate Existing Submit Audit Flow

1. Open **Power Automate** → **Cloud flows** → **Instant cloud flows**
2. Find flow named `Submit_Audit` (created in Phase 2, Task 2.5.8)
3. Select **Edit**

#### Step 2: Add Send Email Action

1. After the step `Update Location last audit fields` (from 2.5.14), add a new action
2. Choose **Outlook** → **Send an email (V2)**
3. Configure the email:

**From:**
```
trolleyaudit@rbwh.com.au (or your shared mailbox)
```

**To:**
```
@{body('Get_Audit_Record')?['AuditorEmail']}
```

**Subject:**
```
[REdI Trolley Audit] Submission Confirmed - @{body('Get_Location')?['DisplayName']} - @{outputs('Calculate_Compliance_Score')?['body']}%
```

**Body:**
[Use the HTML template from Step 2, replacing placeholders with dynamic content]

**IsHtml:**
```
true
```

#### Step 3: Add Conditional Critical Issues Check

1. After the email action, add a **Condition** control
2. Set condition:
   - Left: `CriticalIssuesCount` (from calculations)
   - Operator: `is greater than`
   - Right: `0`

3. In the **If yes** branch, add another **Send email (V2)**:
   - **To:** MERT Educators distribution list or {MEERTEmail}
   - **Subject:** `[URGENT] Critical Issue Found - {Location}`
   - **Body:** Alert email (see Task 4.1.3 template)

#### Step 4: Test the Flow

1. Create a test audit submission in the PowerApp
2. Verify the following:
   - Email received with correct subject line
   - All compliance scores display correctly
   - Critical issues section shows conditionally
   - Follow-up required section displays when compliance < 80%
   - HTML formatting renders properly (no code visible)
   - Links to app are clickable

#### Step 5: Add to Flow List

1. In the Power Automate flows list, tag with labels:
   - `#notifications`
   - `#audit`
   - `#phase4`

---

## Task 4.1.3-4.1.4: Critical Issue Alert

### Task 4.1.3: Create Critical Issue Alert Email Template

**Objective:** Design an urgent email template for critical severity issues that require immediate attention.

#### Step 1: Email Template Design

**Subject Line:** `[URGENT] Critical Issue - {Location} - {IssueTitle}`

**Template Variables:**
```
{IssueNumber}        - Human-readable issue ID (e.g., ISS-2026-0042)
{Location}           - Trolley location name
{IssueTitle}         - Brief issue description
{IssueSeverity}      - "Critical" (always, for this template)
{IssueDescription}   - Detailed description
{ReportedBy}         - Person who reported
{ReportedDate}       - When reported
{EquipmentItem}      - Affected equipment (if applicable)
{ClinicalImpact}     - Safety/clinical impact description
{IssueLink}          - Deep link to issue in app
{LocationManager}    - Ward manager or location owner
{MERTEmail}          - MERT educator email
```

#### Step 2: HTML Email Template Structure

Create the following critical alert template:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Critical Issue Alert</title>
    <style type="text/css">
        body {
            font-family: 'Segoe UI', Calibri, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #FFF3E0;
        }
        .email-container {
            width: 600px;
            margin: 20px auto;
            background-color: #FFFFFF;
            border-collapse: collapse;
            border: 3px solid #D32F2F;
        }
        .header {
            background-color: #D32F2F;
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 26px;
            font-weight: bold;
        }
        .header .alert-badge {
            display: inline-block;
            background-color: rgba(255,255,255,0.3);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-top: 10px;
        }
        .urgent-banner {
            background-color: #D32F2F;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
        }
        .content {
            padding: 30px 20px;
            color: #333333;
        }
        .alert-box {
            background-color: #FFEBEE;
            border-left: 4px solid #D32F2F;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .alert-box h3 {
            margin: 0 0 15px 0;
            color: #D32F2F;
            font-size: 18px;
        }
        .issue-details {
            background-color: #F5F5F5;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .issue-details-row {
            margin: 10px 0;
            display: flex;
            align-items: baseline;
        }
        .issue-details-label {
            font-weight: bold;
            color: #333333;
            width: 120px;
            margin-right: 10px;
        }
        .issue-details-value {
            color: #666666;
            flex: 1;
        }
        .critical-impact {
            background-color: #FFF3E0;
            border-left: 4px solid #F57F17;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .critical-impact h3 {
            margin: 0 0 10px 0;
            color: #F57F17;
            font-size: 16px;
        }
        .action-required {
            background-color: #E8F4F8;
            border-left: 4px solid #1B3A5F;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .action-required h3 {
            margin: 0 0 10px 0;
            color: #1B3A5F;
            font-size: 16px;
        }
        .action-list {
            list-style: none;
            padding: 0;
            margin: 10px 0;
        }
        .action-list li {
            padding: 8px 0 8px 25px;
            position: relative;
            color: #333333;
        }
        .action-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: #1B3A5F;
            font-weight: bold;
        }
        .button {
            background-color: #D32F2F;
            color: white;
            padding: 14px 30px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 20px 0;
            font-weight: bold;
            font-size: 16px;
        }
        .footer {
            background-color: #F5F5F5;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666666;
            border-top: 1px solid #E0E0E0;
        }
        .footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <table class="email-container">
        <tr>
            <td class="urgent-banner">
                ⚠ URGENT - IMMEDIATE ACTION REQUIRED ⚠
            </td>
        </tr>
        <tr>
            <td class="header">
                <h1>REdI Trolley Audit System</h1>
                <p>Critical Issue Alert</p>
                <div class="alert-badge">CRITICAL SEVERITY</div>
            </td>
        </tr>
        <tr>
            <td class="content">
                <p style="font-size: 16px; color: #D32F2F; font-weight: bold; margin-bottom: 20px;">
                    A critical issue has been identified that requires your immediate attention.
                </p>

                <div class="alert-box">
                    <h3>{IssueTitle}</h3>
                    <p>{IssueDescription}</p>
                </div>

                <h3 style="color: #333333;">Issue Details</h3>
                <div class="issue-details">
                    <div class="issue-details-row">
                        <div class="issue-details-label">Issue ID:</div>
                        <div class="issue-details-value">{IssueNumber}</div>
                    </div>
                    <div class="issue-details-row">
                        <div class="issue-details-label">Location:</div>
                        <div class="issue-details-value">{Location}</div>
                    </div>
                    <div class="issue-details-row">
                        <div class="issue-details-label">Severity:</div>
                        <div class="issue-details-value" style="color: #D32F2F; font-weight: bold;">
                            ● CRITICAL
                        </div>
                    </div>
                    <div class="issue-details-row">
                        <div class="issue-details-label">Reported By:</div>
                        <div class="issue-details-value">{ReportedBy}</div>
                    </div>
                    <div class="issue-details-row">
                        <div class="issue-details-label">Reported Date:</div>
                        <div class="issue-details-value">{ReportedDate}</div>
                    </div>
                    {EquipmentItem ? (
                        <div class="issue-details-row">
                            <div class="issue-details-label">Equipment:</div>
                            <div class="issue-details-value">{EquipmentItem}</div>
                        </div>
                    ) : ('')}
                </div>

                <div class="critical-impact">
                    <h3>Clinical/Safety Impact</h3>
                    <p>{ClinicalImpact}</p>
                </div>

                <div class="action-required">
                    <h3>Immediate Action Required</h3>
                    <ul class="action-list">
                        <li>Review issue details immediately</li>
                        <li>Contact {LocationManager} (Ward Manager)</li>
                        <li>Implement corrective action within 24 hours</li>
                        <li>Update issue status in the system once action is taken</li>
                        <li>Do not use trolley until resolved (if safety-critical)</li>
                    </ul>
                </div>

                <p style="text-align: center; margin: 20px 0;">
                    <a href="{IssueLink}" class="button">View Issue Details & Assign Action</a>
                </p>

                <h3 style="color: #333333;">Support</h3>
                <p>
                    If you need assistance with this issue:
                    <br/>
                    <strong>MERT Educator:</strong> <a href="mailto:{MERTEmail}">{MERTEmail}</a>
                    <br/>
                    <strong>Ward Manager:</strong> {LocationManager}
                </p>
            </td>
        </tr>
        <tr>
            <td class="footer">
                <p><strong>This is an urgent automated alert from the REdI Trolley Audit System.</strong></p>
                <p>Do not reply to this email. Contact your MERT Educator immediately.</p>
                <p>&copy; REdI 2026</p>
            </td>
        </tr>
    </table>
</body>
</html>
```

---

### Task 4.1.4: Add Critical Issue Alert to Save Issue Flow

**Objective:** Integrate critical issue email into the "Save New Issue" flow (Task 2.8.1).

#### Step 1: Locate Existing Save Issue Flow

1. Open **Power Automate** → **Cloud flows** → **Instant cloud flows**
2. Find flow named `Save_New_Issue` (created in Phase 2, Task 2.8.1)
3. Select **Edit**

#### Step 2: Add Conditional Check for Critical Severity

1. After the "Create Issue record" action, add a **Condition** control
2. Set condition:
   - Left: `Severity` (from Issue creation output)
   - Operator: `is equal to`
   - Right: `Critical`

#### Step 3: Configure Email Recipients

In the **If yes** branch:

**Get Location Details** (Get item action):
- List: Location
- ID: `LocationId` (from Issue record)

**Get ServiceLine Details** (Get item action):
- List: ServiceLine
- ID: ServiceLineId (from Location record)

#### Step 4: Add Send Email Action

Add **Outlook** → **Send an email (V2)**:

**To (Recipient Logic):**
```
MERT Educators (hardcoded list or use a group)
cc: {ServiceLineContactEmail},{LocationContactEmail}
```

**Subject:**
```
[URGENT] Critical Issue - @{body('Get_Location')?['DisplayName']} - @{body('Create_Issue')?['Title']}
```

**Body:**
[Use Critical Issue Alert template from Step 2]

**IsHtml:**
```
true
```

#### Step 5: Add Overdue Escalation Trigger

Also add a **Schedule cloud flow** trigger (separate flow):

**Flow Name:** `Critical Issue Escalation Check`
- Recurrence: Every 4 hours
- Check: WHERE Severity = 'Critical' AND Status ≠ 'Closed' AND CreatedDate > 2 hours ago
- Escalate to Level 2 if no corrective action logged

---

## Task 4.1.5-4.1.6: Issue Assignment Notification

### Task 4.1.5: Create Issue Assignment Email Template

**Objective:** Design an email notifying the assignee that an issue has been assigned to them.

#### Step 1: Email Template Design

**Subject Line:** `[REdI Trolley Audit] New Issue Assigned - {IssueTitle}`

**Template Variables:**
```
{AssigneeName}       - Person being assigned the issue
{IssueNumber}        - Issue ID (e.g., ISS-2026-0042)
{Location}           - Trolley location
{IssueTitle}         - Brief title
{Severity}           - Critical/High/Medium/Low
{IssueCategory}      - Equipment/Documentation/Condition/Compliance
{Description}        - Full issue description
{TargetResolutionDate} - Due date for resolution
{AssignedBy}         - Who assigned it
{IssueLink}          - Deep link to issue details
```

#### Step 2: HTML Email Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Issue Assigned to You</title>
    <style type="text/css">
        body {
            font-family: 'Segoe UI', Calibri, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #F5F5F5;
        }
        .email-container {
            width: 600px;
            margin: 20px auto;
            background-color: #FFFFFF;
            border-collapse: collapse;
        }
        .header {
            background-color: #1B3A5F;
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: bold;
        }
        .content {
            padding: 30px 20px;
            color: #333333;
        }
        .greeting {
            font-size: 16px;
            margin-bottom: 20px;
        }
        .assignment-box {
            background-color: #E8F4F8;
            border-left: 4px solid #1B3A5F;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .assignment-box h3 {
            margin: 0 0 15px 0;
            color: #1B3A5F;
            font-size: 18px;
        }
        .detail-row {
            margin: 10px 0;
            display: flex;
            align-items: baseline;
        }
        .detail-label {
            font-weight: bold;
            color: #333333;
            width: 140px;
            margin-right: 10px;
        }
        .detail-value {
            color: #666666;
            flex: 1;
        }
        .severity-critical {
            color: #D32F2F;
            font-weight: bold;
        }
        .severity-high {
            color: #F57F17;
            font-weight: bold;
        }
        .severity-medium {
            color: #F9A825;
            font-weight: bold;
        }
        .severity-low {
            color: #388E3C;
            font-weight: bold;
        }
        .description-box {
            background-color: #F9F9F9;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #CCCCCC;
            border-radius: 4px;
        }
        .timeline {
            background-color: #E8F4F8;
            border-left: 4px solid #1B3A5F;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .timeline h4 {
            margin: 0 0 10px 0;
            color: #1B3A5F;
        }
        .action-items {
            background-color: #FFF3E0;
            border-left: 4px solid #F57F17;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .action-items h4 {
            margin: 0 0 10px 0;
            color: #F57F17;
        }
        .action-list {
            list-style: none;
            padding: 0;
            margin: 10px 0;
        }
        .action-list li {
            padding: 8px 0 8px 25px;
            position: relative;
            color: #333333;
        }
        .action-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: #F57F17;
            font-weight: bold;
        }
        .button {
            background-color: #1B3A5F;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 20px 0;
            font-weight: bold;
        }
        .footer {
            background-color: #F5F5F5;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666666;
            border-top: 1px solid #E0E0E0;
        }
        .footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <table class="email-container">
        <tr>
            <td class="header">
                <h1>REdI Trolley Audit System</h1>
                <p>New Issue Assignment</p>
            </td>
        </tr>
        <tr>
            <td class="content">
                <p class="greeting">Hi {AssigneeName},</p>

                <p>An issue has been assigned to you for resolution.</p>

                <div class="assignment-box">
                    <h3>{IssueTitle}</h3>
                    <p>Issue ID: <strong>{IssueNumber}</strong></p>
                </div>

                <h3>Issue Details</h3>
                <div class="detail-row">
                    <div class="detail-label">Location:</div>
                    <div class="detail-value">{Location}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Category:</div>
                    <div class="detail-value">{IssueCategory}</div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Severity:</div>
                    <div class="detail-value">
                        <span class="{Severity === 'Critical' ? 'severity-critical' :
                                     Severity === 'High' ? 'severity-high' :
                                     Severity === 'Medium' ? 'severity-medium' :
                                     'severity-low'}">
                            ● {Severity}
                        </span>
                    </div>
                </div>
                <div class="detail-row">
                    <div class="detail-label">Assigned By:</div>
                    <div class="detail-value">{AssignedBy}</div>
                </div>

                <h3>Description</h3>
                <div class="description-box">
                    <p>{Description}</p>
                </div>

                <div class="timeline">
                    <h4>Timeline</h4>
                    <p><strong>Target Resolution Date:</strong> {TargetResolutionDate}</p>
                    <p style="font-size: 13px; margin: 10px 0 0 0; color: #666666;">
                        Please ensure corrective action is taken and documented by this date.
                    </p>
                </div>

                <div class="action-items">
                    <h4>What You Need to Do</h4>
                    <ul class="action-list">
                        <li>Review the issue details carefully</li>
                        <li>Plan corrective action</li>
                        <li>Log corrective action in the system when started</li>
                        <li>Update status as you progress</li>
                        <li>Request verification when complete</li>
                    </ul>
                </div>

                <p style="text-align: center;">
                    <a href="{IssueLink}" class="button">View & Update Issue</a>
                </p>

                <p>Questions? Check the issue comments or contact {AssignedBy}.</p>
            </td>
        </tr>
        <tr>
            <td class="footer">
                <p>This is an automated message from the REdI Trolley Audit System.</p>
                <p>Do not reply to this email. Contact your MERT Educator for assistance.</p>
                <p>&copy; REdI 2026</p>
            </td>
        </tr>
    </table>
</body>
</html>
```

---

### Task 4.1.6: Add Assignment Notification to Assign Issue Flow

**Objective:** Integrate the assignment email into the "Assign Issue" flow (Task 2.8.3).

#### Step 1: Locate Existing Assign Issue Flow

1. Open **Power Automate** → **Cloud flows**
2. Find flow named `Assign_Issue` (created in Phase 2, Task 2.8.3)
3. Select **Edit**

#### Step 2: Add Send Email After Assignment

After the "Update Issue status to Assigned" action:

1. Add **Outlook** → **Send an email (V2)**

**To:**
```
@{body('Get_Assigned_Person')?['Email']}
```

**Subject:**
```
[REdI Trolley Audit] New Issue Assigned - @{body('Get_Issue')?['Title']}
```

**Body:**
[Use Issue Assignment template from Step 2]

**IsHtml:**
```
true
```

#### Step 3: Add CC to Auditor or Reporter

Add optional **CC**:
```
@{body('Get_Issue')?['ReportedByEmail']}
```

#### Step 4: Test the Flow

1. Create an issue in the system
2. Assign it to a test user
3. Verify email sends with:
   - Correct assignee address
   - All issue details populated
   - Severity colour coding
   - Action items displaying correctly

---

## Task 4.1.7-4.1.8: Weekly Selection Announcement

### Task 4.1.7: Create Weekly Selection Email Template

**Objective:** Design an email announcing the weekly random audit selection to MERT team and ward managers.

#### Step 1: Email Template Design

**Subject Line:** `[REdI Trolley Audit] Weekly Random Selection - {WeekStartDate} to {WeekEndDate}`

**Template Variables:**
```
{WeekStartDate}      - Monday date
{WeekEndDate}        - Sunday date
{GeneratedDate}      - When selection was generated
{SelectionCount}     - Count of trolleys (typically 10)
{TrolleyList}        - Table/list of selected trolleys
{DaysSinceAudit}     - For each trolley
{Priority}           - High/Medium/Low for each
{ServiceLineCounts}  - Breakdown by service line
{StartAuditLink}     - Link to start audits
```

#### Step 2: HTML Email Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Audit Selection</title>
    <style type="text/css">
        body {
            font-family: 'Segoe UI', Calibri, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #F5F5F5;
        }
        .email-container {
            width: 600px;
            margin: 20px auto;
            background-color: #FFFFFF;
            border-collapse: collapse;
        }
        .header {
            background-color: #1B3A5F;
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: bold;
        }
        .header p {
            margin: 5px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }
        .content {
            padding: 30px 20px;
            color: #333333;
        }
        .week-box {
            background-color: #E8F4F8;
            border-left: 4px solid #1B3A5F;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .week-box h3 {
            margin: 0 0 10px 0;
            color: #1B3A5F;
            font-size: 16px;
        }
        .week-box p {
            margin: 5px 0;
        }
        .selection-table {
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
            background-color: #F9F9F9;
        }
        .selection-table th {
            background-color: #1B3A5F;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        .selection-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #E8E8E8;
        }
        .rank {
            background-color: #E8F4F8;
            color: #1B3A5F;
            font-weight: bold;
            text-align: center;
            width: 40px;
        }
        .priority-high {
            background-color: #FFEBEE;
            color: #D32F2F;
            font-weight: bold;
        }
        .priority-medium {
            background-color: #FFF3E0;
            color: #F57F17;
            font-weight: bold;
        }
        .priority-low {
            background-color: #E8F5E9;
            color: #388E3C;
            font-weight: bold;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background-color: #F5F5F5;
            border: 1px solid #E0E0E0;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .stat-card .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #1B3A5F;
        }
        .stat-card .stat-label {
            font-size: 12px;
            color: #666666;
            margin-top: 5px;
        }
        .progress-bar {
            width: 100%;
            background-color: #E0E0E0;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            background-color: #2B9E9E;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }
        .action-box {
            background-color: #E8F4F8;
            border-left: 4px solid #1B3A5F;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .action-box h3 {
            margin: 0 0 10px 0;
            color: #1B3A5F;
            font-size: 16px;
        }
        .button {
            background-color: #1B3A5F;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin: 10px 0;
            font-weight: bold;
        }
        .footer {
            background-color: #F5F5F5;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666666;
            border-top: 1px solid #E0E0E0;
        }
    </style>
</head>
<body>
    <table class="email-container">
        <tr>
            <td class="header">
                <h1>REdI Trolley Audit System</h1>
                <p>Weekly Random Audit Selection</p>
            </td>
        </tr>
        <tr>
            <td class="content">
                <p style="font-size: 16px; margin-bottom: 20px;">
                    Hi MERT Team,
                </p>

                <p>This week's random audit selection has been generated. Please begin conducting these audits this week.</p>

                <div class="week-box">
                    <h3>Selection Period</h3>
                    <p><strong>Week of:</strong> {WeekStartDate} to {WeekEndDate}</p>
                    <p><strong>Generated:</strong> {GeneratedDate}</p>
                    <p><strong>Target Trolleys:</strong> {SelectionCount}</p>
                </div>

                <h3>Selected Trolleys for Audit</h3>

                <table class="selection-table">
                    <tr>
                        <th>#</th>
                        <th>Location</th>
                        <th>Days Since Last Audit</th>
                        <th>Priority</th>
                    </tr>
                    <!-- Repeat this row for each trolley -->
                    <tr>
                        <td class="rank">1</td>
                        <td>{TrolleyName}</td>
                        <td>{DaysSinceAudit}</td>
                        <td class="priority-high">HIGH</td>
                    </tr>
                    <!-- Additional rows generated dynamically -->
                </table>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{CompletedCount}</div>
                        <div class="stat-label">Completed This Week</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{PendingCount}</div>
                        <div class="stat-label">Still to Complete</div>
                    </div>
                </div>

                <p style="font-size: 13px; color: #666666; margin: 15px 0;">
                    <strong>Progress:</strong> {CompletedCount}/{SelectionCount} audits completed
                </p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {CompletedPercentage}%;">
                        {CompletedPercentage}%
                    </div>
                </div>

                <h3>By Service Line</h3>
                <p style="font-size: 14px; color: #666666;">
                    {ServiceLineBreakdown}
                </p>

                <div class="action-box">
                    <h3>Next Steps</h3>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Prioritise High priority trolleys (not audited 6+ months)</li>
                        <li>Spread audits throughout the week</li>
                        <li>Update status as each audit completes</li>
                        <li>Any issues found will trigger immediate notifications</li>
                    </ul>
                </div>

                <p style="text-align: center; margin: 20px 0;">
                    <a href="{AppLink}/audits" class="button">Start Audit</a>
                    <a href="{AppLink}/selection" class="button" style="background-color: #2B9E9E; margin-left: 10px;">View Selection</a>
                </p>

                <p>
                    <strong>Reminders:</strong>
                    <br/>
                    • All selected trolleys should be audited this week if possible
                    <br/>
                    • Report any issues found immediately
                    <br/>
                    • Next week's selection will be generated Monday morning
                </p>
            </td>
        </tr>
        <tr>
            <td class="footer">
                <p>This is an automated message from the REdI Trolley Audit System.</p>
                <p>Do not reply to this email. Contact your MERT Educator for assistance.</p>
                <p>&copy; REdI 2026</p>
            </td>
        </tr>
    </table>
</body>
</html>
```

---

### Task 4.1.8: Add Selection Notification to Generate Selection Flow

**Objective:** Integrate the weekly selection email into the generation flow.

#### Step 1: Locate Generate Selection Flow

1. Open **Power Automate** → **Cloud flows**
2. Find flow named `Generate_Weekly_Selection` (created in Phase 2, Task 2.9.15)
3. Select **Edit**

#### Step 2: Add Email Action After Selection Created

After the "Create RandomAuditSelectionItems" action:

1. Add **Outlook** → **Send an email (V2)**

**To:**
```
MERT.Educators@rbwh.com.au (distribution list)
```

**CC:**
```
(Optional: Ward managers for their trolleys)
```

**Subject:**
```
[REdI Trolley Audit] Weekly Random Selection - @{formatDateTime(addDays(utcNow(), sub(dayOfWeek(utcNow()), 2)), 'dddd d MMMM')} to @{formatDateTime(addDays(utcNow(), sub(dayOfWeek(utcNow()), 2) + 6), 'dddd d MMMM')}
```

**Body:**
[Use Weekly Selection template]

**IsHtml:**
```
true
```

#### Step 3: Build Dynamic Trolley Table

Use a **Table** action to create the selection list:

```
Inputs: RandomAuditSelectionItem records
Columns:
- Rank
- Location DisplayName
- DaysSinceAudit
- PriorityText (HIGH/MEDIUM/LOW)
```

#### Step 4: Calculate Statistics

Add **Compose** actions before the email:

```
CompletedCount: filter(SelectionItems where AuditId is not null).length
PendingCount: filter(SelectionItems where AuditId is null).length
CompletedPercentage: (CompletedCount / 10) * 100
```

#### Step 5: Test Weekly Generation

1. Set the flow to run manually for testing
2. Execute the flow
3. Verify email contains:
   - All 10 selected trolleys
   - Correct days since audit
   - Service line breakdown
   - Progress statistics
   - Working links to app

---

## Task 4.1.9: Overdue Audit Reminder

### Objective

Create a **scheduled flow** that runs daily to identify trolleys with overdue audits and send reminder emails to Ward Managers.

### Implementation Steps

#### Step 1: Create Scheduled Cloud Flow

1. Open **Power Automate** → **Cloud flows** → **Scheduled cloud flows**
2. Click **New scheduled cloud flow**
3. Configure:
   - **Name:** `Daily_Overdue_Audit_Reminders`
   - **Recurrence:**
     - Every: 1 Day
     - At: 06:00 (morning)
     - Time zone: [Your local time zone]

#### Step 2: Query Overdue Trolleys

Add **SharePoint** → **Get items**:

**List:** Location
**Filter Query:**
```
(Status eq 'Active') and ((DaysSinceLastAudit gt 180) or (DaysSinceLastAudit eq null))
```

This retrieves trolleys:
- Not audited in more than 180 days, OR
- Never been audited

#### Step 3: Group by Ward Manager

Add **Outlook** → **Get my profile**:
- Use to get current user context

Add **Compose** action to group trolleys by Service Line:
```
groupBy(outputs('Get_Overdue_Trolleys'), item().ServiceLineId)
```

#### Step 4: Send Ward Manager Emails

Add **Apply to each**:
- For each Service Line group:

**Send email (V2)**:

**To:**
```
@{item()?['ContactEmail']}
```

**Subject:**
```
[REdI Trolley Audit] Overdue Trolleys - Action Required - @{formatDateTime(utcNow(), 'dd/MM/yyyy')}
```

**Body:**

```html
<!DOCTYPE html>
<html>
<head>
    <style type="text/css">
        .overdue-item {
            margin: 10px 0;
            padding: 10px;
            background-color: #FFF3E0;
            border-left: 3px solid #F57F17;
        }
        .overdue-count {
            font-size: 20px;
            font-weight: bold;
            color: #D32F2F;
        }
    </style>
</head>
<body>
    <h2>Trolleys Overdue for Audit</h2>
    <p>Hi Ward Manager,</p>

    <p>The following trolleys in your service line are overdue for audit:</p>

    <div class="overdue-count">@{length(items('Get_Overdue_Trolleys'))} Trolleys</div>

    <h3>Details:</h3>

    @{each(items('Get_Overdue_Trolleys'), concat(item().DisplayName, ' - ', item().DaysSinceLastAudit, ' days since last audit'))}

    <p>Please schedule audits for these trolleys this week.</p>

    <p><a href="https://[app-url]/trolleys">View Trolley List</a></p>
</body>
</html>
```

**IsHtml:** true

#### Step 5: Add Frequency Thresholds

Create conditional branches:

**If > 10 trolleys overdue:**
- Also email MERT Educators
- Add flag for escalation

**If > 5 trolleys overdue:**
- Normal ward manager notification

**If > 180 days overdue:**
- Mark as "Critical" in subject line

#### Step 6: Add Logging

Add **Create item** to log reminder sent:
- List: NotificationLog (create this list first)
- Track: Who received, how many trolleys, when sent

#### Step 7: Test the Flow

1. Manually trigger the flow
2. Verify:
   - Correct trolleys identified
   - Emails sent to right recipients
   - Email formatting displays correctly
   - Links work

---

## Task 4.1.10: Issue Escalation Workflow

### Objective

Create a **scheduled flow** that automatically escalates overdue issues based on age and severity.

### Escalation Rules

```
Critical severity > 3 days → Escalate to Level 2
High severity > 7 days → Escalate to Level 2
Medium/Low severity > 30 days → Escalate to Level 2
Any issue > 30 days → Escalate to Level 3 (executive)
```

### SLA Integration (New)

The Issue schema includes calculated SLA tracking fields that simplify escalation logic:

| Field | Type | Purpose |
|-------|------|---------|
| TargetResolutionDate | Calculated | Auto-calculates SLA deadline based on severity |
| SLAStatus | Calculated | "On Track", "At Risk", "Breached", "Completed" |
| DaysToSLA | Calculated | Days remaining (negative if breached) |

**Simplified Escalation Query using SLA fields:**
```
Filter Query: (SLAStatus eq 'Breached') and (EscalationLevel ne 'Level2') and (EscalationLevel ne 'Level3')
```

This automatically captures all issues that have exceeded their severity-based SLA deadline without needing complex date calculations in the flow.

### Implementation Steps

#### Step 1: Create Scheduled Cloud Flow

1. Open **Power Automate** → **Cloud flows** → **Scheduled cloud flows**
2. Click **New scheduled cloud flow**
3. Configure:
   - **Name:** `Daily_Issue_Escalation`
   - **Recurrence:**
     - Every: 1 Day
     - At: 07:00 (morning, after overdue audit reminders)
     - Time zone: [Your time zone]

#### Step 2: Query Issues for Escalation

Add **SharePoint** → **Get items**:

**List:** Issue
**Filter Query:**
```
(Status ne 'Closed') and (Status ne 'Resolved')
```

This gets all open issues.

#### Step 3: Calculate Age and Check Escalation Rules

Add **Apply to each**:
- For each Issue:

Inside the loop, add **Condition** with nested branches:

**Branch 1: Critical Issues > 3 days old**
```
Condition: (Severity eq 'Critical') AND (Age > 3)
Action: Escalate to Level 2
```

**Branch 2: High Issues > 7 days old**
```
Condition: (Severity eq 'High') AND (Age > 7)
Action: Escalate to Level 2
```

**Branch 3: Any Issue > 30 days old**
```
Condition: (Age > 30)
Action: Escalate to Level 3
```

#### Step 4: Update Issue Escalation Status

In each branch, add **SharePoint** → **Update item**:

**List:** Issue
**Item ID:** @{item()['ID']}

**Update fields:**
- Status: `Escalated`
- EscalationLevel: `2` or `3`
- EscalatedDate: `today()`
- EscalatedTo: `@{body('Get_Escalation_Manager')['Email']}`

#### Step 5: Get Escalation Manager

Before updating, retrieve the manager to escalate to:

**If Level 2 escalation:**
- Get ServiceLine manager
- Get Location manager
- Assign to ServiceLineContactEmail

**If Level 3 escalation:**
- Get MERT Educator list
- Assign to MERT distribution group

Add action:
```
Get Location record → Get ServiceLine record → Get ContactEmail
```

#### Step 6: Send Escalation Notification Emails

After updating issue, send email:

**To:** @{escalationManagerEmail}

**Subject:**
```
[ESCALATED] Issue Overdue - {IssueNumber} - {Location}
```

**Body:**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .escalation-alert {
            background-color: #FFEBEE;
            border-left: 4px solid #D32F2F;
            padding: 15px;
            margin: 15px 0;
        }
        .escalation-level {
            font-size: 24px;
            font-weight: bold;
            color: #D32F2F;
        }
        .days-overdue {
            font-size: 18px;
            font-weight: bold;
            color: #F57F17;
        }
    </style>
</head>
<body>
    <h2>Issue Escalation Notice</h2>

    <div class="escalation-alert">
        <p>An issue has been escalated due to age and severity.</p>
        <p><strong>Escalation Level:</strong> <span class="escalation-level">Level {EscalationLevel}</span></p>
        <p><strong>Days Overdue:</strong> <span class="days-overdue">{DaysOverdue}</span></p>
    </div>

    <h3>Issue Details:</h3>
    <ul>
        <li><strong>ID:</strong> {IssueNumber}</li>
        <li><strong>Title:</strong> {IssueTitle}</li>
        <li><strong>Location:</strong> {Location}</li>
        <li><strong>Severity:</strong> {Severity}</li>
        <li><strong>Status:</strong> {Status}</li>
        <li><strong>Days Open:</strong> {DaysOpen}</li>
        <li><strong>Assigned To:</strong> {AssignedTo}</li>
    </ul>

    <p>Please review and take appropriate action.</p>
    <p><a href="{IssueLink}">View Issue</a></p>
</body>
</html>
```

#### Step 7: Add Escalation History Entry

Create item in escalation log:
- Issue ID
- Previous level
- New level
- Reason (Age threshold met)
- Escalated on (date)
- Escalated to (person/role)

#### Step 8: Prevent Duplicate Escalations

Add condition to check:
```
If EscalationLevel is already 2 or 3 → Skip (already escalated)
Else → Apply escalation rules
```

#### Step 9: Create Dashboard View

Add **Condition** to check if escalation occurred:
```
If any issues escalated today → Send summary to MERT
```

Send summary email to MERT with:
- Count of Level 2 escalations
- Count of Level 3 escalations
- List of escalated issues
- Recommended actions

#### Step 10: Test the Flow

1. Manually create test issues with various ages and severities
2. Run the flow manually
3. Verify:
   - Correct escalation levels applied
   - Emails sent to right recipients
   - History logged
   - Dashboard updated
   - No duplicate escalations occur

---

## Verification Checklist

### Email Templates Verification

- [ ] All 5 email templates created with correct HTML structure
- [ ] REdI branding applied consistently (logo, #1B3A5F colour)
- [ ] All template variables correctly identified
- [ ] HTML renders properly in Outlook, Gmail, mobile devices
- [ ] Alt text added to images
- [ ] Links are formatted as buttons, not plain text
- [ ] Footer includes unsubscribe/preferences link

### Transactional Flows (4.1.1-4.1.8) Verification

**Audit Submission (4.1.1-4.1.2):**
- [ ] Email triggers automatically when audit submitted
- [ ] All compliance subscores display
- [ ] Critical issues section shows when applicable
- [ ] Follow-up required section shows when compliance < 80%
- [ ] Auditor receives email at correct address
- [ ] App link works correctly

**Critical Issue Alert (4.1.3-4.1.4):**
- [ ] Email triggers only for Critical severity issues
- [ ] MERT educators and location manager both notified
- [ ] Urgent banner displays
- [ ] Clinical impact is clear
- [ ] Immediate action list included
- [ ] Link to issue details is clickable

**Issue Assignment (4.1.5-4.1.6):**
- [ ] Email triggers when issue is assigned
- [ ] Correct person receives notification
- [ ] Issue details populate correctly
- [ ] Target resolution date displays
- [ ] Action items list included
- [ ] Reporter/auditor optionally CC'd

**Weekly Selection (4.1.7-4.1.8):**
- [ ] Email triggers after selection generated
- [ ] All 10 trolleys display in table
- [ ] Days since audit accurate
- [ ] Priority levels correct (High/Medium/Low)
- [ ] Service line breakdown included
- [ ] Progress statistics show
- [ ] Start audit button links to app

### Scheduled Flows Verification (4.1.9-4.1.10)

**Overdue Reminders (4.1.9):**
- [ ] Flow runs daily at 06:00
- [ ] Correctly identifies trolleys > 180 days since audit
- [ ] Correctly identifies never-audited trolleys
- [ ] Groups by service line
- [ ] Ward managers receive emails with correct trolleys
- [ ] Email includes count of overdue trolleys
- [ ] Link to trolley list works

**Issue Escalation (4.1.10):**
- [ ] Flow runs daily at 07:00
- [ ] Critical issues > 3 days trigger Level 2 escalation
- [ ] High issues > 7 days trigger Level 2 escalation
- [ ] Any issue > 30 days triggers Level 3 escalation
- [ ] Correct managers notified based on level
- [ ] Issue status updated to "Escalated"
- [ ] EscalationLevel field updated correctly
- [ ] History logged accurately
- [ ] No duplicate escalations occur
- [ ] Summary email sent to MERT with stats

### Recipient Logic Verification

- [ ] Auditors receive confirmation at email from audit form
- [ ] MERT educators receive critical alerts automatically
- [ ] Ward/Location managers receive assignments
- [ ] Assignment recipients can update status
- [ ] Escalation recipients are appropriate for severity level
- [ ] CC/BCC fields used appropriately
- [ ] Distribution lists resolve correctly

### Email Branding Verification

- [ ] REdI logo displays correctly (150x60px)
- [ ] Primary colour #1B3A5F used consistently
- [ ] Secondary colour #2B9E9E used for highlights/buttons
- [ ] Font is Segoe UI or Calibri
- [ ] Text colour is #333333 (dark grey)
- [ ] Footer colour is #666666 (medium grey)
- [ ] Footer includes copyright and contact info

---

## Troubleshooting

### Email Not Sending

**Problem:** Flow runs but email doesn't arrive

**Solutions:**
1. Check **Outlook** connection is valid: Power Automate → **Connections** → **Outlook**
2. Verify email address is valid (use **Get item** to retrieve email from List)
3. Check email is not being flagged as spam (check Junk folder)
4. Verify **IsHtml** toggle is **ON** for HTML formatting

### Email Formatting Issues

**Problem:** Email shows HTML code instead of formatted content

**Solutions:**
1. Ensure **IsHtml** is set to **true** in Send email action
2. Check angle brackets `<>` are properly escaped if in JSON
3. Test with smaller template first, build up complexity
4. Use Power Automate expression syntax correctly

### Variable Not Populating

**Problem:** Email shows `{VariableName}` instead of actual value

**Solutions:**
1. Use **Dynamic content** picker, not manual text entry
2. Ensure parent records are retrieved first (Get item actions)
3. Check column names match exactly (case-sensitive in formulas)
4. Use correct syntax: `@{body('Action_Name')?['ColumnName']}`

### Flow Not Triggering

**Problem:** Flow doesn't run when issue is created/assigned

**Solutions:**
1. Verify trigger is connected to correct action (Submit Audit, Create Issue, etc.)
2. Check **Apply to each** loops are needed for multiple recipients
3. Ensure **Condition** branches are structured correctly
4. Test manually first to verify flow logic
5. Check flow is **Enabled** (toggle in flow details)

### Scheduled Flow Not Running

**Problem:** Daily flows don't run at scheduled time

**Solutions:**
1. Check time zone is set correctly in recurrence
2. Ensure flow is **Enabled**
3. Verify no required connections are missing
4. Check Power Automate environment doesn't have limits
5. Use Power Automate admin to check flow runs history

### Recipients Not Getting Email

**Problem:** Email sent but wrong person receives it or goes to wrong address

**Solutions:**
1. Verify lookup fields are retrieving correct email addresses
2. Test email addresses manually before deploying
3. Use distribution lists for groups, not individual emails
4. Check for typos in hardcoded email addresses
5. Verify permissions allow these users to receive audit/issue notifications

### HTML Table Not Rendering

**Problem:** Table appears as text instead of formatted table

**Solutions:**
1. Ensure `<table>` tags are properly closed
2. Use inline CSS (not `<style>` tags) for compatibility
3. Test in Outlook first (most common email client)
4. Avoid complex nested tables
5. Keep table width to 600px for email clients

---

## Next Steps

After completing Phase 4.1 Notifications:

1. **Test with Real Data** (1-2 hours)
   - Create test audits and verify notifications
   - Assign test issues and verify recipient list
   - Run scheduled flows and check logs

2. **Integrate with PowerApp** (if needed)
   - Add notification preferences screen
   - Allow users to opt out of certain notifications
   - Store preferences in SharePoint

3. **Monitor and Optimize** (ongoing)
   - Check email delivery success rates
   - Adjust recipient lists based on feedback
   - Add new notification types as needed

4. **Phase 4.2 - Advanced Features**
   - Enable PowerApp offline mode
   - Add photo attachment capability
   - Build equipment customization screen

---

## Additional Resources

- **Power Automate Documentation:** https://docs.microsoft.com/en-us/power-automate/
- **Email Best Practices:** https://www.litmus.com/email-marketing-best-practices/
- **Outlook Email Limitations:** https://support.microsoft.com/en-us/office/conditions-and-exceptions-in-rules-26c5111c-5c60-435a-9a7f-8f42853d1c22
- **SharePoint Expression Reference:** https://docs.microsoft.com/en-us/sharepoint/dev/general-development/rest-api-overview

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial implementation guide created |

---

**Document Owner:** MERT Education Team
**Last Updated:** January 25, 2026
**Next Review:** Upon completion of Phase 4.1 implementation

---

*End of Phase 4.1 Notifications Implementation Guide*
