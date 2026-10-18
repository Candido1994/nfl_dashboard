# NFL Dashboard

Painel semanal da NFL, gerado como **páginas HTML estáticas** a partir dos dados do
[nflverse](https://nflverse.com) (via [`nflreadpy`](https://github.com/nflverse/nflreadpy)).
Rode o script uma vez por semana e publique a pasta gerada em qualquer hospedagem de site estático.

> Projeto independente, sem vínculo com a NFL.

## Páginas

| Página | Arquivo | O que mostra |
|---|---|---|
| Painel | `index.html` | Os 32 times: pontos, jardas aéreas e corridas, turnovers, sacks, EPA e success rate (feitos e cedidos), saldos e campanha. Tabela ordenável, filtros por conferência/divisão e rankings por métrica. |
| Confrontos | `confrontos.html` | Jogos da semana atual (ou da próxima, se a atual já terminou), cada um expansível: projeção de pontos, duelos ataque x defesa, destaques e comparativo completo com a posição de cada time na liga. |
| Evolução | `evolucao.html` | Gráfico semana a semana de qualquer métrica (valor ou posição no ranking) e tabela de movimentação do ranking. |
| Jogadores | `jogadores.html` | Líderes por time e tabelas de QBs, corredores, recebedores, defesa e kickers. |

Todas as páginas têm três janelas de período: **temporada**, **últimas 3 semanas** e **último jogo**.
Os cards de confronto têm links que abrem *Jogadores* e *Evolução* já filtrados pelos dois times
(por exemplo `jogadores.html?times=NE,SF`).

## Como rodar

Requer Python 3.10 ou mais novo e acesso à internet (os dados são baixados do nflverse a cada execução).

```bash
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt

python generate.py 2026          # gera a pasta site/
```

Abra `site/index.html` no navegador. Opções:

```bash
python generate.py 2026 --out docs   # escolhe a pasta de saída
python -m nfl_dashboard 2026         # forma equivalente
```

A temporada também pode vir da variável de ambiente `NFL_SEASON`. A data de "atualizado em" usa o fuso de Brasília. Para mudar, defina `NFL_TZ` (por exemplo `NFL_TZ=America/New_York`).

## Estrutura do repositório

```
nfl-dashboard/
├── generate.py              # atalho para a linha de comando
├── requirements.txt
├── nfl_dashboard/           # código Python
│   ├── config.py            # lista de métricas e temporada padrão
│   ├── stats.py             # estatísticas dos times, rankings, confrontos e histórico
│   ├── players.py           # estatísticas de jogadores
│   ├── render.py            # monta o HTML a partir dos templates
│   └── cli.py               # orquestra tudo e grava a pasta de saída
├── templates/
│   ├── layout.html          # estrutura comum (cabeçalho, abas, scripts)
│   └── pages/               # conteúdo de cada página
├── static/
│   ├── css/style.css        # todo o visual (tema claro e escuro)
│   └── js/                  # um script por página (tabelas, filtros, gráfico)
├── tests/                   # testes automatizados
└── site/                    # saída gerada (não é versionada)
```

O Python calcula os números e os grava como JSON dentro de cada página. O navegador só monta tabelas e gráficos
com esses dados, então o site final não precisa de servidor.

## Como os números são calculados

- **Janelas:** "último jogo" e "últimas 3 semanas" contam os jogos do próprio time (a semana de bye não entra).
- **Turnovers cedidos:** interceptações + fumbles perdidos. **Turnovers forçados:** os cedidos pelo adversário no mesmo jogo.
- **Jardas por jogada:** (jardas aéreas + corridas) ÷ (passes tentados + corridas + sacks sofridos).
- **EPA/jogada e success rate:** calculados a partir do play-by-play, só com passes e corridas da temporada regular.
- **Ranking na liga:** de 1 a 32, em que **1 é o melhor em todas as métricas**, inclusive nas defensivas (1º em jardas cedidas = a defesa que menos cede).
- **Campanha:** vitórias-derrotas (e empates, quando existem) em cada janela.
- **Confrontos:** a projeção de pontos é a média entre os pontos que o ataque faz e os que a defesa adversária cede.
  "Vantagem clara" em um duelo ataque x defesa significa diferença de 6 ou mais posições no ranking
  (constante `TH` em `static/js/confrontos.js`).
- **Evolução:** recalculada do zero a cada execução, então não depende de execuções anteriores.
- **Jogadores:** vêm de `load_player_stats` por semana. Colunas que não existirem nos dados contam como zero.

## Personalizando

- **Visual:** edite `static/css/style.css`. As cores ficam nas variáveis do início do arquivo.
- **Textos e estrutura das páginas:** edite os arquivos em `templates/`.
- **Comportamento (tabelas, filtros, gráfico):** edite os arquivos em `static/js/`.
- **Nova métrica:** adicione em `METRICS` (`nfl_dashboard/config.py`) e calcule em `build_games` (`nfl_dashboard/stats.py`).
  Se for média por jogo, ela aparece sozinha no painel e nos rankings.

## Testes

```bash
pip install pytest
pytest
```

Os testes cobrem a montagem das páginas, os rankings e a agregação de jogadores, e não precisam de internet.

## Publicação

A pasta `site/` é um site estático completo e pode ir para qualquer hospedagem estática
(Cloudflare Pages, Netlify, GitHub Pages...). Este repositório já vem com publicação automática no **GitHub Pages**.

### Publicando no GitHub Pages (uma vez)

1. Crie um repositório público no GitHub e envie o projeto:
   ```bash
   git init -b main
   git add .
   git commit -m "Primeira versão"
   git remote add origin https://github.com/SEU_USUARIO/nfl-dashboard.git
   git push -u origin main
   ```
2. No repositório, vá em **Settings → Pages** e, em **Source**, escolha **GitHub Actions**.
3. Vá na aba **Actions**, abra o fluxo **Atualizar site** e clique em **Run workflow**.
   Quando terminar, o endereço aparece no resumo da execução e em Settings → Pages:
   `https://SEU_USUARIO.github.io/nfl-dashboard/`.

### Atualização automática

O fluxo `.github/workflows/atualizar-site.yml` roda **toda terça às 12:00 UTC (09:00 em Brasília)**, depois do Monday Night Football:
instala as dependências, roda os testes, gera o site e publica. Ele também roda quando você envia alterações para a branch `main`
e quando você clica em **Run workflow**.

- **Mudar o dia ou o horário:** edite a linha `cron` do arquivo (o horário é UTC).
- **Mudar a temporada:** em **Settings → Secrets and variables → Actions → Variables**, crie `NFL_SEASON` com o ano (por exemplo `2027`).
  Sem a variável, vale o padrão de `nfl_dashboard/config.py`.
- **Se a execução falhar** (por exemplo, o nflverse fora do ar), o site continua com a última versão publicada.
  Abra a execução na aba Actions para ver o erro e rode de novo depois.
- **Atenção:** em repositórios públicos, o GitHub desativa as execuções agendadas depois de 60 dias sem atividade no repositório.
  Se isso acontecer, na aba Actions clique em **Enable workflow** (ou envie qualquer alteração).

## Limitações conhecidas

- Os nomes das colunas de jogadores seguem o padrão do nflverse. Se o nflverse mudar algum nome, a estatística correspondente aparece zerada.
- Os dados do nflverse costumam ser atualizados na manhã seguinte aos jogos, então rode o script depois disso.
- O estilo usa a fonte Barlow Semi Condensed, carregada do Google Fonts. Sem internet, o navegador usa uma fonte do sistema.

## Dados e licença

Dados: [nflverse](https://nflverse.com). Consulte os termos de uso e a atribuição exigida por eles antes de publicar.

Licença do código: a definir.
