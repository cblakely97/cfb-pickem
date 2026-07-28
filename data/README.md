# Data Directory

This directory contains the canonical data format for `cfb-pickem`

## Current Layout (v0.1)

For initial development each week is stored as a standalone directory:

```
week_XX/
├── players.csv
├── games.csv
├── results.csv
└── picks.csv
```

This layout simplifies development and testing by making each week
self-contained.

## Planned layout

Once `cfb-pickem` is able to support full multi-week seasons, the data
structure will become:

```
season_YYYY/
├── players.csv
├── week_01/
│   ├── games.csv
│   ├── picks.csv
│   └── results.csv
└── week_02/
    ├── games.csv
    ├── picks.csv
    └── results.csv
```

In this layout `players.csv` is shared by the entire season and each week
contains week-specific data.

## `players.csv`

One row per participant.

| Column | Type | Description |
|--------|-------|-------------|
| player_id | string | Stable internal identifier |
| name | string | Display name |

## `games.csv`

One row per game.

| Column | Type | Description |
|---------|------|-------------|
| game_id | string | Stable game identifier |
| away_team | string | Away team |
| home_team | string | Home team |

## `picks.csv`

One row per player-game pair.

| Column | Type | Description |
|---------|------|-------------|
| player_id | string | References players.csv |
| game_id | string | References games.csv |
| picked_team | string | Must equal away_team or home_team |
| confidence | integer | Unique value from 1 to N |

## `results.csv`

One row per game.

| Column | Type | Description |
|--------|-------|-------------|
| game_id | string | Stable internal identifier |
| winner | string | Must equal away_team or home_team |
