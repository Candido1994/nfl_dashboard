"""Cores e logos dos times.

Os logos são baixados uma única vez, no seu computador, com:
    pip install -r requirements-logos.txt
    python -m nfl_dashboard.logos
Eles ficam em static/img/teams/<sigla>.png (128x128). Sem o arquivo, o site mostra um distintivo com a sigla.
"""
import argparse
import io
import re
from pathlib import Path

SIZE = 128                       # lado do arquivo final, em pixels
MARGIN = 0.06                    # margem interna de cada lado (6%)
DEFAULT_DIR = Path(__file__).resolve().parent.parent / "static" / "img" / "teams"
URL_COLUMNS = ("team_logo_espn", "team_logo_squared", "team_logo_wikipedia")  # ordem de preferência
DEFAULT_COLOR = "#5A685F"

_HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")


def normalize_color(value, default=DEFAULT_COLOR):
    """Devolve '#RRGGBB' em maiúsculas, ou o padrão se o valor não for uma cor válida."""
    m = _HEX.match(str(value or "").strip())
    return f"#{m.group(1).upper()}" if m else default


def team_colors(rows):
    """rows: linhas da tabela de times (dicts). Devolve {sigla: '#RRGGBB'}."""
    return {r["team_abbr"]: normalize_color(r.get("team_color")) for r in rows if r.get("team_abbr")}


def load_team_colors():
    """Cores dos times; nunca derruba a geração do site."""
    try:
        import nflreadpy as nfl

        return team_colors(nfl.load_teams().to_dicts())
    except Exception as e:
        print(f"Aviso: não foi possível carregar as cores dos times ({e}).")
        return {}


def pick_logo_url(row):
    """Primeiro endereço de logo disponível, na ordem de URL_COLUMNS."""
    for col in URL_COLUMNS:
        url = row.get(col)
        if url and str(url).startswith("http"):
            return str(url)
    return None


def to_square_png(data, size=SIZE, margin=MARGIN):
    """Centraliza a imagem em um quadrado transparente size x size, com margem, e devolve os bytes do PNG."""
    from PIL import Image

    img = Image.open(io.BytesIO(data)).convert("RGBA")
    box = int(size * (1 - 2 * margin))
    img.thumbnail((box, box), getattr(Image, "Resampling", Image).LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(img, ((size - img.width) // 2, (size - img.height) // 2), img)
    out = io.BytesIO()
    canvas.save(out, "PNG", optimize=True)
    return out.getvalue()


def download_logos(out_dir=DEFAULT_DIR, force=False):
    """Baixa e converte os logos. Devolve (baixados, existentes, falhas)."""
    import nflreadpy as nfl
    import requests

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    done, skipped, failed = [], [], []
    for row in nfl.load_teams().to_dicts():
        abbr = row.get("team_abbr")
        if not abbr:
            continue
        dest = out / f"{abbr.lower()}.png"
        if dest.exists() and not force:
            skipped.append(abbr)
            continue
        url = pick_logo_url(row)
        if not url:
            failed.append((abbr, "sem endereço de logo na tabela de times"))
            continue
        try:
            resp = requests.get(url, timeout=30, headers={"User-Agent": "nfl-dashboard (uso pessoal)"})
            resp.raise_for_status()
            dest.write_bytes(to_square_png(resp.content))
            done.append(abbr)
        except Exception as e:  # rede, formato não suportado (ex.: SVG) etc.
            failed.append((abbr, str(e)))
    return done, skipped, failed


def main(argv=None):
    parser = argparse.ArgumentParser(description="Baixa os logos dos times (uso único).")
    parser.add_argument("--out", default=str(DEFAULT_DIR), help="pasta de saída (padrão: static/img/teams)")
    parser.add_argument("--force", action="store_true", help="baixar de novo mesmo se o arquivo já existir")
    args = parser.parse_args(argv)
    done, skipped, failed = download_logos(args.out, args.force)
    print(f"Baixados: {len(done)} | já existiam: {len(skipped)} | falhas: {len(failed)}")
    for abbr, why in failed:
        print(f"  falhou {abbr}: {why}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())