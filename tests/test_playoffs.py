# tests/test_playoffs.py
import pytest

from nfl_dashboard.playoffs import aproveitamento, build_games, campanha, closed_week


def jogo(semana, mand, visit, pm, pv, tipo="REG"):
    return {"week": semana, "game_type": tipo, "home_team": mand, "away_team": visit,
            "home_score": pm, "away_score": pv}


INFO = {
    "BUF": {"team_conf": "AFC", "team_division": "AFC East"},
    "NYJ": {"team_conf": "AFC", "team_division": "AFC East"},
    "KC": {"team_conf": "AFC", "team_division": "AFC West"},
}


def test_closed_week_so_considera_semanas_com_todos_os_placares():
    rows = [
        jogo(1, "BUF", "NYJ", 20, 10),
        jogo(2, "BUF", "KC", 30, 3),
        jogo(2, "NYJ", "KC", None, None),   # semana 2 ainda não fechada
    ]
    assert closed_week(rows) == 1


def test_closed_week_sem_jogos_devolve_none():
    assert closed_week([]) is None
    assert closed_week([jogo(1, "BUF", "NYJ", None, None)]) is None


def test_closed_week_ignora_playoffs():
    assert closed_week([jogo(19, "BUF", "NYJ", 20, 10, tipo="WC")]) is None


def test_aproveitamento_conta_empate_como_meio_jogo():
    jogos = [
        {"team": "BUF", "opp": "NYJ", "pf": 20, "pa": 10},   # vitória
        {"team": "BUF", "opp": "KC", "pf": 17, "pa": 17},    # empate
    ]
    assert aproveitamento(jogos) == pytest.approx(0.75)
    assert campanha(jogos, "BUF") == (1, 0, 1)


def test_aproveitamento_sem_jogos_devolve_none():
    assert aproveitamento([]) is None


def test_build_games_cria_uma_linha_por_time_e_usa_touchdowns():
    rows = [jogo(1, "BUF", "NYJ", 24, 14)]
    tds = {(1, "BUF"): 3, (1, "NYJ"): 2}
    jogos = build_games(rows, INFO, tds, through=1)
    casa = next(j for j in jogos if j["team"] == "BUF")
    fora = next(j for j in jogos if j["team"] == "NYJ")
    assert (casa["pf"], casa["pa"], casa["td_for"], casa["td_against"]) == (24, 14, 3, 2)
    assert (fora["pf"], fora["pa"], fora["td_for"], fora["td_against"]) == (14, 24, 2, 3)
    assert casa["conf"] and casa["div"]


def test_build_games_respeita_a_semana_limite():
    rows = [jogo(1, "BUF", "NYJ", 24, 14), jogo(2, "BUF", "KC", 10, 7)]
    tds = {(1, "BUF"): 1, (1, "NYJ"): 1, (2, "BUF"): 1, (2, "KC"): 1}
    assert len(build_games(rows, INFO, tds, through=1)) == 2


def test_build_games_falha_sem_touchdowns_em_vez_de_zerar():
    rows = [jogo(1, "BUF", "NYJ", 24, 14)]
    with pytest.raises(ValueError, match="touchdowns ausentes"):
        build_games(rows, INFO, {(1, "BUF"): 3}, through=1)


from nfl_dashboard.playoffs import (
    CADEIA_CRUZ, CADEIA_DIV, _contexto, c_h2h, c_interna, c_pct, ordena,
)


def _ctx(jogos, divisao=None):
    return _contexto(jogos, divisao or {})


def par(a, b, pa, pb, semana=1):
    """Jogo entre a e b: pa pontos de a, pb pontos de b (sem campos de divisão, só para ordenação)."""
    return [
        {"team": a, "opp": b, "week": semana, "pf": pa, "pa": pb, "td_for": 0, "td_against": 0, "conf": True, "div": False},
        {"team": b, "opp": a, "week": semana, "pf": pb, "pa": pa, "td_for": 0, "td_against": 0, "conf": True, "div": False},
    ]


def test_confronto_direto_desempata_dois_times_com_mesmo_aproveitamento():
    jogos = par("A", "B", 20, 10) + par("A", "C", 10, 20) + par("B", "C", 20, 10)
    # A e B estão 1-1 em aproveitamento; A venceu B.
    ctx = _ctx(jogos)
    assert ordena(["B", "A"], [c_pct, c_h2h], ctx) == ["A", "B"]


def test_com_tres_times_sem_varredura_o_confronto_direto_e_ignorado():
    jogos = par("A", "B", 20, 10) + par("B", "C", 20, 10) + par("C", "A", 20, 10)  # ciclo
    ctx = _ctx(jogos)
    ctx["varredura"] = True
    assert c_h2h("A", ["A", "B", "C"], ctx) is None


def test_com_tres_times_a_varredura_classifica_o_time_que_venceu_todos():
    jogos = par("A", "B", 20, 10) + par("A", "C", 20, 10) + par("B", "C", 20, 10)
    ctx = _ctx(jogos)
    ctx["varredura"] = True
    assert c_h2h("A", ["A", "B", "C"], ctx) == 1.0
    assert ordena(["C", "B", "A"], [c_h2h], ctx) == ["A", "B", "C"]


def test_reinicio_depois_de_separar_um_time():
    # A (1,0) fica à frente; B e C empatam em aproveitamento e B vence C no confronto direto.
    jogos = par("A", "B", 20, 10) + par("A", "C", 20, 10) + par("B", "C", 20, 10)
    ctx = _ctx(jogos)
    ctx["varredura"] = False
    assert ordena(["C", "B", "A"], [c_pct, c_h2h], ctx) == ["A", "B", "C"]


def test_empate_total_marca_sorteio_e_ordena_por_sigla():
    jogos = par("B", "A", 10, 10) + par("C", "A", 10, 10)
    ctx = _ctx(jogos)
    assert ordena(["C", "A"], [c_pct], ctx) == ["A", "C"]
    assert ctx["sorteio"] == {"A", "C"}


def test_time_sem_jogos_fica_por_ultimo_sem_quebrar():
    jogos = par("A", "B", 20, 10)
    ctx = _ctx(jogos)
    assert ordena(["Z", "A", "B"], [c_pct], ctx)[-1] == "Z"


def test_cadeias_tem_os_criterios_das_regras_na_ordem():
    assert CADEIA_DIV[0] is c_pct and CADEIA_CRUZ[0] is c_pct
    assert len(CADEIA_DIV) == 12 and len(CADEIA_CRUZ) == 12


def test_interna_nao_vaza_sorteio_quando_a_divisao_empata_totalmente():
    # A e B (mesma divisão) empatam em todos os critérios da divisão; C (outra divisão) perde para D.
    jogos = par("A", "D", 20, 10) + par("B", "D", 20, 10) + par("C", "D", 10, 20)
    ctx = _ctx(jogos, {"A": "X", "B": "X", "C": "Y", "D": "Z"})
    grupo = ["A", "B", "C"]
    assert c_interna("A", grupo, ctx) is None
    assert c_interna("B", grupo, ctx) is None
    assert ctx["sorteio"] == set()
