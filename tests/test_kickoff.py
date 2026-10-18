from nfl_dashboard.stats import local_kickoff


def test_horario_de_verao_dos_eua():
    # 18/10/2026: ET = UTC-4 (horário de verão), Brasília = UTC-3
    assert local_kickoff("2026-10-18", "13:00", "America/Sao_Paulo") == ("dom, 18/10", "14:00")


def test_fim_do_horario_de_verao_dos_eua():
    # 08/11/2026: ET = UTC-5, Brasília = UTC-3
    assert local_kickoff("2026-11-08", "13:00", "America/Sao_Paulo") == ("dom, 08/11", "15:00")


def test_virada_de_dia():
    assert local_kickoff("2026-10-18", "23:30", "America/Sao_Paulo") == ("seg, 19/10", "00:30")


def test_sem_horario_definido_e_fuso_invalido():
    assert local_kickoff("2026-10-18", None, "America/Sao_Paulo") == ("dom, 18/10", "horário a definir")
    assert local_kickoff("2026-10-18", "13:00", "Fuso/Invalido") == ("2026-10-18", "13:00 ET")
