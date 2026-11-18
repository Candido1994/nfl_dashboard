const D = window.__DATA__;
const $ = (id) => document.getElementById(id);
const CATS = D.cats;
const PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd", "#17becf", "#e377c2", "#8c564b"];
const WINDOWS = { s: "Temporada", w3: "Últimas 3 semanas", w1: "Último jogo" };
const esc = (s) =>
  String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
const fmt = (v) => (v == null ? "–" : v);
const TEAM_LABELS = Object.fromEntries(D.teams.map((t) => [t.abbr, t.label]));

const qs = new URLSearchParams(location.search);
let selected = (qs.get("times") || "")
  .split(",")
  .map((x) => x.trim().toUpperCase())
  .filter((x) => Object.prototype.hasOwnProperty.call(TEAM_LABELS, x));
let cat = CATS.some((c) => c.k === qs.get("pos")) ? qs.get("pos") : "qb";
let win = WINDOWS[qs.get("janela")] ? qs.get("janela") : "s";

const currentCat = () => CATS.find((c) => c.k === cat);
let sortKey = currentCat().sort;
let sortDir = -1;

document.querySelector("h1").textContent = `NFL ${D.season} – Jogadores`;
$("sub").textContent = `Semana ${D.week} · Atualizado em ${D.updated} · Temporada regular`;

$("cats").innerHTML = CATS.map((c) => `<button data-c="${c.k}">${c.short}</button>`).join("");
$("cats").onclick = (e) => {
  const c = e.target.dataset.c;
  if (c) {
    cat = c;
    sortKey = currentCat().sort;
    sortDir = -1;
    draw();
  }
};

$("wins").innerHTML = Object.entries(WINDOWS)
  .map(([k, label]) => `<button data-w="${k}">${label}</button>`)
  .join("");
$("wins").onclick = (e) => {
  if (e.target.dataset.w) {
    win = e.target.dataset.w;
    draw();
  }
};

$("add").innerHTML =
  '<option value="">+ Adicionar time</option>' +
  D.teams.map((t) => `<option value="${t.abbr}">${t.label}</option>`).join("");
$("add").onchange = (e) => {
  const abbr = e.target.value;
  if (abbr && !selected.includes(abbr)) selected.push(abbr);
  e.target.value = "";
  draw();
};
$("clr").onclick = () => {
  selected = [];
  draw();
};
$("chips").onclick = (e) => {
  const btn = e.target.closest("button[data-a]");
  if (btn) {
    selected = selected.filter((x) => x !== btn.dataset.a);
    draw();
  }
};
$("pt").onclick = (e) => {
  const s = e.target.dataset.s;
  if (!s) return;
  sortDir = sortKey === s ? -sortDir : -1;
  sortKey = s;
  draw();
};

const rowsOf = (k) =>
  (D.players[k] || []).filter((p) => (!selected.length || selected.includes(p.t)) && p[win]);

const topOf = (k, team, key) =>
  rowsOf(k)
    .filter((p) => p.t === team)
    .sort((a, b) => (b[win][key] ?? -1e9) - (a[win][key] ?? -1e9))[0];

const LEADERS_SPEC = [
  ["qb", "Quarterback", "yds", (x) => `${x.yds} jds · ${x.td} TD · ${x.ints} INT · rating ${fmt(x.rtg)}`],
  ["rb", "Corredor", "yds", (x) => `${x.yds} jds em ${x.car} corridas · ${fmt(x.ypc)} jd/corrida · ${x.td} TD`],
  ["rec", "Recebedor", "yds", (x) => `${x.rec} recepções · ${x.yds} jds · ${x.td} TD`],
  ["def", "Defensor", "tk", (x) => `${x.tk} tackles · ${x.sacks} sacks · ${x.ints} INT`],
  ["def", "Pass rush", "sacks", (x) => `${x.sacks} sacks · ${x.qbh} hits no QB · ${x.tfl} TFL`],
  ["k", "Kicker", "fga", (x) => `${x.fgm}/${x.fga} FG (${fmt(x.pct)}%) · mais longo ${fmt(x.lng)} · ${x.xpm}/${x.xpa} XP`],
];

function renderLeaders() {
  if (!selected.length) return "";
  const cards = selected
    .slice(0, 4)
    .map((t) => {
      const lines = LEADERS_SPEC.map(([k, label, key, formatFn]) => {
        const p = topOf(k, t, key);
        if (!p || !(p[win][key] > 0)) return "";
        return `<div class="ln"><small>${label}</small><b>${esc(p.n)}</b><span>${formatFn(p[win])}</span></div>`;
      }).join("");
      return `<section class="lead"><h3 class="lt">${teamLogo(t, 28)}${esc(TEAM_LABELS[t])}</h3>${lines || '<p class="note">Sem estatísticas neste período.</p>'}</section>`;
    })
    .join("");
  return cards + (selected.length > 4 ? '<p class="hint">Líderes exibidos para os 4 primeiros times.</p>' : "");
}

function renderTable() {
  const c = currentCat();
  const rows = rowsOf(cat);
  const sortClass = (k) =>
    sortKey === k
      ? ` class="sorted ${(k === "n" ? sortDir < 0 : sortDir > 0) ? "asc" : "desc"}"`
      : "";

  rows.sort((a, b) =>
    sortKey === "n"
      ? -sortDir * a.n.localeCompare(b.n)
      : sortDir * ((a[win][sortKey] ?? -1e9) - (b[win][sortKey] ?? -1e9))
  );

  const lim = selected.length ? rows.length : 60;
  let html =
    `<tr><th data-s="n"${sortClass("n")}>Jogador</th><th>Time</th><th>Pos</th>` +
    c.cols.map(([k, label]) => `<th data-s="${k}"${sortClass(k)}>${label}</th>`).join("") +
    "</tr>";

  html += rows
    .slice(0, lim)
    .map(
      (p) =>
        `<tr><td>${esc(p.n)}</td><td><span class="tn">${teamLogo(p.t, 20)}${p.t}</span></td><td>${p.p || "–"}</td>` +
        c.cols.map(([k]) => `<td>${fmt(p[win][k])}</td>`).join("") +
        "</tr>"
    )
    .join("");

  $("pt").innerHTML = rows.length ? html : "";
  $("note").textContent = !rows.length
    ? "Nenhum jogador com estatísticas neste período."
    : rows.length > lim
      ? `Exibindo os ${lim} primeiros de ${rows.length} — filtre por time para ver os demais.`
      : "";
}

function draw() {
  document
    .querySelectorAll("#cats button")
    .forEach((b) => b.classList.toggle("on", b.dataset.c === cat));
  document
    .querySelectorAll("#wins button")
    .forEach((b) => b.classList.toggle("on", b.dataset.w === win));

  const close = iconClose();
  $("chips").innerHTML = selected
    .map((abbr, idx) => {
      const c = PALETTE[idx % PALETTE.length];
      return `<button data-a="${abbr}" style="border-color:${c};color:${c}">${teamLogo(abbr, 20)}${esc(TEAM_LABELS[abbr])} ${close}</button>`;
    })
    .join("");

  $("lead").innerHTML = renderLeaders();
  renderTable();
}

draw();
