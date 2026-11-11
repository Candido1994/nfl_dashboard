"""Classificação dos playoffs: seeds 1 a 7 por conferência e chaveamento do Wild Card.

Funções puras sobre as linhas do calendário e dos touchdowns já carregados, para serem testadas
sem internet. Regras: docs/regras.md (seção 9) e docs/superpowers/specs/2026-11-10-playoffs-design.md.
"""


def closed_week(rows):
    """Maior semana da temporada regular em que todos os jogos já têm placar. None se não houver."""
    por_semana = {}
    for r in rows:
        if r.get("game_type") == "REG":
            por_semana.setdefault(r["week"], []).append(r.get("home_score") is not None)
    fechadas = [w for w, feitos in por_semana.items() if all(feitos)]
    return max(fechadas) if fechadas else None


def _res(j):
    """Resultado de um jogo para o time: 1 vitória, 0,5 empate, 0 derrota."""
    if j["pf"] > j["pa"]:
        return 1.0
    return 0.5 if j["pf"] == j["pa"] else 0.0


def aproveitamento(jogos):
    """(V + 0,5 × E) ÷ J, com o valor exato. None sem jogos."""
    if not jogos:
        return None
    return sum(_res(j) for j in jogos) / len(jogos)


def campanha(jogos, team):
    """(vitórias, derrotas, empates) do time."""
    res = [_res(j) for j in jogos if j["team"] == team]
    return (res.count(1.0), res.count(0.0), res.count(0.5))


def _td(tds, semana, team):
    chave = (semana, team)
    if chave not in tds:
        raise ValueError(f"touchdowns ausentes: semana {semana}, {team}")
    return tds[chave]


def build_games(rows, info, tds, through):
    """Uma linha por time por jogo fechado até `through`. `tds[(semana, sigla)]` = touchdowns marcados."""
    jogos = []
    for r in rows:
        if r.get("game_type") != "REG" or r.get("home_score") is None or r["week"] > through:
            continue
        a, h = r["away_team"], r["home_team"]
        mesma_conf = info[a]["team_conf"] == info[h]["team_conf"]
        mesma_div = mesma_conf and info[a]["team_division"] == info[h]["team_division"]
        for team, opp, pf, pa in ((a, h, r["away_score"], r["home_score"]),
                                  (h, a, r["home_score"], r["away_score"])):
            jogos.append({
                "team": team, "opp": opp, "week": r["week"], "pf": pf, "pa": pa,
                "td_for": _td(tds, r["week"], team), "td_against": _td(tds, r["week"], opp),
                "conf": mesma_conf, "div": mesma_div,
            })
    return jogos
