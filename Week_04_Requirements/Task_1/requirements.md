# Software Requirements Specification

Generated on 2026-10-20 by `requirements_network.py` from 20 input documents in `data/corpus`.

Models: extract = `gpt-5-mini`, merge = `gpt-6-luna`, review = `gpt-5.6-luna`, write = `gpt-5.4-nano`.

908 statements were extracted. 814 were requirement candidates; the other 94 describe the existing system and were used as facts for spotting nonsensical requests, not as requirements.

## Priority scale

| Priority | Meaning |
|---|---|
| High | Agreed in a decision (a thread summary or ratified meeting minutes) or asked for in at least three different source documents. |
| Medium | Asked for in one or two source documents (for example only in the draft specification), with no later decision. |
| Low | Suggested by one person in a discussion and not confirmed by anyone, or an optional convenience. |

## Summary

| ID | Name | Priority |
|---|---|---|
| FR-001 | Material Volume Report | High |
| FR-002 | Branch Capacity Overview | High |
| FR-003 | Shelf Space Report | High |
| FR-004 | Batch Item Transfers | High |
| FR-005 | Automatic Transfer Reversion | High |
| FR-006 | Transfer History and Alerts | High |
| FR-007 | Missing and Damaged Items Report | High |
| FR-008 | Aged In-Transit Report | High |
| FR-009 | Item Purge Identification Criteria | High |
| FR-010 | Batch Status Conversion Tools | High |
| FR-011 | Last Copy Report For Scope | High |
| FR-012 | Quick Delete Volumes And Copies | High |
| FR-013 | Quick Delete Orphaned Bibliographic Records | High |
| FR-014 | Deletion Audit And Purge Safeguards | High |
| FR-015 | Patron Demographics Filter And Group | High |
| FR-016 | Inactive Patrons Report And Export | High |
| FR-017 | Separate Dev And Training Environments | High |
| FR-018 | Role And Group Access Control | High |
| FR-019 | Role-Based Management Capabilities | High |
| FR-020 | System Help Accessibility And Navigation | High |
| FR-021 | High And Low-Level Error Feedback | High |
| FR-022 | Optional Streamlined Staff Login | High |
| FR-023 | Report Templates And Open Reporting | High |
| FR-024 | Shared Folder Report Access Controls | High |
| FR-025 | User-Friendly Query Builder Controls | High |
| FR-026 | Fine-Grained Report Permission Levels | High |
| FR-027 | Predefined Board Statistical Reports | High |
| FR-028 | Transaction Reports With Filters And Grouping | High |
| FR-029 | Report Criteria Display With Results | High |
| FR-030 | Report Queue Position And Status | High |
| FR-031 | Demographic Statistics For Planning | High |
| FR-032 | Value Of Items With Filters | High |
| FR-033 | Financial Data Joinable By Records | High |
| FR-034 | Payments Collected By Branch Reporting | High |
| FR-035 | Patron Balance Threshold Query | High |
| FR-036 | Patron Account Balance Reports | High |
| FR-037 | Fines and Charges Time Type Reports | High |
| FR-038 | Waived Fines By Time And Branch | High |
| FR-039 | Payments Reports By Time Method Library | High |
| FR-040 | Payment Audit Trail Ledger | High |
| FR-041 | Circulation By MARC Fields | High |
| FR-042 | Canned Report Scheduling Options | High |
| FR-043 | Report Output Formats And Pivot | High |
| FR-044 | Email Reports To Addresses And Book | High |
| FR-045 | Report Priority Queue | High |
| FR-046 | Report Cancellation During Processing | High |
| FR-047 | Include Null And Blank Fields | High |
| FR-048 | Real-Time Reporting Support | High |
| FR-049 | Historical Reporting Warehouse | High |
| FR-050 | Survey Name To Identifier Filtering | High |
| FR-051 | Vendor Data Exchange Interfaces | High |
| FR-052 | Read-Only OPAC Data Access | High |
| FR-053 | Data Quality Issue Identification Reports | High |
| FR-054 | Saved Query Reuse With Export Import | High |
| FR-055 | Transfer Query Sharing | Medium |
| FR-056 | Periodic Bibliographic Holds Report | Medium |
| FR-057 | Periodic No Recent Checkout Report | Medium |
| FR-058 | Periodic Item-Level Holds Report | Medium |
| FR-059 | Periodic Transit Holds Report | Medium |
| FR-060 | Periodic Invalid Home Library Report | Medium |
| FR-061 | Patron Behavior Statistics Reports | Medium |
| FR-062 | Uncataloged Inventory With Usage | Medium |
| FR-063 | Patron Checkouts And Holds Summary | Medium |
| FR-064 | Overdue Items Reports With Patron Contact | Medium |
| FR-065 | Circulation Counts By Modifier And Categories | Medium |
| FR-066 | Total Circulation Count By Type | Medium |
| FR-067 | Circulation Count By Dewey Report | Medium |
| FR-068 | Circulation By Patron County | Medium |
| FR-069 | Circulation By Age Demographic | Medium |
| FR-070 | Fines Stopped Reason Report | Medium |
| FR-071 | Transit Items By Library | Medium |
| FR-072 | Claims Returned Report | Medium |
| FR-073 | Weeding Report With Circulation Stats | Medium |
| FR-074 | Bibliographic Field Value Search | Medium |
| FR-075 | Collection Age By Location | Medium |
| FR-076 | Bibliographic Records Edited Count | Medium |
| FR-077 | Bibliographic Additions By User Count | Medium |
| FR-078 | Missing MARC Fields Reports | Medium |
| FR-079 | Patron Count By Age Demographic | Medium |
| FR-080 | Patron Count By County | Medium |
| FR-081 | Patron Count By Geography | Medium |
| FR-082 | Patron Count By Profile Group | Medium |
| FR-083 | Patron Survey Answer Grouping | Medium |
| FR-084 | Voter Survey County By Week | Medium |
| FR-085 | Patron Expiration List | Medium |
| FR-086 | Voter Registration Count By Week | Medium |
| FR-087 | Barred Patrons List | Medium |
| FR-088 | Inactive Status Patron List | Medium |
| FR-089 | Staff Accounts Report | Medium |
| FR-090 | Patrons With Notes Wording | Medium |
| FR-091 | Holds Purchase Alert Report | Medium |
| FR-092 | Items Sent for Holds Report | Medium |
| FR-093 | Items Received for Holds Report | Medium |
| FR-094 | Unfilled Holds Report | Medium |
| FR-095 | Stale Holds Report | Medium |
| FR-096 | Detailed Aged Debt Report | Medium |
| FR-097 | Run Multiple Canned Reports | Medium |
| FR-098 | Report Title Descriptions With Tooltips | Medium |
| FR-099 | Comparative Report Columns | Medium |
| FR-100 | Item Use Counts By Date | Medium |
| FR-101 | Upload Report Filters | Medium |
| FR-102 | Deleted Last-Copy Item Reports | Medium |
| FR-103 | Last Edit Date Field Separation | Medium |
| FR-104 | Separate Last Circulation Date | Medium |
| FR-105 | Separate Check-In And Renewal Timestamps | Medium |
| FR-106 | Historical Bills Snapshot Report | Medium |
| FR-107 | Local Custom Reports For Workflows | Medium |
| FR-108 | Director-Level Financial Reports | Medium |
| FR-109 | Cross-Branch Comparison Reporting | Medium |
| FR-110 | Comprehensive Reporting Data Availability | Medium |
| FR-111 | Scheduled Purge Utility | Low |
| FR-112 | Weeding Report Staff Template Constraints | Low |
| FR-113 | Circulation Count By Shelving Location | Low |
| FR-114 | Circulation By Patron Home Library | Low |
| FR-115 | Items Added List | Low |
| FR-116 | Items Count Report | Low |
| FR-117 | Long Overdue Items Reporting | Low |
| FR-118 | Items By Use Count Filters | Low |
| FR-119 | Items By Creation Date Range | Low |
| FR-120 | Patron Additions By Month Report | Low |
| FR-121 | New Patron Count Previous Month | Low |
| FR-122 | IntraPINES Loans Reports Scope | Low |
| FR-123 | Annual Holds Placed Count | Low |
| FR-124 | Non-Cataloged In-House Use Count | Low |
| FR-125 | Cataloged In-House Use Count Report | Low |
| FR-126 | Detailed Alternative Payments Report | Low |
| FR-127 | Detailed Voids Report | Low |
| FR-128 | Edit Recurring Report Selections | Low |
| FR-129 | Notice Type Reports | Low |
| FR-130 | Transaction Reports Date Time Filters | Low |
| NFR-001 | Consortium Scale Capacity Support | High |
| NFR-002 | Open Hours Report Queuing | High |
| NFR-003 | Web And Windows Client Access | High |
| NFR-004 | Assistive Technology And Section 508 | High |
| NFR-005 | Standards-Compliant HTML Validation | High |
| NFR-006 | Immediate Financial Information Updates | High |
| NFR-007 | Complete And Current Data Across Locations | High |
| NFR-008 | Large Transfer Processing | Medium |
| NFR-009 | Report Performance During Busy Hours | Medium |
| NFR-010 | Excel Export Deduplication Support | Medium |
| NFR-011 | Report Search And Run Usability | Medium |
| CON-001 | Linux Or Solaris Server Platforms | High |
| CON-002 | Relational Database Backend Compatibility | High |
| CON-003 | Management Reporting Processes Scope | High |
| CON-004 | Centralized Multi-Location Reporting | High |
| CON-005 | Archived Transaction Data Anonymization | High |
| CON-006 | Transaction History Retention Policy | High |
| CON-007 | Financial Reporting And Archiving Compliance | High |
| CON-008 | Data Specifications And Dictionaries | High |
| CON-009 | Process Descriptions Deliverable | High |

