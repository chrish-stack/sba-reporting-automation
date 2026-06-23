# CSV Data Profile

Source: `SBA - Weekly Reporting 2025_26 - All Data - Weekly.csv`

This file captures public-safe aggregate/profile notes only. Do not commit the raw CSV to this public repo.

## Ingest summary

- Encoding: `utf-8-sig`
- Rows including header: 9,926
- Data rows: 9,925
- Non-empty data rows: 9,925
- Columns: 26
- Every row has 26 columns.

The first 25 columns match the reporting schema captured in `docs/weekly-sheet-schema.md`. The 26th column has a blank header and appears to contain manual notes/comments in some rows.

## Header row

```text
Date
Platform
Campaign
Ad Name
Audiences
Goal
Cost
Impressions
Reach
Pin Clicks /Link Clicks
Video Plays at 50%
Video Plays at 75%
Video Plays at 100%
Outbound Clicks / LPVs
Cost per Session
Google Sessions
Non-Bounced Sessions (Engaged Sessions)
Cost Per Non-Bounced Session (Cost per engaged user)
Google Conversions
Cost Per Conversion
Time on Site (engaged time)
Bounce Rate (Engagement Rate)
Pages Per Session (Engaged session per user)
Web Referral
Cost Per Web Referral
[blank header / notes column]
```

Important mismatch to normalize:

- CSV header uses `Pin Clicks /Link Clicks` with no space after `/`.
- Earlier visual notes used `Pin Clicks / Link Clicks`.
- The pipeline should accept both spellings and output the canonical name.

## Date ranges

- Unique nonblank Date values: 52
- First row marker includes `FY25/26` in the Date column.
- Weekly ranges include mixed formatting, for example:
  - `7/1/25-7/6/25`
  - `1/26/26-2/1/26`
  - `3/30/26 - 4/05/26`

Automation implications:

- Date-range parser must tolerate spaces around `-`.
- Date parser must tolerate zero-padded and non-zero-padded month/day values.
- `FY25/26` should be treated as a marker row, not a data row.

## Platform values

Top observed platform values:

- Facebook: 7,526
- Pinterest: 791
- TikTok: 599
- Instagram: 575
- Reddit: 211
- Youtube: 133
- NextDoor: 59
- YouTube: 29

Automation implications:

- Normalize `Youtube` and `YouTube` to one canonical value, likely `YouTube`.
- Keep `NextDoor` casing consistent.

## Campaign values

Top observed campaign values:

- Brand: 6,563
- Air Services: 965
- Weddings: 806
- Retail: 716
- Retainer: 191
- FIFA: 188
- Episodic: 178
- Locals: 99
- Co-Op: 75
- Compression: 50
- Air Service: 36
- Co op: 29
- HIT: 24
- Co Op: 3

Automation implications:

- Normalize `Co-Op`, `Co op`, and `Co Op`.
- Decide whether `Air Service` should normalize to `Air Services`.
- Treat campaign values as controlled vocabulary with warnings for unknowns.

## Goal values

Observed goal values:

- Traffic: 6,756
- Awareness: 2,394
- Video Views: 717
- Direct Response: 54
- eNewsletter: 1
- In State: 1

Automation implications:

- `Traffic`, `Awareness`, `Video Views`, and `Direct Response` are expected core values.
- `eNewsletter` and `In State` should be reviewed. `In State` may be a misplaced audience value rather than a valid goal.

## Audience values

Top observed audience values:

- SoCal: 1,655
- NorCal: 1,104
- In State: 1,040
- OOS: 979
- Luxury Drive: 909
- Out of State: 693
- High HHI: 603
- California: 394
- High Intent Travelers: 333
- Major Domestic Airports: 322
- All Zip Codes: 291
- Website Visitors: 273
- Spanish: 210
- Engaged Audience: 111
- South Coast Cities: 91
- Retargeting: 85
- Desert States: 71
- NorCal+Reno: 64
- PNW: 48
- In-State (incl. Luxury Drive): 42
- Soccer Interest Audience: 42
- MT North: 32
- Chicago: 30
- HIT: 29
- Norcal: 25

Automation implications:

- Normalize case variants such as `NorCal` vs `Norcal`.
- Preserve specific compound audiences such as `In-State (incl. Luxury Drive)` unless the team confirms a split/rollup rule.
- Audience controlled-vocabulary config is required early.

## Formula/error fields

Observed `#DIV/0!` counts in the CSV:

- Cost per Session: 85
- Cost Per Non-Bounced Session: 253
- Cost Per Conversion: 99
- Cost Per Web Referral: 970

Automation implications:

- Generated outputs should avoid emitting `#DIV/0!` where possible.
- Prefer blank value plus a validation warning when the denominator is zero or missing.
- Preserve source value in raw/staging if comparing against existing sheet exports.

## Notes/comments column

The CSV has a 26th column with a blank header.

- Nonblank rows in this column: 296
- Example note types include pause instructions, UTM issue comments, performance flags, and manual review notes.

Automation implications:

- Add optional `Notes` or `Manual Notes` field to the internal schema.
- Do not discard this column during ingestion.
- Do not rely on this column for deterministic calculations unless specific rule patterns are approved.

## Recommended next implementation tasks

1. Create canonical schema with 25 required reporting columns plus optional `Manual Notes`.
2. Add header alias mapping for minor variants such as `Pin Clicks /Link Clicks`.
3. Add date-range parser that skips fiscal-year marker rows.
4. Add controlled-vocabulary checks for Platform, Campaign, Goal, and Audience.
5. Add normalization aliases for known variants:
   - `Youtube` -> `YouTube`
   - `Norcal` -> `NorCal`
   - `Co op` / `Co Op` -> `Co-Op`
   - candidate: `Air Service` -> `Air Services`
6. Add formula-error validator for `#DIV/0!` and zero-denominator cases.
7. Generate a profile/validation report before transforming platform-specific raw exports.
