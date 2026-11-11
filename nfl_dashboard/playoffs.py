"""Classificação dos playoffs: seeds 1 a 7 por conferência e chaveamento do Wild Card.

Funções puras sobre as linhas do calendário e dos touchdowns já carregados, para serem testadas
sem internet. Regras: docs/regras.md (seção 9) e docs/superpowers/specs/2026-11-10-playoffs-design.md.
"""

from .stats import label


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


def _contexto(jogos, divisao):
    """Dados compartilhados pelos critérios: jogos fechados, totais de cada time e divisão de cada sigla."""
    rec = {}
    for t in {j["team"] for j in jogos}:
        mine = [j for j in jogos if j["team"] == t]
        rec[t] = (sum(_res(j) for j in mine), len(mine))
    return {"jogos": jogos, "rec": rec, "div": divisao, "sorteio": set(), "varredura": False, "minimo": 1}


def _do(ctx, t):
    return [j for j in ctx["jogos"] if j["team"] == t]


def _agregado(times, ctx):
    """Aproveitamento somado de uma lista de times (times repetidos contam de novo)."""
    v = sum(ctx["rec"][o][0] for o in times if o in ctx["rec"])
    g = sum(ctx["rec"][o][1] for o in times if o in ctx["rec"])
    return v / g if g else None


def c_pct(t, grupo, ctx):
    v = aproveitamento(_do(ctx, t))
    return -1.0 if v is None else v   # sem jogos: fica por último


def c_interna(t, grupo, ctx):
    irmaos = [o for o in grupo if ctx["div"][o] == ctx["div"][t]]
    if len(irmaos) < 2:
        return None
    teste = dict(ctx, sorteio=set())
    ordem = ordena(irmaos, CADEIA_DIV, teste)
    if teste["sorteio"]:
        return None
    return -ordem.index(t)


def c_h2h(t, grupo, ctx):
    outros = {o for o in grupo if o != t}
    jogos = [j for j in _do(ctx, t) if j["opp"] in outros]
    if not jogos:
        return None
    if ctx["varredura"] and len(outros) > 1:
        if {j["opp"] for j in jogos if _res(j) == 1.0} == outros:
            return 1.0
        if {j["opp"] for j in jogos if _res(j) == 0.0} == outros:
            return 0.0
        return None
    return sum(_res(j) for j in jogos) / len(jogos)


def c_divisao(t, grupo, ctx):
    return aproveitamento([j for j in _do(ctx, t) if j["div"]])


def c_conferencia(t, grupo, ctx):
    return aproveitamento([j for j in _do(ctx, t) if j["conf"]])


def _comuns(grupo, ctx):
    conjuntos = [{j["opp"] for j in _do(ctx, t)} for t in grupo]
    return set.intersection(*conjuntos) if conjuntos else set()


def c_comuns(t, grupo, ctx):
    comuns = _comuns(grupo, ctx)
    jogos = [j for j in _do(ctx, t) if j["opp"] in comuns]
    if not jogos or len(jogos) < ctx["minimo"]:
        return None
    return aproveitamento(jogos)


def c_sov(t, grupo, ctx):
    return _agregado({j["opp"] for j in _do(ctx, t) if _res(j) == 1.0}, ctx)


def c_sos(t, grupo, ctx):
    return _agregado([j["opp"] for j in _do(ctx, t)], ctx)


def _media(jogos):
    return sum(j["pf"] - j["pa"] for j in jogos) / len(jogos) if jogos else None


def c_media_conf(t, grupo, ctx):
    return _media([j for j in _do(ctx, t) if j["conf"]])


def c_media_liga(t, grupo, ctx):
    return _media(_do(ctx, t))


def _saldo(jogos):
    return sum(j["pf"] - j["pa"] for j in jogos) if jogos else None


def c_saldo_comuns(t, grupo, ctx):
    comuns = _comuns(grupo, ctx)
    return _saldo([j for j in _do(ctx, t) if j["opp"] in comuns])


def c_saldo_conf(t, grupo, ctx):
    return _saldo([j for j in _do(ctx, t) if j["conf"]])


def c_saldo(t, grupo, ctx):
    return _saldo(_do(ctx, t))


def c_td(t, grupo, ctx):
    jogos = _do(ctx, t)
    return sum(j["td_for"] - j["td_against"] for j in jogos) if jogos else None


CADEIA_DIV = [c_pct, c_h2h, c_divisao, c_comuns, c_conferencia, c_sov, c_sos,
              c_media_conf, c_media_liga, c_saldo_comuns, c_saldo, c_td]

CADEIA_CRUZ = [c_pct, c_interna, c_h2h, c_conferencia, c_comuns, c_sov, c_sos,
               c_media_conf, c_media_liga, c_saldo_conf, c_saldo, c_td]


def ordena(grupo, cadeia, ctx):
    """Ordena times empatados pela cadeia de critérios. Cada critério que separa um time
    (o melhor ou o pior do grupo) posiciona esse time e recomeça a cadeia para os restantes.
    Se nenhum critério separar, o grupo vai para o sorteio pendente (ordem alfabética)."""
    grupo = list(grupo)
    if len(grupo) < 2:
        return grupo
    for crit in cadeia:
        com = {}
        for t in grupo:
            v = crit(t, grupo, ctx)
            if v is not None:
                com[t] = v
        if len(set(com.values())) < 2:
            continue
        topo, fundo = max(com.values()), min(com.values())
        alto = [t for t in grupo if com.get(t) == topo]
        baixo = [t for t in grupo if com.get(t) == fundo]
        if len(alto) == 1:
            return alto + ordena([t for t in grupo if t not in alto], cadeia, ctx)
        if len(baixo) == 1:
            return ordena([t for t in grupo if t not in baixo], cadeia, ctx) + baixo
        return ordena(alto, cadeia, ctx) + ordena([t for t in grupo if t not in alto], cadeia, ctx)
    ctx["sorteio"].update(grupo)
    return sorted(grupo)
