# Arquitetura — NFL Dashboard

> Última atualização: 10/11/2026

## 1. Visão geral

```
nflverse (dados abertos)
      │  nflreadpy + polars
      ▼
Python (nfl_dashboard/)  ──►  JSON por página  ──►  templates/ + static/
        ▲                                                │
 data/transmissoes.json                                  ▼
 (gravado pela página admin                         site/*.html
  pela API do GitHub)                                    │
                          GitHub Actions (agendado/manual/push)
                                                         ▼
                                                   GitHub Pages
```

O Python calcula tudo e embute o resultado como JSON em cada página (`window.__DATA__`). O navegador só monta tabelas,
filtros e gráficos. Não há servidor nem banco de dados. Em tempo de leitura, só há chamadas externas para a fonte (Google Fonts),
o contador de acessos (páginas públicas) e, na página admin, a API do GitHub.

## 2. Estrutura do repositório

```
nfl_dashboard/
├── README.md
├── generate.py                 # atalho da linha de comando
├── LICENSE                     # MIT
├── requirements.txt            # versões exatas
├── requirements-dev.txt        # + ferramentas de teste
├── requirements-logos.txt      # + Pillow, só para baixar os logos (uso único)
├── .github/
│   ├── workflows/atualizar_site.yml
│   └── dependabot.yml
├── data/
│   └── transmissoes.json       # canais por jogo (gravado pela página admin)
├── nfl_dashboard/              # código Python
│   ├── config.py
│   ├── stats.py
│   ├── players.py
│   ├── broadcasts.py
│   ├── rematches.py
│   ├── logos.py
│   ├── render.py
│   ├── cli.py
│   └── __main__.py
├── templates/
│   ├── layout.html
│   └── pages/ (painel, confrontos, evolucao, jogadores, admin)
├── static/
│   ├── css/style.css
│   ├── js/ (comum.js, painel, confrontos, evolucao, jogadores, admin)
│   └── img/teams/              # 32 logos <sigla>.png (128x128)
├── tests/
├── docs/                       # PRD.md, arquitetura.md, regras.md, design.md, memory.md
└── site/                       # saída gerada (ignorada pelo Git)
```

## 3. Módulos Python

| Módulo | Responsabilidade |
|---|---|
| `config.py` | Lista de métricas (`METRICS`), canais de transmissão (`CHANNELS`), temporada padrão, fuso e rótulo do fuso, `REPO_URL`, `GOATCOUNTER_URL`. |
| `stats.py` | Estatísticas dos times: `build_games`, `summarize`, `build_teams`, `compute_ranks`, `select_games`, `bye_teams`, `build_matchups`, `build_history`, `local_kickoff`, `divisional`, `load_team_info`, `team_weeks_from`. |
| `players.py` | Agregação de jogadores por janela e por categoria (`build_player_pages`, `load_players`, `PLAYER_CATS`). |
| `broadcasts.py` | Transmissões: `load_broadcasts` (lê e valida o JSON), `attach_channels` (acrescenta os canais a cada jogo), `schedule_rows` (calendário completo) e `admin_page` (dados da página admin). |
| `rematches.py` | Reencontros: `last_meeting` e `attach_last_meetings` (placar do último jogo entre os dois times). |
| `logos.py` | Cores dos times (`load_team_colors`) e script de uso único que baixa e converte os logos (`python -m nfl_dashboard.logos`). |
| `render.py` | Lê `templates/` e `static/`, substitui os marcadores, grava as páginas e copia o `static/`. Define as quatro páginas públicas (`PAGES`) e as ocultas (`HIDDEN_PAGES`, com a admin). |
| `cli.py` | Orquestra: baixa e calcula os dados, monta o dicionário de cada página e chama `write_site`. |

`polars`, `nflreadpy` e `Pillow` são importados dentro das funções que os usam, para os módulos poderem ser importados (e testados) sem essas bibliotecas.

## 4. Fluxo de dados

1. `build_games(season)` junta agenda (jogos disputados da temporada regular), estatísticas semanais dos times e play-by-play (EPA e success rate). Gera uma linha por time por jogo, com os números do time e do adversário.
2. `build_teams` resume cada time em três janelas: `w1` (último jogo), `w3` (últimos 3) e `s` (temporada).
3. `schedule_rows` carrega o calendário completo (todas as fases) uma única vez.
4. `compute_ranks` calcula a posição de cada time por métrica e janela.
5. `build_matchups` escolhe os jogos a mostrar (`select_games`: semana pendente ou rodada dos playoffs), converte o horário (`local_kickoff`) e marca jogos de divisão (`divisional`).
6. `load_broadcasts` lê `data/transmissoes.json` e `attach_channels` acrescenta `key` e `canais` a cada jogo.
7. `attach_last_meetings` acrescenta `previous` (placar do último jogo entre os dois times, se houver).
8. `build_history` recalcula o acumulado e a média móvel ao fim de cada semana.
9. `load_players` baixa as estatísticas semanais de jogadores e `build_player_pages` as agrega por janela.
10. `admin_page` monta os jogos da página admin (semana exibida e a seguinte).
11. `load_team_colors` busca a cor de cada time; ela é copiada para os dados de todas as páginas (`colors`).
12. `cli.main` junta tudo e `render.write_site` grava os HTML.

