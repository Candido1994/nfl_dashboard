const D=window.__DATA__;
const WL={w1:"Última semana",w3:"Últimas 3 semanas",s:"Temporada"};
let win="s",flt="ALL",sk="pd",sd=-1,rk="pd";
const M=D.metrics,mk=Object.fromEntries(M.map(m=>[m.k,m]));
document.querySelector("h1").textContent="NFL "+D.season+" – Painel semanal";
document.getElementById("sub").textContent="Semana "+D.week+" • atualizado em "+D.updated+" • médias por jogo";
const $=id=>document.getElementById(id);
$("wins").innerHTML=Object.entries(WL).map(([k,l])=>`<button data-w="${k}">${l}</button>`).join("");
$("wins").onclick=e=>{if(e.target.dataset.w){win=e.target.dataset.w;draw()}};
const divs=[...new Set(D.teams.map(t=>t.div).filter(Boolean))].sort();
$("flt").innerHTML='<option value="ALL">Todos os times</option><option>AFC</option><option>NFC</option>'+divs.map(d=>`<option>${d}</option>`).join("");
$("flt").onchange=e=>{flt=e.target.value;draw()};
$("rk").innerHTML=M.map(m=>`<option value="${m.k}">${m.l}</option>`).join("");
$("rk").onchange=e=>{rk=e.target.value;draw()};
function rows(){return D.teams.filter(t=>flt==="ALL"||t.conf===flt||t.div===flt).filter(t=>t[win]).map(t=>({t,v:t[win]}))}
function draw(){
 document.querySelectorAll("#wins button").forEach(b=>b.classList.toggle("on",b.dataset.w===win));
 const R=rows();
 R.sort((a,b)=>sk==="team"?sd*-a.t.abbr.localeCompare(b.t.abbr):sd*(a.v[sk]-b.v[sk]));
 const sc=k=>sk===k?` class="sorted ${(k==="team"?sd<0:sd>0)?"asc":"desc"}"`:"";
 let h=`<tr><th data-s="team"${sc("team")}>Time</th><th data-s="g"${sc("g")}>J</th><th data-s="pct"${sc("pct")}>V-D</th>`+M.map(m=>`<th data-s="${m.k}"${sc(m.k)}>${m.l}</th>`).join("")+"</tr>";
 h+=R.map(r=>"<tr><td><span class=\"tn\">"+teamLogo(r.t.abbr,24)+r.t.label+"</span></td><td>"+r.v.g+"</td><td>"+r.v.rec+"</td>"+M.map(m=>{
  const x=r.v[m.k],c=(m.k.endsWith("diff")||m.k==="pd")?(x>0?"var(--good)":x<0?"var(--bad)":""):"";
  return `<td style="color:${c}">${x==null?"–":x}</td>`}).join("")+"</tr>").join("");
 $("tb").innerHTML=h;
 $("tb").onclick=e=>{const s=e.target.dataset.s;if(!s)return;sd=(sk===s)?-sd:-1;sk=s;draw()};
 const m=mk[rk],S=rows().filter(r=>r.v[rk]!=null).sort((a,b)=>(m.hb?-1:1)*(a.v[rk]-b.v[rk]));
 const mx=Math.max(...S.map(r=>Math.abs(r.v[rk])))||1;
 $("rank").innerHTML=S.map((r,i)=>`<div class="r"><span class="n"><b>${i+1}</b>${teamLogo(r.t.abbr,20)}${r.t.label}</span><span class="t"><i style="width:${Math.abs(r.v[rk])/mx*100}%;background:${r.v[rk]<0?"var(--bad)":"var(--acc)"}"></i></span><span class="v">${r.v[rk]}</span></div>`).join("");
}
draw();