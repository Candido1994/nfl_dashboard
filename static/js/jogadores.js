const D=window.__DATA__;
const $=id=>document.getElementById(id);
const CATS=D.cats,PAL=["#1f77b4","#d62728","#2ca02c","#ff7f0e","#9467bd","#17becf","#e377c2","#8c564b"];
const WL={s:"Temporada",w3:"Últimas 3 semanas",w1:"Último jogo"};
const esc=s=>String(s).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
const f=v=>v==null?"–":v;
const TL=Object.fromEntries(D.teams.map(t=>[t.abbr,t.label]));
let cat="qb",win="s",sel=[],sk="",sd=-1;
const qs=new URLSearchParams(location.search);
sel=(qs.get("times")||"").split(",").map(x=>x.trim().toUpperCase()).filter(x=>Object.prototype.hasOwnProperty.call(TL,x));
if(CATS.some(c=>c.k===qs.get("pos")))cat=qs.get("pos");
if(WL[qs.get("janela")])win=qs.get("janela");
const C=()=>CATS.find(c=>c.k===cat);
sk=C().sort;
document.querySelector("h1").textContent="NFL "+D.season+" – Jogadores";
$("sub").textContent="Semana "+D.week+" • atualizado em "+D.updated+" • temporada regular";
$("cats").innerHTML=CATS.map(c=>`<button data-c="${c.k}">${c.short}</button>`).join("");
$("cats").onclick=e=>{const c=e.target.dataset.c;if(c){cat=c;sk=C().sort;sd=-1;draw()}};
$("wins").innerHTML=Object.entries(WL).map(([k,l])=>`<button data-w="${k}">${l}</button>`).join("");
$("wins").onclick=e=>{if(e.target.dataset.w){win=e.target.dataset.w;draw()}};
$("add").innerHTML='<option value="">+ Adicionar time</option>'+D.teams.map(t=>`<option value="${t.abbr}">${t.label}</option>`).join("");
$("add").onchange=e=>{const a=e.target.value;if(a&&!sel.includes(a))sel.push(a);e.target.value="";draw()};
$("clr").onclick=()=>{sel=[];draw()};
$("chips").onclick=e=>{const a=e.target.dataset.a;if(a){sel=sel.filter(x=>x!==a);draw()}};
$("pt").onclick=e=>{const s=e.target.dataset.s;if(!s)return;sd=(sk===s)?-sd:-1;sk=s;draw()};
const rowsOf=k=>(D.players[k]||[]).filter(p=>(!sel.length||sel.includes(p.t))&&p[win]);
const topOf=(k,team,key)=>rowsOf(k).filter(p=>p.t===team).sort((a,b)=>(b[win][key]??-1e9)-(a[win][key]??-1e9))[0];
const LD=[
 ["qb","Quarterback","yds",x=>`${x.yds} jds • ${x.td} TD • ${x.ints} INT • rating ${f(x.rtg)}`],
 ["rb","Corredor","yds",x=>`${x.yds} jds em ${x.car} corridas • ${f(x.ypc)} jd/corrida • ${x.td} TD`],
 ["rec","Recebedor","yds",x=>`${x.rec} recepções • ${x.yds} jds • ${x.td} TD`],
 ["def","Defensor","tk",x=>`${x.tk} tackles • ${x.sacks} sacks • ${x.ints} INT`],
 ["def","Pass rush","sacks",x=>`${x.sacks} sacks • ${x.qbh} hits no QB • ${x.tfl} TFL`],
 ["k","Kicker","fga",x=>`${x.fgm}/${x.fga} FG (${f(x.pct)}%) • mais longo ${f(x.lng)} • ${x.xpm}/${x.xpa} XP`]
];
function leaders(){
 if(!sel.length)return"";
 const cards=sel.slice(0,4).map(t=>{
  const lines=LD.map(([k,l,key,fn])=>{const p=topOf(k,t,key);if(!p||!(p[win][key]>0))return"";
   return`<div class="ln"><small>${l}</small><b>${esc(p.n)}</b><span>${fn(p[win])}</span></div>`}).join("");
  return`<section class="lead"><h3>${esc(TL[t])}</h3>${lines||'<p class="note">Sem estatísticas neste período.</p>'}</section>`}).join("");
 return cards+(sel.length>4?`<p class="hint">Líderes mostrados para os 4 primeiros times selecionados.</p>`:"")}
function table(){
 const c=C(),R=rowsOf(cat);
 const sc=k=>sk===k?` class="sorted ${(k==="n"?sd<0:sd>0)?"asc":"desc"}"`:"";
 R.sort((a,b)=>sk==="n"?-sd*a.n.localeCompare(b.n):sd*((a[win][sk]??-1e9)-(b[win][sk]??-1e9)));
 const lim=sel.length?R.length:60;
 let h=`<tr><th data-s="n"${sc("n")}>Jogador</th><th>Time</th><th>Pos</th>`+c.cols.map(([k,l])=>`<th data-s="${k}"${sc(k)}>${l}</th>`).join("")+"</tr>";
 h+=R.slice(0,lim).map(p=>`<tr><td>${esc(p.n)}</td><td>${p.t}</td><td>${p.p||"–"}</td>`+c.cols.map(([k])=>`<td>${f(p[win][k])}</td>`).join("")+"</tr>").join("");
 $("pt").innerHTML=R.length?h:"";
 $("note").textContent=!R.length?"Nenhum jogador com estatísticas neste período.":(R.length>lim?`Mostrando os ${lim} primeiros de ${R.length} – filtre por time para ver os demais.`:"")}
function draw(){
 document.querySelectorAll("#cats button").forEach(b=>b.classList.toggle("on",b.dataset.c===cat));
 document.querySelectorAll("#wins button").forEach(b=>b.classList.toggle("on",b.dataset.w===win));
 $("chips").innerHTML=sel.map((a,k)=>{const c=PAL[k%PAL.length];return`<button data-a="${a}" style="border-color:${c};color:${c}">${esc(TL[a])} ✕</button>`}).join("");
 $("lead").innerHTML=leaders();
 table()}
draw();
