"""Functions for validating weekly college football pick'em submissions"""

from pathlib import Path

import pandas as pd


def check_invalid_picked_teams(
    picks: pd.DataFrame,
    games: pd.DataFrame,
) -> list[str]:
    """Return errors for picks with teams that are not in a game"""
    errors: list[str] = []

    merged = picks.merge(
        games,
        on="game_id",
        how="left",
        validate="many_to_one",
    )

    invalid_mask = (
        (merged["picked_team"] != merged["home_team"])
        &
        (merged["picked_team"] != merged["away_team"])
    )

    invalid_rows = merged.loc[
        invalid_mask,
        ["player_id", "game_id", "picked_team", "home_team", "away_team"],
    ]

    for row in invalid_rows.itertuples(index=False):
        errors.append(
            f"Player {row.player_id!r} picked {row.picked_team!r} "
            f"for game {row.game_id!r}; "
            f"valid teams are {row.away_team!r} and {row.home_team!r}."
        )

    return errors


def check_unknown_games(
    picks: pd.DataFrame,
    games: pd.DataFrame,
) -> list[str]:
    """Return errors for game IDs appearing in picks but not games"""
    errors: list[str] = []

    unknown_mask = ~picks["game_id"].isin(games["game_id"])

    unknown_games = (
        picks.loc[unknown_mask, ["player_id", "game_id"]]
        .drop_duplicates()
    )

    for row in unknown_games.itertuples(index=False):
        errors.append(
            f"Player {row.player_id!r} has picked for game {row.game_id!r} "
            "which is not in games.csv"
        )

    return errors


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
) -> list[str]:
    """Return errors for players with duplicated confidence values"""
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


def check_confidence_values_in_range(
    picks: pd.DataFrame,
    games: pd.DataFrame,
) -> list[str]:
    """Return errors for players with out of range confidence values"""
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
    errors.extend(check_duplicate_confidence_values(picks))
    errors.extend(check_confidence_values_in_range(picks, games))

    return errors
