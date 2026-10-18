"""Estatísticas de jogadores (QB, corrida, recepção, defesa e kickers)."""


SUM_FIELDS = [
    "attempts", "completions", "passing_yards", "passing_tds", "passing_interceptions",
    "sacks_suffered", "passing_epa",
    "carries", "rushing_yards", "rushing_tds", "rushing_epa", "rushing_fumbles_lost",
    "targets", "receptions", "receiving_yards", "receiving_tds", "receiving_epa",
    "def_tackles_solo", "def_tackle_assists", "def_tackles_with_assist",
    "def_tackles_for_loss", "def_sacks", "def_qb_hits", "def_interceptions",
    "def_pass_defended", "def_fumbles_forced",
    "fg_made", "fg_att", "fg_long", "pat_made", "pat_att",
    "fg_made_40_49", "fg_made_50_59", "fg_made_60_",
]


DEF_KEYS = [
    "def_tackles_solo", "def_tackle_assists", "def_tackles_with_assist", "def_sacks",
    "def_interceptions", "def_pass_defended", "def_tackles_for_loss", "def_qb_hits",
]


def _num(v):
    try:
        return float(v) if v is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def _div(a, b, scale=1, nd=1):
    return round(a * scale / b, nd) if b else None


def _agg(rows):
    a = {k: 0.0 for k in SUM_FIELDS}
    for r in rows:
        for k in SUM_FIELDS:
            v = _num(r.get(k))
            a[k] = max(a[k], v) if k == "fg_long" else a[k] + v
    a["gp"] = len(rows)
    return a


def _stat_qb(a):
    att, cmp_ = a["attempts"], a["completions"]
    yds, td, it = a["passing_yards"], a["passing_tds"], a["passing_interceptions"]
    rtg = None
    if att:
        def c(x):
            return max(0.0, min(2.375, x))
        rtg = round(
            (c((cmp_ / att - 0.3) * 5) + c((yds / att - 3) * 0.25)
             + c(td / att * 20) + c(2.375 - it / att * 25)) / 6 * 100, 1)
    return {
        "gp": int(a["gp"]), "cmp": int(cmp_), "att": int(att), "pct": _div(cmp_, att, 100),
        "yds": int(yds), "ypa": _div(yds, att), "td": int(td), "ints": int(it),
        "sk": int(a["sacks_suffered"]), "rtg": rtg, "epa": round(a["passing_epa"], 1),
        "epa_db": _div(a["passing_epa"], att + a["sacks_suffered"], 1, 2),
    }


def _stat_rb(a):
    return {
        "gp": int(a["gp"]), "car": int(a["carries"]), "yds": int(a["rushing_yards"]),
        "ypc": _div(a["rushing_yards"], a["carries"]), "td": int(a["rushing_tds"]),
        "epa": round(a["rushing_epa"], 1), "fl": int(a["rushing_fumbles_lost"]),
    }


def _stat_rec(a):
    return {
        "gp": int(a["gp"]), "tgt": int(a["targets"]), "rec": int(a["receptions"]),
        "yds": int(a["receiving_yards"]), "ypr": _div(a["receiving_yards"], a["receptions"]),
        "catch": _div(a["receptions"], a["targets"], 100), "td": int(a["receiving_tds"]),
        "epa": round(a["receiving_epa"], 1),
    }


def _stat_def(a):
    solo = a["def_tackles_solo"]
    ast = max(a["def_tackle_assists"], a["def_tackles_with_assist"])
    return {
        "gp": int(a["gp"]), "tk": int(solo + ast), "solo": int(solo), "ast": int(ast),
        "tfl": int(a["def_tackles_for_loss"]), "sacks": round(a["def_sacks"], 1),
        "qbh": int(a["def_qb_hits"]), "ints": int(a["def_interceptions"]),
        "pd": int(a["def_pass_defended"]), "ff": int(a["def_fumbles_forced"]),
    }


def _stat_k(a):
    return {
        "gp": int(a["gp"]), "fgm": int(a["fg_made"]), "fga": int(a["fg_att"]),
        "pct": _div(a["fg_made"], a["fg_att"], 100), "lng": int(a["fg_long"]) or None,
        "fg40": int(a["fg_made_40_49"] + a["fg_made_50_59"] + a["fg_made_60_"]),
        "xpm": int(a["pat_made"]), "xpa": int(a["pat_att"]),
    }


