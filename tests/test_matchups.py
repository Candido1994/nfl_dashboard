from nfl_dashboard.stats import select_games


def _g(game_type, week, home_score=None, away="AAA", home="BBB", gameday="2027-01-10"):
    return {"game_type": game_type, "week": week, "away_team": away, "home_team": home,
            "home_score": home_score, "away_score": None if home_score is None else 10,
            "gameday": gameday, "gametime": "13:00"}


def test_temporada_regular_mostra_a_primeira_semana_pendente():
    rows = [_g("REG", 1, 20), _g("REG", 2, 17), _g("REG", 3), _g("REG", 3, away="CCC", home="DDD"), _g("REG", 4)]
    games, rnd, wk = select_games(rows)
    assert rnd is None and wk == 3 and len(games) == 2


def test_fim_da_temporada_regular_sem_playoffs_no_calendario():
    rows = [_g("REG", 17, 20), _g("REG", 18, 24)]
    assert select_games(rows) is None


def test_wild_card_apos_a_temporada_regular():
    rows = [_g("REG", 18, 24), _g("WC", 19), _g("WC", 19, away="CCC", home="DDD")]
    games, rnd, wk = select_games(rows)
    assert rnd == "Wild Card" and wk == 19 and len(games) == 2


def test_avanca_para_a_proxima_rodada_quando_a_anterior_termina():
    rows = [_g("REG", 18, 24), _g("WC", 19, 20), _g("DIV", 20), _g("DIV", 20, away="CCC", home="DDD")]
    games, rnd, wk = select_games(rows)
    assert rnd == "Rodada Divisional" and wk == 20 and len(games) == 2


def test_rodada_em_andamento_continua_visivel_com_placares():
    rows = [_g("REG", 18, 24), _g("WC", 19, 20), _g("WC", 19, away="CCC", home="DDD")]
    games, rnd, _ = select_games(rows)
    assert rnd == "Wild Card" and len(games) == 2  # inclui o jogo já finalizado


def test_depois_do_super_bowl_mostra_o_resultado_final():
    rows = [_g("REG", 18, 24), _g("WC", 19, 20), _g("DIV", 20, 17), _g("CON", 21, 31), _g("SB", 22, 27)]
    games, rnd, wk = select_games(rows)
    assert rnd == "Super Bowl" and wk == 22 and games[0]["home_score"] == 27


def test_jogos_de_playoff_sem_times_definidos_sao_ignorados():
    rows = [_g("REG", 18, 24), {"game_type": "WC", "week": 19, "away_team": None, "home_team": None, "home_score": None}]
    assert select_games(rows) is None


def test_toda_rodada_tem_cor_no_css_e_no_js():
    from pathlib import Path

    from nfl_dashboard.stats import POSTSEASON

    root = Path(__file__).resolve().parent.parent
    css = (root / "static" / "css" / "style.css").read_text(encoding="utf-8")
    js = (root / "static" / "js" / "confrontos.js").read_text(encoding="utf-8")
    for nome in POSTSEASON.values():
        assert f'"{nome}":' in js, nome          # nome da rodada mapeado para uma classe
    for classe in ("wc", "div", "con", "sb"):
        assert f".po-{classe}{{" in css, classe  # classe definida no CSS