# Local Handoff Plan

## Recommended product shape

Build this as a local reporting pipeline first.

The SBA reporting owner should be able to keep a project folder on their computer, drop weekly exports into an input folder, run the assistant, and receive clean weekly reporting outputs.

This avoids hosting, user management, IT approval, and cloud storage of sensitive client exports while still giving the team a path toward deeper API automation later.

## User-facing workflow

1. Export the weekly files from the required platforms or TapClicks.
2. Put the files into a dated local input folder.
3. Run the SBA Reporting Assistant.
4. Review the validation report and flags file.
5. Use the generated weekly-sheet-ready CSV in the existing Google Sheet workflow.
6. Optionally use the generated AI prompt or AI insight draft.

## Target local folder shape

```text
SBA Reporting Assistant/
  00_READ_ME_FIRST.md
  01_Input_Exports/
  02_Outputs/
  03_Config/
  04_Archive/
  app/
  setup.bat
  run_sba_report.bat
```

## Output package per reporting week

```text
02_Outputs/YYYY-MM-DD_to_YYYY-MM-DD/
  01_validation_report.md
  02_weekly_sheet_ready.csv
  03_flags_review.csv
  04_ai_insight_prompt.md
  05_ai_insight_draft.md
  06_run_log.txt
```

## Configuration model

Keep business rules visible and editable through config files where possible:

- known audiences
- known campaigns
- known objectives
- known pillars
- platform column mappings
- metric thresholds
- month-overlap rules
- AI provider/model selection

API keys and credentials must stay local only. Use `.env` or an encrypted settings store later. Never commit real keys.

## Development sequence

1. Meta-only proof of concept using one clean week and one messy week.
2. Validate automated output against manually cleaned output.
3. Add Meta edge-case rules.
4. Add YouTube cleanup and completion-count calculations.
5. Add other paid platforms one at a time.
6. Add optional AI insight generation.
7. Add API pulling only after manual-export normalization is trusted.

## Handoff principle

The team should not need to understand Python, GitHub, or AI prompts to run the first version. The tool should explain problems in plain English and fail safely when required files or columns are missing.