PLAYER_CATS = {
    "qb": {
        "title": "Quarterbacks", "short": "QBs", "sort": "yds", "stat": _stat_qb,
        "gate": lambda a, p: p == "QB" and a["attempts"] > 0,
        "cols": [["gp", "J"], ["cmp", "Cmp"], ["att", "Att"], ["pct", "Cmp%"], ["yds", "Jds"],
                 ["ypa", "Jd/Att"], ["td", "TD"], ["ints", "INT"], ["sk", "Sacks"],
                 ["rtg", "Rating"], ["epa", "EPA"], ["epa_db", "EPA/jogada"]],
    },
    "rb": {
        "title": "Corredores", "short": "Corrida", "sort": "yds", "stat": _stat_rb,
        "gate": lambda a, p: a["carries"] > 0,
        "cols": [["gp", "J"], ["car", "Corridas"], ["yds", "Jds"], ["ypc", "Jd/corrida"],
                 ["td", "TD"], ["epa", "EPA"], ["fl", "Fumbles perdidos"]],
    },
    "rec": {
        "title": "Recebedores", "short": "Recepção", "sort": "yds", "stat": _stat_rec,
        "gate": lambda a, p: a["targets"] > 0 or a["receptions"] > 0,
        "cols": [["gp", "J"], ["tgt", "Alvos"], ["rec", "Recepções"], ["yds", "Jds"],
                 ["ypr", "Jd/rec"], ["catch", "Aproveit. %"], ["td", "TD"], ["epa", "EPA"]],
    },
    "def": {
        "title": "Defesa", "short": "Defesa", "sort": "tk", "stat": _stat_def,
        "gate": lambda a, p: any(a[k] > 0 for k in DEF_KEYS),
        "cols": [["gp", "J"], ["tk", "Tackles"], ["solo", "Solo"], ["ast", "Assist."],
                 ["tfl", "TFL"], ["sacks", "Sacks"], ["qbh", "Hits no QB"], ["ints", "INT"],
                 ["pd", "Passes def."], ["ff", "Fumbles forçados"]],
    },
    "k": {
        "title": "Kickers", "short": "Kickers", "sort": "fgm", "stat": _stat_k,
        "gate": lambda a, p: a["fg_att"] > 0 or a["pat_att"] > 0,
        "cols": [["gp", "J"], ["fgm", "FG feitos"], ["fga", "FG tent."], ["pct", "FG %"],
                 ["lng", "Mais longo"], ["fg40", "FG 40+"], ["xpm", "XP feitos"], ["xpa", "XP tent."]],
    },
}


PLAYER_META = [
    {"k": k, "title": v["title"], "short": v["short"], "cols": v["cols"], "sort": v["sort"]}
    for k, v in PLAYER_CATS.items()
]


def build_player_pages(rows, team_weeks):
    """rows: linhas semanais de load_player_stats (dicts). Janelas contam os jogos do time atual."""
    by_player = {}
    for r in rows:
        pid = r.get("player_id") or r.get("player_display_name") or r.get("player_name")
        if pid is None or r.get("week") is None:
            continue
        by_player.setdefault(pid, []).append(r)
    out = {c: [] for c in PLAYER_CATS}
    for rs in by_player.values():
        rs.sort(key=lambda r: r["week"])
        last = rs[-1]
        team = last.get("team")
        weeks = team_weeks.get(team, [])
        w3, w1 = set(weeks[-3:]), set(weeks[-1:])
        groups = {
            "s": rs,
            "w3": [r for r in rs if r["week"] in w3],
            "w1": [r for r in rs if r["week"] in w1],
        }
        aggs = {w: (_agg(x) if x else None) for w, x in groups.items()}
        pos = last.get("position")
        name = last.get("player_display_name") or last.get("player_name") or str(rs[0].get("player_id"))
        for cat, spec in PLAYER_CATS.items():
            if not spec["gate"](aggs["s"], pos):
                continue
            row = {"n": name, "t": team, "p": pos}
            for w, a in aggs.items():
                row[w] = spec["stat"](a) if a else None
            out[cat].append(row)
    return out


def load_players(season, team_weeks):
    """Nunca derruba a geração das outras páginas."""
    import nflreadpy as nfl
    import polars as pl

    try:
        ps = nfl.load_player_stats([season], summary_level="week")
        if "season_type" in ps.columns:
            ps = ps.filter(pl.col("season_type") == "REG")
        rows = ps.to_dicts()
    except Exception as e:
        print(f"Aviso: não foi possível carregar estatísticas de jogadores ({e}).")
        rows = []
    return build_player_pages(rows, team_weeks)
