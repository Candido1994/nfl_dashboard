const D=window.__DATA__;
const WL={s:"Temporada",w3:"Últimas 3 semanas",w1:"Último jogo"};
let win="s";
const $=id=>document.getElementById(id);
const f=v=>v==null?"–":v;
const NT=D.nteams||32,TH=6;
const MK=Object.fromEntries(D.metrics.map(m=>[m.k,m]));
document.querySelector("h1").textContent="NFL "+D.season+(D.week?" – Confrontos da semana "+D.week:" – Confrontos");
$("sub").textContent="Atualizado em "+D.updated+" • médias por jogo • horários: "+(D.tz||"ET");
$("bye").textContent=D.bye.length?"Folga (bye): "+D.bye.join(", "):"";
$("wins").innerHTML=Object.entries(WL).map(([k,l])=>`<button data-w="${k}">${l}</button>`).join("");
$("wins").onclick=e=>{if(e.target.dataset.w){win=e.target.dataset.w;draw()}};
$("ex").onclick=()=>document.querySelectorAll("#games .card").forEach(d=>d.open=true);
$("co").onclick=()=>document.querySelectorAll("#games .card").forEach(d=>d.open=false);
// posição na liga (1º = melhor) para a janela selecionada
const rk=(k,a)=>{const r=D.ranks&&D.ranks[win]&&D.ranks[win][k];return r&&r[a]!=null?r[a]:null};
const chip=r=>r==null?"":`<span class="rk ${r<=NT/4?"g":r>NT*3/4?"b":""}">${r}º</span>`;
function cmp(m,a,b){if(a==null||b==null||a===b)return["",""];const aw=m.hb?a>b:a<b;return aw?["w",""]:["","w"]}
const recs=t=>`<b>${t.abbr}</b> – temporada ${f(t.s&&t.s.rec)} • últimos 3: ${f(t.w3&&t.w3.rec)} • último: ${f(t.w1&&t.w1.rec)}`;
const GROUPS=[["Pontos",["pf","pa","pd"]],["Jardas",["pass_yds","pass_yds_a","rush_yds","rush_yds_a","yd_diff"]],["Turnovers",["to_lost","to_gain","to_diff"]],["Sacks",["sacks_taken","sacks_made"]],["Eficiência",["ypp","ypp_a","epa","epa_a","sr","sr_a"]]];
const DU=[["pf","pa","Pontos"],["pass_yds","pass_yds_a","Jd aéreas"],["rush_yds","rush_yds_a","Jd corridas"],["epa","epa_a","EPA/jogada"],["sr","sr_a","Success rate"]];
// duelos do ataque de atk contra a defesa de dfn; gap > 0 favorece o ataque
function duels(atk,dfn){
 const S=atk[win],Dd=dfn[win];
 return DU.map(([ko,kd,l])=>{const ra=rk(ko,atk.abbr),rd=rk(kd,dfn.abbr),gap=ra!=null&&rd!=null?rd-ra:null;
  return{l,x:S?S[ko]:null,y:Dd?Dd[kd]:null,ra,rd,gap,edge:gap==null?"":gap>=TH?"a":gap<=-TH?"d":"e"}})}
function resumo(g){
 const a=g.away,h=g.home,A=a[win],H=h[win];
 if(!A||!H)return`<section class="sec"><p class="note">Sem dados suficientes para este período.</p></section>`;
 const d1=duels(a,h),d2=duels(h,a);
 const pj=(O,Dd)=>((O.pf+Dd.pa)/2).toFixed(1);
 const aw=d1.filter(x=>x.edge==="a").length+d2.filter(x=>x.edge==="d").length;
 const hw=d2.filter(x=>x.edge==="a").length+d1.filter(x=>x.edge==="d").length;
 return`<section class="sec"><h3>Resumo</h3><div class="proj"><div><small>${a.label}</small><b>${pj(A,H)}</b></div><span class="mid">pontos projetados</span><div><small>${h.label}</small><b>${pj(H,A)}</b></div></div>
 <p class="tally">Duelos ataque x defesa com vantagem clara (de ${d1.length+d2.length}): <b>${a.abbr} ${aw}</b> × <b>${hw} ${h.abbr}</b></p>
 <p class="note">Projeção simples: média entre os pontos que o ataque faz e os que a defesa adversária cede. Vantagem clara = diferença de ${TH} ou mais posições no ranking da liga.</p>
 <p class="note"><b>Aviso:</b> projeção apenas didática; não use para apostas nem para fins lucrativos.</p></section>`}
