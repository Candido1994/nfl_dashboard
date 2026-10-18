from nfl_dashboard.stats import compute_ranks


def _team(abbr, **vals):
    return {"abbr": abbr, "s": vals}


def test_ranking_respeita_maior_e_menor_melhor():
    teams = [
        _team("A", pf=30, pa=10),
        _team("B", pf=20, pa=20),
        _team("C", pf=10, pa=30),
    ]
    r = compute_ranks(teams, "s")
    assert r["pf"] == {"A": 1, "B": 2, "C": 3}   # mais pontos feitos = melhor
    assert r["pa"] == {"A": 1, "B": 2, "C": 3}   # menos pontos cedidos = melhor


def test_empates_dividem_a_mesma_posicao_e_none_e_ignorado():
    teams = [_team("A", pf=20), _team("B", pf=20), _team("C", pf=10), _team("D", pf=None)]
    r = compute_ranks(teams, "s")
    assert r["pf"] == {"A": 1, "B": 1, "C": 3}
