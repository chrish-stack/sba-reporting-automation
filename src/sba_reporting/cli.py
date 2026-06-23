from __future__ import annotations

import argparse
from pathlib import Path

from .config import ReportingRules
from .normalize import normalize_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sba-reporting", description="Local SBA reporting assistant")
    sub = parser.add_subparsers(dest="command", required=True)
    normalize = sub.add_parser("normalize", help="Normalize an All Data - Weekly CSV export")
    normalize.add_argument("--input", required=True, help="Path to the source CSV")
    normalize.add_argument("--output-dir", required=True, help="Directory for generated outputs")
    normalize.add_argument("--config", help="Optional JSON rules config; defaults to built-in rules")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "normalize":
        rules = ReportingRules.from_json(Path(args.config)) if args.config else ReportingRules.defaults()
        result = normalize_csv(Path(args.input), Path(args.output_dir), rules=rules)
        print(f"Rows read: {result.rows_read}")
        print(f"Rows written: {result.rows_written}")
        print(f"Flags: {len(result.issues)}")
        print(f"Weekly CSV: {result.output_csv}")
        print(f"Flags CSV: {result.flags_csv}")
        print(f"Validation report: {result.validation_report}")
        for name, path in result.summary_paths.items():
            print(f"Summary {name}: {path}")
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
