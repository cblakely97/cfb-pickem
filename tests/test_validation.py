from pathlib import Path

import pandas as pd

from cfb_pickem.validation import (
    validate_week,
    check_duplicate_picks,
    check_unknown_players,
)


def test_check_duplicate_picks_detects_duplicate() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_1"],
            "picked_team": ["A", "B"],
            "confidence": [1, 1]
        }
    )

    errors = check_duplicate_picks(picks)

    assert errors == [
        "Player 'coleman' has multiple picks for game 'game_1'."
    ]


def test_check_duplicate_picks_accepts_unique_picks() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["james", "james"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "D"],
            "confidence": [1, 2],
        }
    )

    errors = check_duplicate_picks(picks)

    assert errors == []


def test_check_unknown_players_detects_unknown() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "john", "jim"],
            "game_id": ["game_1", "game_1", "game_1"],
            "picked_team": ["A", "B", "A"],
            "confidence": [1, 1, 1]
        }
    )

    players = pd.DataFrame(
        {
            "player_id": ["coleman", "john"],
            "name": ["Coleman", "John"]
        }
    )

    errors = check_unknown_players(picks,players)

    assert errors == [
        "Player 'jim' is not in players.csv"
    ]


def test_check_unknown_players_accepts_players() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "john", "jim"],
            "game_id": ["game_1", "game_1", "game_1"],
            "picked_team": ["A", "B", "A"],
            "confidence": [1, 1, 1]
        }
    )

    players = pd.DataFrame(
        {
            "player_id": ["coleman", "john", "jim"],
            "name": ["Coleman", "John", "Jim"]
        }
    )

    errors = check_unknown_players(picks,players)

    assert errors == []

def test_validate_week_combines_validation_checks(
    tmp_path: Path,
) -> None:
    players = pd.DataFrame(
        {
            "player_id": ["coleman"],
            "name": ["Coleman"],
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1"],
            "away_team": ["A"],
            "home_team": ["B"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": ["unknown", "unknown"],
            "game_id": ["game_1", "game_1"],
            "picked_team": ["A", "B"],
            "confidence": [1, 1],
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1"],
            "winner": ["A"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(tmp_path / "games.csv", index=False)
    picks.to_csv(tmp_path / "picks.csv", index=False)
    results.to_csv(tmp_path / "results.csv", index=False)

    errors = validate_week(tmp_path)

    expected = [
        "Player 'unknown' has multiple picks for game 'game_1'.",
        "Player 'unknown' is not in players.csv",
    ]

    assert errors == expected
