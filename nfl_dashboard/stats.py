"""Cálculo das estatísticas dos times a partir do nflverse (via nflreadpy)."""
from .config import BASE, METRICS


def build_games(season):
    """Uma linha por time por jogo, com stats do time e do adversário."""
    import nflreadpy as nfl
    import polars as pl

    sched = nfl.load_schedules([season]).filter(
        (pl.col("game_type") == "REG") & pl.col("home_score").is_not_null()
    )
    home = sched.select(
        pl.col("week"),
        pl.col("home_team").alias("team"),
        pl.col("away_team").alias("opp"),
        pl.col("home_score").alias("pf"),
        pl.col("away_score").alias("pa"),
    )
    away = sched.select(
        pl.col("week"),
        pl.col("away_team").alias("team"),
        pl.col("home_team").alias("opp"),
        pl.col("away_score").alias("pf"),
        pl.col("home_score").alias("pa"),
    )
    games = pl.concat([home, away])

    ts = nfl.load_team_stats([season], summary_level="week").filter(
        pl.col("season_type") == "REG"
    )

    def f(c):
        return pl.col(c).fill_null(0)

    # EPA e success rate por time/semana (jogadas de passe e corrida)
    pbp = nfl.load_pbp([season]).filter(
        (pl.col("season_type") == "REG")
        & pl.col("play_type").is_in(["pass", "run"])
        & pl.col("epa").is_not_null()
        & pl.col("posteam").is_not_null()
    )
    pb = pbp.group_by(["week", "posteam"]).agg(
        pl.col("epa").sum().alias("epa_sum"),
        pl.len().alias("epa_n"),
        pl.col("success").fill_null(0).sum().alias("succ_sum"),
    ).rename({"posteam": "team"})

    off = ts.select(
        pl.col("week"),
        pl.col("team"),
        f("passing_yards").alias("pass_yds"),
        f("rushing_yards").alias("rush_yds"),
        (
            f("passing_interceptions")
            + f("sack_fumbles_lost")
            + f("rushing_fumbles_lost")
            + f("receiving_fumbles_lost")
        ).alias("to_lost"),
        f("sacks_suffered").alias("sacks_taken"),
        (f("attempts") + f("carries") + f("sacks_suffered")).alias("plays"),
    ).join(pb, on=["week", "team"], how="left").with_columns(
        pl.col("epa_sum", "epa_n", "succ_sum").fill_null(0)
    )
    opp = off.rename({c: c + "_o" for c in off.columns if c != "week"})

    g = games.join(off, on=["week", "team"]).join(
        opp, left_on=["week", "opp"], right_on=["week", "team_o"]
    )
    return g.with_columns(
        (pl.col("pass_yds_o")).alias("pass_yds_a"),
        (pl.col("rush_yds_o")).alias("rush_yds_a"),
        (pl.col("to_lost_o")).alias("to_gain"),
        (pl.col("sacks_taken_o")).alias("sacks_made"),
        (pl.col("pf") - pl.col("pa")).alias("pd"),
        (pl.col("pass_yds") + pl.col("rush_yds")).alias("tot"),
        (pl.col("pass_yds_o") + pl.col("rush_yds_o")).alias("tot_a"),
    ).with_columns(
        (pl.col("tot") - pl.col("tot_a")).alias("yd_diff"),
        (pl.col("to_gain") - pl.col("to_lost")).alias("to_diff"),
    )


def summarize(df):
    import polars as pl

    n = df.height
    if n == 0:
        return None
    out = {k: df[k].sum() / n for k in BASE}
    out["ypp"] = df["tot"].sum() / df["plays"].sum()
    out["ypp_a"] = df["tot_a"].sum() / df["plays_o"].sum()
    out = {k: round(float(v), 2) for k, v in out.items()}
    out["g"] = n
    w = df.filter(pl.col("pf") > pl.col("pa")).height
    l = df.filter(pl.col("pf") < pl.col("pa")).height
    t = n - w - l
    out["rec"] = f"{w}-{l}" + (f"-{t}" if t else "")
    out["pct"] = round((w + 0.5 * t) / n, 3)

    def ratio(a, b, scale=1, nd=3):
        den = df[b].sum()
        return round(float(df[a].sum()) * scale / den, nd) if den else None

    out["epa"] = ratio("epa_sum", "epa_n")
    out["epa_a"] = ratio("epa_sum_o", "epa_n_o")
    out["sr"] = ratio("succ_sum", "epa_n", 100, 1)
    out["sr_a"] = ratio("succ_sum_o", "epa_n_o", 100, 1)
    return out


def label(abbr, info):
    m = info.get(abbr, {})
    nick = m.get("team_nick") or (m.get("team_name") or abbr).split()[-1]
    return f"{abbr} - {nick}"


