// Utilidades compartilhadas pelas páginas. Não declare `D` aqui: cada página declara o seu.

// Cor do texto (claro ou escuro) que contrasta com a cor de fundo informada.
const tlInk = (h) => {
  const m = /^#([0-9a-f]{6})$/i.exec(h || "");
  if (!m) return "#fff";
  const n = parseInt(m[1], 16);
  return ((n >> 16) * 299 + ((n >> 8) & 255) * 587 + (n & 255) * 114) / 1000 > 150
    ? "#17211B"
    : "#fff";
};

// Logo do time: usa static/img/teams/<sigla>.png; se o arquivo faltar, vira um distintivo com a sigla na cor do time.
const teamLogo = (abbr, size) => {
  const c = (window.__DATA__.colors || {})[abbr] || "#5A685F";
  return `<span class="tl tl-${size}" style="--c:${c};--ink:${tlInk(c)}"><img src="static/img/teams/${String(abbr).toLowerCase()}.png" alt="" width="${size}" height="${size}" loading="lazy" decoding="async" onerror="this.remove()"><i>${abbr}</i></span>`;
};

// "NE - Patriots" -> sigla e apelido em partes separadas, para o CSS poder quebrar a linha entre elas em telas estreitas.
const teamName = (l) => {
  const i = String(l).indexOf(" - ");
  return i < 0
    ? l
    : `${l.slice(0, i)}<span class="dsh"> - </span><span class="nk">${l.slice(i + 3)}</span>`;
};

const iconChevron = () =>
  '<svg class="chev" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const iconArrow = () =>
  '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3.5 8h9m-3.5-3.5L12.5 8 9 11.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const iconClose = () =>
  '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4.5 4.5l7 7m0-7l-7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';

const iconSun = () =>
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.5"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41m11.32-11.32l1.41-1.41" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';

const iconMoon = () =>
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

// Alternância manual de tema claro/escuro (salva em localStorage; padrão segue o sistema).
(() => {
  const btn = document.getElementById("theme-btn");
  if (!btn) return;
  const mq = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");
  const current = () =>
    document.documentElement.dataset.theme || (mq && mq.matches ? "dark" : "light");
  const sync = () => {
    const isDark = current() === "dark";
    btn.innerHTML = isDark ? iconSun() : iconMoon();
    const label = isDark ? "Mudar para tema claro" : "Mudar para tema escuro";
    btn.setAttribute("aria-label", label);
    btn.title = label;
  };
  btn.onclick = () => {
    const next = current() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try {
      localStorage.setItem("nfl_theme", next);
    } catch (e) {}
    sync();
  };
  if (mq && mq.addEventListener) mq.addEventListener("change", sync);
  sync();
})();
