"""Testes de orquestração do cli.main (garante que cada base do nflverse é baixada uma só vez)."""
import polars as pl

from nfl_dashboard import cli


def test_cli_carrega_cada_base_apenas_uma_vez(monkeypatch, tmp_path):
    import nflreadpy

    chamadas = {"schedules": 0, "team_stats": 0, "teams": 0, "pbp": 0, "player_stats": 0}

    sched = pl.DataFrame([
        {
            "game_type": "REG", "week": 1, "away_team": "BUF", "home_team": "KC",
            "away_score": 20, "home_score": 24, "gameday": "2026-09-10",
            "gametime": "20:20", "location": "Home",
        },
        {
            "game_type": "REG", "week": 1, "away_team": "NE", "home_team": "MIA",
            "away_score": None, "home_score": None, "gameday": "2026-09-13",
            "gametime": "13:00", "location": "Home",
        },
    ])
    ts = pl.DataFrame([
        {
            "season_type": "REG", "week": 1, "team": t,
            "passing_yards": 250, "rushing_yards": 100,
            "passing_interceptions": 1, "sack_fumbles_lost": 0,
            "rushing_fumbles_lost": 0, "receiving_fumbles_lost": 0,
            "sacks_suffered": 2, "attempts": 30, "carries": 25,
            "passing_tds": 2, "rushing_tds": 1, "def_tds": 0,
            "special_teams_tds": 0, "pt_return_tds": 0, "fumble_recovery_tds": 0,
        }
        for t in ("BUF", "KC")
    ])
    teams = pl.DataFrame([
        {
            "team_abbr": abbr, "team_name": name, "team_nick": nick,
            "team_conf": "AFC", "team_division": "AFC East", "team_color": "#00338D",
        }
        for abbr, name, nick in (
            ("BUF", "Buffalo Bills", "Bills"),
            ("KC", "Kansas City Chiefs", "Chiefs"),
            ("NE", "New England Patriots", "Patriots"),
            ("MIA", "Miami Dolphins", "Dolphins"),
        )
    ])
    pbp = pl.DataFrame([
        {"season_type": "REG", "week": 1, "posteam": "BUF", "play_type": "pass", "epa": 0.2, "success": 1},
        {"season_type": "REG", "week": 1, "posteam": "KC", "play_type": "run", "epa": 0.1, "success": 1},
    ])
    ps = pl.DataFrame([
        {
            "season_type": "REG", "week": 1, "player_id": "P1",
            "player_display_name": "J. Allen", "team": "BUF", "position": "QB",
            "attempts": 30, "completions": 20, "passing_yards": 250, "passing_tds": 2,
        }
    ])

    def fake_schedules(seasons):
        chamadas["schedules"] += 1
        return sched

    def fake_team_stats(seasons, summary_level="week"):
        chamadas["team_stats"] += 1
        return ts

    def fake_teams():
        chamadas["teams"] += 1
        return teams

    def fake_pbp(seasons):
        chamadas["pbp"] += 1
        return pbp

    def fake_player_stats(seasons, summary_level="week"):
        chamadas["player_stats"] += 1
        return ps

    monkeypatch.setattr(nflreadpy, "load_schedules", fake_schedules)
    monkeypatch.setattr(nflreadpy, "load_team_stats", fake_team_stats)
    monkeypatch.setattr(nflreadpy, "load_teams", fake_teams)
    monkeypatch.setattr(nflreadpy, "load_pbp", fake_pbp)
    monkeypatch.setattr(nflreadpy, "load_player_stats", fake_player_stats)

    assert cli.main(["2026", "--out", str(tmp_path)]) == 0
    assert chamadas == {"schedules": 1, "team_stats": 1, "teams": 1, "pbp": 1, "player_stats": 1}
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "playoffs.html").exists()
