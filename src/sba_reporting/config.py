from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .schema import DEFAULT_HEADER_ALIASES, DEFAULT_VALUE_ALIASES

@dataclass(frozen=True)
class ReportingRules:
    header_aliases: dict[str, str]
    value_aliases: dict[str, dict[str, str]]
    expected_values: dict[str, set[str]]

    @classmethod
    def defaults(cls) -> "ReportingRules":
        return cls(
            header_aliases={k: v for k, v in DEFAULT_HEADER_ALIASES.items()},
            value_aliases={field: dict(values) for field, values in DEFAULT_VALUE_ALIASES.items()},
            expected_values={
                "Platform": {"Facebook", "Instagram", "YouTube", "TikTok", "Pinterest", "NextDoor", "Reddit"},
                "Goal": {"Traffic", "Awareness", "Video Views", "Direct Response"},
                "Campaign": {"Brand", "Co-Op", "Retainer", "Episodic", "Retail", "Air Services", "Compression", "HIT", "Locals", "Weddings", "FIFA"},
            },
        )

    @classmethod
    def from_json(cls, path: Path) -> "ReportingRules":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        defaults = cls.defaults()
        header_aliases = dict(defaults.header_aliases)
        header_aliases.update(payload.get("header_aliases", {}))

        value_aliases = {field: dict(values) for field, values in defaults.value_aliases.items()}
        for field, aliases in payload.get("value_aliases", {}).items():
            value_aliases.setdefault(field, {}).update(aliases)

        expected_values = {field: set(values) for field, values in defaults.expected_values.items()}
        for field, values in payload.get("expected_values", {}).items():
            expected_values[field] = set(values)

        return cls(header_aliases=header_aliases, value_aliases=value_aliases, expected_values=expected_values)
