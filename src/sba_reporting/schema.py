from __future__ import annotations

from dataclasses import dataclass

CANONICAL_COLUMNS: list[str] = [
    "Date",
    "Platform",
    "Campaign",
    "Ad Name",
    "Audiences",
    "Goal",
    "Cost",
    "Impressions",
    "Reach",
    "Pin Clicks / Link Clicks",
    "Video Plays at 50%",
    "Video Plays at 75%",
    "Video Plays at 100%",
    "Outbound Clicks / LPVs",
    "Cost per Session",
    "Google Sessions",
    "Non-Bounced Sessions (Engaged Sessions)",
    "Cost Per Non-Bounced Session (Cost per engaged user)",
    "Google Conversions",
    "Cost Per Conversion",
    "Time on Site (engaged time)",
    "Bounce Rate (Engagement Rate)",
    "Pages Per Session (Engaged session per user)",
    "Web Referral",
    "Cost Per Web Referral",
]

OPTIONAL_NOTES_COLUMN = "Manual Notes"
OUTPUT_COLUMNS: list[str] = CANONICAL_COLUMNS + [OPTIONAL_NOTES_COLUMN]

DEFAULT_HEADER_ALIASES: dict[str, str] = {
    "": OPTIONAL_NOTES_COLUMN,
    "Pin Clicks /Link Clicks": "Pin Clicks / Link Clicks",
    "Pin Clicks / Link Clicks": "Pin Clicks / Link Clicks",
}

DEFAULT_VALUE_ALIASES: dict[str, dict[str, str]] = {
    "Platform": {
        "Youtube": "YouTube",
    },
    "Campaign": {
        "Co op": "Co-Op",
        "Co Op": "Co-Op",
    },
    "Audiences": {
        "Norcal": "NorCal",
    },
}

FORMULA_COLUMNS = {
    "Cost per Session",
    "Cost Per Non-Bounced Session (Cost per engaged user)",
    "Cost Per Conversion",
    "Cost Per Web Referral",
}

@dataclass(frozen=True)
class RowIssue:
    row_number: int
    severity: str
    field: str
    message: str
    value: str = ""

    def as_csv_row(self) -> dict[str, str]:
        return {
            "row_number": str(self.row_number),
            "severity": self.severity,
            "field": self.field,
            "message": self.message,
            "value": self.value,
        }
