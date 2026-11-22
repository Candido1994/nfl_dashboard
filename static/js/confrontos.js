const D = window.__DATA__;
const WINDOWS = { s: "Temporada", w3: "Últimas 3 semanas", w1: "Último jogo" };
const $ = (id) => document.getElementById(id);
const fmt = (v) => (v == null ? "–" : v);
const NTEAMS = D.nteams || 32;
const EDGE_THRESHOLD = 6;

// Classe de cor de cada rodada (os nomes vêm de POSTSEASON em nfl_dashboard/stats.py)
const ROUND_CLASS = {
  "Wild Card": "wc",
  "Rodada Divisional": "div",
  "Final da Conferência": "con",
  "Super Bowl": "sb",
};

const METRIC_MAP = Object.fromEntries(D.metrics.map((m) => [m.k, m]));

let win = "s";

document.querySelector("h1").textContent =
  `NFL ${D.season}` +
  (D.round
    ? ` – Playoffs · ${D.round}`
    : D.week
      ? ` – Confrontos da semana ${D.week}`
      : " – Confrontos");

$("sub").textContent = `Atualizado em ${D.updated} · Horários: ${D.tz || "ET"}`;
$("bye").textContent = D.bye.length ? `Folga (bye) na semana ${D.week}: ${D.bye.join(", ")}` : "";
if (D.games.some((g) => g.canais && g.canais.length)) {
  $("tv").textContent = "Transmissão no Brasil informada manualmente; confirme na programação oficial.";
}

$("wins").innerHTML = Object.entries(WINDOWS)
  .map(([k, label]) => `<button data-w="${k}">${label}</button>`)
  .join("");
$("wins").onclick = (e) => {
  if (e.target.dataset.w) {
    win = e.target.dataset.w;
    draw();
  }
};
$("ex").onclick = () => document.querySelectorAll("#games .card").forEach((d) => (d.open = true));
$("co").onclick = () => document.querySelectorAll("#games .card").forEach((d) => (d.open = false));

// Posição na liga (1º = melhor) para a janela selecionada
const rankOf = (k, abbr) => {
  const r = D.ranks && D.ranks[win] && D.ranks[win][k];
  return r && r[abbr] != null ? r[abbr] : null;
};

const rankChip = (r) =>
  r == null ? "" : `<span class="rk ${r <= NTEAMS / 4 ? "g" : r > (NTEAMS * 3) / 4 ? "b" : ""}">${r}º</span>`;

function compareCells(m, a, b) {
  if (a == null || b == null || a === b) return ["", ""];
  const awayWins = m.hb ? a > b : a < b;
  return awayWins ? ["w", ""] : ["", "w"];
}

const recordsLine = (t) =>
  `<b>${t.abbr}</b> · temporada ${fmt(t.s && t.s.rec)} · últimos 3: ${fmt(t.w3 && t.w3.rec)} · último: ${fmt(t.w1 && t.w1.rec)}`;

const GROUPS = [
  ["Pontos", ["pf", "pa", "pd"]],
  ["Jardas", ["pass_yds", "pass_yds_a", "rush_yds", "rush_yds_a", "yd_diff"]],
  ["Turnovers", ["to_lost", "to_gain", "to_diff"]],
  ["Sacks", ["sacks_taken", "sacks_made"]],
  ["Eficiência", ["ypp", "ypp_a", "epa", "epa_a", "sr", "sr_a"]],
];

const DUELS = [
  ["pf", "pa", "Pontos"],
  ["pass_yds", "pass_yds_a", "Jd aéreas"],
  ["rush_yds", "rush_yds_a", "Jd corridas"],
  ["epa", "epa_a", "EPA/jogada"],
  ["sr", "sr_a", "Success rate"],
];

// Duelos do ataque de atk contra a defesa de dfn; gap > 0 favorece o ataque
function buildDuels(atk, dfn) {
  const S = atk[win];
  const Dd = dfn[win];
  return DUELS.map(([ko, kd, label]) => {
    const ra = rankOf(ko, atk.abbr);
    const rd = rankOf(kd, dfn.abbr);
    const gap = ra != null && rd != null ? rd - ra : null;
    const edge =
      gap == null ? "" : gap >= EDGE_THRESHOLD ? "a" : gap <= -EDGE_THRESHOLD ? "d" : "e";
    return { l: label, x: S ? S[ko] : null, y: Dd ? Dd[kd] : null, ra, rd, gap, edge };
  });
}

// Placar do último jogo entre os dois times na temporada (só aparece se já se enfrentaram)
function previousMeeting(g) {
  const p = g.previous;
  if (!p) return "";
  const wa = p.as >= p.hs ? "w" : "";
  const wh = p.hs >= p.as ? "w" : "";
  const when = [
    p.round ? `Playoffs · ${p.round}` : `Semana ${p.week}`,
    p.day,
    `jogo em ${p.home}`,
  ]
    .filter(Boolean)
    .join(" · ");
  return (
    `<section class="sec"><h3>Último confronto nesta temporada</h3>` +
    `<div class="pbox"><span class="pt">${teamLogo(p.away, 24)}${p.away}<b class="ps ${wa}">${p.as}</b></span>` +
    `<span class="px">×</span>` +
    `<span class="pt"><b class="ps ${wh}">${p.hs}</b>${p.home}${teamLogo(p.home, 24)}</span></div>` +
    `<p class="note">${when}</p></section>`
  );
}

