"""Linha de comando: calcula tudo e grava o site em uma pasta."""
import argparse
import os
from datetime import datetime

from .config import DEFAULT_SEASON, METRICS
from .players import PLAYER_META, load_players
from .render import write_site
from .stats import (
    build_games, build_history, build_matchups, build_teams, compute_ranks,
    load_team_info, team_weeks_from,
)


def _now():
    """Data/hora de atualização no fuso do usuário (padrão: Brasília; troque com NFL_TZ)."""
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo(os.environ.get("NFL_TZ", "America/Sao_Paulo")))
    except Exception:  # sem base de fusos (ex.: Windows sem tzdata)
        return datetime.now()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gera o painel semanal da NFL (HTML estático).")
    default_season = int(os.environ.get("NFL_SEASON") or DEFAULT_SEASON)
    parser.add_argument("temporada", nargs="?", type=int, default=default_season,
                        help=f"ano da temporada (padrão: variável NFL_SEASON ou {DEFAULT_SEASON})")
    parser.add_argument("--out", default="site", help="pasta de saída (padrão: site)")
    args = parser.parse_args(argv)
    season = args.temporada

    g = build_games(season)
    info = load_team_info()
    teams = build_teams(g, info)
    updated = _now().strftime("%d/%m/%Y %H:%M")
    week = int(g["week"].max() or 0)
    metrics = [{"k": k, "l": l, "hb": hb} for k, l, hb in METRICS]

    mu = build_matchups(season, info, {t["abbr"]: t for t in teams})
    weeks, hteams = build_history(g, info)

    pages = {
        "painel": {
            "season": season, "week": week, "updated": updated,
            "metrics": metrics, "teams": teams,
        },
        "confrontos": {
            "season": season, "updated": updated, "metrics": metrics,
            "nteams": sum(1 for t in teams if t.get("s")),
            "ranks": {w: compute_ranks(teams, w) for w in ("s", "w3", "w1")},
            **(mu or {"week": None, "games": [], "bye": []}),
        },
        "evolucao": {
            "season": season, "updated": updated,
            "metrics": metrics + [{"k": "pct", "l": "Aproveitamento", "hb": 1}],
            "weeks": weeks, "teams": hteams,
        },
        "jogadores": {
            "season": season, "updated": updated, "week": week,
            "teams": [{"abbr": t["abbr"], "label": t["label"]}
                      for t in sorted(teams, key=lambda t: t["label"])],
            "cats": PLAYER_META,
            "players": load_players(season, team_weeks_from(g)),
        },
    }
    for path in write_site(args.out, pages):
        print(f"OK: {path}")
    if not mu:
        print("Aviso: sem jogos pendentes (temporada regular encerrada ou ainda sem calendário).")
    return 0
