# Memória do projeto — NFL Dashboard

> Última atualização: 10/11/2026

Este documento reúne os pedidos, decisões e modificações do projeto que ficaram registrados na memória do assistente, com a data de cada um.

**Sobre as datas:** todas no fuso de Brasília. A memória não guarda data por linha, só a data da última atualização de cada arquivo.
As datas dos registros 1 a 26 são **aproximadas** (dia ou intervalo), deduzidas dessas atualizações e de eventos que você informou.
Os registros a partir do 27 levam a data conhecida.

## 1. Pedidos e decisões registrados

| # | Data (aprox.) | Tipo | Registro |
|---|---|---|---|
| 1 | 17/10/2026 | Pedido | Acompanhar semana a semana o desempenho dos times da NFL na temporada 26/27. |
| 2 | 17/10/2026 | Pedido | Métricas: pontos por jogo (feitos e cedidos), jardas aéreas e corridas (feitas e cedidas) e turnovers (forçados e cedidos). |
| 3 | 17/10/2026 | Decisão | Fonte de dados: nflverse, via a biblioteca Python `nflreadpy`. |
| 4 | 17/10/2026 | Preferência | Receber perguntas do assistente para montar um bom relatório semanal. |
| 5 | 17/10/2026 | Decisão | Formato: página/dashboard visual. |
| 6 | 17/10/2026 | Decisão | Escopo: todos os 32 times. |
| 7 | 17/10/2026 | Decisão | Médias por jogo em três janelas: última semana, últimas 3 semanas e temporada. |
| 8 | 17/10/2026 | Decisão | Geração: script Python que gera HTML estático a cada semana. |
| 9 | 17/10/2026 | Decisão | Métricas extras: saldos (pontos, jardas, turnovers), sacks e jardas por jogada. |
| 10 | 17/10/2026 | Decisão | Visualização: tabela ordenável, rankings por métrica e filtros por divisão e conferência. |
| 11 | 17/10/2026 | Pedido | Nomes dos times no formato "NE - Patriots". |
| 12 | 17/10/2026 | Pedido | Página separada de confrontos (semana atual se houver jogo pendente, senão a próxima), com comparativo e cada jogo expansível. |
| 13 | 17/10/2026 | Pedido | Vitórias e derrotas por janela (temporada, últimos 3 jogos, último jogo). |
| 14 | 17/10/2026 | Pedido | Histórico semanal (evolução) e EPA/jogada com success rate. |
| 15 | 17/10/2026 | Decisão | Não usar a API do Claude no script (sem depender de limites de uso); o card organiza os dados para o usuário concluir, sem pesquisa na internet. |
| 16 | 17/10/2026 | Pedido | Dados de jogadores por time: melhor recebedor, corredor e defensor, kickers e QBs. |
| 17 | 17/10/2026 | Implementação | Entregues: painel dos 32 times, confrontos, evolução semanal, EPA e success rate, redesign visual. |
| 18 | 17/10/2026 | Decisão | Página de jogadores separada; o card do confronto leva a ela com o filtro dos dois times. |
| 19 | 17–18/10/2026 | Pedido | Link no card para a evolução já filtrada pelos dois times (gostou do link de jogadores). |
| 20 | 18/10/2026 | Decisão | Repositório público no GitHub, com GitHub Actions para atualizar toda semana; antes, organizar o projeto em CSS, templates, script Python e README. |
| 21 | 18/10/2026 | Pedido | Criar o fluxo do GitHub Actions e publicar no GitHub Pages. |
| 22 | 18/10/2026 | Implementação | Site publicado no GitHub Pages com link de acesso. |
| 23 | 18/10/2026 | Pedido | Horários dos jogos em Brasília; rodapé "projeto independente, sem vínculo com a NFL"; versões das dependências fixas. |
| 24 | 18/10/2026 | Decisão | Licença MIT para o código; dados do nflverse sob CC BY 4.0 (atribuição); aviso de que as projeções são didáticas, sem apostas nem fins lucrativos. |
| 25 | 25/10/2026 | Pedido | Páginas funcionando nos playoffs, com etiqueta da rodada (Wild Card, Divisional, Conference, Super Bowl); etiqueta de jogo de divisão em linha própria no card. |
| 26 | 25–27/10/2026 | Pedido | Cores diferentes para cada rodada dos playoffs, funcionando nos temas claro e escuro; amarelo mantido no jogo de divisão. |
| 27 | 27/10/2026 | Pedido | Criar `PRD.md`, `arquitetura.md`, `regras.md` e `design.md` (pasta `docs/`) a partir do projeto, mantidos atualizados; depois, o `memory.md` com os registros e as datas. |
| 28 | 29/10/2026 | Pergunta | Se um `AGENTS.md` na raiz seria necessário para gerenciar os arquivos de documentação e direcionar o assistente. A mensagem saiu sem a interrogação e foi lida como pedido de criação. |
| 29 | 30/10/2026 | Decisão | O `AGENTS.md` não foi criado: o usuário confirmou que não alterou nenhum arquivo e o projeto segue sem ele. Reavaliar se passar a usar um agente de código (Claude Code, Codex, Cursor). |
| 30 | 30/10/2026 | Pedido | Planejar, antes de mexer em arquivos, duas features: logos dos times (páginas e tamanhos a avaliar) e indicação de onde cada jogo é transmitido no Brasil (ESPN, sportv2, ge tv, Disney+), marcada por ele. Opcional: se não atualizar na semana, nada muda no site nem no fluxo. |
| 31 | 30/10/2026 | Decisão | Logos oficiais baixados por script (a partir do nflverse), em todas as páginas; transmissões atualizadas por página admin com token do GitHub. |
| 32 | 31/10/2026 | Pedido | Seguir para a etapa 2 (transmissões) após a confirmação de que os logos funcionaram. Respostas: outros canais podem surgir no futuro; jogo sem canal marcado não mostra nada; a atualização será feita pelo celular e pelo desktop. |
| 33 | 03/11/2026 | Pedido | Em Confrontos, quando os dois times já se enfrentaram antes na temporada (rivais de divisão), mostrar ao expandir o card o placar do último jogo entre eles. |
| 34 | 04/11/2026 | Pedido | Atualizar todos os documentos com as etapas dos logos, das transmissões (página admin) e dos reencontros. |
| 35 | 10/11/2026 | Pedido | Em Confrontos, a lista de times em folga (bye) está confusa: mostrar só os times de folga da semana atual (semana 10 em diante). |
| 36 | 10/11/2026 | Implementação | Folgas corrigidas: a lista usa o calendário da temporada (sem siglas antigas como OAK, SD e STL) e mostra a semana no rótulo; nota de transmissão em linha própria. Testes em 45. |
| 37 | 10/11/2026 | Pedido | Página de playoffs com dados reais: seeds 1 a 7 de AFC e NFC com a última semana fechada, chaveamento do Wild Card e desempate pelas regras do usuário. Sem previsão de campeão, cenários nem parcial de semana. |
| 38 | 10/11/2026 | Decisão | Aba "Playoffs" no menu de todas as páginas públicas; RF-50 passa a cinco páginas. |
| 39 | 10/11/2026 | Decisão | HTML de teste (`playoffs-teste.html`, na raiz, fora do repositório) como protótipo do layout: quadro de seeds e chaveamento abaixo, sem variação ▲▼ e sem coluna de critério. |
| 40 | 10/11/2026 | Decisão | Sorteio pendente: marcação neutra ao lado do time, nunca amarela; a ordem provisória é alfabética pela sigla e o site nunca sorteia sozinho. |
| 41 | 10/11/2026 | Decisão | Motivo do desempate: a página aplica a ordem de critérios que o usuário pediu (`regras.md`, seção 9), sem criar uma ordem própria. |
| 42 | 10/11/2026 | Decisão | Ranking de pontos por média por jogo (pontos feitos menos sofridos, dividido pelos jogos), e não pelo total: os times têm números de jogos diferentes (bye). |
| 43 | 10/11/2026 | Decisão | Só semanas fechadas: a página usa a maior semana em que todos os jogos da temporada regular têm placar; não mostra parcial de semana. |
| 44 | 10/11/2026 | Decisão | Falha do build: se a checagem de consistência falhar, o build para e não publica a página; o site segue na última versão publicada. |
| 45 | 10/11/2026 | Decisão | Dispensa consciente do spec §9: a conferência de V-D-E contra os jogos fechados não é feita, porque a campanha sai dos mesmos jogos (tautológica). A regra "seeds 5 a 7 não são campeões" é conferida pela divisão com um campeão entre os seeds 1 a 4. |
| 46 | 10/11/2026 | Decisão | Desempate entre divisões: a ordem interna da divisão nunca cai no sorteio (quando cairia, o critério é ignorado). O sorteio decide só dentro da divisão. |
| 47 | 10/11/2026 | Decisão | Teste da checagem de campeão usa uma divisão inexistente para o seed 5, porque a versão com a divisão do seed 1 nunca falharia. |
| 48 | 10/11/2026 | Decisão | Datas: o pedido e a implementação são registrados em 10/11/2026 (data da sessão e da spec, aprovada nesse dia). |
| 49 | 10/11/2026 | Implementação | Página Playoffs na branch `playoffs-impl` (ainda não mesclada na `main`): `playoffs.py`, `team_week_tds` em `stats.py`, template, JS e CSS, integração ao build e à aba, commits `7b30d0c` a `dd93ba3`. Testes de 45 para 69. |
| 50 | 10/11/2026 | Implementação | Documentos atualizados (PRD, regras, arquitetura, design, memory e README), com as datas de 10/11/2026. |
| 51 | 10/11/2026 | Ocorrência | Marcador corrigido: a documentação dizia `__DADOS__`, mas o código (`render.py` e `layout.html`) usa `{{DATA}}`. Corrigido em `regras.md`, `arquitetura.md` e `memory.md` nesta data. |
| 52 | 10/11/2026 | Decisão | Aprovação do plano de implementação (`docs/superpowers/plans/2026-11-10-playoffs.md`, skill writing-plans) com execução por subagentes (subagent-driven-development), em worktree na branch `playoffs-impl`, com um commit por tarefa. |