## Functional requirements

### FR-001: Material Volume Report

**Priority:** High  
**Sources:** `conversations/conv_pines014_material_volume.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide a consolidated Material Volume Report for a selected library and point in time. It shall support historical date filters and include breakdowns for new acquisitions, checked-in items, checked-out items, total items (including checked-out items), holds, adult fiction, board books, fiction and non-fiction, format, and other library-defined categories. It shall also provide views of material added in the last 30, 60, and 90 days and provide inventory reporting.

### FR-002: Branch Capacity Overview

**Priority:** High  
**Sources:** `conversations/conv_pines015_capacity_interface.eml`, `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide an overview of capacity across all branches with drill-down to individual branches. It shall support sorting and filtering by region, library type, and current load, and provide grouping by system or region. It shall display capacity trends over time and allow CSV export, with capacity metrics based on items versus shelf space, physical items versus a configured limit, and circulation volume versus processing capacity for the 286 locations. It shall use green, yellow, and red color coding to distinguish under-capacity, nearing-capacity, and at-or-over-capacity levels.

### FR-003: Shelf Space Report

**Priority:** High  
**Sources:** `conversations/conv_pines016_shelf_space.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide a Shelf Space Report that compares, for each genre and format, the percentage of total circulations, the percentage of the collection, and the percentage of total shelf space. It shall be available per library and per system and support date-range and quarterly views. It shall provide side-by-side library comparisons to support assessing shelf-space efficiency and redistribution.

### FR-004: Batch Item Transfers

**Priority:** High  
**Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`

The system shall provide a utility to transfer batches of items between branches and other locations, including temporary locations. It shall support querying candidate materials, saving and reusing queries, manually selecting titles or items, and changing item locations via a batch update of the location field. It shall preview transfer effects and require confirmation before changes, support an undo function, and perform transaction-safe and auditable updates. It shall generate printable pull lists and transit labels with barcodes and restrict transfer initiation to managers and administrators.

### FR-005: Automatic Transfer Reversion

**Priority:** High  
**Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`

The system shall automatically return transferred items to their original location after a configured period or when configured events or criteria occur. It shall support reversion based on item status changes to sold or returned, and on checkout at the destination. It shall also support event- or program-based temporary transfers, including reverting transferred items after the event.

### FR-006: Transfer History and Alerts

**Priority:** High  
**Sources:** `conversations/conv_pines018_item_transfer.eml`

The system shall track and audit all item transfers, including who transferred an item, when, and from and to which locations. It shall notify users when a transfer is delayed or encounters an issue. The system shall provide transfer history tracking for audit purposes.

### FR-007: Missing and Damaged Items Report

**Priority:** High  
**Sources:** `conversations/conv_pines019_020_missing_intransit.eml`, `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide missing and damaged item reports per branch. The reports shall include items whose status is missing, include condition notes, and support analysis by shelf location. It shall support configurable date ranges for trend analysis.

### FR-008: Aged In-Transit Report

**Priority:** High  
**Sources:** `conversations/conv_pines019_020_missing_intransit.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide a consolidated report of in-transit items by merging transit-to and transit-from information. The report shall be filterable or groupable per branch and per system and list items in transit longer than a configurable threshold X days. It shall default the threshold to 7 days and qualify an item when its transit record has a null arrival date and its departure date is more than X days ago. It shall support sorting by due date.

### FR-009: Item Purge Identification Criteria

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide reports and a utility to identify item records for purging using customizable, combinable criteria. The criteria shall include status-based conditions such as items missing for more than X months, items with discard/weed status, and items that are damaged. The criteria shall also support time in status and last-circulation activity.

### FR-010: Batch Status Conversion Tools

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`

