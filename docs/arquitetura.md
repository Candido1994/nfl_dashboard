# Arquitetura — NFL Dashboard

> Última atualização: 27/10/2026

## 1. Visão geral

```
nflverse (dados abertos)
      │  nflreadpy + polars
      ▼
Python (nfl_dashboard/)  ──►  JSON por página  ──►  templates/ + static/
                                                         │
                                                         ▼
                                                    site/*.html
                                                         │
                          GitHub Actions (agendado/manual/push)
                                                         ▼
                                                   GitHub Pages
```

O Python calcula tudo e embute o resultado como JSON em cada página (`window.__DATA__`). O navegador só monta tabelas,
filtros e gráficos. Não há servidor, banco de dados nem chamadas de rede em tempo de leitura (exceto a fonte e o contador de acessos).

## 2. Estrutura do repositório

```
nfl_dashboard/
├── generate.py                 # atalho da linha de comando
├── LICENSE                     # MIT
├── requirements.txt            # versões exatas
├── requirements-dev.txt        # + ferramentas de teste
├── .github/
│   ├── workflows/atualizar_site.yml
│   └── dependabot.yml
├── nfl_dashboard/              # código Python
│   ├── config.py
│   ├── stats.py
│   ├── players.py
│   ├── render.py
│   ├── cli.py
│   └── __main__.py
├── templates/
│   ├── layout.html
│   └── pages/ (painel, confrontos, evolucao, jogadores)
├── static/
│   ├── css/style.css
│   └── js/ (painel, confrontos, evolucao, jogadores)
├── tests/
├── docs/                       # estes documentos
└── site/                       # saída gerada (ignorada pelo Git)
```

## 3. Módulos Python

| Módulo | Responsabilidade |
|---|---|
| `config.py` | Lista de métricas (`METRICS`: chave, rótulo, maior-é-melhor), temporada padrão, fuso e rótulo do fuso, `REPO_URL`, `GOATCOUNTER_URL`. |
| `stats.py` | Estatísticas dos times: `build_games`, `summarize`, `build_teams`, `compute_ranks`, `select_games`, `build_matchups`, `build_history`, `local_kickoff`, `divisional`, `load_team_info`, `team_weeks_from`. |
| `players.py` | Agregação de jogadores por janela e por categoria (`build_player_pages`, `load_players`, `PLAYER_CATS`). |
| `render.py` | Lê `templates/` e `static/`, substitui os marcadores, grava as páginas e copia o `static/`. Define as quatro páginas e a ordem das abas. |
| `cli.py` | Orquestra: baixa e calcula os dados, monta o dicionário de cada página e chama `write_site`. |

`polars` e `nflreadpy` são importados dentro das funções que os usam, para os módulos poderem ser importados (e testados) sem essas bibliotecas.

## 4. Fluxo de dados

1. `build_games(season)` junta agenda (jogos disputados da temporada regular), estatísticas semanais dos times e play-by-play (EPA e success rate por time e semana). Gera uma linha por time por jogo, com os números do time e do adversário.
2. `build_teams` resume cada time em três janelas: `w1` (último jogo), `w3` (últimos 3) e `s` (temporada).
3. `compute_ranks` calcula a posição de cada time por métrica e janela.
4. `build_matchups` pega o calendário e `select_games` escolhe os jogos a mostrar (semana pendente ou rodada dos playoffs); `local_kickoff` converte o horário; `divisional` marca jogos de divisão.
5. `build_history` recalcula o acumulado e a média móvel ao fim de cada semana.
6. `load_players` baixa as estatísticas semanais de jogadores e `build_player_pages` as agrega por janela.
7. `cli.main` monta o JSON de cada página e `render.write_site` grava os HTML.

## 5. Modelo de dados por página (`window.__DATA__`)

| Página | Campos principais |
|---|---|
| Painel | `season`, `week`, `updated`, `metrics[]`, `teams[]` (cada um com `abbr`, `label`, `conf`, `div` e as janelas `w1`, `w3`, `s`). |
| Confrontos | `season`, `updated`, `tz`, `metrics[]`, `nteams`, `ranks{s,w3,w1}`, `week`, `round`, `games[]`, `bye[]`. Cada jogo: `away`, `home` (times), `day`, `time`, `as`, `hs`, `division`, `round`, `neutral`. |
| Evolução | `season`, `updated`, `metrics[]` (+ aproveitamento), `weeks[]`, `teams[]` com `series[]` (`week`, `s`, `w3`). |
| Jogadores | `season`, `updated`, `week`, `teams[]`, `cats[]` (colunas e ordenação padrão), `players{qb,rb,rec,def,k}` com as janelas `s`, `w3`, `w1`. |