## 2. Preferências de trabalho

| # | Data | Registro |
|---|---|---|
| P1 | 18–19/10/2026 (aprox.) | Entregar código e arquivos direto no chat, para copiar e colar (o usuário só faz o commit); sem arquivos para baixar nem zip. |
| P2 | 27/10/2026 | Manter `PRD.md`, `arquitetura.md`, `regras.md` e `design.md` (pasta `docs/`) sempre atualizados e enviá-los completos a cada modificação relacionada. |
| P3 | 27/10/2026 | Manter também este `memory.md`, com a data da solicitação, da modificação e da implementação. |

## 3. Decisões e modificações da conversa não registradas como pedido na memória

Itens que aconteceram no projeto, mas não têm registro próprio na memória do assistente. Datas só quando foram informadas.

| Data | Tipo | Registro |
|---|---|---|
| 18/10/2026 | Implementação | Projeto reorganizado em módulos Python, CSS, templates, JS e testes; páginas renomeadas para `index`, `confrontos`, `evolucao` e `jogadores`. |
| 18/10/2026 | Implementação | Fluxo do GitHub Actions criado e atualizado para ferramentas com Node 24 (`checkout@v7`, `setup-python@v7`, `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`) e runner `ubuntu-24.04`. |
| 18/10/2026 | Decisão | Versões das bibliotecas fixas em `requirements.txt` a partir do log da execução (polars 2.0.0 e nflreadpy 0.1.5). |
| 18/10/2026 | Implementação | Rodapé com atribuição CC BY 4.0, licença MIT e avisos didáticos na página e nos cards de Confrontos. |
| 18–19/10/2026 | Implementação | Contador de acessos opcional (GoatCounter, sem cookies) em `config.py` e `render.py`; teste ajustado para não depender do número de scripts. |
| 20/10/2026 | Ocorrência | A execução agendada das 09:00 saiu com atraso de cerca de 4h26 (13:26); o build manual das 13:02 funcionou. |
| 20/10/2026 | Decisão | Agendamento passou do minuto 00 para o minuto 7 (menos disputado) e os testes deixaram de rodar nas execuções agendadas. |
| 20/10/2026 | Decisão | Variável `NFL_SEASON` criada no GitHub; Dependabot aprovado para o `certifi`. |
| 24–25/10/2026 | Implementação | Etiqueta amarela de jogo de divisão no card de Confrontos, depois movida para linha própria. |
| 25/10/2026 | Decisão | Agendamento em segunda, terça e sábado às 11:07 UTC (08:07 em Brasília). *Confirmar no arquivo do fluxo.* |
| 25–27/10/2026 | Implementação | Playoffs em Confrontos, com seleção da rodada, "x" no campo neutro e cores por rodada (azul, violeta, laranja e rosa), mantendo o amarelo para jogo de divisão. |
| 27/10/2026 | Implementação | Criação dos documentos `PRD.md`, `arquitetura.md`, `regras.md`, `design.md` e `memory.md`. |
| 29/10/2026 | Ocorrência | `AGENTS.md` e atualizações de `arquitetura.md`, `regras.md` e `memory.md` foram propostos por engano (pergunta lida como pedido) e **não foram aplicados**. |
| 30/10/2026 | Implementação | Etapa dos logos: `comum.js`, `logos.py` (script de uso único), `requirements-logos.txt`, cores dos times nas páginas, logos em todas as páginas e aviso de marcas no rodapé. Cabeçalho do card com sigla e apelido em linhas separadas em telas estreitas e seta no canto inferior. |
| 30–31/10/2026 | Ocorrência | O build falhou porque `config.py` e `render.py` do repositório não tinham o `REPO_URL`; corrigido com os arquivos completos. |
| 31/10/2026 | Ocorrência | Confirmado que a etapa dos logos funcionou. |
| 31/10/2026 | Implementação | Etapa das transmissões: `broadcasts.py`, `data/transmissoes.json`, linha "Onde assistir" e nota no card, página `admin.html` (token do GitHub, política de segurança, sem contador) e `CHANNELS` no `config.py`. |
| 31/10–03/11/2026 | Ocorrência | O editor acusava erro no `layout.html` por causa de `{{DATA}}` dentro de um script; o marcador passou a ser `__DADOS__` (a documentação foi corrigida para `{{DATA}}` em 10/11/2026, registro 51). |
| 03/11/2026 | Ocorrência | Build e deploy confirmados sem erro após o ajuste do marcador. |
| 03/11/2026 | Implementação | Reencontros: `rematches.py` e o bloco "Último confronto nesta temporada" no card expandido. |
| 04/11/2026 | Implementação | Atualização dos documentos `PRD.md`, `arquitetura.md`, `regras.md`, `design.md` e `memory.md` e do `README.md`. |
| 10/11/2026 | Ocorrência | Lista de folgas com 8 times na semana 6 (4 reais); causa: o cadastro de times do nflverse tem siglas antigas (OAK, SD, STL) e `LAR` duplicando os Rams. Corrigido filtrando pelos times do calendário da temporada. |