The system shall provide reports and tools to identify items for conversion from one status to another. The system shall support batch status conversions, including changing many items from one status (such as missing) to another status (such as discard/weed) at once. This shall be done using the conversion report to assist the process.

### FR-011: Last Copy Report For Scope

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`

The system shall provide a last-copy report that identifies copies which are the last in a specified library or system scope. For each item record, the report shall flag whether it is the only copy in the specified scope. The report shall supply information useful to catalogers editing WorldCat entries.

### FR-012: Quick Delete Volumes And Copies

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`

The system shall provide a quick method to delete volume entries together with their associated copy entries. When a volume entry is deleted, the system shall delete the related copy entries as part of the same action.

### FR-013: Quick Delete Orphaned Bibliographic Records

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`

The system shall provide a quick method to identify and delete bibliographic records that have no attached item records. The identification shall be based on the absence of attached item records, and the system shall support deletion of those orphaned bibliographic records.

### FR-014: Deletion Audit And Purge Safeguards

**Priority:** High  
**Sources:** `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`

The system shall count and track record deletions by location and system, recording the record type and identifier, timestamp, deleting user, the user’s location, and the reason for deletion. The system shall track denied deletion attempts and provide an interface to query deletion audit data and generate reports aggregated by arbitrary date range, user, record type, and location. The system shall present purge candidates in read-only reports, require a separate confirmation before deletion, and maintain an audit trail for all purges.

### FR-015: Patron Demographics Filter And Group

**Priority:** High  
**Sources:** `conversations/conv_pines023_patron_characteristics.eml`, `early_draft_srs_galecia.txt`

The system shall allow queries and reports to filter or group by patron age range, zip code, county of residence, home branch, patron type, and preferred language. The system shall support configurable age ranges and support combining filters using AND/OR logic. The system shall include null values in results rather than excluding those records.

### FR-016: Inactive Patrons Report And Export

**Priority:** High  
**Sources:** `conversations/conv_pines023_patron_characteristics.eml`, `conversations/conv_pines024_inactive_patrons.eml`, `early_draft_srs_galecia.txt`

The system shall generate a list of patrons with no circulation or electronic activity in a configurable number of days. The report shall be configurable to organizational levels including system, home library, and county, and shall include current mailing addresses while allowing excluding specific patrons. The report shall flag or separately list patrons with outstanding fines and shall support CSV export for the fine-owing group or with flags, and it shall treat electronic activity such as OPAC logins, online hold placements, and online renewals as activity. The system shall also support recurring scheduling and background processing with cached results using a performance-optimized query.

### FR-017: Separate Dev And Training Environments

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall provide separate development, training, and production environments. The system shall isolate training from production data and support migrating configurations, templates, permissions, and saved queries between environments through export and import.

### FR-018: Role And Group Access Control

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `email_staff_login.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall control user rights through security groups and roles, supporting access control for individuals, workgroups, and staff groups. The system shall allow permissions to be administered by changing role assignments, and it shall include the roles Global Admin, Local Admin, Library Manager, and Staff, with Library Director as a distinct role alongside those four roles.

### FR-019: Role-Based Management Capabilities

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`

The system shall provide Local Admin users with elevated permissions to configure local settings and run reports. The system shall provide Library Manager users capabilities to supervise a single organizational unit and support planning and direction of library services. The system shall provide Library Director users with capabilities to plan and direct library services and priorities. The system shall provide Global Admin users the ability to implement consortium-level software changes and configurations and generate statistical reports for the consortium.

### FR-020: System Help Accessibility And Navigation

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall provide an online, hierarchical, cross-linked HTML help system describing system functions. The system shall provide context-sensitive help that is searchable and accessible to screen readers. The system shall support staff finding documentation without leaving the system to access help.

### FR-021: High And Low-Level Error Feedback

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall provide high-level error reporting and user feedback when reports or processes fail. The system shall provide low-level, query-specific feedback for administrators identifying the table, field, and error type. This feedback shall be available for Local and Global System Administrators from the front-end interface.

### FR-022: Optional Streamlined Staff Login

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall support optional streamlined staff login methods, including card-swipe login, while retaining individual username-and-password authentication as a fallback. The system shall identify the individual staff member when they log in by any supported method. The system shall apply permissions based on the user’s assigned role or security group.

### FR-023: Report Templates And Open Reporting

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `survey_results_2009.txt`

The system shall provide canned, on-demand, and open-template reporting, including delivered prewritten canned reports and on-demand reports with preselected criteria. Administrators shall be able to create and share report templates that users can run unchanged or modify. The system shall allow authorized users to clone reports or templates and add canned templates. Open-template reporting shall expose reportable attributes for filtering and display, and users shall be able to select report fields, filter by available reportable fields, and edit canned-report display options, with administrators able to restrict which filters and display fields non-admin users may alter while preserving result correctness and integrity.

### FR-024: Shared Folder Report Access Controls

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall allow administrators to use shared folders to control which staff may run particular reports or ad hoc reports on specific data sets. The system shall administer these permissions through roles so that staff report access can be managed by role. The system shall allow administrators to allow or disallow staff from running specific reports.

### FR-025: User-Friendly Query Builder Controls

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`

The system shall provide a user-friendly query interface for available record types. The system shall allow staff to select fields and values from picklists, use selectable regular-expression matching, and construct queries using Boolean operators. The system shall allow administrators to control access to query tables and fields.

### FR-026: Fine-Grained Report Permission Levels

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall provide fine-grained permissions distinguishing who may create, clone, modify, and run reports. The system shall support permission administration that is straightforward to administer. The system shall allow permission levels to control who can create and clone reports.

### FR-027: Predefined Board Statistical Reports

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide predefined board reports containing basic statistics required by the Georgia Annual Report and Application for State Aid. The system shall provide these reports for consumption by library boards and other external consumers. The system shall include basic statistics required for board/executive reporting.

### FR-028: Transaction Reports With Filters And Grouping

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `survey_results_2009.txt`

The system shall provide transaction reports for checkouts, check-ins, renewals, holds placed and filled, fines collected, patron registrations, and other available transaction types. The system shall allow reports across all transactions or filtered by transaction type. The system shall support grouping or cross-tabulation by terminal, branch, selected group of libraries, system, county, hour, patron age range, patron type, and patron location. The system shall provide reports per patron, library, selected group of libraries, system, and county, with check-in counts reportable individually and cumulatively by book drop, terminal, and staff or self-service method, and checkout and renewal counts distinguishing staff checkouts, self-checkouts, staff renewals, self-checkout renewals, online renewals, and OPAC renewals; hold reports shall distinguish placement at a staff desk, a public computer inside the library, or remotely.

