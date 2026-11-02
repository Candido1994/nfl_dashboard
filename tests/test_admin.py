from nfl_dashboard.render import ADMIN_HEAD, HIDDEN_PAGES, PAGES, render_page, write_site


def test_admin_fica_fora_do_menu():
    assert "admin" not in PAGES and "admin" in HIDDEN_PAGES
    for key in PAGES:
        assert "admin.html" not in render_page(key, {}, "v1")


def test_admin_tem_cabecalhos_de_seguranca_e_nao_tem_contador():
    html = render_page("admin", {"games": []}, "v1")
    assert "{{" not in html
    assert 'name="robots" content="noindex,nofollow"' in html
    assert "Content-Security-Policy" in html and "connect-src https://api.github.com" in html
    assert "goatcounter" not in html.lower()
    assert "static/js/admin.js?v=v1" in html


def test_paginas_publicas_nao_levam_os_cabecalhos_do_admin():
    html = render_page("painel", {}, "v1")
    assert "Content-Security-Policy" not in html and "noindex" not in html
    assert "goatcounter" in html.lower()  # o contador continua nas páginas públicas


def test_csp_do_admin_so_permite_conexao_com_a_api_do_github():
    assert "default-src 'none'" in ADMIN_HEAD
    assert "connect-src https://api.github.com;" in ADMIN_HEAD
    assert "form-action 'none'" in ADMIN_HEAD


def test_write_site_grava_o_admin(tmp_path):
    written = write_site(tmp_path, {"admin": {"games": []}})
    assert [p.name for p in written] == ["admin.html"]
    assert (tmp_path / "admin.html").exists()