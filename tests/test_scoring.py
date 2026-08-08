from pathlib import Path

import numpy as np
import pandas as pd

from pandas.testing import assert_frame_equal

from cfb_pickem.scoring import score_week


def test_score_week(tmp_path: Path) -> None:
    """Correct picks receive their assigned confidence points."""

    week_dir = tmp_path / "week_01"
    week_dir.mkdir()

    players = pd.DataFrame(
        {
            "player_id": ["coleman", "dad", "zach"],
            "name": ["Coleman", "Dad", "Zach"],
        }
    )

    games = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3"],
            "away_team": ["A", "C", "E"],
            "home_team": ["B", "D", "F"],
        }
    )

    schedule = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3", "game_4"],
            "away_team": ["A", "C", "E", "G"],
            "home_team": ["B", "D", "F", "H"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": [
                "coleman",
                "coleman",
                "coleman",
                "coleman",
                "dad",
                "dad",
                "dad",
                "dad",
                "zach",
                "zach",
                "zach",
                "zach",
            ],
            "game_id": [
                "game_1",
                "game_2",
                "game_3",
                "game_4",
                "game_1",
                "game_2",
                "game_3",
                "game_4",
                "game_1",
                "game_2",
                "game_3",
                "game_4",
            ],
            "picked_team": [
                "A",
                "D",
                "E",
                "G",
                "B",
                "C",
                "F",
                "H",
                "B",
                "D",
                "F",
                "H",
            ],
            "confidence": [
                3,
                2,
                1,
                np.nan,
                1,
                2,
                3,
                np.nan,
                1,
                2,
                3,
                np.nan,
            ],
            "pick_type": [
                "regular",
                "regular",
                "regular",
                "bonus",
                "regular",
                "regular",
                "regular",
                "bonus",
                "regular",
                "regular",
                "regular",
                "bonus",
            ],
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3", "game_4"],
            "winner": ["B", "D", "F", "H"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    actual = score_week(week_dir)

    expected = pd.DataFrame(
        {
            "player_id": ["zach", "dad", "coleman"],
            "name": ["Zach", "Dad", "Coleman"],
            "points": [11, 9, 2],
        }
    )

    assert_frame_equal(actual, expected)


def test_score_week_with_no_correct_picks(tmp_path: Path) -> None:
    """A player with no correct picks receives zero points."""
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
            ],
            "game_id": [
                "game_1",
                "game_2",
                "game_3",
            ],
            "picked_team": [
                "A",
                "C",
                "E",
            ],
            "confidence": [
                1,
                2,
                np.nan,
            ],
            "pick_type": [
                "regular",
                "regular",
                "bonus",
            ]
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3"],
            "winner": ["B", "D", "F"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    actual = score_week(week_dir)

    expected = pd.DataFrame(
        {
            "player_id": ["coleman"],
            "name": ["Coleman"],
            "points": [0],
        }
    )

    assert_frame_equal(actual,expected)


def test_score_week_ties_sorted_alphabetically(tmp_path: Path) -> None:
    """When ties exist the output is sorted alphabetically by name."""
    week_dir = tmp_path / "week_01"
    week_dir.mkdir()

    players = pd.DataFrame(
        {
            "player_id": ["coleman", "alex"],
            "name": ["Coleman", "Alex"],
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
                "alex",
                "alex",
                "alex",
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
                "B",
                "C",
                "E",
                "A",
                "D",
                "E",
            ],
            "confidence": [
                2,
                1,
                np.nan,
                1,
                2,
                np.nan
            ],
            "pick_type": [
                "regular",
                "regular",
                "bonus",
                "regular",
                "regular",
                "bonus",
            ]
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3"],
            "winner": ["B", "D", "F"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    actual = score_week(week_dir)

    expected = pd.DataFrame(
        {
            "player_id": ["alex", "coleman"],
            "name": ["Alex", "Coleman"],
            "points": [2, 2],
        }
    )

    assert_frame_equal(actual,expected)