### FR-029: Report Criteria Display With Results

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`

The system shall display report selection criteria and the report name with the report results. The system shall include the date selection criteria as part of the displayed results content. The displayed output shall show the report name alongside the results.

### FR-030: Report Queue Position And Status

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt`

The system shall show users the position and status of submitted reports in the processing queue. The system shall display queue position and submission time for submitted reports. The system shall indicate whether a report is waiting, running, completed, or failed.

### FR-031: Demographic Statistics For Planning

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt`

The system shall provide demographic statistics for transactions by geographical region and age range to support program planning. It shall protect patron identity by producing anonymized demographic statistics without personally identifiable information. The system shall include transactions grouped by geographical regions and age ranges, using age ranges and geographical detail that are useful for planning.

### FR-032: Value Of Items With Filters

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`, `evergreen_reference_2009.txt`

The system shall generate a value-of-items report using purchase price in item records. It shall support reporting for the entire collection or a selectable portion, with filters for item status, material type, and collection. The system shall support views grouped or selected by call number or shelving location.

### FR-033: Financial Data Joinable By Records

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall attach fines, charges, waivers, payments, and ecommerce transactions to patron records and item records. It shall make the associated financial data joinable so it can be used in financial reports and queries. The system shall support joining financial data across these patron and item record sources.

### FR-034: Payments Collected By Branch Reporting

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall track payments collected at each library branch or location. It shall provide support for branch-level reporting based on the location where payments were collected. It shall also support end-of-month reporting using the tracked branch payment data.

### FR-035: Patron Balance Threshold Query

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall allow staff to query patron accounts with balances greater than a specified dollar threshold. It shall provide queries that are easy and fast to execute. The system shall enable staff to perform these balance-threshold queries using the specified threshold value.

### FR-036: Patron Account Balance Reports

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall provide patron account balance reports by patron, home library, and system. The reports shall allow users to view balances at the patron level as well as aggregated by the home library and across the system. This supports reconciliation of account balances for patrons and libraries within the system.

### FR-037: Fines and Charges Time Type Reports

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall report fines and charges accrued by time period, including last 12 months, year-to-date, and last month. The system shall also report fines and charges accrued by charge type, including overdue fines, damaged-item charges, and lost-item charges. This allows users to analyze accrued amounts across both timing and type categories.

### FR-038: Waived Fines By Time And Branch

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall report fines waived by time period and branch, including monthly views and branch-level reconciliation views. This enables users to review waived fines over time for specific branches. It also provides reconciliation perspectives at the branch level.

### FR-039: Payments Reports By Time Method Library

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall report payments by time period, payment method, and library or branch. Payment method reporting shall include staff desk, self-check station, OPAC, cash, credit card, and check. This supports reconciliation views of payment activity across these categories.

### FR-040: Payment Audit Trail Ledger

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall maintain an audit-trail ledger of patron payments. The ledger shall record which charges each payment was applied to and allow each payment to be traced to a specific charge. This provides traceability from payments back to the charges they affect.

### FR-041: Circulation By MARC Fields

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall provide circulation reporting by MARC fields, presenting the fields for each record on a single row. This supports pulling MARC record fields so they are displayed together in one row of data for circulation reporting.

### FR-042: Canned Report Scheduling Options

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall allow canned reports to run immediately or on a recurring schedule at hourly, daily, weekly, monthly, or yearly intervals. The system shall support date ranges of yesterday, last week, last month, or last year for canned reports. This enables users to control when canned report data is generated and which date window is used.

### FR-043: Report Output Formats And Pivot

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall support report output and export in Excel, HTML, and CSV formats. The system shall also provide pivot-table-style output. Users shall be able to obtain reports in these formats according to the report output options.

### FR-044: Email Reports To Addresses And Book

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall allow users to email reports to one or more addresses. The system shall maintain an address book of commonly used report delivery destinations. This enables users to send report outputs via configured email destinations.

### FR-045: Report Priority Queue

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `evergreen_reference_2009.txt`

The system shall allow authorized users to prioritize reports in the processing queue. It shall enable certain report types to pop to the top over more resource-consuming reports, including allowing a director’s board report to jump ahead of a staff member’s ad-hoc query.

### FR-046: Report Cancellation During Processing

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall allow authorized users to cancel scheduled or running reports and to check for cancellation requests during report processing. It shall support canceling a report that has been scheduled to run or is currently running, and it shall process cancellation signals during execution.

### FR-047: Include Null And Blank Fields

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall include null and blank fields explicitly in report and query results rather than excluding them by default. It shall include all nulls and blank fields in results regardless of the filters or the displayed fields.

### FR-048: Real-Time Reporting Support

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall support real-time reporting for reports that require current data. It shall be able to provide outputs for scenarios such as what is overdue today during busy periods.

### FR-049: Historical Reporting Warehouse

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall support historical reporting that can retrieve data for a past date or date range. It shall include data as it existed before changes such as shelving-location updates and support a reporting warehouse for historical data.

### FR-050: Survey Name To Identifier Filtering

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall allow users to select a survey by name for report filtering and internally resolve the name to the survey identifier. It shall support filtering by survey name rather than requiring users to enter the survey ID.

### FR-051: Vendor Data Exchange Interfaces

**Priority:** High  
**Sources:** `meeting_tech_subcommittee_2009-06-30.txt`

The system shall interface with vendor websites through published APIs or automated transfers of standard-format data files. The system shall support standard-format data files including USMARC21 and EDIFACT. The system shall not depend on EDI availability at every library.

### FR-052: Read-Only OPAC Data Access

**Priority:** High  
**Sources:** `meeting_tech_subcommittee_2009-06-30.txt`

The system shall query OPAC data, including patron-created holds and circulation transactions. The system shall not modify OPAC data. This access shall support interaction between Management Processes and the patron interface for reporting purposes.

### FR-053: Data Quality Issue Identification Reports

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide data-quality reports identifying items with invalid item types, items with excessively long call numbers, and bibliographic records with no attached item records. This supports users in locating and reviewing data issues across item and bibliographic record relationships. The system shall generate these reports based on the stated data-quality conditions.

### FR-054: Saved Query Reuse With Export Import

**Priority:** High  
**Sources:** `conversations/conv_pines018_item_transfer.eml`, `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`

The system shall allow users to save and reuse queries and provide export/import functionality for saved queries. This supports repeated use of saved queries over time. The system shall also enable users to move saved queries in and out using export and import.

### FR-055: Transfer Query Sharing

