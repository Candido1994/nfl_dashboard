const D=window.__DATA__;
const $=id=>document.getElementById(id);
const T=D.teams,W=D.weeks,MET=D.metrics;
const DIG={epa:3,epa_a:3,pct:3};
const PAL=["#1f77b4","#d62728","#2ca02c","#ff7f0e","#9467bd","#17becf","#e377c2","#8c564b"];
const WL={s:"Acumulado da temporada",w3:"Últimos 3 jogos (móvel)"},ML={v:"Valor",r:"Posição no ranking"};
let win="s",mode="v",mk="pd",sel=[];
const qs=new URLSearchParams(location.search);
const urlTeams=(qs.get("times")||"").split(",").map(x=>x.trim().toUpperCase()).filter(a=>T.some(t=>t.abbr===a));
if(MET.some(m=>m.k===qs.get("metrica")))mk=qs.get("metrica");
if(Object.prototype.hasOwnProperty.call(WL,qs.get("janela")))win=qs.get("janela");
if(Object.prototype.hasOwnProperty.call(ML,qs.get("modo")))mode=qs.get("modo");
const met=()=>MET.find(m=>m.k===mk);
const fmt=v=>v==null?"–":v.toFixed(DIG[mk]??1);
const val=(t,i)=>{const x=t.series[i][win];return x?x[mk]:null};
function ranks(i){const m=met();const a=T.map(t=>({a:t.abbr,v:val(t,i)})).filter(o=>o.v!=null).sort((x,y)=>m.hb?y.v-x.v:x.v-y.v);const r={};a.forEach((o,j)=>r[o.a]=j+1);return r}
function topN(n){const i=W.length-1;if(i<0)return[];const r=ranks(i);return Object.keys(r).sort((a,b)=>r[a]-r[b]).slice(0,n)}
document.querySelector("h1").textContent="NFL "+D.season+" – Evolução semanal";
$("sub").textContent="Atualizado em "+D.updated+" • recalculado a cada execução, sem depender de execuções anteriores";
$("mk").innerHTML=MET.map(m=>`<option value="${m.k}">${m.l}</option>`).join("");
$("mk").value=mk;$("mk").onchange=e=>{mk=e.target.value;draw()};
$("wins").innerHTML=Object.entries(WL).map(([k,l])=>`<button data-w="${k}">${l}</button>`).join("");
$("wins").onclick=e=>{if(e.target.dataset.w){win=e.target.dataset.w;draw()}};
$("modes").innerHTML=Object.entries(ML).map(([k,l])=>`<button data-m="${k}">${l}</button>`).join("");
$("modes").onclick=e=>{if(e.target.dataset.m){mode=e.target.dataset.m;draw()}};
$("add").innerHTML='<option value="">+ Adicionar time</option>'+[...T].sort((a,b)=>a.label.localeCompare(b.label)).map(t=>`<option value="${t.abbr}">${t.label}</option>`).join("");
$("add").onchange=e=>{const a=e.target.value;if(a&&!sel.includes(a))sel.push(a);e.target.value="";draw()};
$("clr").onclick=()=>{sel=[];draw()};
$("chips").onclick=e=>{const a=e.target.dataset.a;if(a){sel=sel.filter(x=>x!==a);draw()}};
function chart(){
 if(!W.length){$("ch").innerHTML="";return}
 const R=W.map((_,i)=>ranks(i)),N=T.length;
 const yv=(t,i)=>mode==="r"?(R[i][t.abbr]??null):val(t,i);
 const all=[];T.forEach(t=>W.forEach((_,i)=>{const v=yv(t,i);if(v!=null)all.push(v)}));
 if(!all.length){$("ch").innerHTML="";return}
 let lo=Math.min(...all),hi=Math.max(...all);if(lo===hi){lo-=1;hi+=1}
 const X0=38,X1=330,Y0=12,Y1=192;
 const px=i=>W.length>1?X0+i*(X1-X0)/(W.length-1):(X0+X1)/2;
 const py=v=>mode==="r"?Y0+(v-1)/(N-1)*(Y1-Y0):Y1-(v-lo)/(hi-lo)*(Y1-Y0);
 let s="";
 const ticks=mode==="r"?[1,Math.round(N/4),Math.round(N/2),Math.round(3*N/4),N]:[lo,(lo+hi)/2,hi];
 ticks.forEach(v=>{const y=py(v);s+=`<line x1="${X0}" x2="${X1}" y1="${y}" y2="${y}" stroke="var(--line)" stroke-dasharray="3 4"/><text x="${X0-4}" y="${y+3}" text-anchor="end" font-size="10.5" fill="var(--mut)">${mode==="r"?v:v.toFixed(DIG[mk]??1)}</text>`});
 W.forEach((w,i)=>{s+=`<text x="${px(i)}" y="206" text-anchor="middle" font-size="10.5" fill="var(--mut)">${w}</text>`});
 s+=`<text x="${(X0+X1)/2}" y="219" text-anchor="middle" font-size="10.5" fill="var(--mut)">Semana</text>`;
 const path=t=>{let d="",pen=false;W.forEach((_,i)=>{const v=yv(t,i);if(v==null){pen=false;return}d+=(pen?"L":"M")+px(i).toFixed(1)+" "+py(v).toFixed(1)+" ";pen=true});return d};
 T.filter(t=>!sel.includes(t.abbr)).forEach(t=>{s+=`<path d="${path(t)}" fill="none" stroke="var(--mut)" stroke-opacity=".25" stroke-width="1"/>`});
 sel.forEach((a,k)=>{const t=T.find(x=>x.abbr===a);if(!t)return;const c=PAL[k%PAL.length],i=W.length-1,v=yv(t,i);
  s+=`<path d="${path(t)}" fill="none" stroke="${c}" stroke-width="2.2"/>`;
  if(v!=null)s+=`<circle cx="${px(i)}" cy="${py(v)}" r="3" fill="${c}"/><text x="${px(i)+6}" y="${py(v)+3}" font-size="10.5" font-weight="700" fill="${c}">${a}</text>`});
 $("ch").innerHTML=s}
