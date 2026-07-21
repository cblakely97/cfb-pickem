from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from cfb_pickem.scoring import score_week


def test_score_week(tmp_path: Path) -> None:
    """Correct picks receive their assigned confidence points."""

    players = pd.DataFrame(
        {
            "player_id": ["coleman", "dad", "zach"],
            "name": ["Coleman", "Dad", "Zach"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": [
                "coleman",
                "coleman",
                "coleman",
                "dad",
                "dad",
                "dad",
                "zach",
                "zach",
                "zach",
            ],
            "game_id": [
                "game_1",
                "game_2",
                "game_3",
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
                "E",
                "B",
                "C",
                "F",
                "B",
                "D",
                "F",
            ],
            "confidence": [
                3,
                2,
                1,
                1,
                2,
                3,
                1,
                2,
                3,
            ],
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2", "game_3"],
            "winner": ["B", "D", "F"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    picks.to_csv(tmp_path / "picks.csv", index=False)
    results.to_csv(tmp_path / "results.csv", index=False)

    actual = score_week(tmp_path)

    expected = pd.DataFrame(
        {
            "player_id": ["zach", "dad", "coleman"],
            "name": ["Zach", "Dad", "Coleman"],
            "points": [6, 4, 2],
        }
    )

    assert_frame_equal(actual, expected)

def test_score_week_with_no_correct_picks(tmp_path: Path) -> None:
    """A player with no correct picks receives zero points."""

    players = pd.DataFrame(
        {
            "player_id": ["coleman"],
            "name": ["Coleman"],
        }
    )

    picks = pd.DataFrame(
        {
            "player_id": [
                "coleman",
                "coleman",
            ],
            "game_id": [
                "game_1",
                "game_2",
            ],
            "picked_team": [
                "A",
                "C",
            ],
            "confidence": [
                1,
                2,
            ],
        }
    )

    results = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "winner": ["B", "D"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    picks.to_csv(tmp_path / "picks.csv", index=False)
    results.to_csv(tmp_path / "results.csv", index=False)

    actual = score_week(tmp_path)

    assert actual.loc[0,"points"] == 0
