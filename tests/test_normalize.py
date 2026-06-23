from __future__ import annotations

import csv
from pathlib import Path

from sba_reporting.normalize import normalize_csv, normalize_header, parse_date_range


def test_normalize_header_maps_aliases_and_blank_notes_column():
    assert normalize_header(["Date", "Pin Clicks /Link Clicks", ""]) == [
        "Date", "Pin Clicks / Link Clicks", "Manual Notes"
    ]


def test_parse_date_range_tolerates_spaces_and_padding():
    parsed = parse_date_range("3/30/26 - 4/05/26")
    assert parsed is not None
    assert parsed[0].isoformat() == "2026-03-30"
    assert parsed[1].isoformat() == "2026-04-05"


def test_normalize_csv_outputs_clean_rows_and_flags(tmp_path: Path):
    src = Path(__file__).parent / "fixtures" / "sample_all_data_weekly.csv"
    result = normalize_csv(src, tmp_path)

    assert result.rows_read == 4
    assert result.skipped_marker_rows == 1
    assert result.rows_written == 2
    assert result.output_csv.exists()
    assert result.flags_csv.exists()
    assert result.validation_report.exists()
    assert (tmp_path / "summaries" / "weekly_summary.csv").exists()
    assert (tmp_path / "summaries" / "audiences_summary.csv").exists()
    assert (tmp_path / "summaries" / "campaigns_summary.csv").exists()
    assert (tmp_path / "summaries" / "ad_per_audience_summary.csv").exists()

    rows = list(csv.DictReader(result.output_csv.open(encoding="utf-8")))
    assert rows[0]["Platform"] == "YouTube"
    assert rows[0]["Campaign"] == "Co-Op"
    assert rows[0]["Audiences"] == "NorCal"
    assert rows[0]["Manual Notes"] == "Check UTM"

    flags_text = result.flags_csv.read_text(encoding="utf-8")
    assert "Normalized alias to YouTube" in flags_text
    assert "Normalized alias to Co-Op" in flags_text
    assert "Formula error in source" in flags_text
    assert "Unexpected campaign" in flags_text
    assert "Unexpected goal" in flags_text

    weekly_rows = list(csv.DictReader((tmp_path / "summaries" / "weekly_summary.csv").open(encoding="utf-8")))
    youtube_summary = next(row for row in weekly_rows if row["Platform"] == "YouTube")
    assert youtube_summary["Cost"] == "100"
    assert youtube_summary["Impressions"] == "10000"
    assert youtube_summary["CPM"] == "10.00"
    assert youtube_summary["CPC"] == "10.00"
    assert youtube_summary["CPM Views to 100%"] == "200.00"
