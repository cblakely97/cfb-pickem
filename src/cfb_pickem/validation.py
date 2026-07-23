"""Functions for validating weekly college football pick'em submissions"""

from pathlib import Path

import pandas as pd


def check_duplicate_player_game_pairs(picks: pd.DataFrame) -> list[str]:
    """Return errors for players with multiple picks for one game."""
    errors: list[str] = []

    duplicate_mask = picks.duplicated(
        subset=["player_id", "game_id"],
        keep=False,
    )

    duplicate_rows = (
        picks.loc[duplicate_mask, ["player_id", "game_id"]]
        .drop_duplicates()
    )

    for row in duplicate_rows.itertuples(index=False):
        errors.append(
            f"Player {row.player_id!r} has multiple picks "
            f"for game {row.game_id!r}."
        )

    return errors


def check_unknown_players(
    picks: pd.DataFrame,
    players: pd.DataFrame,
) -> list[str]:
    """Return errors for player IDs appearing in picks but not players."""
    errors: list[str] = []

    unknown_mask = ~picks["player_id"].isin(players["player_id"])

    unknown_players = (
        picks.loc[unknown_mask, ["player_id"]]
        .drop_duplicates()
    )

    for row in unknown_players.itertuples(index=False):
        errors.append(
            f"Player {row.player_id!r} is not in players.csv"
        )

    return errors


def check_duplicate_confidence_values(
    picks: pd.DataFrame,
    games: pd.DataFrame,
) -> list[str]:
    """Return errors for players with duplicated/invalid confidence values"""
    errors: list[str] = []

    duplicate_mask = picks.duplicated(
        subset=["player_id", "confidence"],
        keep=False,
    )

    duplicate_rows = (
        picks.loc[duplicate_mask, ["player_id", "confidence"]]
        .drop_duplicates()
    )

    for row in duplicate_rows.itertuples(index=False):
        errors.append(
            f"Player {row.player_id!r} has reused confidence value "
            f"{row.confidence!r}."
        )

    return errors


def check_invalid_confidence_values(
    picks: pd.DataFrame,
    games: pd.DataFrame,
) -> list[str]:
    """Return errors for players with duplicated/invalid confidence values"""
    errors: list[str] = []

    ngames = len(games)

    invalid_range_mask = ~picks["confidence"].between(1, ngames)

    invalid_rows = (
        picks.loc[invalid_range_mask, ["player_id", "confidence"]]
        .drop_duplicates()
    )

    for row in invalid_rows.itertuples(index=False):
        errors.append(
            f"Player {row.player_id!r} has invalid confidence value "
            f"{row.confidence!r}; expected a value from 1 to {ngames}."
        )

    return errors


def validate_week(data_dir: Path) -> list[str]:
    """Return validation errors found in weekly pick'em submissions.

    Parameters
    ----------
    data_dir
        Directory containing players, games, picks, and results CSV files.

    Returns
    -------
    list[str]
        Human-readable validation errors. An empty list means that all input
        data passed all implemented checks.
    """
    players = pd.read_csv(data_dir / "players.csv")
    games = pd.read_csv(data_dir / "games.csv")
    picks = pd.read_csv(data_dir / "picks.csv")
    results = pd.read_csv(data_dir / "results.csv")

    errors: list[str] = []

    errors.extend(check_duplicate_player_game_pairs(picks))
    errors.extend(check_unknown_players(picks, players))
    errors.extend(check_duplicate_confidence_values(picks, games))
    errors.extend(check_invalid_confidence_values(picks, games))

    return errors