def compute_ranks(teams, win="s"):
    """Posição de cada time na liga por métrica (1 = melhor, inclusive na defesa)."""
    ranks = {}
    for k, _, hb in METRICS:
        vals = [
            (t["abbr"], t[win][k])
            for t in teams
            if t.get(win) and t[win].get(k) is not None
        ]
        ranks[k] = {
            a: 1 + sum(1 for _, o in vals if (o > v if hb else o < v)) for a, v in vals
        }
    return ranks


_DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def local_kickoff(gameday, gametime, tz_name):
    """O nflverse informa gameday/gametime no horário do Leste dos EUA (ET).
    Converte para o fuso escolhido e devolve ("dom, 18/10", "14:00")."""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    day = str(gameday or "")[:10]
    if not day:
        return "", ""
    clock = str(gametime or "")[:5]
    try:
        if not clock:
            d = datetime.strptime(day, "%Y-%m-%d")
            return f"{_DIAS[d.weekday()]}, {d:%d/%m}", "horário a definir"
        et = datetime.strptime(f"{day} {clock}", "%Y-%m-%d %H:%M").replace(
            tzinfo=ZoneInfo("America/New_York")
        )
        loc = et.astimezone(ZoneInfo(tz_name))
        return f"{_DIAS[loc.weekday()]}, {loc:%d/%m}", f"{loc:%H:%M}"
    except Exception:  # fuso inválido ou sem base de fusos: mostra o horário original
        return day, f"{clock} ET" if clock else ""


def divisional(info, a, b):
    """Nome da divisão quando os dois times são da mesma divisão; senão None."""
    da = info.get(a, {}).get("team_division")
    return da if da and da == info.get(b, {}).get("team_division") else None


def build_matchups(season, info, by_abbr, tz_name="America/Sao_Paulo"):
    """Jogos da semana atual (se ainda há jogo pendente) ou da próxima."""
    import nflreadpy as nfl
    import polars as pl

    sched = nfl.load_schedules([season]).filter(pl.col("game_type") == "REG")
    pending = sched.filter(pl.col("home_score").is_null())
    if pending.height == 0:
        return None
    wk = int(pending["week"].min())
    wg = sched.filter(pl.col("week") == wk).sort(["gameday", "gametime"])
    games, playing = [], set()
    for r in wg.to_dicts():
        a, h = r["away_team"], r["home_team"]
        playing |= {a, h}
        empty = lambda x: {"abbr": x, "label": label(x, info), "w1": None, "w3": None, "s": None}
        day, time = local_kickoff(r.get("gameday"), r.get("gametime"), tz_name)
        games.append(
            {
                "away": by_abbr.get(a) or empty(a),
                "home": by_abbr.get(h) or empty(h),
                "day": day,
                "time": time,
                "as": r.get("away_score"),
                "hs": r.get("home_score"),
                "division": divisional(info, a, h),
            }
        )
    bye = sorted(label(a, info) for a in info if a not in playing)
    return {"week": wk, "games": games, "bye": bye}


def build_history(g, info):
    """Acumulado da temporada e janela móvel de 3 jogos ao fim de cada semana."""
    import polars as pl

    weeks = sorted(g["week"].unique().to_list())
    teams = []
    for (team,), d in g.sort("week").partition_by("team", as_dict=True).items():
        series = []
        for w in weeks:
            dd = d.filter(pl.col("week") <= w)
            series.append({"week": w, "s": summarize(dd), "w3": summarize(dd.tail(3))})
        meta = info.get(team, {})
        teams.append(
            {
                "abbr": team,
                "label": label(team, info),
                "conf": meta.get("team_conf", ""),
                "div": meta.get("team_division", ""),
                "series": series,
            }
        )
    return weeks, teams


def load_team_info():
    """Dicionário sigla -> dados do time (nome, conferência, divisão)."""
    import nflreadpy as nfl

    return {
        r["team_abbr"]: r
        for r in nfl.load_teams().select(
            "team_abbr", "team_name", "team_conf", "team_division"
        ).to_dicts()
    }


def build_teams(g, info):
    """Uma entrada por time com as três janelas: último jogo (w1), últimos 3 (w3) e temporada (s)."""
    teams = []
    for (team,), d in g.sort("week").partition_by("team", as_dict=True).items():
        meta = info.get(team, {})
        teams.append(
            {
                "abbr": team,
                "label": label(team, info),
                "name": meta.get("team_name", team),
                "conf": meta.get("team_conf", ""),
                "div": meta.get("team_division", ""),
                "w1": summarize(d.tail(1)),
                "w3": summarize(d.tail(3)),
                "s": summarize(d),
            }
        )
    return teams


def team_weeks_from(g):
    """Semanas em que cada time jogou (para as janelas dos jogadores)."""
    out = {}
    for r in g.select("team", "week").to_dicts():
        out.setdefault(r["team"], set()).add(r["week"])
    return {t: sorted(w) for t, w in out.items()}