## 4. Pendências

| Pendência | Situação |
|---|---|
| Confirmar o agendamento do fluxo (`cron: "7 11 * * 1,2,6"`) | Sem resposta: os documentos assumem segunda, terça e sábado às 11:07 UTC. |
| Teste real da página admin com o token do GitHub | A página foi testada com a API simulada; o primeiro salvamento real ainda não foi confirmado. |
| Reforço de segurança do admin (transmissões em branch separada e `main` protegida) | Oferecido, sem decisão. |
| Contagem de testes | Conferido em 10/11/2026: o `pytest` tinha 44 testes (não 46); agora são 45, com o teste de folgas. Documentos atualizados. Com a página Playoffs, são 69 (reconfirmar na verificação final da implementação). |
| Touchdowns: `fumble_recovery_tds` | **Em aberto.** A coluna ficou fora de `TD_COLS` (regra 9.2 de `regras.md`) porque a sobreposição com `rushing_tds` não foi confirmada. Confirmar no dicionário do nflverse; o dicionário não estava acessível na implementação. |
| Playoffs após a temporada regular | **Em aberto.** A página continua mostrando os seeds finais e o chaveamento do Wild Card, sem resultados de playoffs. Confirmar esse comportamento (spec, seção 12, item 3). |
| Histórico de semanas na página Playoffs | Fora desta etapa: a página mostra só a última semana fechada. Guardar o histórico no JSON fica para uma etapa futura. |
| Verificação visual da página Playoffs | Pendente: 360, 390, 414 e 1100 px com dados reais, sem rolagem lateral da página (Tarefa 8 do plano). |
| Divergência do marcador `__DADOS__` / `{{DATA}}` | Resolvida em 10/11/2026: o código usa `{{DATA}}`; a documentação foi corrigida (registro 51). |
| Sorteio na tela (spec, seção 12, item 2) | Resolvida: etiqueta neutra "Sorteio pendente" ao lado do time (registro 40). |
| Touchdowns: colunas e definição (spec, seção 12, item 1) | Resolvida, exceto `fumble_recovery_tds` (ver acima). Colunas e decisão: spike da Tarefa 1 e `regras.md`, seção 9.2. |