**Priority:** Medium  
**Sources:** `conversations/conv_pines018_item_transfer.eml`

The system shall allow users to share saved transfer queries with other users for reuse. This enables reuse of transfer query definitions previously saved by other users.

### FR-056: Periodic Bibliographic Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a periodic report listing bibliographic records that have holds.

### FR-057: Periodic No Recent Checkout Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a periodic report of items that have not been checked out in a specified number of days.

### FR-058: Periodic Item-Level Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a periodic report of item-level holds.

### FR-059: Periodic Transit Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a periodic report of in-transit items with outstanding holds.

### FR-060: Periodic Invalid Home Library Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a periodic report of patrons with an invalid home library.

### FR-061: Patron Behavior Statistics Reports

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`

The system shall provide statistics for understanding and predicting patron behavior. The system shall compute average time until an item is returned. The system shall compute likelihood of renewal and the percentage of checkouts that are renewals.

### FR-062: Uncataloged Inventory With Usage

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `interview_cataloging_2009-05-08.txt`

The system shall track uncataloged material as inventory without requiring individual catalog records. It shall support quick distribution with minimal branch labor and identify how the uncataloged material is being used. The system shall count uncataloged material transactions and include those counts in circulation statistics and reports.

### FR-063: Patron Checkouts And Holds Summary

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall display the number of checkouts and placed holds per patron. It shall provide a subtotal of holds by type, including active, frozen, and frozen-until. The system shall present this patron transaction summary for staff review.

### FR-064: Overdue Items Reports With Patron Contact

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide reports of items overdue by a specified number of days. The system shall include daily and shelf-reading views and provide patron contact information in the overdue reports. This allows users to identify overdue items and contact affected patrons.

### FR-065: Circulation Counts By Modifier And Categories

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide circulation count reports grouped by circulation modifier, Cat1, and Cat2. The system shall also support a modifier-only view of circulation counts. This allows users to analyze circulation by modifier alone or by modifier with Cat1 and Cat2 categories.

### FR-066: Total Circulation Count By Type

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide circulation count reports including checkouts, renewals, and non-cataloged uses. The system shall include a breakdown by circulation type and also provide a total view that combines cataloged and non-cataloged circulation. This supports reporting both overall activity and the composition of that activity.

### FR-067: Circulation Count By Dewey Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Circulation Count by Dewey report. This report shall present circulation counts organized according to Dewey. The intent is to give users circulation reporting by Dewey classification.

### FR-068: Circulation By Patron County

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Circulation Count by Circulation Location report broken down by patron county. This report groups circulation counts by each patron county using the circulation location breakdown.

### FR-069: Circulation By Age Demographic

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Circulation Count by Age Demographic report. This report presents circulation counts segmented by an age demographic category.

### FR-070: Fines Stopped Reason Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a list of items by fines-stopped reason. This report categorizes items according to the fines-stopped reason associated with them and presents them in a list.

### FR-071: Transit Items By Library

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a list of items in transit for a given sending library and destination library. The list shall identify items based on the sending library and their destination library so the responsible parties can view in-transit holdings.

### FR-072: Claims Returned Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Claims Returned report identifying items recorded as claims returned. The report shall present the subset of items whose status indicates they were recorded as claims returned.

### FR-073: Weeding Report With Circulation Stats

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a weeding report that includes the date of last circulation for each item and the number of circulations. The report shall use these two circulation-derived fields to support weeding decisions.

### FR-074: Bibliographic Field Value Search

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a list of items that have a specified value in the bibliographic record. The system shall return the set of items matching the specified bibliographic field value.

### FR-075: Collection Age By Location

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide an age-of-collection report by call number or by shelving location. The report shall present collection age organized around one of these location identifiers.

### FR-076: Bibliographic Records Edited Count

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Bib Records Edited Count report. The report shall summarize counts of bibliographic records that were edited.

### FR-077: Bibliographic Additions By User Count

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Bib Records Added by User by Library Count report. The report shall break down the count of bibliographic records added by users by library.

### FR-078: Missing MARC Fields Reports

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide reports listing bibliographic records missing specified MARC fields. The reports shall identify which bibliographic records lack the required MARC fields specified for the report.

### FR-079: Patron Count By Age Demographic

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Patron Count by Age Demographic report. The report presents patron counts grouped by age demographic. This supports users who need age-based patron statistics.

### FR-080: Patron Count By County

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Patron Count by County report. The report presents patron counts grouped by county. This supports users who need patron statistics broken out by county.

### FR-081: Patron Count By Geography

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Patron Count by County, City, and Zip Code report. The report presents patron counts grouped by county, city, and zip code. This supports users who need geographic patron statistics across multiple location levels.

### FR-082: Patron Count By Profile Group

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Patron Count by Profile Group report. The report presents patron counts grouped by profile group. This supports users who need profile group-based patron statistics.

### FR-083: Patron Survey Answer Grouping

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide patron counts and lists grouped or filtered by survey answer. The system shall generate patron counts by survey answer and provide lists of patrons corresponding to specific survey answers. This supports users who need to review patron responses and associated patron details.

### FR-084: Voter Survey County By Week

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Voter Survey Responses County by Week report. The report presents voter survey response counts grouped by county and by week. This supports users who need weekly county-level visibility into voter survey responses.

### FR-085: Patron Expiration List

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a list of patrons by expiration date. The list identifies patrons and includes their expiration date. This supports users who need to find patrons approaching or having specific expiration dates.

### FR-086: Voter Registration Count By Week

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Voter Registration Survey Responses Count by Week report. The report presents voter registration survey response counts grouped by week. This supports users who need weekly trends for voter registration survey responses.

### FR-087: Barred Patrons List

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a list of patrons who are barred. The list identifies barred patrons for review and follow-up. This supports users who need to identify patrons subject to barred status.

### FR-088: Inactive Status Patron List

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a list of patrons with inactive status. The list identifies patrons whose status is inactive. This supports users who need to review patrons by inactive status.

### FR-089: Staff Accounts Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Staff Accounts report that includes the date of last password change and account expiration. The report shall be available for staff account records so users can review password history and expiration status. This supports monitoring of staff account access by providing both fields in a single report.

### FR-090: Patrons With Notes Wording

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a list of patrons whose notes contain specified wording. The list shall return patrons matching the wording condition within their notes. This allows users to find patrons based on note content.

### FR-091: Holds Purchase Alert Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Holds Purchase Alert report. The report shall present the holds purchase alert information in a dedicated report format. This supports users who need to review purchase-related hold alerts.

### FR-092: Items Sent for Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide an Items Sent for Holds report. The report shall list items that have been sent for holds. This enables users to review the outgoing status of held items.

### FR-093: Items Received for Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide an Items Received for Holds report. The report shall list items that have been received for holds. This enables users to review the received status of held items.

### FR-094: Unfilled Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide an Unfilled Holds report. The report shall identify holds that are unfilled. This supports users needing visibility into holds that have not been filled.

### FR-095: Stale Holds Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a Stale Holds report identifying holds left on the hold shelf awaiting pickup for too long. The report shall focus on holds that have been waiting beyond the stated too-long threshold. This supports users in locating and acting on stale shelf holds.

### FR-096: Detailed Aged Debt Report

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a detailed Aged Debt report for users who need aged debt details. The system shall support generating an aged debt detailed report output. Evidence indicates it may be partially available and needs enhancement, so the report shall be provided as part of the system’s capabilities.

### FR-097: Run Multiple Canned Reports

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall allow users to select multiple canned reports to run at the same time. The system shall display the results within one document for the selected reports. This supports combined viewing of multiple canned report outputs.

### FR-098: Report Title Descriptions With Tooltips

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide quick access to reports with descriptions available for report and template titles. The system shall show descriptions when users interact with report and template titles, using pop-up boxes. This lets users understand what a report or template does via the title descriptions.

### FR-099: Comparative Report Columns

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall support comparative report columns for current and prior month circulation, prior-year month circulation, and percentage differences. It shall present these columns within reports so users can compare circulation across time periods and view computed percentage differences.

### FR-100: Item Use Counts By Date

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide total item use counts and breakdowns by usage date ranges, including fiscal year and month. It shall allow users to obtain both overall item use totals and date-range-specific use counts for the requested periods.

### FR-101: Upload Report Filters

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall allow users to upload a text file containing identifiers such as barcodes or TCNs and use it as a report filter. It shall apply the uploaded identifiers to filter report results based on those identifier values.

### FR-102: Deleted Last-Copy Item Reports

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide reports of deleted items that were the last copy owned by the library system or the last copy in a facility. The reports shall cover items removed from the system. This shall allow use cases such as updating WorldCat based on the last-copy status.

### FR-103: Last Edit Date Field Separation

**Priority:** Medium  
**Sources:** `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`

The system shall provide a last edit date for item and bibliographic records. The last edit date shall update only when a record is edited. The last edit date shall be separate from the last circulation date.

### FR-104: Separate Last Circulation Date

**Priority:** Medium  
**Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall provide a separate last circulation date field on item records and reports. The system shall maintain last circulation date separately from other item dates on reports. This field shall be available for use in item reporting.

### FR-105: Separate Check-In And Renewal Timestamps

**Priority:** Medium  
**Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall store check-in event timestamps separately from renewal timestamps. The system shall produce check-in date and time reports that exclude renewals. This separation shall ensure renewal events do not appear as check-in time values.

### FR-106: Historical Bills Snapshot Report

**Priority:** Medium  
**Sources:** `evergreen_reference_2009.txt`, `survey_results_2009.txt`

The system shall provide a snapshot bills report showing bill states or billing information as of a past point in time. The report shall support viewing historical bill information. This shall allow bill details to be retrieved for prior moments in time.

### FR-107: Local Custom Reports For Workflows

**Priority:** Medium  
**Sources:** `survey_results_2009.txt`

The system shall support local and custom reports for collection development, program attendance tracking, and staff productivity. This allows users to define or use local/custom reporting that covers these operational areas. The system shall provide reporting capabilities tailored to these specific use cases.

### FR-108: Director-Level Financial Reports

**Priority:** Medium  
**Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide financial reports suitable for director-level use. This enables users at the director level to view financial information in an appropriate report format. The system shall generate financial reporting intended for that audience.

### FR-109: Cross-Branch Comparison Reporting

**Priority:** Medium  
**Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall provide reports and analysis comparing branches or selected groups of libraries. This allows users to compare information across multiple branches or library groups. The system shall support both reporting and analytical views for these comparisons.

### FR-110: Comprehensive Reporting Data Availability

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`

