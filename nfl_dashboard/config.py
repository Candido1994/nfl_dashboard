"""Configuração do projeto: métricas exibidas nas páginas."""

DEFAULT_SEASON = 2026

# (chave, rótulo, maior_é_melhor) -- a ordem define as colunas do painel
METRICS = [
    ("pf", "Pontos feitos", 1),
    ("pa", "Pontos cedidos", 0),
    ("pd", "Saldo de pontos", 1),
    ("pass_yds", "Jd aéreas feitas", 1),
    ("pass_yds_a", "Jd aéreas cedidas", 0),
    ("rush_yds", "Jd corridas feitas", 1),
    ("rush_yds_a", "Jd corridas cedidas", 0),
    ("yd_diff", "Saldo de jardas", 1),
    ("to_lost", "Turnovers cedidos", 0),
    ("to_gain", "Turnovers forçados", 1),
    ("to_diff", "Saldo de turnovers", 1),
    ("sacks_taken", "Sacks sofridos", 0),
    ("sacks_made", "Sacks aplicados", 1),
    ("ypp", "Jd/jogada (ataque)", 1),
    ("ypp_a", "Jd/jogada (defesa)", 0),
    ("epa", "EPA/jogada (ataque)", 1),
    ("epa_a", "EPA/jogada (defesa)", 0),
    ("sr", "Success rate % (ataque)", 1),
    ("sr_a", "Success rate % (defesa)", 0),
]

# métricas calculadas como razão de somas (não como média simples por jogo)
RATIOS = ("ypp", "ypp_a", "epa", "epa_a", "sr", "sr_a")
# métricas que são médias simples por jogo
BASE = [k for k, _, _ in METRICS if k not in RATIOS]
