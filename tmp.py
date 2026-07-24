import pandas as pd

from pathlib import Path

from cfb_pickem.scoring import score_week

from cfb_pickem.validation import check_unknown_players

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

errors = check_unknown_players(players,picks)

print(errors)
exit()

standings = score_week(Path("data/test_week"))
print(standings)
