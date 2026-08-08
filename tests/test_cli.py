from pathlib import Path

import numpy as np
import pandas as pd

from cfb_pickem.cli import run_validation


def test_run_validation_reports_valid_week(
    tmp_path: Path,
    capsys,
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
            "game_id": ["game_1"],
            "away_team": ["A"],
            "home_team": ["B"],
        }
    )
    schedule = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )
    picks = pd.DataFrame(
        {
            "player_id": ["coleman", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "D"],
            "confidence": [1, np.nan],
            "pick_type": ["regular", "bonus"],
        }
    )
    results = pd.DataFrame(
        {
            "game_id": ["game_1"],
            "winner": ["A"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    exit_code = run_validation(week_dir)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Validation passed.\n"

def test_run_validation_reports_errors(
    tmp_path: Path,
    capsys,
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
            "game_id": ["game_1"],
            "away_team": ["A"],
            "home_team": ["B"],
        }
    )
    schedule = pd.DataFrame(
        {
            "game_id": ["game_1", "game_2"],
            "away_team": ["A", "C"],
            "home_team": ["B", "D"],
        }
    )
    picks = pd.DataFrame(
        {
            "player_id": ["unknown", "coleman"],
            "game_id": ["game_1", "game_2"],
            "picked_team": ["A", "C"],
            "confidence": [1, np.nan],
            "pick_type": ["regular", "bonus"],
        }
    )
    results = pd.DataFrame(
        {
            "game_id": ["game_1"],
            "winner": ["A"],
        }
    )

    players.to_csv(tmp_path / "players.csv", index=False)
    games.to_csv(week_dir / "games.csv", index=False)
    schedule.to_csv(week_dir / "schedule.csv", index=False)
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    exit_code = run_validation(week_dir)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Validation failed:" in captured.out
    assert "unknown" in captured.out
