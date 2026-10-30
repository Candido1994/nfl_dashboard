# Memória do projeto — NFL Dashboard

> Última atualização: 27/10/2026

Este documento reúne os pedidos, decisões e modificações do projeto que ficaram registrados na memória do assistente, com a data de cada um.

**Sobre as datas:** a memória não guarda data por linha, só a data da última atualização de cada arquivo. As datas da seção 1 são **aproximadas**
(dia ou intervalo), deduzidas dessas atualizações e de eventos que você informou. Os registros novos levam a data exata.

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

## 2. Preferências de trabalho

| # | Data (aprox.) | Registro |
|---|---|---|
| P1 | 18–19/10/2026 | Entregar código e arquivos direto no chat, para copiar e colar (o usuário só faz o commit); sem arquivos para baixar nem zip. |
| P2 | 27/10/2026 | Manter `PRD.md`, `arquitetura.md`, `regras.md` e `design.md` (pasta `docs/`) sempre atualizados e enviá-los completos a cada modificação relacionada. |
| P3 | 27/10/2026 | Manter também este `memory.md`, com a data da solicitação, da modificação e da implementação. |

## 3. Decisões e modificações da conversa ainda não registradas na memória

Itens que aconteceram no projeto mas não viraram registro na memória do assistente. Datas só quando foram informadas.

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

## 4. Como manter este documento

1. A cada nova solicitação, decisão ou implementação, acrescentar uma linha com a **data exata** (dia da solicitação e, quando diferente, da implementação).
2. Registrar o tipo: Pedido, Decisão, Implementação, Preferência ou Ocorrência.
3. Quando o registro mudar `PRD.md`, `arquitetura.md`, `regras.md` ou `design.md`, atualizar também o documento correspondente e o histórico dele.
4. Se um registro for substituído por outro, manter as duas linhas e indicar qual valeu por último.

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir dos registros da memória e da conversa. |