const D = window.__DATA__;
const $ = (id) => document.getElementById(id);
const TEAMS = D.teams;
const WEEKS = D.weeks;
const METRICS = D.metrics;
const DIGITS = { epa: 3, epa_a: 3, pct: 3 };
const PALETTE = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd", "#17becf", "#e377c2", "#8c564b"];
const WINDOWS = { s: "Acumulado da temporada", w3: "Últimos 3 jogos (móvel)" };
const MODES = { v: "Valor", r: "Posição no ranking" };

let win = "s";
let mode = "v";
let metricKey = "pd";
let selected = [];

const qs = new URLSearchParams(location.search);
const urlTeams = (qs.get("times") || "")
  .split(",")
  .map((x) => x.trim().toUpperCase())
  .filter((a) => TEAMS.some((t) => t.abbr === a));

if (METRICS.some((m) => m.k === qs.get("metrica"))) metricKey = qs.get("metrica");
if (Object.prototype.hasOwnProperty.call(WINDOWS, qs.get("janela"))) win = qs.get("janela");
if (Object.prototype.hasOwnProperty.call(MODES, qs.get("modo"))) mode = qs.get("modo");

const currentMetric = () => METRICS.find((m) => m.k === metricKey);
const fmt = (v) => (v == null ? "–" : v.toFixed(DIGITS[metricKey] ?? 1));
const valueAt = (t, i) => {
  const x = t.series[i][win];
  return x ? x[metricKey] : null;
};

function ranksAt(i) {
  const m = currentMetric();
  const list = TEAMS.map((t) => ({ a: t.abbr, v: valueAt(t, i) }))
    .filter((o) => o.v != null)
    .sort((x, y) => (m.hb ? y.v - x.v : x.v - y.v));
  const out = {};
  list.forEach((o, j) => (out[o.a] = j + 1));
  return out;
}

function topN(n) {
  const i = WEEKS.length - 1;
  if (i < 0) return [];
  const r = ranksAt(i);
  return Object.keys(r)
    .sort((a, b) => r[a] - r[b])
    .slice(0, n);
}

document.querySelector("h1").textContent = `NFL ${D.season} – Evolução semanal`;
$("sub").textContent = `Atualizado em ${D.updated}`;

