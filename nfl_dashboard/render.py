"""Monta as páginas HTML a partir de templates/, static/ e dos dados calculados."""
import json
import shutil
from datetime import datetime
from pathlib import Path

from .config import GOATCOUNTER_URL, REPO_URL

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"

# chave -> configuração da página (a ordem define a ordem das abas)
PAGES = {
    "painel": {
        "file": "index.html", "tab": "Painel", "title": "NFL – Painel semanal",
        "body_class": "dash",
    },
    "confrontos": {
        "file": "confrontos.html", "tab": "Confrontos", "title": "NFL – Confrontos da semana",
        "body_class": "narrow",
    },
    "evolucao": {
        "file": "evolucao.html", "tab": "Evolução", "title": "NFL – Evolução semanal",
        "body_class": "mid",
    },
    "jogadores": {
        "file": "jogadores.html", "tab": "Jogadores", "title": "NFL – Jogadores",
        "body_class": "dash",
    },
}

# páginas fora do menu (sem aba, sem contador de acessos e com cabeçalhos de segurança)
HIDDEN_PAGES = {
    "admin": {
        "file": "admin.html", "tab": "Admin", "title": "NFL – Transmissões (admin)",
        "body_class": "narrow",
    },
}

# A página admin só pode falar com a API do GitHub (limita para onde um token poderia ser enviado).
ADMIN_HEAD = (
    '<meta name="robots" content="noindex,nofollow">\n'
    '<meta name="referrer" content="no-referrer">\n'
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
    "script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src https://api.github.com; "
    "base-uri 'none'; form-action 'none'\">"
)


def _page(key):
    return PAGES.get(key) or HIDDEN_PAGES[key]


def _nav(active):
    links = []
    for key, p in PAGES.items():
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{p["file"]}"{cur}>{p["tab"]}</a>')
    return "".join(links)


def _json_for_script(data):
    """JSON seguro para ficar dentro de <script> (evita fechar a tag por acidente)."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_page(key, data, version=None):
    page = _page(key)
    hidden = key in HIDDEN_PAGES
    layout = (TEMPLATES / "layout.html").read_text(encoding="utf-8")
    content = (TEMPLATES / "pages" / f"{key}.html").read_text(encoding="utf-8")
    use_counter = bool(GOATCOUNTER_URL) and not hidden
    values = {
        "TITLE": page["title"],
        "H1": page["title"],
        "BODY_CLASS": page["body_class"],
        "NAV": _nav(key),
        "VERSION": version or datetime.now().strftime("%Y%m%d%H%M%S"),
        "SCRIPT": key,
        "REPO_URL": REPO_URL,
        "HEAD_EXTRA": ADMIN_HEAD if hidden else "",
        "ANALYTICS": (
            f'<script data-goatcounter="{GOATCOUNTER_URL}" async src="https://gc.zgo.at/count.js"></script>'
            if use_counter else ""
        ),
        "ANALYTICS_NOTE": (
            "<p>Contagem de acessos anônima e sem cookies (GoatCounter).</p>" if use_counter else ""
        ),
    }
    html = layout
    for name, value in values.items():
        html = html.replace("{{" + name + "}}", value)
    # conteúdo e dados por último: não são reprocessados pelas trocas acima
    html = html.replace("{{CONTENT}}", content)
    return html.replace("{{DATA}}", _json_for_script(data))


def write_site(out_dir, pages_data):
    """Copia static/ e grava uma página HTML por chave de pages_data. Retorna os caminhos gravados."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(STATIC, out / "static", dirs_exist_ok=True)
    version = datetime.now().strftime("%Y%m%d%H%M%S")
    written = []
    for key, data in pages_data.items():
        path = out / _page(key)["file"]
        path.write_text(render_page(key, data, version), encoding="utf-8")
        written.append(path)
    return written