from pathlib import Path

import pandas as pd

from cfb_pickem.validation import (
    validate_week,
    check_duplicate_player_game_pairs,
    check_duplicate_confidence_values,
    check_confidence_values_in_range,
    check_unknown_players,
    check_unknown_games,
    check_invalid_picked_teams,
)


def test_check_invalid_picked_teams_accept_values() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "C"],
            "confidence": [1, 2]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_invalid_picked_teams(picks, games)

    assert errors == []


def test_check_invalid_picked_teams_detect_invalid() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "A"],
            "confidence": [1, 2]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_invalid_picked_teams(picks, games)

    assert errors == [
        "Player 'coleman' picked 'A' for game 'game_2'; "
        "valid teams are 'C' and 'D'."
    ]


def test_check_unknown_games_accept_values() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "B"],
            "confidence": [1, 2]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_unknown_games(picks, games)

    assert errors == []


def test_check_unknown_games_detect_unknown() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_3"],
            "picked_team": ["A", "B"],
            "confidence": [1, 2]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_unknown_games(picks, games)

    assert errors == [
        "Player 'coleman' has picked for game 'game_3' "
        "which is not in games.csv"
    ]


def test_check_confidence_values_in_range_accept_values() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "B"],
            "confidence": [1, 2]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_confidence_values_in_range(picks, games)

    assert errors == []


def test_check_confidence_values_in_range_detect_invalid() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "B"],
            "confidence": [1, 3]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_confidence_values_in_range(picks, games)

    assert errors == [
        "Player 'coleman' has invalid confidence value 3; "
        "expected a value from 1 to 2."
    ]


def test_check_duplicate_confidence_values_detects_duplicates() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "B"],
            "confidence": [1, 1]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_duplicate_confidence_values(picks)

    assert errors == [
        "Player 'coleman' has reused confidence value 1."
    ]


def test_check_duplicate_confidence_values_accepts_unique_values() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "B"],
            "confidence": [1, 2]
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    errors = check_duplicate_confidence_values(picks)

    assert errors == []


def test_check_duplicate_player_game_pairs_detects_duplicate() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_1"],
            "picked_team": ["A", "B"],
            "confidence": [1, 1]
        }
    )

    errors = check_duplicate_player_game_pairs(picks)

    assert errors == [
        "Player 'coleman' has multiple picks for game 'game_1'."
    ]


def test_check_duplicate_player_game_pairs_accepts_unique_picks() -> None:
    picks = pd.DataFrame(
        {
            "player_id": ["james", "james"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "D"],
            "confidence": [1, 2],
        }
    )

    errors = check_duplicate_player_game_pairs(picks)

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
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": ["unknown", "unknown", "coleman"],
            "game_id": ["game_1", "game_1", "game_2"],
            "picked_team": ["A", "B", "C"],
            "confidence": [1, 1, 4],
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "winner": ["A", "C"],
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
        "Player 'unknown' has reused confidence value 1.",
        "Player 'coleman' has invalid confidence value 4; "
        "expected a value from 1 to 2."
    ]

    assert errors == expected
