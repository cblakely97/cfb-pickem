from pathlib import Path

import numpy as np
import pandas as pd

from cfb_pickem.validation import (
    check_confidence_values_in_range,
    check_duplicate_confidence_values,
    check_duplicate_player_game_pairs,
    check_invalid_picked_teams,
    check_missing_player_game_pairs,
    check_unknown_games,
    check_unknown_players,
    validate_week,
)


def test_check_missing_player_game_pairs_detects_missing_pick() -> None:
    players = pd.DataFrame(
        {
            "player_id": ["coleman", "james"],
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": [
                "coleman",
                "coleman",
                "james",
            ],
            "game_id": [
                "game_1",
                "game_2",
                "game_1",
            ],
        }
    )

    errors = check_missing_player_game_pairs(
        picks,
        players,
        games,
    )

    assert errors == [
        "Player 'james' is missing a pick for game 'game_2'."
    ]

def test_check_missing_player_game_pairs_accepts_complete_picks() -> None:
    players = pd.DataFrame(
        {
            "player_id": ["coleman", "james"],
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": [
                "coleman",
                "coleman",
                "james",
                "james",
            ],
            "game_id": [
                "game_1",
                "game_2",
                "game_1",
                "game_2",
            ],
        }
    )

    errors = check_missing_player_game_pairs(
        picks,
        players,
        games,
    )

    assert errors == []


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
        (
            "Player 'coleman' picked 'A' for game 'game_2'; "
            "valid teams are 'C' and 'D'."
        )
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
        (
            "Player 'coleman' has picked for unknown game 'game_3' "
            "which is not in games.csv."
        )
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
        (
            "Player 'coleman' has invalid confidence value 3; "
        "expected a value from 1 to 2."
        )
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
    week_dir = tmp_path / "week_01"
    week_dir.mkdir()

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

    schedule = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_9", "game_7", "game_8"],
            "away_team": ["A", "C", "E", "G", "W"],
            "home_team": ["B", "D", "F", "H", "X"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": ["unknown", 
                          "unknown", 
                          "unknown",
                          "coleman", 
                          "coleman",
                          "coleman",
                          ],
            "game_id": ["game_1",
                        "game_1",
                        "game_7",
                        "game_2",
                        "game_3",
                        "game_8",
                        ],
            "picked_team": ["A", "B", "G", "C", "F", "W"],
            "confidence": [1, 1, np.nan, 4, 2, np.nan,],
            "pick_type": ["regular", "regular", "bonus", 
                          "regular", "regular", "bonus"]
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "winner": ["A", "C"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    errors = validate_week(week_dir)

    expected = [
        "Player 'unknown' has multiple picks for game 'game_1'.",
        "Player 'unknown' is not in players.csv",
        "Player 'unknown' has reused confidence value 1.",
        (
            "Player 'coleman' has invalid confidence value 4; "
            "expected a value from 1 to 2."
        ),
        (
            "Player 'coleman' has picked for unknown game 'game_3' which is not "
            "in games.csv."
        ),
        "Player 'coleman' is missing a pick for game 'game_1'."
    ]

    assert errors == expected


def test_validate_week_accepts_valid_week(tmp_path : Path,) -> None:
    week_dir = tmp_path / "week_01"
    week_dir.mkdir()

    players = pd.DataFrame(
        {
            "player_id": ["coleman", "james"],
            "name": ["Coleman", "James"],
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )

    schedule = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3"],
            "away_team": ["A", "C", "E"],
            "home_team": ["B", "D", "F"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": [
                "coleman",
                "coleman",
                "coleman",
                "james",
                "james",
                "james",
            ],
            "game_id": [
                "game_1",
                "game_2",
                "game_3",
                "game_1",
                "game_2",
                "game_3",
            ],
            "picked_team": [
                "A",
                "D",
                "F",
                "B",
                "C",
                "E",
            ],
            "confidence": [
                2,
                1,
                np.nan,
                1,
                2,
                np.nan,
            ],
            "pick_type": [
                "regular",
                "regular",
                "bonus",
                "regular",
                "regular",
                "bonus",
            ],
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "winner": ["A", "D"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    assert validate_week(week_dir) == []





