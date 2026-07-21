from pathlib import Path

import pandas as pd

from cfb_pickem.validation import (
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
    picks=pd.DataFrame(
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
