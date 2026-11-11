// static/js/playoffs.js
const D = window.__DATA__;
const $ = id => document.getElementById(id);
const pct = v => v == null ? "–" : v.toFixed(3).replace("0.", ".");
const rec = s => `${s.w}-${s.l}${s.t ? "-" + s.t : ""}`;

document.querySelector("h1").textContent = "NFL " + D.season + " – Playoffs";
$("sub").textContent = D.week
  ? `Atualizado em ${D.updated} • posição após a semana ${D.week}`
  : `Atualizado em ${D.updated}`;

function quadro(conf) {
  let linhas = "";
  D.conferencias[conf].seeds.forEach(s => {
    if (s.seed === 1) linhas += `<tr class="gh"><th colspan="4">Campeões de divisão (seeds 1 a 4)</th></tr>`;
    if (s.seed === 5) linhas += `<tr class="gh cut"><th colspan="4">Wild Card (seeds 5 a 7)</th></tr>`;
    linhas += `<tr><td class="n">${s.seed}</td>`
      + `<td class="tm">${teamLogo(s.abbr, 24)}<b>${teamName(s.label)}</b>${s.sorteio ? ' <span class="tg">Sorteio pendente</span>' : ""}</td>`
      + `<td class="dv">${s.div}</td>`
      + `<td class="rc">${rec(s)}<small>${pct(s.pct)}</small></td></tr>`;
  });
  return `<div class="wrap"><table class="seeds pt"><colgroup><col style="width:56px"><col style="width:44%"><col style="width:28%"><col style="width:28%"></colgroup>`
    + `<thead><tr><th class="n">Seed</th><th>Time</th><th>Divisão</th><th>V-D</th></tr></thead><tbody>${linhas}</tbody></table></div>`;
}

function chave(conf) {
  const C = D.conferencias[conf];
  const lab = Object.fromEntries(C.seeds.map(s => [s.abbr, s.label]));
  const num = Object.fromEntries(C.seeds.map(s => [s.abbr, s.seed]));
  const lado = a => `<span class="sd">${num[a]}</span>${teamLogo(a, 28)}<b>${teamName(lab[a])}</b>`;
  const jogos = C.jogos.map(([menor, maior]) =>
    `<li><span class="tm">${lado(maior)}</span><span class="at">@</span><span class="tm r">${lado(menor)}</span></li>`
  ).join("");
  return `<h3 class="bk-h"><span class="potag po-div">Divisional Round</span></h3>`
    + `<ul class="bk"><li class="bye">${teamLogo(C.bye, 28)}<span class="tx"><b>${lab[C.bye]} (seed 1)</b>Bye week: entra na Divisional Round</span></li></ul>`
    + `<h3 class="bk-h"><span class="potag po-wc">Wild Card Round</span></h3><ul class="bk">${jogos}</ul>`;
}

function draw() {
  if (!D.week) {
    $("conteudo").innerHTML = '<p class="hint">Sem semanas fechadas na temporada.</p>';
    return;
  }
  $("conteudo").innerHTML = Object.keys(D.conferencias)
    .map(c => `<section class="conf"><h2>${c}</h2>${quadro(c)}${chave(c)}</section>`).join("");
}
draw();