function summarySection(g) {
  const a = g.away;
  const h = g.home;
  const As = a.s;
  const Hs = h.s;
  if (!As || !Hs || As.pf == null || Hs.pa == null || Hs.pf == null || As.pa == null) {
    return '<section class="sec"><p class="note">Sem dados suficientes para este período</p></section>';
  }

  const sAway = (As.pf + Hs.pa) / 2;
  const sHome = (Hs.pf + As.pa) / 2;
  const Aw3 = a.w3;
  const Hw3 = h.w3;
  const hasW3 = Boolean(
    Aw3 && Hw3 && Aw3.g >= 3 && Hw3.g >= 3 &&
    Aw3.pf != null && Hw3.pa != null && Hw3.pf != null && Aw3.pa != null
  );

  let mainAway = Math.round(sAway);
  let mainHome = Math.round(sHome);
  let mainLabel = "Placar projetado (temporada)";
  let subHtml =
    '<div class="proj-sub"><span class="proj-empty">Janela de 3 jogos ainda incompleta · 100% temporada</span></div>';

  if (hasW3) {
    const w3Away = (Aw3.pf + Hw3.pa) / 2;
    const w3Home = (Hw3.pf + Aw3.pa) / 2;
    mainAway = Math.round(0.4 * sAway + 0.6 * w3Away);
    mainHome = Math.round(0.4 * sHome + 0.6 * w3Home);
    mainLabel = "Placar projetado (40/60)";
    subHtml =
      `<div class="proj-sub">` +
      `<span>Temporada <b>${Math.round(sAway)} × ${Math.round(sHome)}</b></span>` +
      `<span>Últimos 3 jogos <b>${Math.round(w3Away)} × ${Math.round(w3Home)}</b></span>` +
      `</div>`;
  }

  const A = a[win];
  const H = h[win];
  let tallyHtml = "";
  if (A && H) {
    const d1 = buildDuels(a, h);
    const d2 = buildDuels(h, a);
    const aw = d1.filter((x) => x.edge === "a").length + d2.filter((x) => x.edge === "d").length;
    const hw = d2.filter((x) => x.edge === "a").length + d1.filter((x) => x.edge === "d").length;
    tallyHtml = `<p class="tally">Vantagens claras (de ${d1.length + d2.length} duelos, diferença ≥ ${EDGE_THRESHOLD} pos.): <b>${a.abbr} ${aw}</b> × <b>${hw} ${h.abbr}</b></p>`;
  }

  return (
    `<section class="sec"><h3>Resumo</h3>` +
    `<div class="proj-wrap">` +
    `<div class="proj">` +
    `<div>${teamLogo(a.abbr, 28)}<small>${a.label}</small><b>${mainAway}</b></div>` +
    `<span class="mid">${mainLabel}</span>` +
    `<div>${teamLogo(h.abbr, 28)}<small>${h.label}</small><b>${mainHome}</b></div>` +
    `</div>` +
    `${subHtml}` +
    `</div>` +
    `${tallyHtml}` +
    `<p class="note">Média ataque × defesa adversária (40% temporada, 60% últimos 3) · Uso didático</p>` +
    `</section>`
  );
}

function highlightsSection(g) {
  const a = g.away;
  const h = g.home;
  if (!a[win] || !h[win]) return "";
  const items = [];
  [
    [a, h],
    [h, a],
  ].forEach(([atk, dfn]) => {
    const d = buildDuels(atk, dfn).filter((x) => x.gap != null);
    if (!d.length) return;
    const best = d.reduce((p, c) => (c.gap > p.gap ? c : p));
    const worst = d.reduce((p, c) => (c.gap < p.gap ? c : p));
    if (best.gap >= EDGE_THRESHOLD) {
      items.push(
        `<li class="op"><b>Oportunidade (${atk.abbr}):</b> ${best.l} — ataque ${best.ra}º × defesa ${best.rd}ª de ${dfn.abbr}</li>`
      );
    }
    if (worst.gap <= -EDGE_THRESHOLD) {
      items.push(
        `<li class="ob"><b>Obstáculo (${atk.abbr}):</b> ${worst.l} — ataque ${worst.ra}º × defesa ${worst.rd}ª de ${dfn.abbr}</li>`
      );
    }
  });
  return items.length
    ? `<section class="sec"><h3>Destaques</h3><ul class="hl">${items.join("")}</ul></section>`
    : "";
}

