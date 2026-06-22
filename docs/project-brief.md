# Santa Barbara Reporting Automation Brief

Created: 2026-06-22

## Working problem

The Santa Barbara / Visit Santa Barbara weekly paid-media reporting workflow is still heavily manual. The team exports ad-level data from multiple platforms, cleans it in Excel, adds missing classification fields, imports it into a weekly Google Sheet, then uses pivot tables to identify top-performing ads by platform, audience, campaign, and objective.

The weekly process is estimated at 2.5 to 3 hours every Tuesday, using previous Monday through Sunday data.

The current working file is `SBA - Weekly Reporting 2024/25`, where raw platform data is added and pivot tables drive insights.

## Platforms mentioned

Weekly paid exports currently include:

- Meta
- Pinterest
- YouTube
- TikTok
- Reddit
- NextDoor

The exports are pulled at the Ads level, so the automation needs ad-name-level detail.

## Why automation failed before

The issue is not just data access. TapClicks already contains most platform data.

The failure point is classification.

Business logic lives inside campaign names, ad set names, ad names, manual Excel cleanup, Google Sheet formulas, and pivot-table conventions. The same ad can appear across multiple audiences, months, pillars, and objectives, so simple mapping inside TapClicks has produced confusing output.

Known blockers:

- Same ad names reused across audiences.
- Audience, pillar, month, objective, and placement data embedded in naming strings.
- Meta Brand Traffic requires special cleanup.
- Month-overlap reporting weeks require manual ad-name changes.
- Google Analytics / website-performance data is combined manually.
- Some metrics are calculated in spreadsheets, not native platform exports.

## First automation target

Build a local pull-and-staging pipeline, not a hosted platform or report redesign.

Initial pipeline:

1. Ingest raw platform export files manually at first.
2. Validate date range, platform, export level, and required columns.
3. Normalize column names across platforms.
4. Parse campaign/ad set/ad name fields.
5. Assign clean values for platform, campaign, audience, objective, pillar, placement, and month.
6. Apply platform-specific rules.
7. Output a cleaned table that matches the current weekly Google Sheet structure.
8. Let the existing pivot tables and ChatGPT-assisted review continue until the cleaned pull/staging layer is trusted.

Later, once the export-to-output path is validated, add API pulling through TapClicks/platform APIs and optional AI insight generation using the team's own API keys.

## Rules captured so far

### Meta

- Classify most Meta ads as `Facebook` unless the ad group/ad set name specifically says IG-only.
- If name includes `FB+IG`, classify as `Facebook`.
- Meta retainer ads include:
  - Monthly Traffic
  - Direct Response
- Meta Brand Traffic is special:
  - Pillar names should be removed from the audience field.
  - Pillar names should remain attached to the ad name when relevant.
  - FB and IG placements need separation when applicable.

### YouTube

- YouTube exports extra fields even with custom weekly columns selected.
- Strip unnecessary fields early.
- YouTube completion counts need calculation because the export provides percentages.
- Current manual formula:
  - `Views * Views to %`

### Month overlap

When a reporting week crosses two months, previous-month ads need the month appended to the end of the ad name so spend/results do not blend in the pivot table.

Example from the how-to doc:

- Reporting week: `2/24/25 - 3/2/25`
- February ads need `- February` appended to the ad name.

## Insight logic to preserve

Weekly insights focus on cost efficiency by objective:

- Awareness campaigns: CPM
- Traffic campaigns: CPC
- Video campaigns: CPM Views to 100%

Traffic campaigns also require budget-hog detection: ads/ad sets consuming spend without strong efficiency should be flagged.

## Recommended phased build

### Phase 1: Proof of concept

Start with one controlled case:

- Meta > Brand > Luxury Drive
- One clean week
- One messy/edge-case week

Success means the cleaned output matches the manual final spreadsheet rows.

### Phase 2: Rules engine

Create a mapping config that stores:

- Approved audience names
- Known campaign names
- Known objectives
- Known pillars
- Known platforms
- Month naming rules
- Placement rules
- Platform-specific metric mappings

Use deterministic rules first. AI can help classify edge cases later, but it should not guess the core mappings every week.

### Phase 3: Google Sheet output

Output cleaned rows directly into the existing raw-data tab shape.

Do not touch the pivot tables until the clean-data layer is validated.

### Phase 4: GA4/site data

Add GA4/site-performance matching after paid-platform export normalization works.

Likely join keys to investigate:

- Ad name
- Campaign
- Audience
- Date range
- Landing page / referral path
- UTM campaign
- UTM content

Stronger UTM discipline is likely the clean future-state solution.