function table(){
 const i=W.length-1;
 if(i<0){$("th").textContent="Sem jogos ainda";$("tb").innerHTML="";return}
 $("th").textContent="Movimentação do ranking – semana "+W[i]+(i>0?" vs "+W[i-1]:"");
 const r=ranks(i),p=i>0?ranks(i-1):{};
 const rows=Object.keys(r).sort((a,b)=>r[a]-r[b]);
 let h='<tr><th>#</th><th style="text-align:left">Time</th><th>Δ</th><th>Atual</th><th>Sem. ant.</th></tr>';
 h+=rows.map(a=>{const t=T.find(x=>x.abbr===a),d=p[a]!=null?p[a]-r[a]:null;
  const dd=d==null?"–":d>0?`<span class="up">▲${d}</span>`:d<0?`<span class="dn">▼${-d}</span>`:"=";
  return`<tr><td>${r[a]}</td><td style="text-align:left">${t.label}</td><td>${dd}</td><td>${fmt(val(t,i))}</td><td>${fmt(i>0?val(t,i-1):null)}</td></tr>`}).join("");
 $("tb").innerHTML=h}
function draw(){
 document.querySelectorAll("#wins button").forEach(b=>b.classList.toggle("on",b.dataset.w===win));
 document.querySelectorAll("#modes button").forEach(b=>b.classList.toggle("on",b.dataset.m===mode));
 $("chips").innerHTML=sel.map((a,k)=>{const t=T.find(x=>x.abbr===a),c=PAL[k%PAL.length];return`<button data-a="${a}" style="border-color:${c};color:${c}">${t?t.label:a} ✕</button>`}).join("");
 chart();table()}
sel=urlTeams.length?urlTeams:topN(3);draw();
