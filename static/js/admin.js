const D=window.__DATA__;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const R=D.repo,API="https://api.github.com";
const FILE=`${API}/repos/${R.owner}/${R.name}/contents/${R.path}`;
const TKEY="nfl_admin_token";
const IDS=D.channels.map(c=>c.id);
let memTok="";
const sel={};
D.games.forEach(g=>{sel[g.key]=new Set(g.canais)});
const snap=()=>JSON.stringify(D.games.map(g=>[g.key,IDS.filter(id=>sel[g.key].has(id))]));
let saved=snap();

document.querySelector("h1").textContent="NFL "+D.season+" – Transmissões (admin)";
$("sub").textContent="Atualizado em "+D.updated+" • semana atual e a seguinte";

// ---- token (na memória; guardado no navegador só se a pessoa pedir) ----
const getTok=()=>{if(memTok)return memTok;try{return localStorage.getItem(TKEY)||""}catch(e){return ""}};
const setTok=(v,keep)=>{memTok=v;try{keep&&v?localStorage.setItem(TKEY,v):localStorage.removeItem(TKEY)}catch(e){}};
function tkState(){const t=getTok();$("tkstate").textContent=t?"· pronto":"· necessário para salvar";$("tkbox").open=!t}

// ---- mensagens ----
function say(text,kind){const m=$("msg");m.textContent=text;m.className="msg"+(kind?" "+kind:"")}
function actionsLink(){const a=document.createElement("a");a.href=`https://github.com/${R.owner}/${R.name}/actions`;a.textContent=" Abrir Actions";a.target="_blank";a.rel="noopener noreferrer";$("msg").appendChild(a)}
class GhError extends Error{constructor(s){super("GitHub "+s);this.status=s}}
const errText=e=>e.status===401?"Token inválido ou expirado. Gere outro e cole em \"Token do GitHub\".":
 e.status===403?"Sem permissão. O token precisa de \"Contents: Read and write\" neste repositório.":
 e.status===404?"Repositório não encontrado para este token. Confira se o token foi criado para o repositório certo.":
 e.status===409||e.status===422?"O arquivo mudou durante o salvamento. Toque em Salvar de novo.":
 e.message&&!/^GitHub \d+$/.test(e.message)?e.message:"Falha de rede ou resposta inesperada. Tente de novo.";

// ---- tela ----
function render(){
 if(!D.games.length){$("adm").innerHTML='<p class="hint">Nenhum jogo pendente para marcar agora.</p>';return}
 const weeks=[...new Set(D.games.map(g=>g.week))];
 $("adm").innerHTML=weeks.map(w=>{
  const gs=D.games.filter(g=>g.week===w),rd=gs[0].round;
  return`<h2>${rd?"Playoffs · "+esc(rd):"Semana "+w}</h2>`+gs.map(g=>`<section class="adm-card"><div class="adm-h">${teamLogo(g.awayAbbr,28)}<b>${esc(g.away)}</b><span class="at">@</span><b>${esc(g.home)}</b>${teamLogo(g.homeAbbr,28)}</div><div class="m">${esc(g.day)} ${esc(g.time)}</div><div class="chks">${D.channels.map(c=>`<label class="chk"><input type="checkbox" data-k="${esc(g.key)}" data-c="${esc(c.id)}"${sel[g.key].has(c.id)?" checked":""}><span>${esc(c.label)}</span></label>`).join("")}</div></section>`).join("")}).join("")}
function dirty(){$("dirty").textContent=snap()===saved?"":"Alterações não salvas"}
$("adm").onchange=e=>{const i=e.target,k=i.dataset&&i.dataset.k;if(!k||!sel[k])return;i.checked?sel[k].add(i.dataset.c):sel[k].delete(i.dataset.c);dirty()};

// ---- GitHub ----
const hdr=t=>({"Authorization":"Bearer "+t,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"});
async function getRemote(t){
 const r=await fetch(FILE+"?ref="+encodeURIComponent(R.branch),{headers:hdr(t),cache:"no-store"});
 if(r.status===404)return{sha:null,jogos:{}};
 if(!r.ok)throw new GhError(r.status);
 const j=await r.json();
 let data;
 try{data=JSON.parse(decodeURIComponent(escape(atob(String(j.content).replace(/\s/g,"")))))}
 catch(e){throw new Error("O arquivo data/transmissoes.json no repositório está com erro de formato. Corrija-o no GitHub e tente de novo.")}
 return{sha:j.sha,jogos:(data&&typeof data.jogos==="object"&&data.jogos&&!Array.isArray(data.jogos))?data.jogos:{}}}
async function prefill(){
 const t=getTok();if(!t)return;
 try{const rem=await getRemote(t);D.games.forEach(g=>{sel[g.key]=new Set(Array.isArray(rem.jogos[g.key])?rem.jogos[g.key]:[])});saved=snap();render();dirty();say("Marcações carregadas do repositório.","ok")}
 catch(e){say(errText(e),"err")}}
async function save(){
 const t=getTok();
 if(!t){say("Cole o seu token do GitHub antes de salvar.","err");$("tkbox").open=true;return}
 $("save").disabled=true;say("Salvando…");
 try{
  for(let tentativa=0;tentativa<2;tentativa++){
   const rem=await getRemote(t);
   const jogos={...rem.jogos};
   D.games.forEach(g=>{const ids=IDS.filter(id=>sel[g.key].has(id));if(ids.length)jogos[g.key]=ids;else delete jogos[g.key]});
   const ordenado=Object.fromEntries(Object.keys(jogos).sort().map(k=>[k,jogos[k]]));
   const texto=JSON.stringify({versao:1,jogos:ordenado},null,2)+"\n";
   const corpo={message:"Atualiza transmissões ("+new Date().toLocaleDateString("pt-BR")+")",content:btoa(unescape(encodeURIComponent(texto))),branch:R.branch};
   if(rem.sha)corpo.sha=rem.sha;
   const r=await fetch(FILE,{method:"PUT",headers:{...hdr(t),"Content-Type":"application/json"},body:JSON.stringify(corpo)});
   if(r.ok){saved=snap();dirty();say("Salvo! O site é atualizado em 1 a 2 minutos.","ok");actionsLink();return}
   if((r.status===409||r.status===422)&&tentativa===0)continue;
   throw new GhError(r.status)}
 }catch(e){say(errText(e),"err")}
 finally{$("save").disabled=false}}

// ---- eventos ----
$("save").onclick=save;
$("tksave").onclick=()=>{const v=$("tok").value.trim();if(!v){say("Cole o token no campo.","err");return}setTok(v,$("rem").checked);$("tok").value="";say("Token pronto para uso.","ok");tkState();prefill()};
$("tkclear").onclick=()=>{setTok("",false);tkState();say("Token removido.")};
render();tkState();dirty();if(getTok())prefill();