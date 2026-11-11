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
