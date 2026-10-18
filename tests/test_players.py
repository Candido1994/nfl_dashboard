from nfl_dashboard.players import build_player_pages


def _rows(pid, name, pos, team, weeks=range(1, 6), **stats):
    return [{"player_id": pid, "player_display_name": name, "position": pos,
             "team": team, "week": w, **stats} for w in weeks]


def test_qb_janelas_e_rating():
    rows = _rows("q1", "QB Um", "QB", "NE", attempts=30, completions=20, passing_yards=250,
                 passing_tds=2, passing_interceptions=1, sacks_suffered=2, passing_epa=3.0)
    out = build_player_pages(rows, {"NE": [1, 2, 3, 4, 5]})
    qb = out["qb"][0]
    assert qb["s"]["gp"] == 5 and qb["w3"]["gp"] == 3 and qb["w1"]["gp"] == 1
    assert qb["s"]["att"] == 150 and qb["s"]["yds"] == 1250
    assert qb["s"]["rtg"] == round(qb["w1"]["rtg"], 1)  # mesmas médias por jogo


def test_quem_entra_em_cada_lista():
    rows = (
        _rows("r1", "RB", "RB", "SF", carries=15, rushing_yards=70)
        + _rows("w1", "WR", "WR", "SF", targets=6, receptions=4, receiving_yards=50)
        + _rows("k1", "K", "K", "SF", fg_att=2, fg_made=2, fg_long=44)
        + _rows("x1", "Sem stats", "QB", "SF", attempts=None)
    )
    out = build_player_pages(rows, {"SF": [1, 2, 3, 4, 5]})
    assert [p["n"] for p in out["rb"]] == ["RB"]
    assert [p["n"] for p in out["rec"]] == ["WR"]
    assert [p["n"] for p in out["k"]] == ["K"]
    assert out["qb"] == []
    assert out["k"][0]["s"]["lng"] == 44  # maior valor, não a soma
