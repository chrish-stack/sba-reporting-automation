from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .config import ReportingRules
from .schema import (
    CANONICAL_COLUMNS,
    FORMULA_COLUMNS,
    OPTIONAL_NOTES_COLUMN,
    OUTPUT_COLUMNS,
    RowIssue,
)
from .summaries import write_summaries

_DATE_RANGE_RE = re.compile(
    r"^\s*(\d{1,2})/(\d{1,2})/(\d{2,4})\s*-\s*(\d{1,2})/(\d{1,2})/(\d{2,4})\s*$"
)

@dataclass
class NormalizationResult:
    input_path: Path
    output_dir: Path
    rows_read: int = 0
    rows_written: int = 0
    skipped_marker_rows: int = 0
    issues: list[RowIssue] = field(default_factory=list)
    platform_counts: Counter[str] = field(default_factory=Counter)
    campaign_counts: Counter[str] = field(default_factory=Counter)
    goal_counts: Counter[str] = field(default_factory=Counter)
    audience_counts: Counter[str] = field(default_factory=Counter)
    alias_counts: Counter[str] = field(default_factory=Counter)
    summary_paths: dict[str, Path] = field(default_factory=dict)
    normalized_rows: list[dict[str, str]] = field(default_factory=list)

    @property
    def output_csv(self) -> Path:
        return self.output_dir / "weekly_sheet_ready.csv"

    @property
    def flags_csv(self) -> Path:
        return self.output_dir / "flags_review.csv"

    @property
    def validation_report(self) -> Path:
        return self.output_dir / "validation_report.md"


def normalize_header(header: list[str], rules: ReportingRules | None = None) -> list[str]:
    rules = rules or ReportingRules.defaults()
    normalized: list[str] = []
    blank_seen = 0
    for raw in header:
        cleaned = raw.strip().lstrip("\ufeff")
        if cleaned == "":
            blank_seen += 1
            normalized.append(OPTIONAL_NOTES_COLUMN if blank_seen == 1 else f"Extra Blank Column {blank_seen}")
        else:
            normalized.append(rules.header_aliases.get(cleaned, cleaned))
    return normalized


def parse_date_range(value: str) -> tuple[date, date] | None:
    match = _DATE_RANGE_RE.match(value or "")
    if not match:
        return None
    m1, d1, y1, m2, d2, y2 = match.groups()
    return _make_date(m1, d1, y1), _make_date(m2, d2, y2)


def _make_date(month: str, day: str, year: str) -> date:
    y = int(year)
    if y < 100:
        y += 2000
    return date(y, int(month), int(day))


def normalize_value(column: str, value: str, result: NormalizationResult, row_number: int, rules: ReportingRules | None = None) -> str:
    rules = rules or ReportingRules.defaults()
    value = value.strip()
    aliases = rules.value_aliases.get(column, {})
    if value in aliases:
        new_value = aliases[value]
        result.alias_counts[f"{column}: {value} -> {new_value}"] += 1
        result.issues.append(RowIssue(row_number, "info", column, f"Normalized alias to {new_value}", value))
        return new_value
    return value


def normalize_csv(input_path: Path, output_dir: Path, rules: ReportingRules | None = None) -> NormalizationResult:
    rules = rules or ReportingRules.defaults()
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result = NormalizationResult(input_path=input_path, output_dir=output_dir)

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row")
        normalized_headers = normalize_header(reader.fieldnames, rules)
        missing = [c for c in CANONICAL_COLUMNS if c not in normalized_headers]
        if missing:
            raise ValueError(f"Input CSV is missing required columns: {missing}")

        reader.fieldnames = normalized_headers
        with result.output_csv.open("w", encoding="utf-8", newline="") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for row_number, row in enumerate(reader, start=2):
                result.rows_read += 1
                if (row.get("Date") or "").strip().upper().startswith("FY"):
                    result.skipped_marker_rows += 1
                    result.issues.append(RowIssue(row_number, "info", "Date", "Skipped fiscal-year marker row", row.get("Date", "")))
                    continue

                clean: dict[str, str] = {}
                for column in OUTPUT_COLUMNS:
                    clean[column] = normalize_value(column, row.get(column, ""), result, row_number, rules)

                if _is_incomplete_placeholder_row(clean):
                    result.issues.append(RowIssue(row_number, "info", "row", "Skipped incomplete placeholder row", clean.get("Date", "")))
                    continue

                _validate_row(clean, row_number, result, rules)
                writer.writerow(clean)
                result.normalized_rows.append(clean)
                result.rows_written += 1
                result.platform_counts[clean["Platform"]] += 1
                result.campaign_counts[clean["Campaign"]] += 1
                result.goal_counts[clean["Goal"]] += 1
                result.audience_counts[clean["Audiences"]] += 1

    result.summary_paths = write_summaries(result.normalized_rows, output_dir)
    _write_flags(result)
    _write_report(result)
    return result