## 5. Como manter este documento

1. A cada nova solicitação, decisão ou implementação, acrescentar uma linha com a **data exata** (dia da solicitação e, quando diferente, da implementação).
2. Registrar o tipo: Pedido, Pergunta, Decisão, Implementação, Preferência ou Ocorrência.
3. Quando o registro mudar `PRD.md`, `arquitetura.md`, `regras.md` ou `design.md`, atualizar também o documento correspondente e o histórico dele.
4. Se um registro for substituído por outro, manter as duas linhas e indicar qual valeu por último.
5. Ao resolver uma pendência, atualizar a tabela da seção 4.

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir dos registros da memória e da conversa. |
| 30/10/2026 | Inclusão dos registros 26 a 29 (cores por rodada, documentos e a decisão sobre o `AGENTS.md`); tipo "Pergunta" criado; seção 3 corrigida. |
| 04/11/2026 | Inclusão dos registros 30 a 34 (logos, transmissões, reencontros e atualização dos documentos); seção 3 ampliada; nova seção de pendências. |
| 10/11/2026 | Inclusão dos registros 35 e 36 (folgas), ocorrência na seção 3 e pendência da contagem de testes resolvida. |
| 10/11/2026 | Inclusão dos registros 37 a 51 (página Playoffs: pedido, decisões, implementação e correção do marcador); pendências da página e touchdowns, com as resolvidas marcadas. |
| 10/11/2026 | Inclusão do registro 52 (aprovação do plano de implementação e da execução por subagentes em worktree). |