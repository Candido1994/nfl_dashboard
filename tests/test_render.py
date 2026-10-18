import re

from nfl_dashboard.render import PAGES, render_page, write_site


def test_todas_as_paginas_renderizam_sem_placeholders():
    for key in PAGES:
        html = render_page(key, {"season": 2026, "weeks": [], "teams": [], "metrics": []}, "v1")
        assert "{{" not in html, key
        assert f'static/js/{key}.js?v=v1' in html
        assert html.count('aria-current="page"') == 1


def test_aba_ativa_e_links():
    html = render_page("evolucao", {}, "v1")
    assert '<a href="evolucao.html" aria-current="page">Evolução</a>' in html
    for p in PAGES.values():
        assert f'href="{p["file"]}"' in html


def test_json_nao_fecha_a_tag_script():
    html = render_page("painel", {"x": "</script><b>"}, "v1")
    assert html.count("</script>") == 2  # dados + arquivo js
    assert "<\\/script>" in html


def test_write_site_copia_static_e_grava_paginas(tmp_path):
    data = {k: {} for k in PAGES}
    written = write_site(tmp_path, data)
    assert {p.name for p in written} == {p["file"] for p in PAGES.values()}
    assert (tmp_path / "static" / "css" / "style.css").exists()
    for key in PAGES:
        assert (tmp_path / "static" / "js" / f"{key}.js").exists()



def test_contador_de_acessos_so_aparece_quando_configurado(monkeypatch):
    import nfl_dashboard.render as render

    monkeypatch.setattr(render, "GOATCOUNTER_URL", "")
    assert "goatcounter" not in render.render_page("painel", {}, "v1").lower()

    monkeypatch.setattr(render, "GOATCOUNTER_URL", "https://exemplo.goatcounter.com/count")
    html = render.render_page("painel", {}, "v1")
    assert 'data-goatcounter="https://exemplo.goatcounter.com/count"' in html
    assert "sem cookies" in html and "{{" not in html
    