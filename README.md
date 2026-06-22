# SBA Reporting Automation

Private working repo for the Santa Barbara / Visit Santa Barbara reporting automation project.

## Current goal

Build a lightweight data normalization pipeline that turns raw weekly paid-media exports into a clean table matching the existing `SBA - Weekly Reporting 2024/25` Google Sheet structure.

This is not a full report redesign. The first win is to preserve the current workflow while removing the repetitive manual cleanup:

1. Import raw platform exports.
2. Normalize columns across platforms.
3. Parse campaign, ad set, ad name, platform, audience, objective, pillar, placement, and month.
4. Apply platform-specific rules.
5. Output a clean CSV/table ready for the weekly reporting sheet and existing pivot tables.

## Source context captured so far

- Shared ChatGPT thread: https://chatgpt.com/share/6a39877a-2c14-83ea-8487-3b3b7df2edf4
- Local how-to PDF: `C:/Users/chris/OneDrive/Desktop/How To_ Santa Barbara Reports.pdf`
- Canonical Obsidian project note: `G:/My Drive/Chris - Obsidian Brain/projects/santa-barbara-reporting-automation/santa-barbara-reporting-automation.md`

Do not commit client exports, credentials, API keys, screenshots with account identifiers, or downloaded report data unless intentionally sanitized.

## First proof-of-concept scope

Start with one controlled case:

- Platform: Meta
- Campaign family: Brand
- Audience/example: Luxury Drive
- Test weeks:
  - Clean week: one month, normal naming, no overlap.
  - Messy week: month overlap, repeated ad names, multiple audiences, pillar names included.

Success means the automated output matches the manually cleaned rows Taylor/JLP would paste into the weekly report.

## Planned structure

```text
src/sba_reporting/       # parser and normalization code
configs/                 # rules, mappings, known audiences/campaigns/objectives
samples/                 # sanitized sample fixtures only
outputs/                 # generated local outputs, ignored by git
docs/                    # project brief, questions, working notes
tests/                   # parser and fixture tests
```

## Next input needed from accounting/reporting team

See `docs/intake-questions.md`.
