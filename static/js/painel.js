const D = window.__DATA__;
const WINDOWS = { w1: "Última semana", w3: "Últimas 3 semanas", s: "Temporada" };
const VIEWS = {
  resumo: {
    label: "Resumo",
    keys: ["pf", "pa", "pd", "yd_diff", "to_diff", "epa", "epa_a", "sr", "sr_a"],
  },
  ataque: {
    label: "Ataque",
    keys: ["pf", "pass_yds", "rush_yds", "to_lost", "sacks_taken", "ypp", "epa", "sr"],
  },
  defesa: {
    label: "Defesa",
    keys: ["pa", "pass_yds_a", "rush_yds_a", "to_gain", "sacks_made", "ypp_a", "epa_a", "sr_a"],
  },
  eficiencia: {
    label: "Eficiência",
    keys: ["pd", "yd_diff", "to_diff", "ypp", "ypp_a", "epa", "epa_a", "sr", "sr_a"],
  },
  todas: {
    label: "Todas",
    keys: null,
  },
};

const METRICS = D.metrics;
const METRIC_MAP = Object.fromEntries(METRICS.map((m) => [m.k, m]));
const COLORS = D.colors || {};
const $ = (id) => document.getElementById(id);

let win = "s";
let view = "resumo";
let flt = "ALL";
let sortKey = "pd";
let sortDir = -1;
let rankKey = "pd";

document.querySelector("h1").textContent = `NFL ${D.season} – Painel semanal`;
$("sub").textContent = `Semana ${D.week} · Atualizado em ${D.updated} · Médias por jogo`;

$("wins").innerHTML = Object.entries(WINDOWS)
  .map(([k, label]) => `<button data-w="${k}">${label}</button>`)
  .join("");
$("wins").onclick = (e) => {
  if (e.target.dataset.w) {
    win = e.target.dataset.w;
    draw();
  }
};

$("views").innerHTML = Object.entries(VIEWS)
  .map(([k, spec]) => `<button role="tab" data-v="${k}">${spec.label}</button>`)
  .join("");
$("views").onclick = (e) => {
  const v = e.target.dataset.v;
  if (!v) return;
  view = v;
  const visible = visibleMetrics();
  if (!["team", "g", "pct"].includes(sortKey) && !visible.some((m) => m.k === sortKey)) {
    sortKey = visible[0].k;
    sortDir = -1;
  }
  draw();
};

const divs = [...new Set(D.teams.map((t) => t.div).filter(Boolean))].sort();
$("flt").innerHTML =
  '<option value="ALL">Todos os times</option><option>AFC</option><option>NFC</option>' +
  divs.map((d) => `<option>${d}</option>`).join("");
$("flt").onchange = (e) => {
  flt = e.target.value;
  draw();
};

$("rk").innerHTML = METRICS.map((m) => `<option value="${m.k}">${m.l}</option>`).join("");
$("rk").onchange = (e) => {
  rankKey = e.target.value;
  draw();
};

function visibleMetrics() {
  const keys = VIEWS[view].keys;
  if (!keys) return METRICS;
  const set = new Set(keys);
  return METRICS.filter((m) => set.has(m.k));
}

function filteredRows() {
  return D.teams
    .filter((t) => flt === "ALL" || t.conf === flt || t.div === flt)
    .filter((t) => t[win])
    .map((t) => ({ t, v: t[win] }));
}

function draw() {
  document
    .querySelectorAll("#wins button")
    .forEach((b) => b.classList.toggle("on", b.dataset.w === win));
  document.querySelectorAll("#views button").forEach((b) => {
    const active = b.dataset.v === view;
    b.classList.toggle("on", active);
    b.setAttribute("aria-selected", active ? "true" : "false");
  });

  const cols = visibleMetrics();
  const rows = filteredRows();
  rows.sort((a, b) =>
    sortKey === "team"
      ? sortDir * -a.t.abbr.localeCompare(b.t.abbr)
      : sortDir * (a.v[sortKey] - b.v[sortKey])
  );

  const sortClass = (k) =>
    sortKey === k
      ? ` class="sorted ${(k === "team" ? sortDir < 0 : sortDir > 0) ? "asc" : "desc"}"`
      : "";

  let html =
    `<tr><th data-s="team"${sortClass("team")}>Time</th>` +
    `<th data-s="g"${sortClass("g")}>J</th>` +
    `<th data-s="pct"${sortClass("pct")}>V-D</th>` +
    cols.map((m) => `<th data-s="${m.k}"${sortClass(m.k)}>${m.l}</th>`).join("") +
    "</tr>";

  html += rows
    .map((r) => {
      const cells = cols
        .map((m) => {
          const val = r.v[m.k];
          const color =
            m.k.endsWith("diff") || m.k === "pd"
              ? val > 0
                ? "var(--good)"
                : val < 0
                  ? "var(--bad)"
                  : ""
              : "";
          return `<td style="color:${color}">${val == null ? "–" : val}</td>`;
        })
        .join("");
      return `<tr><td><span class="tn">${teamLogo(r.t.abbr, 24)}${r.t.label}</span></td><td>${r.v.g}</td><td>${r.v.rec}</td>${cells}</tr>`;
    })
    .join("");

  const tb = $("tb");
  tb.classList.toggle("all-cols", view === "todas");
  tb.innerHTML = html;
  tb.onclick = (e) => {
    const s = e.target.dataset.s;
    if (!s) return;
    sortDir = sortKey === s ? -sortDir : -1;
    sortKey = s;
    draw();
  };

  const m = METRIC_MAP[rankKey];
  const ranked = filteredRows()
    .filter((r) => r.v[rankKey] != null)
    .sort((a, b) => (m.hb ? -1 : 1) * (a.v[rankKey] - b.v[rankKey]));
  const maxAbs = Math.max(...ranked.map((r) => Math.abs(r.v[rankKey]))) || 1;

  $("rank").innerHTML = ranked
    .map((r, i) => {
      const val = r.v[rankKey];
      const barColor = val < 0 ? "var(--bad)" : COLORS[r.t.abbr] || "var(--acc)";
      return (
        `<div class="r">` +
        `<span class="n"><b>${i + 1}</b>${teamLogo(r.t.abbr, 20)}${r.t.label}</span>` +
        `<span class="t"><i style="width:${(Math.abs(val) / maxAbs) * 100}%;background:${barColor}"></i></span>` +
        `<span class="v">${val}</span>` +
        `</div>`
      );
    })
    .join("");
}

draw();
