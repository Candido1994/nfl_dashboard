import io

from nfl_dashboard.logos import normalize_color, pick_logo_url, team_colors, to_square_png


def test_normalize_color():
    assert normalize_color("#1f5fbf") == "#1F5FBF"
    assert normalize_color("1F5FBF") == "#1F5FBF"
    assert normalize_color(None) == "#5A685F"
    assert normalize_color("azul") == "#5A685F"
    assert normalize_color("#12345") == "#5A685F"


def test_team_colors_ignora_linhas_sem_sigla():
    rows = [{"team_abbr": "NE", "team_color": "#002244"}, {"team_abbr": "SF"}, {"team_color": "#FFFFFF"}]
    assert team_colors(rows) == {"NE": "#002244", "SF": "#5A685F"}


def test_pick_logo_url_segue_a_ordem_de_preferencia():
    row = {"team_logo_wikipedia": "https://w/x.svg", "team_logo_espn": "https://e/x.png"}
    assert pick_logo_url(row) == "https://e/x.png"
    assert pick_logo_url({"team_logo_wikipedia": "https://w/x.svg"}) == "https://w/x.svg"
    assert pick_logo_url({"team_logo_espn": "", "team_logo_squared": "sem-http"}) is None
    assert pick_logo_url({}) is None


def test_to_square_png_centraliza_com_margem_e_transparencia():
    try:
        from PIL import Image
    except ImportError:  # Pillow só é necessário no computador de quem baixa os logos
        return
    buf = io.BytesIO()
    Image.new("RGBA", (400, 200), (200, 30, 30, 255)).save(buf, "PNG")
    out = Image.open(io.BytesIO(to_square_png(buf.getvalue()))).convert("RGBA")
    assert out.size == (128, 128)
    assert out.getpixel((0, 0))[3] == 0          # canto transparente (margem)
    assert out.getpixel((64, 64))[3] == 255      # centro preenchido
    assert out.getpixel((64, 2))[3] == 0         # faixa de cima vazia (imagem larga fica centralizada)