def _is_incomplete_placeholder_row(row: dict[str, str]) -> bool:
    """Skip formula/placeholder rows that have a date but no actual ad record fields."""
    required_identity_fields = ["Platform", "Campaign", "Ad Name", "Audiences", "Goal"]
    return bool(row.get("Date")) and all(not row.get(field) for field in required_identity_fields)


def _validate_row(row: dict[str, str], row_number: int, result: NormalizationResult, rules: ReportingRules) -> None:
    if not parse_date_range(row["Date"]):
        result.issues.append(RowIssue(row_number, "warning", "Date", "Could not parse weekly date range", row["Date"]))
    expected_platforms = rules.expected_values.get("Platform", set())
    expected_campaigns = rules.expected_values.get("Campaign", set())
    expected_goals = rules.expected_values.get("Goal", set())
    if row["Platform"] and expected_platforms and row["Platform"] not in expected_platforms:
        result.issues.append(RowIssue(row_number, "warning", "Platform", "Unexpected platform", row["Platform"]))
    if row["Campaign"] and expected_campaigns and row["Campaign"] not in expected_campaigns:
        result.issues.append(RowIssue(row_number, "warning", "Campaign", "Unexpected campaign", row["Campaign"]))
    if row["Goal"] and expected_goals and row["Goal"] not in expected_goals:
        result.issues.append(RowIssue(row_number, "warning", "Goal", "Unexpected goal; review before treating as canonical", row["Goal"]))
    for column in FORMULA_COLUMNS:
        if row.get(column) == "#DIV/0!":
            result.issues.append(RowIssue(row_number, "warning", column, "Formula error in source; generated outputs should prefer blank plus warning", row[column]))


def _write_flags(result: NormalizationResult) -> None:
    with result.flags_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["row_number", "severity", "field", "message", "value"])
        writer.writeheader()
        for issue in result.issues:
            writer.writerow(issue.as_csv_row())


def _counter_lines(counter: Counter[str], limit: int = 20) -> list[str]:
    if not counter:
        return ["- none"]
    return [f"- {key or '[blank]'}: {count}" for key, count in counter.most_common(limit)]


def _issue_summary(issues: list[RowIssue]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for issue in issues:
        counts[f"{issue.severity} / {issue.field} / {issue.message}"] += 1
    return counts


def _write_report(result: NormalizationResult) -> None:
    summary = _issue_summary(result.issues)
    lines = [
        "# SBA Reporting Assistant Validation Report",
        "",
        f"Input: `{result.input_path}`",
        f"Rows read: {result.rows_read}",
        f"Rows written: {result.rows_written}",
        f"Fiscal marker rows skipped: {result.skipped_marker_rows}",
        f"Issues/flags: {len(result.issues)}",
        "",
        "## Output files",
        "",
        f"- Weekly sheet ready CSV: `{result.output_csv}`",
        f"- Flags review CSV: `{result.flags_csv}`",
        *[f"- Summary: `{path}`" for path in result.summary_paths.values()],
        "",
        "## Alias normalizations",
        "",
        *_counter_lines(result.alias_counts),
        "",
        "## Issue summary",
        "",
        *_counter_lines(summary, limit=50),
        "",
        "## Platform counts",
        "",
        *_counter_lines(result.platform_counts),
        "",
        "## Campaign counts",
        "",
        *_counter_lines(result.campaign_counts),
        "",
        "## Goal counts",
        "",
        *_counter_lines(result.goal_counts),
        "",
        "## Audience counts",
        "",
        *_counter_lines(result.audience_counts),
        "",
    ]
    result.validation_report.write_text("\n".join(lines), encoding="utf-8")
