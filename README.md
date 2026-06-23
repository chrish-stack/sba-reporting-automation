# SBA Reporting Automation

Public planning/code repo for the Santa Barbara / Visit Santa Barbara reporting automation project.

## Current goal

Build a local-first reporting automation pipeline that the SBA reporting owner can run on their own computer.

The first official deliverable is a pull-and-staging assistant:

1. Ingest manually exported platform files first, then support APIs once access is confirmed.
2. Validate that the pull/export has the right date range, platform, granularity, and columns.
3. Normalize columns across platforms.
4. Parse campaign, ad set, ad name, platform, audience, objective, pillar, placement, and month.
5. Apply embedded Santa Barbara reporting rules.
6. Output a clean CSV/table ready for the existing weekly reporting sheet and pivot tables.
7. Optionally generate an AI insight prompt/draft using the user's own OpenAI/Claude API key.

This is not a full hosted platform at the start. The best first version is a handoff-friendly local pipeline: raw exports in, validated/staged weekly reporting files out.

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

## v0.01 local build

v0.01 can normalize an `All Data - Weekly` CSV export into a clean weekly-sheet-ready CSV plus validation flags.

Run from the repo root:

```bash
PYTHONPATH=src python -m sba_reporting.cli normalize \
  --input "data/raw/google-sheet-examples-2026-06-23/SBA - Weekly Reporting 2025_26 - All Data - Weekly.csv" \
  --output-dir "outputs/v0.01-smoke"
```

Generated files:

- `weekly_sheet_ready.csv` — normalized rows in the canonical weekly reporting column order.
- `flags_review.csv` — row-level warnings and alias normalizations for human review.
- `validation_report.md` — plain-English run summary with counts and issue rollups.

Current v0.01 behavior:

- Skips fiscal-year marker rows like `FY25/26`.
- Skips incomplete placeholder rows that have a date but no ad identity fields.
- Preserves the blank 26th source column as `Manual Notes`.
- Normalizes known aliases like `Youtube` -> `YouTube`, `Co op`/`Co Op` -> `Co-Op`, and `Norcal` -> `NorCal`.
- Flags source `#DIV/0!` formula errors instead of silently trusting them.

Run tests:

```bash
PYTHONPATH=src python -m pytest -q
```

## Next input needed from accounting/reporting team

See `docs/intake-questions.md`.
