"""Reencontros na temporada: placar do último jogo entre os dois times, quando já se enfrentaram antes.

Na temporada regular isso só acontece entre rivais de divisão (que se enfrentam duas vezes);
nos playoffs, entre quaisquer times que já tenham jogado entre si na temporada.
"""
from .stats import POSTSEASON, local_kickoff


def last_meeting(rows, away, home, week, tz_name="America/Sao_Paulo"):
    """Último jogo já disputado entre os dois times, em semana anterior à `week`. None se não houver."""
    pair = {away, home}
    done = [
        r for r in rows
        if {r.get("away_team"), r.get("home_team")} == pair
        and r.get("home_score") is not None and r.get("away_score") is not None
        and r["week"] < week
    ]
    if not done:
        return None
    r = max(done, key=lambda r: (r["week"], str(r.get("gameday") or ""), str(r.get("gametime") or "")))
    day, _ = local_kickoff(r.get("gameday"), r.get("gametime"), tz_name)
    return {
        "week": r["week"],
        "round": POSTSEASON.get(r.get("game_type")),   # None na temporada regular
        "day": day,
        "away": r["away_team"], "as": r["away_score"],
        "home": r["home_team"], "hs": r["home_score"],
    }


def attach_last_meetings(rows, mu, tz_name="America/Sao_Paulo"):
    """Acrescenta 'previous' a cada jogo de mu (None quando os times ainda não se enfrentaram)."""
    if not mu:
        return
    for g in mu["games"]:
        g["previous"] = last_meeting(rows, g["away"]["abbr"], g["home"]["abbr"], mu["week"], tz_name)