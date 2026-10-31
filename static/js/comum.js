// Utilidades compartilhadas pelas páginas. Não declare `D` aqui: cada página declara o seu.

// Cor do texto (claro ou escuro) que contrasta com a cor de fundo informada.
const tlInk=h=>{const m=/^#([0-9a-f]{6})$/i.exec(h||"");if(!m)return"#fff";const n=parseInt(m[1],16);return((n>>16)*299+((n>>8)&255)*587+(n&255)*114)/1000>150?"#17211B":"#fff"};

// Logo do time: usa static/img/teams/<sigla>.png; se o arquivo faltar, vira um distintivo com a sigla na cor do time.
const teamLogo=(abbr,size)=>{
 const c=(window.__DATA__.colors||{})[abbr]||"#5A685F";
 return`<span class="tl tl-${size}" style="--c:${c};--ink:${tlInk(c)}"><img src="static/img/teams/${String(abbr).toLowerCase()}.png" alt="" width="${size}" height="${size}" loading="lazy" decoding="async" onerror="this.remove()"><i>${abbr}</i></span>`};

// "NE - Patriots" -> sigla e apelido em partes separadas, para o CSS poder quebrar a linha entre elas em telas estreitas.
const teamName=l=>{const i=String(l).indexOf(" - ");return i<0?l:`${l.slice(0,i)}<span class="dsh"> - </span><span class="nk">${l.slice(i+3)}</span>`};