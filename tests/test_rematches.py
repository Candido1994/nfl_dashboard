from nfl_dashboard.rematches import attach_last_meetings, last_meeting


def _r(gt, week, away, home, a=None, h=None, day="2026-10-04"):
    return {"game_type": gt, "week": week, "away_team": away, "home_team": home,
            "away_score": a, "home_score": h, "gameday": day, "gametime": "13:00"}


ROWS = [
    _r("REG", 5, "GB", "DET", 24, 20, "2026-10-04"),
    _r("REG", 6, "KC", "BUF", 31, 28, "2026-10-11"),
    _r("REG", 12, "DET", "GB", None, None, "2026-11-22"),   # o jogo de agora (ainda sem placar)
]


def test_rival_de_divisao_que_ja_se_enfrentou():
    p = last_meeting(ROWS, "DET", "GB", 12)
    assert p["week"] == 5 and p["round"] is None
    # placar na orientação em que o jogo aconteceu (GB visitante, DET mandante)
    assert (p["away"], p["as"], p["home"], p["hs"]) == ("GB", 24, "DET", 20)
    assert p["day"] == "dom, 04/10"


def test_sem_encontro_anterior():
    assert last_meeting(ROWS, "KC", "DAL", 12) is None
    assert last_meeting(ROWS, "DET", "GB", 5) is None      # o jogo é da mesma semana: não conta como anterior


def test_pega_o_mais_recente_e_ignora_jogos_sem_placar():
    rows = ROWS + [_r("REG", 9, "DET", "GB", 17, 27, "2026-11-01"), _r("REG", 10, "DET", "GB", None, None)]
    p = last_meeting(rows, "GB", "DET", 12)
    assert p["week"] == 9 and (p["away"], p["as"], p["home"], p["hs"]) == ("DET", 17, "GB", 27)


def test_reencontro_nos_playoffs_informa_a_rodada_anterior():
    rows = ROWS + [_r("WC", 19, "GB", "DET", 21, 14, "2027-01-10")]
    assert last_meeting(rows, "DET", "GB", 20)["round"] == "Wild Card"
    assert last_meeting(rows, "GB", "DET", 20)["week"] == 19


def test_attach_last_meetings_marca_cada_jogo():
    mu = {"week": 12, "games": [
        {"away": {"abbr": "DET"}, "home": {"abbr": "GB"}},
        {"away": {"abbr": "KC"}, "home": {"abbr": "DAL"}},
    ]}
    attach_last_meetings(ROWS, mu)
    assert mu["games"][0]["previous"]["week"] == 5
    assert mu["games"][1]["previous"] is None
    attach_last_meetings(ROWS, None)  # sem jogos: não faz nada