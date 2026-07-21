# College Football Pick'em

A Python project for managing and scoring a custom college football confidence pick'em competition.

The planned competition format includes:

* 10 commissioner-selected games each week;
* confidence points assigned to each pick;
* a weekly bonus game based on a changing theme;
* season-long standings;
* restrictions on repeatedly selecting the same teams.

The project is currently in its initial development stage. At present, it can read a set of weekly CSV files and calculate confidence-point standings.

## Project Structure

```text
cfb-pickem/
├── data/
│   └── test_week/
│       ├── players.csv
│       ├── games.csv
│       ├── picks.csv
│       └── results.csv
├── src/
│   └── cfb_pickem/
│       ├── __init__.py
│       ├── scoring.py
│       └── validation.py
├── tests/
│   └── test_scoring.py
├── README.md
└── pyproject.toml
```

## Current Functionality

The `score_week` function:

1. reads player, pick, and result data from CSV files;
2. matches each pick to the corresponding game result;
3. awards the selected confidence value for a correct pick;
4. awards zero points for an incorrect pick;
5. sums points for each player;
6. returns standings sorted from highest to lowest score.

## Input Files

Each weekly data directory must contain the following files.

### `players.csv`

Identifies each participant.

```csv
player_id,name
coleman,Coleman
dad,Dad
zach,Zach
```

### `games.csv`

Lists the games available for selection.

```csv
game_id,away_team,home_team
game_1,Team A,Team B
game_2,Team C,Team D
game_3,Team E,Team F
```

### `picks.csv`

Contains one row for each player's pick in each game.

```csv
player_id,game_id,picked_team,confidence
coleman,game_1,Team A,3
coleman,game_2,Team D,2
coleman,game_3,Team E,1
```

### `results.csv`

Records the winner of each completed game.

```csv
game_id,winner
game_1,Team B
game_2,Team D
game_3,Team F
```

## Development Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Scoring a Test Week

From a Python session:

```python
from pathlib import Path

from cfb_pickem.scoring import score_week

standings = score_week(Path("data/test_week"))
print(standings)
```

Example output:

```text
  player_id     name  points
0      zach     Zach       6
1       dad      Dad       5
2   coleman  Coleman       3
```

## Running Tests

Run the complete test suite from the repository root:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

## Planned Development

Near-term development goals include:

* validating missing or duplicate picks;
* validating confidence values;
* supporting multiple weeks;
* enforcing repeat-team restrictions;
* adding themed bonus games;
* importing responses from Google Forms;
* generating season standings and a leaderboard website.

## Status

This project is under active development and is not yet ready for running a full competition.

