# Weekly Sheet Schema Notes

Source reviewed: exported Google Sheets PDF `SBA - Weekly Reporting 2025/26` and screenshots of the Google Sheet tabs.

Do not commit the raw PDF, screenshots, spreadsheets, platform exports, API credentials, or live client data to this public repo. This file captures public-safe structural notes only.

## Workbook tabs visible

Visible tabs from screenshots:

- `All Data - Weekly`
- `Monthly Data`
- `Audiences`
- `Weekly`
- `Campaigns`
- `Ad per Audience`

## `All Data - Weekly` raw/staged data tab

This appears to be the primary table the local pipeline should generate first.

Visible columns:

1. `Date`
2. `Platform`
3. `Campaign`
4. `Ad Name`
5. `Audiences`
6. `Goal`
7. `Cost`
8. `Impressions`
9. `Reach`
10. `Pin Clicks / Link Clicks`
11. `Video Plays at 50%`
12. `Video Plays at 75%`
13. `Video Plays at 100%`
14. `Outbound Clicks / LPVs`
15. `Cost per Session`
16. `Google Sessions`
17. `Non-Bounced Sessions (Engaged Sessions)`
18. `Cost Per Non-Bounced Session (Cost per engaged user)`
19. `Google Conversions`
20. `Cost Per Conversion`
21. `Time on Site (engaged time)`
22. `Bounce Rate (Engagement Rate)`
23. `Pages Per Session (Engaged session per user)`
24. `Web Referral`
25. `Cost Per Web Referral`

Observed structure:

- Header row is frozen/filterable.
- There is an `FY25/26` marker row before data.
- Rows are ad-level records by week.
- `Date` values use weekly ranges like `7/1/25-7/6/25`.
- `Platform` includes `Facebook`, `Instagram`, and other platform tabs/exports later.
- `Campaign` includes families such as `Brand`, `Co-Op`, `Retainer`, `Retail`.
- `Goal` includes `Awareness`, `Video Views`, `Traffic`, `Direct Response`.
- Awareness/video rows often have paid-platform metrics but blank site/Google metrics.
- Traffic/direct-response rows often have Google/site metrics and calculated efficiency columns.

## `Monthly Data` tab

This appears to use the same schema as `All Data - Weekly`, but the date range is monthly.

Visible example:

- `Date` range like `1/1/25-1/31/25`.
- Same column family: Date, Platform, Campaign, Ad Name, Audiences, Goal, Cost, Impressions, Reach, clicks, video metrics, outbound clicks/LPVs, Google/site metrics, referral metrics.

Automation implication:

- Build one canonical normalized schema that can support both weekly and monthly outputs.
- Weekly and monthly differ mainly by date range and aggregation/pull period, not by column family.

## Pivot/report tabs

The screenshots show pivot-style tabs that summarize the raw/staged data:

### `Ad per Audience`

Visible row dimensions:

- Date
- Platform
- Goal
- Audiences
- Ad Name

Visible value columns:

- SUM of Cost
- SUM of Impressions
- SUM of Reach
- SUM of Pin Clicks / Link Clicks
- SUM of Video Plays at 50%
- SUM of Video Plays at 100%
- SUM of Outbound Clicks / LPVs
- SUM of Google Sessions
- COUNTA of Platform
- Frequency
- CPM
- CPC
- AVERAGE of CPM Views to 50%
- AVERAGE of CPM Views to 100%
- CPLPV
- Cost per session

Automation implication:

- The local assistant does not need to rebuild this pivot first.
- It must output raw/staged rows that make this pivot compute correctly.
- Later, it can reproduce the pivot as a generated summary CSV for validation.

### `Audiences`

Visible row dimensions:

- Audiences
- Platform
- Campaign
- Goal

Visible value/calculated columns:

- SUM of Cost
- SUM of Impressions
- SUM of Reach
- SUM of Pin Clicks / Link Clicks
- SUM of Video Plays at 50%
- SUM of Video Plays at 100%
- SUM of Outbound Clicks / LPVs
- Frequency
- CPM
- CPC
- AVERAGE of CPM Views to 50%
- AVERAGE of CPM Views to 100%
- CPLPV

Automation implication:

- Audience normalization is a primary business-rule requirement.
- Unknown or unexpected audience names should be flagged, not guessed.

### `Weekly`

Visible row dimensions:

- Date
- Platform
- Goal
- Audiences
- Campaign

Visible value/calculated columns:

- SUM of Cost
- SUM of Impressions
- SUM of Reach
- SUM of Pin Clicks / Link Clicks
- SUM of Video Plays at 50%
- SUM of Video Plays at 100%
- SUM of Outbound Clicks / LPVs
- Frequency
- CPM
- CPC
- AVERAGE of CPM Views to 50%
- AVERAGE of CPM Views to 100%
- CPLPV

Automation implication:

- The first validation report should compare weekly totals by Date + Platform + Goal + Audience + Campaign.

### `Campaigns`

Visible row dimensions:

- Date
- Goal
- Platform
- Audiences
- Campaign

Visible value/calculated columns:

- SUM of Cost
- SUM of Impressions
- SUM of Reach
- SUM of Pin Clicks / Link Clicks
- SUM of Video Plays at 50%
- SUM of Video Plays at 100%
- SUM of Outbound Clicks / LPVs
- Frequency
- CPM
- CPC
- AVERAGE of CPM Views to 50%
- AVERAGE of CPM Views to 100%
- CPLPV

Automation implication:

- Campaign names must be normalized into stable campaign families before this pivot can be trusted.

## Calculated metric formulas to implement/validate

Likely formulas based on visible columns and values:

- `Frequency = Impressions / Reach`
- `CPM = Cost / Impressions * 1000`
- `CPC = Cost / Pin Clicks or Link Clicks`
- `CPM Views to 50% = Cost / Video Plays at 50% * 1000`
- `CPM Views to 100% = Cost / Video Plays at 100% * 1000`
- `CPLPV = Cost / Outbound Clicks or LPVs`
- `Cost per Session = Cost / Google Sessions`
- `Cost Per Non-Bounced Session = Cost / Non-Bounced Sessions`
- `Cost Per Conversion = Cost / Google Conversions`
- `Cost Per Web Referral = Cost / Web Referral`

Guardrail:

- Blank or zero denominators should produce blank/flagged values rather than noisy `#DIV/0!` in generated outputs.

## First implementation implication

The first real code should define this canonical row schema and validation rules before platform-specific parsing gets too complex.

Recommended first code tasks:

1. Define `WeeklyRecord` schema with the 25 visible columns above.
2. Define required vs optional metrics by `Goal`.
3. Build CSV/XLSX ingestion for an export matching this schema.
4. Generate validation report for missing columns, bad date ranges, unknown platforms/campaigns/audiences/goals, and zero-denominator formulas.
5. Generate a cleaned `weekly_sheet_ready.csv` in the same column order.
6. Generate pivot-style validation summaries for weekly totals.
