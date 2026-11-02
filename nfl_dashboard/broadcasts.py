"""Transmissões no Brasil.

Lê data/transmissoes.json (preenchido pela página admin) e monta os dados dessa página.
É tudo opcional: sem o arquivo, ou com ele vazio, o site fica exatamente como sem transmissões.
"""
import json
from pathlib import Path

from .config import CHANNELS

BROADCASTS_PATH = Path(__file__).resolve().parent.parent / "data" / "transmissoes.json"
FILE_IN_REPO = "data/transmissoes.json"
BRANCH = "main"


def game_key(season, week, away, home):
    """Identificador estável do jogo no arquivo de transmissões. Ex.: 2026_09_GB_DET."""
    return f"{season}_{int(week):02d}_{away}_{home}"


def clean_games(raw, channels=CHANNELS):
    """Mantém só jogos com canais conhecidos, sem repetição e na ordem de CHANNELS."""
    known = [cid for cid, _ in channels]
    out = {}
    if not isinstance(raw, dict):
        return out
    for key, vals in raw.items():
        if not isinstance(key, str) or not isinstance(vals, list):
            continue
        ids = [c for c in known if c in vals]
        if ids:
            out[key] = ids
    return out


def load_broadcasts(path=BROADCASTS_PATH):
    """{chave do jogo: [ids dos canais]}. Nunca derruba a geração do site."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        print(f"Aviso: transmissoes.json ilegível ou com erro de formato ({e}); site publicado sem transmissões.")
        return {}
    return clean_games(data.get("jogos") if isinstance(data, dict) else None)


def attach_channels(season, mu, broadcasts, channels=CHANNELS):
    """Acrescenta 'key' e 'canais' (nomes na ordem de CHANNELS) a cada jogo de mu. mu pode ser None."""
    if not mu:
        return
    names = dict(channels)
    for g in mu["games"]:
        g["key"] = game_key(season, mu["week"], g["away"]["abbr"], g["home"]["abbr"])
        g["canais"] = [names[c] for c in broadcasts.get(g["key"], [])]


def schedule_rows(season):
    """Linhas do calendário (todas as fases). Em caso de falha, lista vazia."""
    try:
        import nflreadpy as nfl

        return nfl.load_schedules([season]).to_dicts()
    except Exception as e:
        print(f"Aviso: não foi possível carregar o calendário para a página admin ({e}).")
        return []


def parse_repo(repo_url):
    parts = [p for p in str(repo_url).rstrip("/").split("/") if p]
    owner, name = (parts[-2], parts[-1]) if len(parts) >= 2 else ("", "")
    return {"owner": owner, "name": name, "branch": BRANCH, "path": FILE_IN_REPO}


def _sort_key(r):
    return (str(r.get("gameday") or ""), str(r.get("gametime") or ""))


def _admin_game(season, r, info, tz_name, broadcasts, rnd):
    from .stats import label, local_kickoff

    away, home = r["away_team"], r["home_team"]
    day, time = local_kickoff(r.get("gameday"), r.get("gametime"), tz_name)
    key = game_key(season, r["week"], away, home)
    return {
        "key": key, "week": r["week"], "round": rnd,
        "away": label(away, info), "home": label(home, info),
        "awayAbbr": away, "homeAbbr": home,
        "day": day, "time": time, "canais": broadcasts.get(key, []),
    }


def admin_page(season, rows, info, tz_name, broadcasts, updated, repo_url, channels=CHANNELS):
    """Dados da página admin: jogos ainda não disputados da semana exibida em Confrontos
    (ou da rodada dos playoffs) e, na temporada regular, também os da semana seguinte."""
    from .stats import select_games

    games = []
    picked = select_games(rows)
    if picked:
        wg, rnd, wk = picked
        pending = sorted((r for r in wg if r.get("home_score") is None), key=_sort_key)
        games += [_admin_game(season, r, info, tz_name, broadcasts, rnd) for r in pending]
        if rnd is None:
            later = sorted({r["week"] for r in rows if r.get("game_type") == "REG" and r["week"] > wk})
            if later:
                nxt = sorted(
                    (r for r in rows if r.get("game_type") == "REG" and r["week"] == later[0]), key=_sort_key
                )
                games += [_admin_game(season, r, info, tz_name, broadcasts, None) for r in nxt]
    return {
        "season": season,
        "updated": updated,
        "channels": [{"id": c, "label": l} for c, l in channels],
        "games": games,
        "repo": parse_repo(repo_url),
    }