The system shall make available for reporting bibliographic, item, patron, circulation, hold, financial, and staff-account records and their documented relationships. This enables report generation across these record types while preserving the documented relationships between them. The system shall provide access to these datasets for use in reporting.

### FR-111: Scheduled Purge Utility

**Priority:** Low  
**Sources:** `conversations/conv_pines021_item_purging.eml`

The system shall allow the item purge and cleanup utility to run on a schedule. The utility shall be able to run automatically at a configured time such as at the end of each year.

### FR-112: Weeding Report Staff Template Constraints

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall allow front-line staff to set a call-number range for a weeding report. The system shall allow front-line staff to add or remove display fields from an approved picklist. The system shall prevent front-line staff from altering a template to display deleted items.

### FR-113: Circulation Count By Shelving Location

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Circulation Count by Shelving Location report. This report shall present circulation counts organized by shelving location. This supports analyzing circulation distribution across shelving locations.

### FR-114: Circulation By Patron Home Library

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Circulation Count by Circulation Location report broken down by patron home library. This enables circulation counts to be analyzed by the patron’s home library in the context of circulation locations.

### FR-115: Items Added List

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a list of items added. This list presents the items that have been added, as a report output for users to review.

### FR-116: Items Count Report

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide an Items Count report. This report outputs item counts for users to analyze.

### FR-117: Long Overdue Items Reporting

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall allow items to be marked long overdue and provide a report of long-overdue items by system. This supports marking items as long overdue and then generating a report showing long-overdue items grouped by system.

### FR-118: Items By Use Count Filters

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide reports listing items above or below a specified total use count for collection analysis and weeding. This includes generating a list of items with a greater than total use count and a list of items with a less than total use count for weeding.

