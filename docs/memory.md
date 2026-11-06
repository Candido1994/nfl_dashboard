# Memória do projeto — NFL Dashboard

> Última atualização: 04/11/2026

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
| 31/10–03/11/2026 | Ocorrência | O editor acusava erro no `layout.html` por causa de `{{DATA}}` dentro de um script; o marcador passou a ser `__DADOS__`. |
| 03/11/2026 | Ocorrência | Build e deploy confirmados sem erro após o ajuste do marcador. |
| 03/11/2026 | Implementação | Reencontros: `rematches.py` e o bloco "Último confronto nesta temporada" no card expandido. |
| 04/11/2026 | Implementação | Atualização dos documentos `PRD.md`, `arquitetura.md`, `regras.md`, `design.md` e `memory.md` e do `README.md`. |

## 4. Pendências

| Pendência | Situação |
|---|---|
| Confirmar o agendamento do fluxo (`cron: "7 11 * * 1,2,6"`) | Sem resposta: os documentos assumem segunda, terça e sábado às 11:07 UTC. |
| Teste real da página admin com o token do GitHub | A página foi testada com a API simulada; o primeiro salvamento real ainda não foi confirmado. |
| Reforço de segurança do admin (transmissões em branch separada e `main` protegida) | Oferecido, sem decisão. |
| Contagem de testes (46) | Conferir no `pytest` do repositório se o total confere. |

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