function duelTable(g) {
  const a = g.away;
  const h = g.home;
  if (!a[win] || !h[win]) return "";
  const block = (atk, dfn) =>
    `<tr class="gh"><th colspan="4">Ataque ${atk.abbr} × defesa ${dfn.abbr}</th></tr>` +
    buildDuels(atk, dfn)
      .map((x) => {
        const edgeLabel =
          x.edge === "a"
            ? '<span class="ea">Ataque</span>'
            : x.edge === "d"
              ? '<span class="ed">Defesa</span>'
              : x.edge === "e"
                ? '<span class="ee">Equilíbrio</span>'
                : "–";
        return `<tr><td class="lb">${x.l}</td><td><b>${fmt(x.x)}</b>${rankChip(x.ra)}</td><td><b>${fmt(x.y)}</b>${rankChip(x.rd)}</td><td>${edgeLabel}</td></tr>`;
      })
      .join("");
  return (
    `<section class="sec"><h3>Ataque × defesa</h3>` +
    `<table class="duel"><tr><th></th><th>Ataque faz</th><th>Defesa cede</th><th>Vantagem</th></tr>${block(a, h)}${block(h, a)}</table>` +
    `</section>`
  );
}

function fullTable(g) {
  const a = g.away;
  const h = g.home;
  const A = a[win];
  const H = h[win];
  const cell = (S, t, k, cls) =>
    `<td class="${cls}"><b>${S ? fmt(S[k]) : "–"}</b>${rankChip(rankOf(k, t.abbr))}</td>`;
  const rows = GROUPS.map(
    ([groupName, keys]) =>
      `<tr class="gh"><th colspan="3">${groupName}</th></tr>` +
      keys
        .map((k) => {
          const m = METRIC_MAP[k];
          const x = A ? A[k] : null;
          const y = H ? H[k] : null;
          const [c1, c2] = compareCells(m, x, y);
          return `<tr>${cell(A, a, k, c1)}<td class="lb">${m.l}</td>${cell(H, h, k, c2)}</tr>`;
        })
        .join("")
  ).join("");
  return (
    `<section class="sec"><details open><summary>Comparativo completo</summary>` +
    `<table><tr><th>${a.abbr}<br>${A ? A.rec : "–"}</th><th></th><th>${h.abbr}<br>${H ? H.rec : "–"}</th></tr>${rows}</table>` +
    `<p class="note">Selo = posição na liga (1º = melhor) · Verde = melhor no confronto</p>` +
    `</details></section>`
  );
}

function card(g, i, isOpen) {
  const a = g.away;
  const h = g.home;
  const A = a[win];
  const H = h[win];
  const score = g.as != null ? ` · <b>Final: ${g.as} × ${g.hs}</b>` : "";
  const poTag = g.round ? `<span class="potag">Playoffs · ${g.round}</span>` : "";
  const divTag = g.division ? `<span class="dvtag">${g.division}</span>` : "";
  const tagRow = poTag || divTag ? `<div class="dvrow">${poTag}${divTag}</div>` : "";
  const bcRow =
    g.canais && g.canais.length
      ? `<div class="bcrow"><span class="bcl">Onde assistir</span>${g.canais.map((c) => `<span class="bc">${c}</span>`).join("")}</div>`
      : "";
  const arrow = iconArrow();

  return (
    `<details class="card${g.division ? " dv" : ""}${g.round ? " po po-" + (ROUND_CLASS[g.round] || "") : ""}" data-i="${i}"${isOpen ? " open" : ""}>` +
    `<summary>` +
    `<h2 class="mu">` +
    `<span class="tm"><span class="tt">${teamLogo(a.abbr, 40)}<span class="tx"><b>${teamName(a.label)}</b><small>${A ? A.rec : "–"}</small></span></span></span>` +
    `<span class="at">${g.neutral ? "×" : "@"}</span>` +
    `<span class="tm"><span class="tt">${teamLogo(h.abbr, 40)}<span class="tx"><b>${teamName(h.label)}</b><small>${H ? H.rec : "–"}</small></span></span></span>` +
    `</h2>` +
    `<div class="m">${g.day} ${g.time}${score}</div>${tagRow}${bcRow}${iconChevron()}` +
    `</summary>` +
    `<div class="cb">` +
    `<div class="golinks">` +
    `<a class="btn go" href="jogadores.html?times=${a.abbr},${h.abbr}">Jogadores dos dois times ${arrow}</a>` +
    `<a class="btn go" href="evolucao.html?times=${a.abbr},${h.abbr}">Evolução dos dois times ${arrow}</a>` +
    `</div>` +
    `${previousMeeting(g)}${summarySection(g)}${highlightsSection(g)}${duelTable(g)}` +
    `<section class="sec"><h3>Campanha</h3><p class="note form">${recordsLine(a)}<br>${recordsLine(h)}</p></section>` +
    `${fullTable(g)}` +
    `</div></details>`
  );
}

function draw() {
  document
    .querySelectorAll("#wins button")
    .forEach((b) => b.classList.toggle("on", b.dataset.w === win));
  const openSet = new Set([...document.querySelectorAll("#games .card[open]")].map((d) => +d.dataset.i));
  $("games").innerHTML = D.games.length
    ? D.games.map((g, i) => card(g, i, openSet.has(i))).join("")
    : '<p class="hint">Sem jogos pendentes na temporada regular</p>';
}

draw();
