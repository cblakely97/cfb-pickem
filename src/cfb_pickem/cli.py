"""Command-line inferface for cfb-pickem"""

import argparse
from pathlib import Path

from cfb_pickem.scoring import score_week
from cfb_pickem.validation import validate_week


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="cfb-pickem",
        description="Validate and score college football pick'em data.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a directory of weekly pick'em CSV files.",
    )
    validate_parser.add_argument(
        "data_dir",
        type=Path,
        help="Directory containing the weekly CSV files.",
    )

    score_parser = subparsers.add_parser(
        "score",
        help="Calculate standings for a weekly pick'em directory.",
    )
    score_parser.add_argument(
        "data_dir",
        type=Path,
        help="Directory containing the weekly CSV files.",
    )

    return parser

def run_validation(data_dir: Path) -> int:
    """Validate weekly data and return a process exit code"""
    errors = validate_week(data_dir)

    if errors:
        print("Validation failed:")

        for error in errors:
            print(f"- {error}")

        return 1

    print("Validation passed.")
    return 0


def run_score(data_dir: Path) -> int:
    """Calculate and print weekly standings."""
    try:
        standings = score_week(data_dir)
    except ValueError as exc:
        print(exc)
        return 1

    print(standings.to_string(index=False))
    return 0


def main() -> None:
    """Run the cfb-pickem command-line interface"""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate":
        exit_code = run_validation(args.data_dir)
    elif args.command == "score":
        exit_code = run_score(args.data_dir)
    else:
        parser.error(f"Unknown command: {args.command}")

    raise SystemExit(exit_code)

if __name__=="__main__":
    main()