function destaques(g){
 const a=g.away,h=g.home;if(!a[win]||!h[win])return"";
 const out=[];
 [[a,h],[h,a]].forEach(([atk,dfn])=>{
  const d=duels(atk,dfn).filter(x=>x.gap!=null);if(!d.length)return;
  const best=d.reduce((p,c)=>c.gap>p.gap?c:p),worst=d.reduce((p,c)=>c.gap<p.gap?c:p);
  if(best.gap>=TH)out.push(`<li class="op"><b>Oportunidade para ${atk.abbr}:</b> ${best.l} – ataque ${best.ra}º x defesa ${best.rd}ª de ${dfn.abbr}.</li>`);
  if(worst.gap<=-TH)out.push(`<li class="ob"><b>Obstáculo para ${atk.abbr}:</b> ${worst.l} – ataque ${worst.ra}º x defesa ${worst.rd}ª de ${dfn.abbr}.</li>`)});
 return out.length?`<section class="sec"><h3>Destaques do confronto</h3><ul class="hl">${out.join("")}</ul></section>`:""}
function duelTable(g){
 const a=g.away,h=g.home;if(!a[win]||!h[win])return"";
 const blk=(atk,dfn)=>`<tr class="gh"><th colspan="4">Ataque ${atk.abbr} x defesa ${dfn.abbr}</th></tr>`+duels(atk,dfn).map(x=>{
  const t=x.edge==="a"?'<span class="ea">Ataque</span>':x.edge==="d"?'<span class="ed">Defesa</span>':x.edge==="e"?'<span class="ee">Equilíbrio</span>':"–";
  return`<tr><td class="lb">${x.l}</td><td><b>${f(x.x)}</b>${chip(x.ra)}</td><td><b>${f(x.y)}</b>${chip(x.rd)}</td><td>${t}</td></tr>`}).join("");
 return`<section class="sec"><h3>Ataque x defesa</h3><table class="duel"><tr><th></th><th>Ataque faz</th><th>Defesa cede</th><th>Vantagem</th></tr>${blk(a,h)}${blk(h,a)}</table></section>`}
function fullTable(g){
 const a=g.away,h=g.home,A=a[win],H=h[win];
 const cell=(S,t,k,c)=>`<td class="${c}"><b>${S?f(S[k]):"–"}</b>${chip(rk(k,t.abbr))}</td>`;
 const rows=GROUPS.map(([gn,ks])=>`<tr class="gh"><th colspan="3">${gn}</th></tr>`+ks.map(k=>{const m=MK[k],x=A?A[k]:null,y=H?H[k]:null,[c1,c2]=cmp(m,x,y);
  return`<tr>${cell(A,a,k,c1)}<td class="lb">${m.l}</td>${cell(H,h,k,c2)}</tr>`}).join("")).join("");
 return`<section class="sec"><details open><summary>Comparativo completo</summary><table><tr><th>${a.abbr}<br>${A?A.rec:"–"}</th><th></th><th>${h.abbr}<br>${H?H.rec:"–"}</th></tr>${rows}</table><p class="note">O número pequeno ao lado do valor é a posição na liga (1º = melhor, inclusive na defesa). Verde = melhor valor entre os dois times.</p></details></section>`}
function card(g,i,open){
 const a=g.away,h=g.home,A=a[win],H=h[win];
 const sc=g.as!=null?` • <b>Final: ${g.as} x ${g.hs}</b>`:"";
 const dv=g.division?`<div class="dvrow"><span class="dvtag">Jogo de divisão · ${g.division}</span></div>`:"";
 return`<details class="card${g.division?" dv":""}" data-i="${i}"${open?" open":""}><summary><h2 class="mu"><span class="tm"><b>${a.label}</b><small>${A?A.rec:"–"}</small></span><span class="at">@</span><span class="tm"><b>${h.label}</b><small>${H?H.rec:"–"}</small></span></h2><div class="m">${g.day} ${g.time}${sc}</div>${dv}</summary>
 <div class="cb"><div class="golinks"><a class="btn go" href="jogadores.html?times=${a.abbr},${h.abbr}">Jogadores dos dois times →</a><a class="btn go" href="evolucao.html?times=${a.abbr},${h.abbr}">Evolução dos dois times →</a></div>${resumo(g)}${destaques(g)}${duelTable(g)}<section class="sec"><h3>Campanha</h3><p class="note form">${recs(a)}<br>${recs(h)}</p></section>${fullTable(g)}</div></details>`}
function draw(){
 document.querySelectorAll("#wins button").forEach(b=>b.classList.toggle("on",b.dataset.w===win));
 const op=new Set([...document.querySelectorAll("#games .card[open]")].map(d=>+d.dataset.i));
 $("games").innerHTML=D.games.length?D.games.map((g,i)=>card(g,i,op.has(i))).join(""):'<p class="hint">Sem jogos pendentes na temporada regular.</p>'}
draw();