Cada janela de um time guarda as médias por jogo das métricas, `g` (jogos), `rec` (campanha) e `pct` (aproveitamento).

## 6. Camada de apresentação

- **Templates:** `layout.html` traz cabeçalho, abas, rodapé e scripts. Os marcadores são `{{TITLE}}`, `{{H1}}`, `{{BODY_CLASS}}`, `{{NAV}}`, `{{VERSION}}`, `{{SCRIPT}}`, `{{REPO_URL}}`, `{{ANALYTICS}}`, `{{ANALYTICS_NOTE}}`, `{{CONTENT}}` e `{{DATA}}`. O conteúdo e os dados são trocados por último, para não serem reprocessados.
- **Páginas:** cada arquivo em `templates/pages/` tem só o miolo (`<main>`); o JS da página tem o mesmo nome.
- **JavaScript:** um script por página, sem bibliotecas externas. O gráfico de evolução é SVG feito à mão.
- **Cache:** CSS e JS levam `?v=<data-hora do build>` para o navegador não usar arquivos antigos.
- **Parâmetros de URL:** `jogadores.html?times=NE,SF&pos=qb&janela=w3` e `evolucao.html?times=NE,SF&metrica=epa&janela=w3&modo=r`. Os times são validados contra a lista conhecida.

## 7. Publicação e automação

| Item | Configuração |
|---|---|
| Fluxo | `.github/workflows/atualizar_site.yml`, nome "Atualizar site". |
| Gatilhos | Agendado (segunda, terça e sábado às 11:07 UTC = 08:07 em Brasília), manual (`workflow_dispatch`) e `push` na `main`. |
| Jobs | `build` (instala, testa, gera e envia o artefato) e `deploy` (publica no Pages). |
| Testes | Rodam em push e execução manual; **não** rodam nas execuções agendadas. |
| Permissões | `contents: read`, `pages: write`, `id-token: write`. |
| Concorrência | Grupo `pages`, sem cancelar a execução em andamento. |
| Runner | `ubuntu-24.04`, Python 3.12. |
| Actions | `checkout@v7`, `setup-python@v7`, `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`. |
| Variáveis | `NFL_SEASON` (variável do repositório, opcional) e `NFL_TZ` (definida no fluxo). |
| Dependabot | Pedido mensal para as actions; alertas de segurança podem abrir pedidos para as bibliotecas Python. |

## 8. Dependências

`requirements.txt` fixa as versões exatas da última execução bem-sucedida (por exemplo `nflreadpy` 0.1.5 e `polars` 2.0.0), incluindo as
dependências indiretas. `tzdata` fica sem versão. `requirements-dev.txt` acrescenta `pytest`.

## 9. Configuração

| Onde | O quê |
|---|---|
| `nfl_dashboard/config.py` | `DEFAULT_SEASON`, `DEFAULT_TZ`, `REPO_URL`, `GOATCOUNTER_URL`, `METRICS`. |
| Variável `NFL_SEASON` | Temporada (ambiente local ou variável do GitHub). |
| Variável `NFL_TZ` | Fuso de exibição (padrão `America/Sao_Paulo`). |
| `--out` | Pasta de saída do site (padrão `site`). |

## 10. Testes

24 testes em `tests/`: montagem das páginas (rodapé, avisos, contador, escape do JSON), rankings, agregação de jogadores, conversão de horários,
jogo de divisão, seleção de jogos nos playoffs e consistência entre as rodadas, o CSS e o JS de Confrontos. Não dependem de internet.

## 11. Segurança

- JSON dentro de `<script>` troca `</` por `<\/`, para um texto nos dados não fechar a tag.
- Nomes de jogadores são escapados antes de entrar no HTML; os filtros da URL só aceitam times conhecidos.
- O projeto não tem senhas, tokens nem chaves; as permissões do fluxo são mínimas.
- O fluxo não é disparado por pull requests de terceiros.
- Recomendado na conta do GitHub: verificação em duas etapas, e-mail privado e alertas do Dependabot ligados.

## 12. Playoffs

`select_games` usa o `game_type` do nflverse (`WC`, `DIV`, `CON`, `SB`). Com a temporada regular encerrada, mostra a primeira rodada com jogo pendente
e, se todas já foram disputadas, a última. Jogos sem times definidos são ignorados. As demais páginas continuam na temporada regular.

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir do estado atual do projeto. |