$("mk").innerHTML = METRICS.map((m) => `<option value="${m.k}">${m.l}</option>`).join("");
$("mk").value = metricKey;
$("mk").onchange = (e) => {
  metricKey = e.target.value;
  draw();
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

$("modes").innerHTML = Object.entries(MODES)
  .map(([k, label]) => `<button data-m="${k}">${label}</button>`)
  .join("");
$("modes").onclick = (e) => {
  if (e.target.dataset.m) {
    mode = e.target.dataset.m;
    draw();
  }
};

$("add").innerHTML =
  '<option value="">+ Adicionar time</option>' +
  [...TEAMS]
    .sort((a, b) => a.label.localeCompare(b.label))
    .map((t) => `<option value="${t.abbr}">${t.label}</option>`)
    .join("");
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

function renderChart() {
  if (!WEEKS.length) {
    $("ch").innerHTML = "";
    return;
  }
  const allRanks = WEEKS.map((_, i) => ranksAt(i));
  const N = TEAMS.length;
  const yVal = (t, i) => (mode === "r" ? (allRanks[i][t.abbr] ?? null) : valueAt(t, i));
  const all = [];
  TEAMS.forEach((t) =>
    WEEKS.forEach((_, i) => {
      const v = yVal(t, i);
      if (v != null) all.push(v);
    })
  );
  if (!all.length) {
    $("ch").innerHTML = "";
    return;
  }

  let lo = Math.min(...all);
  let hi = Math.max(...all);
  if (lo === hi) {
    lo -= 1;
    hi += 1;
  }

  const X0 = 38;
  const X1 = 330;
  const Y0 = 12;
  const Y1 = 192;
  const px = (i) => (WEEKS.length > 1 ? X0 + (i * (X1 - X0)) / (WEEKS.length - 1) : (X0 + X1) / 2);
  const py = (v) =>
    mode === "r" ? Y0 + ((v - 1) / (N - 1)) * (Y1 - Y0) : Y1 - ((v - lo) / (hi - lo)) * (Y1 - Y0);

  let svg = "";
  const ticks =
    mode === "r"
      ? [1, Math.round(N / 4), Math.round(N / 2), Math.round((3 * N) / 4), N]
      : [lo, (lo + hi) / 2, hi];

  ticks.forEach((v) => {
    const y = py(v);
    svg +=
      `<line x1="${X0}" x2="${X1}" y1="${y}" y2="${y}" stroke="var(--line)" stroke-dasharray="3 4"/>` +
      `<text x="${X0 - 4}" y="${y + 3}" text-anchor="end" font-size="10.5" fill="var(--mut)">${mode === "r" ? v : v.toFixed(DIGITS[metricKey] ?? 1)}</text>`;
  });

  WEEKS.forEach((w, i) => {
    svg += `<text x="${px(i)}" y="206" text-anchor="middle" font-size="10.5" fill="var(--mut)">${w}</text>`;
  });
  svg += `<text x="${(X0 + X1) / 2}" y="219" text-anchor="middle" font-size="10.5" fill="var(--mut)">Semana</text>`;

  const buildPath = (t) => {
    let d = "";
    let pen = false;
    WEEKS.forEach((_, i) => {
      const v = yVal(t, i);
      if (v == null) {
        pen = false;
        return;
      }
      d += `${pen ? "L" : "M"}${px(i).toFixed(1)} ${py(v).toFixed(1)} `;
      pen = true;
    });
    return d;
  };

  TEAMS.filter((t) => !selected.includes(t.abbr)).forEach((t) => {
    svg += `<path d="${buildPath(t)}" fill="none" stroke="var(--mut)" stroke-opacity=".25" stroke-width="1"/>`;
  });

  selected.forEach((abbr, idx) => {
    const t = TEAMS.find((x) => x.abbr === abbr);
    if (!t) return;
    const c = PALETTE[idx % PALETTE.length];
    const lastIdx = WEEKS.length - 1;
    const v = yVal(t, lastIdx);
    svg += `<path d="${buildPath(t)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
    if (v != null) {
      svg += `<circle cx="${px(lastIdx)}" cy="${py(v)}" r="3" fill="${c}"/><text x="${px(lastIdx) + 6}" y="${py(v) + 3}" font-size="10.5" font-weight="700" fill="${c}">${abbr}</text>`;
    }
  });

  $("ch").innerHTML = svg;
}

function renderTable() {
  const i = WEEKS.length - 1;
  if (i < 0) {
    $("th").textContent = "Sem jogos ainda";
    $("tb").innerHTML = "";
    return;
  }
  $("th").textContent =
    `Movimentação do ranking – semana ${WEEKS[i]}` + (i > 0 ? ` vs ${WEEKS[i - 1]}` : "");
  const r = ranksAt(i);
  const p = i > 0 ? ranksAt(i - 1) : {};
  const rows = Object.keys(r).sort((a, b) => r[a] - r[b]);

  let html = '<tr><th>#</th><th style="text-align:left">Time</th><th>Δ</th><th>Atual</th><th>Sem. ant.</th></tr>';
  html += rows
    .map((abbr) => {
      const t = TEAMS.find((x) => x.abbr === abbr);
      const diff = p[abbr] != null ? p[abbr] - r[abbr] : null;
      const diffCell =
        diff == null
          ? "–"
          : diff > 0
            ? `<span class="up">▲${diff}</span>`
            : diff < 0
              ? `<span class="dn">▼${-diff}</span>`
              : "=";
      return `<tr><td>${r[abbr]}</td><td style="text-align:left"><span class="tn">${teamLogo(abbr, 20)}${t.label}</span></td><td>${diffCell}</td><td>${fmt(valueAt(t, i))}</td><td>${fmt(i > 0 ? valueAt(t, i - 1) : null)}</td></tr>`;
    })
    .join("");
  $("tb").innerHTML = html;
}

function draw() {
  document
    .querySelectorAll("#wins button")
    .forEach((b) => b.classList.toggle("on", b.dataset.w === win));
  document
    .querySelectorAll("#modes button")
    .forEach((b) => b.classList.toggle("on", b.dataset.m === mode));

  const close = iconClose();
  $("chips").innerHTML = selected
    .map((abbr, idx) => {
      const t = TEAMS.find((x) => x.abbr === abbr);
      const c = PALETTE[idx % PALETTE.length];
      return `<button data-a="${abbr}" style="border-color:${c};color:${c}">${teamLogo(abbr, 20)}${t ? t.label : abbr} ${close}</button>`;
    })
    .join("");

  renderChart();
  renderTable();
}

selected = urlTeams.length ? urlTeams : topN(3);
draw();
