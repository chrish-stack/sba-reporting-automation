from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

METRIC_COLUMNS = [
    "Cost",
    "Impressions",
    "Reach",
    "Pin Clicks / Link Clicks",
    "Video Plays at 50%",
    "Video Plays at 75%",
    "Video Plays at 100%",
    "Outbound Clicks / LPVs",
    "Google Sessions",
]

CALCULATED_COLUMNS = [
    "Frequency",
    "CPM",
    "CPC",
    "CPM Views to 50%",
    "CPM Views to 100%",
    "CPLPV",
]

SUMMARY_SPECS = {
    "weekly_summary.csv": ["Date", "Platform", "Goal", "Audiences", "Campaign"],
    "audiences_summary.csv": ["Audiences", "Platform", "Campaign", "Goal"],
    "campaigns_summary.csv": ["Date", "Goal", "Platform", "Audiences", "Campaign"],
    "ad_per_audience_summary.csv": ["Date", "Platform", "Goal", "Audiences", "Ad Name"],
}


def parse_number(value: str | None) -> Decimal:
    text = (value or "").strip()
    if not text or text == "#DIV/0!":
        return Decimal("0")
    text = text.replace("$", "").replace(",", "").replace("%", "")
    try:
        return Decimal(text)
    except InvalidOperation:
        return Decimal("0")


def safe_div(numerator: Decimal, denominator: Decimal, multiplier: Decimal = Decimal("1")) -> str:
    if denominator == 0:
        return ""
    value = numerator / denominator * multiplier
    return f"{value.quantize(Decimal('0.01'))}"


def format_metric(value: Decimal) -> str:
    if value == value.to_integral_value():
        return str(int(value))
    return f"{value.quantize(Decimal('0.01'))}"


def write_summaries(rows: list[dict[str, str]], output_dir: Path) -> dict[str, Path]:
    summary_dir = output_dir / "summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for filename, dimensions in SUMMARY_SPECS.items():
        path = summary_dir / filename
        _write_summary(rows, dimensions, path)
        written[filename] = path
    return written


def _write_summary(rows: list[dict[str, str]], dimensions: list[str], path: Path) -> None:
    groups: dict[tuple[str, ...], dict[str, Decimal]] = defaultdict(lambda: {metric: Decimal("0") for metric in METRIC_COLUMNS})
    counts: dict[tuple[str, ...], int] = defaultdict(int)
    for row in rows:
        key = tuple(row.get(dim, "") for dim in dimensions)
        counts[key] += 1
        for metric in METRIC_COLUMNS:
            groups[key][metric] += parse_number(row.get(metric))

    fieldnames = dimensions + METRIC_COLUMNS + ["Record Count"] + CALCULATED_COLUMNS
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(groups):
            totals = groups[key]
            out = {dim: value for dim, value in zip(dimensions, key)}
            for metric in METRIC_COLUMNS:
                out[metric] = format_metric(totals[metric])
            out["Record Count"] = str(counts[key])
            out["Frequency"] = safe_div(totals["Impressions"], totals["Reach"])
            out["CPM"] = safe_div(totals["Cost"], totals["Impressions"], Decimal("1000"))
            out["CPC"] = safe_div(totals["Cost"], totals["Pin Clicks / Link Clicks"])
            out["CPM Views to 50%"] = safe_div(totals["Cost"], totals["Video Plays at 50%"], Decimal("1000"))
            out["CPM Views to 100%"] = safe_div(totals["Cost"], totals["Video Plays at 100%"], Decimal("1000"))
            out["CPLPV"] = safe_div(totals["Cost"], totals["Outbound Clicks / LPVs"])
            writer.writerow(out)
