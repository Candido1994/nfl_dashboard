import json

from nfl_dashboard.broadcasts import (
    admin_page, attach_channels, clean_games, game_key, load_broadcasts, parse_repo,
)

CANAIS = [("espn", "ESPN"), ("sportv2", "sportv2"), ("getv", "ge tv"), ("disney", "Disney+")]


def test_game_key():
    assert game_key(2026, 9, "GB", "DET") == "2026_09_GB_DET"
    assert game_key(2026, 19, "NE", "SF") == "2026_19_NE_SF"


def test_clean_games_ignora_canais_desconhecidos_e_ordena():
    raw = {
        "a": ["disney", "espn", "espn", "canal-que-nao-existe"],
        "b": [],
        "c": "espn",
        "d": ["xyz"],
        7: ["espn"],
    }
    assert clean_games(raw, CANAIS) == {"a": ["espn", "disney"]}
    assert clean_games(None, CANAIS) == {}
    assert clean_games([1, 2], CANAIS) == {}


def test_load_broadcasts_arquivo_ausente_invalido_e_valido(tmp_path):
    assert load_broadcasts(tmp_path / "nao-existe.json") == {}
    ruim = tmp_path / "ruim.json"
    ruim.write_text("{ isto não é json", encoding="utf-8")
    assert load_broadcasts(ruim) == {}
    ok = tmp_path / "ok.json"
    ok.write_text(json.dumps({"versao": 1, "jogos": {"2026_09_GB_DET": ["disney", "espn"]}}), encoding="utf-8")
    assert load_broadcasts(ok) == {"2026_09_GB_DET": ["espn", "disney"]}
    vazio = tmp_path / "vazio.json"
    vazio.write_text(json.dumps({"versao": 1, "jogos": {}}), encoding="utf-8")
    assert load_broadcasts(vazio) == {}


def test_attach_channels_marca_so_os_jogos_informados():
    mu = {"week": 9, "games": [
        {"away": {"abbr": "GB"}, "home": {"abbr": "DET"}},
        {"away": {"abbr": "KC"}, "home": {"abbr": "BUF"}},
    ]}
    attach_channels(2026, mu, {"2026_09_GB_DET": ["espn", "disney"]}, CANAIS)
    assert mu["games"][0]["key"] == "2026_09_GB_DET"
    assert mu["games"][0]["canais"] == ["ESPN", "Disney+"]
    assert mu["games"][1]["canais"] == []
    attach_channels(2026, None, {}, CANAIS)  # sem jogos: não faz nada


def _row(gt, week, away, home, score=None, day="2026-11-01"):
    return {"game_type": gt, "week": week, "away_team": away, "home_team": home,
            "home_score": score, "away_score": None if score is None else 10,
            "gameday": day, "gametime": "13:00"}


def test_admin_page_lista_semana_atual_pendente_e_a_seguinte():
    rows = [
        _row("REG", 8, "AAA", "BBB", 20),
        _row("REG", 9, "GB", "DET", None, "2026-11-01"),
        _row("REG", 9, "KC", "BUF", 24, "2026-10-29"),     # já disputado: fica de fora
        _row("REG", 10, "NE", "SF", None, "2026-11-08"),
        _row("REG", 11, "DAL", "NYG", None, "2026-11-15"),  # duas semanas depois: fica de fora
    ]
    info = {"GB": {"team_nick": "Packers"}, "DET": {"team_nick": "Lions"}}
    page = admin_page(2026, rows, info, "America/Sao_Paulo", {"2026_09_GB_DET": ["espn"]}, "x",
                      "https://github.com/dono/repo", CANAIS)
    assert [g["key"] for g in page["games"]] == ["2026_09_GB_DET", "2026_10_NE_SF"]
    assert page["games"][0]["canais"] == ["espn"] and page["games"][1]["canais"] == []
    assert page["games"][0]["away"] == "GB - Packers"
    assert page["games"][0]["round"] is None
    assert page["channels"][3] == {"id": "disney", "label": "Disney+"}
    assert page["repo"] == {"owner": "dono", "name": "repo", "branch": "main", "path": "data/transmissoes.json"}


def test_admin_page_nos_playoffs_lista_so_a_rodada_atual():
    rows = [_row("REG", 18, "AAA", "BBB", 20), _row("WC", 19, "NE", "SF"), _row("WC", 19, "KC", "BUF")]
    page = admin_page(2026, rows, {}, "America/Sao_Paulo", {}, "x", "https://github.com/dono/repo", CANAIS)
    assert len(page["games"]) == 2 and all(g["round"] == "Wild Card" for g in page["games"])


def test_admin_page_sem_calendario_ou_sem_jogos():
    assert admin_page(2026, [], {}, "America/Sao_Paulo", {}, "x", "https://github.com/a/b")["games"] == []


def test_parse_repo():
    assert parse_repo("https://github.com/Candido1994/nfl_dashboard/")["owner"] == "Candido1994"
    assert parse_repo("")["name"] == ""