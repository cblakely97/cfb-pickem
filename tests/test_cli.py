from pathlib import Path

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
    picks = pd.DataFrame(
        {
            "player_id": ["coleman"],
            "game_id": ["game_1"],
            "picked_team": ["A"],
            "confidence": [1],
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
    picks = pd.DataFrame(
        {
            "player_id": ["unknown"],
            "game_id": ["game_1"],
            "picked_team": ["A"],
            "confidence": [1],
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
    picks.to_csv(week_dir / "picks.csv", index=False)
    results.to_csv(week_dir / "results.csv", index=False)

    exit_code = run_validation(week_dir)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Validation failed:" in captured.out
    assert "unknown" in captured.out