### FR-119: Items By Creation Date Range

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`

The system shall provide a list of items by creation date range. This report filters items based on a creation date range so users can view items created within the selected window.

### FR-120: Patron Additions By Month Report

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Patron Added Count by Month report. The report shall show counts of patrons added for each month.

### FR-121: New Patron Count Previous Month

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a New Patron Count report showing patrons added in the previous month by demographic category. The report shall present the previous-month patron additions grouped by the demographic category.

### FR-122: IntraPINES Loans Reports Scope

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide IntraPINES Loans reports for all systems and facilities. The system shall also provide IntraPINES Loans reports by system and by facility. This allows users to view loan information across broad scope and by specific organization units.

### FR-123: Annual Holds Placed Count

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide an annual count of holds placed. The count shall be summarized on a year basis for holds that are placed. This allows users to track annual hold placement volume.

### FR-124: Non-Cataloged In-House Use Count

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Non-Cat In House Use Count by Month report. The report shall present non-cataloged in-house use counts grouped by month. This allows users to review monthly usage trends for non-cataloged in-house activities.

### FR-125: Cataloged In-House Use Count Report

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Cataloged In House Use Count report for users who need to view in-house use counts. The report shall be available as a distinct canned report output. This supports recurring reporting needs as described for canned reports.

### FR-126: Detailed Alternative Payments Report

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Detailed Forgive, Work, and Goods Payments Received report for users who need to review detailed payment categories. The system shall generate the report as a dedicated report output. This report shall reflect the named payment types included in its title.

### FR-127: Detailed Voids Report

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide a Detailed Voids report for users who need a detailed view of voids. The system shall make the report available as a dedicated report output. The report content shall correspond to the titled “Detailed Voids”.

### FR-128: Edit Recurring Report Selections

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall allow users to edit recurring reports. Editing shall include changing report selections by adding or removing selected reports. The system shall also allow users to edit the email delivery addresses associated with those recurring reports.

### FR-129: Notice Type Reports

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall provide reports for pre-overdue notices, overdue notices, and holds notices sent. It shall generate report outputs corresponding to each notice type.

### FR-130: Transaction Reports Date Time Filters

**Priority:** Low  
**Sources:** `early_draft_srs_galecia.txt`

The system shall allow reports to filter transactions by a specific date and time. The system shall also allow filtering by workstation. The system shall also allow filtering by staff member.

## Non-functional requirements

### NFR-001: Consortium Scale Capacity Support

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall support a consortium scale with 286 locations. The system shall support 17 million annual circulations and purchasing and processing over 900,000 items per year.

### NFR-002: Open Hours Report Queuing

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall allow searches and reports to run during open hours without disrupting other system functions, including circulation and OPAC access. The system shall queue reports for background processing and separate reporting workload from production operations to avoid impacting the production database and live functions.

### NFR-003: Web And Windows Client Access

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall be accessible through a web browser or a Windows-compatible client. If browser-based, it shall support Microsoft Internet Explorer 6.0 and later and Mozilla Firefox 2.0 and later.

### NFR-004: Assistive Technology And Section 508

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall support screen readers, screen magnification, and other assistive technologies, including JAWS, NVDA, and ZoomText, and comply with Section 508 accessibility standards. Reporting interfaces shall be accessible, and web output shall include alternative text, ARIA labels, and semantic HTML structure.

### NFR-005: Standards-Compliant HTML Validation

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall produce standards-compliant HTML for web interfaces, help, and report output. HTML output shall validate against W3C standards.

### NFR-006: Immediate Financial Information Updates

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall allow financial information to be updated easily. It shall reflect front-desk payments immediately after a patron makes a payment at the front desk. The system shall keep financial information current based on those updates.

### NFR-007: Complete And Current Data Across Locations

**Priority:** High  
**Sources:** `meeting_tech_subcommittee_2009-06-30.txt`

The system shall ensure data from all locations is complete and current. This requirement applies to the data available for reporting across multiple locations. The system shall maintain the stated completeness and currency for location data.

### NFR-008: Large Transfer Processing

**Priority:** Medium  
**Sources:** `conversations/conv_pines018_item_transfer.eml`

The system shall process large item transfers efficiently, including transfers at the scale of 9.6 million items. It shall use smaller sub-batches to avoid database locking during batch updates.

### NFR-009: Report Performance During Busy Hours

**Priority:** Medium  
**Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`

The system shall provide acceptable report performance during busy hours and reliable, tested report output. This means the system shall return report results within an acceptable performance level when usage is high, and shall produce output that has been tested and proven. The system shall support dependable reporting behavior for users who run reports under these conditions.

### NFR-010: Excel Export Deduplication Support

**Priority:** Medium  
**Sources:** `survey_results_2009.txt`

The system shall produce Excel exports without excessive duplicate rows or provide an option to deduplicate exported data. This applies when users export report data to Excel. The system shall either prevent excessive duplicates in the export or offer a deduplication option for the exported data.

### NFR-011: Report Search And Run Usability

**Priority:** Medium  
**Sources:** `survey_results_2009.txt`

The system shall provide a user interface that makes it easy to find and run reports. This supports users who need to locate specific reports and execute them through the interface. The system shall present report finding and running in a way that avoids user difficulty in accessing needed reports.

## Constraints

### CON-001: Linux Or Solaris Server Platforms

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

The system shall operate on Linux or Solaris servers. This includes the stated Linux RHEL 5 and Solaris 10 on SPARC environments.

### CON-002: Relational Database Backend Compatibility

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall use and operate with the existing fully relational database structure. The system shall be compatible with PostgreSQL 8.3 and not require denormalized reporting schemas.

### CON-003: Management Reporting Processes Scope

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall support management reporting and analysis for collection use, branch capacity and collection distribution, patron demographics and interests, staff productivity and workflow, and financial transactions. The system shall not manage acquisitions or cataloging, constrain OPAC functionality, or provide day-to-day patron-facing functions.

### CON-004: Centralized Multi-Location Reporting

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system shall be consolidated centrally and accept input from and provide services to multiple locations. The system shall provide consistent reporting across those locations.

### CON-005: Archived Transaction Data Anonymization

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_report_features.eml`, `survey_results_2009.txt`

The system shall anonymize archived transaction data by deleting information that could identify a patron. The system shall protect patron privacy in accordance with State Law. The system shall retain useful demographic statistics for reporting.

### CON-006: Transaction History Retention Policy

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `survey_results_2009.txt`

The system shall retain detailed transaction history for a configurable number of days. It shall also retain monthly and annual transaction aggregates indefinitely. The system shall make the retained historical transaction data available for reporting.

### CON-007: Financial Reporting And Archiving Compliance

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `email_financial_reports.eml`

The system shall ensure that reports and data archiving comply with standard accounting practice. It shall also comply with applicable state, county, and municipal auditing requirements. The system shall apply these compliance requirements to both generated reports and archived data.

### CON-008: Data Specifications And Dictionaries

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system project shall provide complete data specifications and data dictionaries for authority records, bibliographic records, order records, item records, hold/request records, and other records used by Management Processes. The data dictionaries shall include field names, data types, and relationships. This deliverable shall cover the records maintained or accessed by Management Processes.

### CON-009: Process Descriptions Deliverable

**Priority:** High  
**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

The system project shall provide high-level descriptions of major processes including bibliographic record import and export. The system project shall also include high-level descriptions of authority validation against internal and external authority sources. The system project shall additionally describe standard report processes.

## Discarded requirements (blacklist)

Candidates that were found in the inputs but left out of the specification, with the reason.

### DR-001: Trigger-Based Deletion Logging

**Sources:** `conversations/conv_pines022_deletions.eml`  
**Statement:** The system shall implement a database trigger that logs deletions to an audit table.  
**Reason:** Discarded as an implementation prescription; the Deletion Audit Tracking requirement specifies the needed audit capability without mandating a database trigger.

### DR-002: Age Calculation Implementation

**Sources:** `conversations/conv_pines023_patron_characteristics.eml`  
**Statement:** The system shall calculate age range at query time from the birth_date field by creating query age brackets.  
**Reason:** Discarded as an implementation detail. The Patron Characteristics in Reports requirement captures configurable age ranges without prescribing how they are calculated.

### DR-003: Null Inclusion Choice

**Sources:** `conversations/conv_pines023_patron_characteristics.eml`  
**Statement:** The system shall let users choose whether reports include or exclude records with null values.  
**Reason:** The later decision requiring null values in report results wins; the conflicting choice to exclude nulls is discarded.

### DR-004: Project Scope and Process Items

**Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`  
**Statement:** The system shall document optimal report functionality, compile report lists, gather requirements, route development through a testing group, hold meetings, circulate and draft specification documents, and use an iterative methodology.  
**Reason:** These candidates describe project governance, meetings, specification writing, review, or development process rather than system behavior.

