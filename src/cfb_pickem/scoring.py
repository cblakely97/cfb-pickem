"""Functions for calculating weekly college football pick'em scores."""

from pathlib import Path

import pandas as pd

def score_week(data_dir: Path) -> pd.DataFrame:
    """Calculate weekly standings from pick'em CSV files.

    The input directory must contain ``players.csv``, ``picks.csv``,
    and ``results.csv``. Correct picks receive the assigned confidence
    value, while incorrect picks receive zero points.

    Parameters
    ----------
    data_dir
        Directory containing the weekly input CSV files.

    Returns
    -------
    pandas.DataFrame
        Standings sorted from highest to lowest score. The returned columns
        are ``player_id``, ``name``, and ``points``.
    """
    players = pd.read_csv(data_dir / "players.csv")
    picks = pd.read_csv(data_dir / "picks.csv")
    results = pd.read_csv(data_dir / "results.csv")

    scored = picks.merge(
            results,
            on="game_id",
            how="left",
            validate="many_to_one",
            )

    scored["correct"] = scored["picked_team"] == scored["winner"]
    scored["points"] = scored["confidence"].where(scored["correct"], 0)

    standings = (
            scored.groupby("player_id", as_index=False)["points"]
            .sum()
            .merge(players, on="player_id", how="left")
            .sort_values("points", ascending=False)
            )
    return standings[["player_id", "name", "points"]].reset_index(drop=True)