## 5. Modelo de dados por página (`window.__DATA__`)

Todas as páginas recebem também `colors` (`{sigla: "#RRGGBB"}`).

| Página | Campos principais |
|---|---|
| Painel | `season`, `week`, `updated`, `metrics[]`, `teams[]` (cada um com `abbr`, `label`, `conf`, `div` e as janelas `w1`, `w3`, `s`). |
| Confrontos | `season`, `updated`, `tz`, `metrics[]`, `nteams`, `ranks{s,w3,w1}`, `week`, `round`, `games[]`, `bye[]` (rótulos "SIGLA - Apelido" dos times de folga na semana exibida, calculados por `bye_teams`). Cada jogo: `away`, `home` (times), `day`, `time`, `as`, `hs`, `division`, `round`, `neutral`, `key`, `canais[]` (nomes) e `previous` (`week`, `round`, `day`, `away`, `as`, `home`, `hs`, ou `null`). |
| Evolução | `season`, `updated`, `metrics[]` (+ aproveitamento), `weeks[]`, `teams[]` com `series[]` (`week`, `s`, `w3`). |
| Jogadores | `season`, `updated`, `week`, `teams[]`, `cats[]` (colunas e ordenação padrão), `players{qb,rb,rec,def,k}` com as janelas `s`, `w3`, `w1`. |
| Admin | `season`, `updated`, `channels[]` (`id`, `label`), `games[]` (`key`, `week`, `round`, `away`, `home`, `awayAbbr`, `homeAbbr`, `day`, `time`, `canais[]` com ids) e `repo` (`owner`, `name`, `branch`, `path`). |

Cada janela de um time guarda as médias por jogo das métricas, `g` (jogos), `rec` (campanha) e `pct` (aproveitamento).

## 6. Camada de apresentação

- **Templates:** `layout.html` traz cabeçalho, abas, rodapé e scripts. Os marcadores são `{{TITLE}}`, `{{H1}}`, `{{BODY_CLASS}}`, `{{NAV}}`, `{{VERSION}}`, `{{SCRIPT}}`, `{{REPO_URL}}`, `{{HEAD_EXTRA}}`, `{{ANALYTICS}}`, `{{ANALYTICS_NOTE}}` e `{{CONTENT}}`. Os dados entram por último, no marcador `__DADOS__` (nome de variável válido em JavaScript, para o editor não acusar erro de sintaxe).
- **Páginas:** cada arquivo em `templates/pages/` tem só o miolo (`<main>`); o JS da página tem o mesmo nome.
- **Páginas ocultas:** a admin fica em `HIDDEN_PAGES`: sem aba no menu, sem contador de acessos e com `{{HEAD_EXTRA}}` preenchido (noindex, sem referrer e política de segurança de conteúdo).
- **JavaScript:** `comum.js` carrega antes do script da página e traz `teamLogo`, `teamName` e `tlInk`; não declara `D` (cada página declara o seu). Sem bibliotecas externas; o gráfico de evolução é SVG feito à mão.
- **Logos:** `teamLogo(sigla, tamanho)` monta a imagem de `static/img/teams/<sigla>.png`; se o arquivo faltar, o `onerror` remove a imagem e aparece o distintivo com a sigla na cor do time.
- **Cache:** CSS e JS levam `?v=<data-hora do build>` para o navegador não usar arquivos antigos.
- **Parâmetros de URL:** `jogadores.html?times=NE,SF&pos=qb&janela=w3` e `evolucao.html?times=NE,SF&metrica=epa&janela=w3&modo=r`. Os times são validados contra a lista conhecida.

## 7. Página admin das transmissões

1. O navegador lê o token (campo ou, se o usuário pediu para lembrar, `localStorage`); por padrão ele fica só na memória da aba.
2. Com o token, a página busca `data/transmissoes.json` em `api.github.com/repos/<dono>/<repo>/contents/...` e preenche as caixas.
3. Ao salvar, busca a versão atual (para obter o `sha`), altera só os jogos listados, preserva as outras chaves, ordena e grava com `PUT` (commit "Atualiza transmissões (data)" na `main`). Em conflito (409/422), repete uma vez.
4. O commit na `main` dispara o fluxo (testes, geração e publicação), que leva 1 a 2 minutos.

