"""Functions for calculating weekly college football pick'em scores."""

from pathlib import Path

import pandas as pd

from cfb_pickem.validation import validate_week


def score_week(
    data_dir: Path,
    bonus_points : int = 5,
) -> pd.DataFrame:
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
    # Check week for errors
    errors = validate_week(data_dir)

    if errors:
        formatted_errors = "\n".join(
            f"- {error}" for error in errors
        )
        raise ValueError(
            "Cannot score invalid weekly data:\n"
            f"{formatted_errors}"
            )

    season_dir = data_dir.parent

    players = pd.read_csv(season_dir / "players.csv")
    picks = pd.read_csv(data_dir / "picks.csv")
    results = pd.read_csv(data_dir / "results.csv")

    scored = picks.merge(
            results,
            on="game_id",
            how="left",
            validate="many_to_one",
            )

    regular_mask = scored["pick_type"] == "regular"
    bonus_mask = scored["pick_type"] == "bonus"

    scored["correct"] = scored["picked_team"] == scored["winner"]

    scored["points"] = 0

    scored.loc[
        regular_mask & scored["correct"],
        "points",
    ] = scored.loc[
        regular_mask & scored["correct"],
        "confidence",
    ]

    scored.loc[
        bonus_mask & scored["correct"],
        "points",
    ] = bonus_points

    scored["points"] = scored["points"].astype(int)

    standings = (
            scored.groupby("player_id", as_index=False)["points"]
            .sum()
            .merge(
                players,
                on="player_id",
                how="left",
                validate="one_to_one",
            )
            .sort_values(
                ["points", "name"],
                ascending=[False,True],
            )
            )
    return standings[["player_id", "name", "points"]].reset_index(drop=True)