### DR-005: Scope and Priority Process

**Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`  
**Statement:** The system shall treat selected requirements as high priority for KCLS, adapt a draft specification, or specify requirements only within a particular scope.  
**Reason:** These are project prioritization, document-development, or scoping directions, not system requirements.

### DR-006: Data Specifications as System Feature

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide complete data specifications and process descriptions.  
**Reason:** These are specification or documentation deliverables, not runtime system behavior; they are represented as project deliverables only where appropriate.

### DR-007: Report Permission Administration Duplicate

**Sources:** `email_report_features.eml`  
**Statement:** The system shall provide easy-to-administer report permissions.  
**Reason:** Merged into the Access Control and Template Use Permissions requirements; no separate capability is needed.

### DR-008: Period-Specific Retention

**Sources:** `email_financial_reports.eml`  
**Statement:** The system shall retain specified audit data for seven years where required.  
**Reason:** The candidate is a proposal with an unsupported fixed period; the applicable audit compliance requirement does not specify a seven-year retention period.

### DR-009: Transaction Retention Period

**Sources:** `email_report_features.eml`  
**Statement:** The system shall retain transaction data for X years to comply with State Law.  
**Reason:** The later decision specifying configurable raw-history retention in days and indefinite monthly and annual aggregates wins; the unspecified years-based proposal is discarded.

### DR-010: Current-System Capability Statements

**Sources:** `evergreen_reference_2009.txt`  
**Statement:** The system shall provide features already stated as existing, including report writer, drag-and-drop fields, basic filters and sorting, saved definitions, existing canned reports, and existing record types and relationships.  
**Reason:** These candidates describe existing-system facts rather than new requirements. New requirements for enhanced capabilities are retained separately.

### DR-011: System Configuration Dependencies

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall depend on undocumented configurations or unspecified attachments as specific functionality.  
**Reason:** Discarded where the candidate supplies no requirement detail beyond a reference to an absent appendix or unspecified configuration; no numbers or behavior can be invented.

### DR-012: Capacity Metrics Decision Process

**Sources:** `conversations/conv_pines015_capacity_interface.eml`  
**Statement:** The system shall have the specific metrics that define capacity decided before building the capacity interface.  
**Reason:** This specifies a project decision that must precede construction, rather than system behavior; the Branch Capacity Overview requirement captures the capacity metrics supported by the system.

### DR-013: Transfer Coordinator Authorization

**Sources:** `conversations/conv_pines018_item_transfer.eml`  
**Statement:** The system shall restrict item transfers to designated roles such as managers, administrators, and transfer coordinators.  
**Reason:** The Transfer Authorization decision restricts transfer initiation to managers and administrators. That decision wins over this earlier proposal, which additionally names transfer coordinators.

### DR-014: General Technical Constraints

**Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`  
**Statement:** The system shall accommodate technical constraints including server operating system choices and supported browsers.  
**Reason:** This proposal adds no specific technical constraint beyond the Server Operating Systems and Client Access requirements, which state the supported environments and browsers.

### DR-015: Items Edited Count Report

**Sources:** `early_draft_srs_galecia.txt`, `evergreen_reference_2009.txt`  
**Statement:** The system shall provide an Items Edited Count report.  
**Reason:** The Items Edited Count report appears only in proposal-level candidates, with no decision or other evidence establishing it as an agreed need.

### DR-016: Appendix Reporting Definitions

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall support the reporting definitions described in Appendix A and the fine-grained reporting requirements described in Appendix B.  
**Reason:** The requirement depends on reporting definitions in attached appendices that are not present in the available sources. Without those concrete definitions, the behavior is unsupported and cannot be tested.

### DR-017: Unresolved Appended Report Definitions

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall support reporting definitions described in attached appendices.  
**Reason:** The requirement depends on reporting definitions in attached appendices that are not present in the available sources. Without those concrete definitions, the behavior is unsupported and cannot be tested.

### DR-018: Checkout Count Report

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Checkout Count report containing checkouts only.  
**Reason:** The Checkout Count report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-019: Non-Cataloged Count Report

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Non-Cat Count report.  
**Reason:** The Non-Cataloged Count report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-020: Items Added Count Report

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide an Items Added Count report.  
**Reason:** The Items Added Count report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-021: Currently Checked-Out Items

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a report of items currently checked out.  
**Reason:** The Items Currently Checked Out report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-022: Bibliographic Record Counts

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Bib Records Count report.  
**Reason:** The Bib Records Count report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-023: Patron Count Report

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Patron Count report.  
**Reason:** The Patron Count report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-024: Patron Count by Home Library

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Patron Count by Home Library report.  
**Reason:** The Patron Count by Home Library report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-025: Bills Currently Owed Report

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Bills Currently Owed by Patrons report.  
**Reason:** The Bills Currently Owed by Patrons report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-026: Detailed Payments Received Report

**Sources:** `early_draft_srs_galecia.txt`  
**Statement:** The system shall provide a Detailed Payments Received report.  
**Reason:** The Detailed Payments Received report is identified in the existing-system facts as an existing canned report. This requirement specifies no new or changed behavior.

### DR-027: Patron Report Access

**Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`  
**Statement:** The system shall allow patrons to access reports only indirectly through OPAC displays, including reports displayed on screens at libraries.  
**Reason:** The Management Processes Scope requirement excludes day-to-day patron-facing functions, and the available facts support querying OPAC data for reporting—not patron access to management reports through OPAC displays. Therefore, patron-facing report access is outside the supported scope.