## 8. Publicação e automação

| Item | Configuração |
|---|---|
| Fluxo | `.github/workflows/atualizar_site.yml`, nome "Atualizar site". |
| Gatilhos | Agendado (segunda, terça e sábado às 11:07 UTC = 08:07 em Brasília; confirmar no arquivo), manual (`workflow_dispatch`) e `push` na `main` (inclusive o commit da página admin). |
| Jobs | `build` (instala, testa, gera e envia o artefato) e `deploy` (publica no Pages). |
| Testes | Rodam em push e execução manual; **não** rodam nas execuções agendadas. |
| Permissões | `contents: read`, `pages: write`, `id-token: write`. |
| Concorrência | Grupo `pages`, sem cancelar a execução em andamento. |
| Runner | `ubuntu-24.04`, Python 3.12. |
| Actions | `checkout@v7`, `setup-python@v7`, `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`. |
| Variáveis | `NFL_SEASON` (variável do repositório, opcional) e `NFL_TZ` (definida no fluxo). |
| Dependabot | Pedido mensal para as actions; alertas de segurança podem abrir pedidos para as bibliotecas Python. |

## 9. Dependências

`requirements.txt` fixa as versões exatas da última execução bem-sucedida (por exemplo `nflreadpy` 0.1.5 e `polars` 2.0.0), incluindo as
dependências indiretas. `tzdata` fica sem versão. `requirements-dev.txt` acrescenta `pytest`. `requirements-logos.txt` acrescenta
`Pillow` (sem versão fixa) e só é usado na máquina de quem baixa os logos.

## 10. Configuração

| Onde | O quê |
|---|---|
| `nfl_dashboard/config.py` | `DEFAULT_SEASON`, `DEFAULT_TZ`, `REPO_URL`, `GOATCOUNTER_URL`, `CHANNELS`, `METRICS`. |
| Variável `NFL_SEASON` | Temporada (ambiente local ou variável do GitHub). |
| Variável `NFL_TZ` | Fuso de exibição (padrão `America/Sao_Paulo`). |
| `--out` | Pasta de saída do site (padrão `site`). |
| `python -m nfl_dashboard.logos [--force] [--out pasta]` | Baixa os logos para `static/img/teams/` (uso único). |

## 11. Testes

45 testes em `tests/`: montagem das páginas (rodapé, avisos, contador, escape do JSON, página admin e seus cabeçalhos), rankings,
agregação de jogadores, conversão de horários, jogo de divisão, seleção de jogos nos playoffs, folgas (bye) e consistência entre as rodadas,
o CSS e o JS de Confrontos, cores e logos, transmissões (validação e dados da admin) e reencontros. Não dependem de internet.

## 12. Segurança

- JSON dentro de `<script>` troca `</` por `<\/`, para um texto nos dados não fechar a tag.
- Nomes de jogadores e textos da página admin são escapados antes de entrar no HTML; os filtros da URL só aceitam times conhecidos.
- O repositório não tem senhas, tokens nem chaves; as permissões do fluxo são mínimas e o fluxo não é disparado por pull requests de terceiros.
- **Página admin:** política de segurança que só permite conectar em `api.github.com`, `noindex`, sem referrer e sem scripts de terceiros; token só na memória da aba por padrão.
- **Alcance do token:** o GitHub não limita um token a um arquivo; com "Contents: Read and write" ele pode alterar qualquer arquivo do repositório. Mitigações: validade curta, revogação se perder o aparelho e, opcionalmente, branch separada para as transmissões com a `main` protegida.
- Recomendado na conta do GitHub: verificação em duas etapas, e-mail privado e alertas do Dependabot ligados.

## 13. Playoffs

`select_games` usa o `game_type` do nflverse (`WC`, `DIV`, `CON`, `SB`). Com a temporada regular encerrada, mostra a primeira rodada com jogo pendente
e, se todas já foram disputadas, a última. Jogos sem times definidos são ignorados. As demais páginas continuam na temporada regular.
A página admin lista só a rodada atual nesse período.

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir do estado atual do projeto. |
| 29/10/2026 | Inclusão do `AGENTS.md` e da pasta `docs/` na estrutura do repositório (proposta revertida em 30/10/2026: o `AGENTS.md` não foi criado). |
| 04/11/2026 | Logos (`logos.py`, `comum.js`, `static/img`), transmissões (`broadcasts.py`, página admin, `data/`), reencontros (`rematches.py`), marcador `__DADOS__`, páginas ocultas, cores nas páginas e testes (46). |
| 10/11/2026 | Folgas (bye): `bye_teams` em `stats.py` usa o calendário da temporada (não mais o cadastro de times, que tinha siglas antigas); nova linha `#tv` para a nota de transmissão em `confrontos.html`; testes em 45. |