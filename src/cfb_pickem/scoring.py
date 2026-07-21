from pathlib import Path

import pandas as pd

def score_week(data_dir: Path) -> pd.DataFrame:
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
    return standings[["player_id", "name", "points"]]
