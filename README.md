# NFL Dashboard

Painel semanal da NFL, gerado como **páginas HTML estáticas** a partir dos dados do
[nflverse](https://nflverse.com) (via [`nflreadpy`](https://github.com/nflverse/nflreadpy)).
O site é atualizado automaticamente pelo GitHub Actions e pode ser publicado em qualquer hospedagem de site estático.

> Projeto independente, sem vínculo com a NFL. As projeções são apenas didáticas: não use para apostas nem para fins lucrativos.
> Logos e marcas são propriedade dos respectivos titulares.

## Páginas

| Página | Arquivo | O que mostra |
|---|---|---|
| Painel | `index.html` | Os 32 times com logo: pontos, jardas aéreas e corridas, turnovers, sacks, EPA e success rate (feitos e cedidos), saldos e campanha. Tabela ordenável, filtros por conferência/divisão e rankings por métrica. |
| Confrontos | `confrontos.html` | Jogos da semana atual (ou da próxima, se a atual já terminou), com horários em Brasília. Nos playoffs, mostra a rodada em andamento. Cada jogo é expansível e mostra o placar do último confronto entre os times (quando já se enfrentaram), projeção de pontos, duelos ataque x defesa, destaques e comparativo completo. Jogos de divisão ganham etiqueta amarela, jogos de playoffs uma etiqueta colorida por rodada e, quando informado, a linha "Onde assistir" com os canais no Brasil. |
| Evolução | `evolucao.html` | Gráfico semana a semana de qualquer métrica (valor ou posição no ranking) e tabela de movimentação do ranking. |
| Jogadores | `jogadores.html` | Líderes por time e tabelas de QBs, corredores, recebedores, defesa e kickers. |
| Playoffs | `playoffs.html` | Seeds 1 a 7 de AFC e NFC pela temporada regular (campeões de divisão e os três melhores restantes), com campanha e aproveitamento, e o chaveamento do Wild Card da última semana fechada. Os critérios de desempate estão em `docs/regras.md`, seção 9. |
| Admin (oculta) | `admin.html` | Página para marcar onde cada jogo passa no Brasil. Fora do menu e sem função sem o token do GitHub do administrador. |

As páginas públicas, exceto Playoffs, têm três janelas de período: **temporada**, **últimas 3 semanas** e **último jogo**.
Os cards de confronto têm links que abrem *Jogadores* e *Evolução* já filtrados pelos dois times
(por exemplo `jogadores.html?times=NE,SF`).

## Como rodar

Requer Python 3.12 ou mais novo (a versão usada no GitHub Actions) e acesso à internet, porque os dados são baixados do nflverse a cada execução.

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

A temporada também pode vir da variável de ambiente `NFL_SEASON`.

**Fuso horário:** o nflverse informa os horários dos jogos em horário do Leste dos EUA (ET). O site converte para o horário de Brasília,
e o "atualizado em" usa o mesmo fuso. Para outro fuso, defina `NFL_TZ` (por exemplo `NFL_TZ=America/New_York`).

### Logos dos times (uma vez)

Os logos ficam em `static/img/teams/<sigla>.png` (128 × 128 px). Sem o arquivo de um time, o site mostra um distintivo com a sigla na cor dele.
Para baixar os 32 logos a partir dos endereços da tabela de times do nflverse:

```bash
pip install -r requirements-logos.txt
python -m nfl_dashboard.logos              # baixa só o que falta
python -m nfl_dashboard.logos --force      # baixa de novo
```

Depois, faça o commit da pasta `static/img/teams/`. Logos são marcas dos titulares e não estão cobertos pelas licenças do projeto.

## Estrutura do repositório

```
nfl-dashboard/
├── generate.py              # atalho para a linha de comando
├── LICENSE                  # licença MIT do código
├── requirements.txt         # dependências, com versões exatas
├── requirements-dev.txt     # dependências + ferramentas de teste
├── requirements-logos.txt   # dependências + Pillow (só para baixar os logos)
├── .github/
│   ├── workflows/atualizar_site.yml   # gera e publica o site (agendado e manual)
│   └── dependabot.yml                 # atualização mensal das ferramentas do fluxo
├── data/
│   └── transmissoes.json    # canais de transmissão por jogo (gravado pela página admin)
├── nfl_dashboard/           # código Python
│   ├── config.py            # métricas, canais, temporada, fuso, URL do repositório e contador de acessos
│   ├── stats.py             # estatísticas dos times, rankings, confrontos e histórico
│   ├── players.py           # estatísticas de jogadores
│   ├── broadcasts.py        # transmissões no Brasil e dados da página admin
│   ├── rematches.py         # placar do último confronto entre os dois times
│   ├── playoffs.py          # classificação dos playoffs (seeds, desempate e chaveamento)
│   ├── logos.py             # cores dos times e script que baixa os logos
│   ├── render.py            # monta o HTML a partir dos templates
│   └── cli.py               # orquestra tudo e grava a pasta de saída
├── templates/
│   ├── layout.html          # estrutura comum (cabeçalho, abas, rodapé, scripts)
│   └── pages/               # conteúdo de cada página
├── static/
│   ├── css/style.css        # todo o visual (tema claro e escuro)
│   ├── js/                  # comum.js + um script por página (tabelas, filtros, gráfico, admin)
│   └── img/teams/           # logos dos times
├── tests/                   # testes automatizados
├── docs/                    # PRD, arquitetura, regras, design e memória do projeto
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
- **Playoffs:** a classificação usa só a temporada regular e as semanas já fechadas (todos os placares). O desempate segue a ordem de `docs/regras.md`, seção 9; o sorteio nunca é automático e aparece como "sorteio pendente".
- **Confrontos:** a projeção de pontos é a média entre os pontos que o ataque faz e os que a defesa adversária cede.
  "Vantagem clara" em um duelo ataque x defesa significa diferença de 6 ou mais posições no ranking
  (constante `TH` em `static/js/confrontos.js`).
- **Último confronto:** o jogo já disputado entre os dois times em semana anterior, em qualquer fase da temporada; na temporada regular, só rivais de divisão.
- **Jogo de divisão:** os dois times pertencem à mesma divisão, segundo a tabela de times do nflverse.
- **Horários:** convertidos de ET para Brasília, considerando o horário de verão dos EUA. Se o horário de um jogo ainda não estiver definido, aparece "horário a definir".
- **Evolução:** recalculada do zero a cada execução, então não depende de execuções anteriores.
- **Jogadores:** vêm de `load_player_stats` por semana. Colunas que não existirem nos dados contam como zero.

## Transmissões no Brasil

A informação é **opcional e manual**: não há fonte automática. Se você não atualizar em uma semana, o site e o fluxo funcionam exatamente como antes.

1. **Crie um token** no GitHub: Settings → Developer settings → Personal access tokens → Fine-grained tokens. Escolha só este repositório,
   permissão **Contents: Read and write** e validade curta (por exemplo 90 dias).
2. Abra `admin.html` no endereço do seu site, cole o token e toque em **Usar token**.
3. Marque os canais de cada jogo (semana atual e a seguinte) e toque em **Salvar transmissões**.
   A página grava `data/transmissoes.json` no repositório; o commit dispara o fluxo e o site atualiza em 1 a 2 minutos.

Cuidados com o token: ele permite alterar **qualquer arquivo** do repositório (o GitHub não limita a um arquivo). Por padrão fica só na memória da aba;
a opção "Lembrar neste aparelho" é menos segura. Se perder o aparelho, revogue o token no GitHub. Depois de um salvamento pela página,
rode `git pull` no seu computador antes de enviar novas alterações.

## Personalizando

- **Visual:** edite `static/css/style.css`. As cores ficam nas variáveis do início do arquivo.
- **Textos e estrutura das páginas:** edite os arquivos em `templates/`.
- **Comportamento (tabelas, filtros, gráfico):** edite os arquivos em `static/js/`.
- **Nova métrica:** adicione em `METRICS` (`nfl_dashboard/config.py`) e calcule em `build_games` (`nfl_dashboard/stats.py`).
  Se for média por jogo, ela aparece sozinha no painel e nos rankings.
- **Novo canal de transmissão:** acrescente uma linha em `CHANNELS` (`nfl_dashboard/config.py`); a página admin e os cards passam a usá-lo.
- **Contador de acessos (opcional):** o site pode usar o [GoatCounter](https://www.goatcounter.com), que conta visitas sem cookies.
  Defina `GOATCOUNTER_URL` em `nfl_dashboard/config.py` (por exemplo `https://SEU-CODIGO.goatcounter.com/count`).
  Com o campo vazio, nenhum script é incluído. Quando ativo, o rodapé informa que a contagem é anônima e sem cookies. A página admin nunca carrega o contador.

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes cobrem a montagem das páginas (incluindo rodapé, avisos, contador de acessos e a página admin), os rankings, os jogos de divisão,
a seleção de jogos nos playoffs, a conversão de horários, as cores e logos, as transmissões, os reencontros e a agregação de jogadores.
Eles não precisam de internet.

## Documentação

- [PRD](docs/PRD.md): produto, escopo e requisitos
- [Arquitetura](docs/arquitetura.md): módulos, fluxo de dados e publicação
- [Regras](docs/regras.md): cálculos, seleção de jogos e regras de conteúdo
- [Design](docs/design.md): cores, tipografia e componentes
- [Memória do projeto](docs/memory.md): decisões e modificações com data

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

O fluxo `.github/workflows/atualizar_site.yml` roda **toda segunda, terça e sábado às 11:07 UTC (08:07 em Brasília)**:
instala as dependências, roda os testes, gera o site e publica. Ele também roda quando você envia alterações para a branch `main`
(inclusive as feitas pela página admin) e quando você clica em **Run workflow**. Nas execuções agendadas os testes não rodam: elas só atualizam os dados.

| Dia | Para que serve |
|---|---|
| Segunda | Resultados dos jogos de domingo. O Monday Night Football aparece como pendente em Confrontos. |
| Terça | Resultado do Monday Night Football e correções de estatísticas que o nflverse faz depois dos jogos. |
| Sábado | Resultado do Thursday Night Football e jogos de domingo prontos em Confrontos. |

- **Mudar o dia ou o horário:** edite a linha `cron` do arquivo. O horário é UTC, e os dias usam números (0 = domingo, 1 = segunda, ..., 6 = sábado).
  O minuto 7 evita o início da hora cheia, quando a fila do GitHub costuma estar mais cheia.
- **Atrasos:** o GitHub pode atrasar execuções agendadas, às vezes por horas. Se precisar da atualização na hora, use **Run workflow**.
- **Mudar a temporada:** em **Settings → Secrets and variables → Actions → Variables**, crie `NFL_SEASON` com o ano (por exemplo `2027`).
  Sem a variável, vale o padrão de `nfl_dashboard/config.py`.
- **Se a execução falhar** (por exemplo, o nflverse fora do ar), o site continua com a última versão publicada.
  Abra a execução na aba Actions para ver o erro e rode de novo depois.
- **Atenção:** em repositórios públicos, o GitHub desativa as execuções agendadas depois de 60 dias sem atividade no repositório.
  Se isso acontecer, na aba Actions clique em **Enable workflow** (ou envie qualquer alteração).

## Dependências

`requirements.txt` fixa as **versões exatas** usadas na última execução bem-sucedida do fluxo (Python 3.12), incluindo as bibliotecas das quais o
`nflreadpy` e o `polars` dependem. Assim, uma versão nova de qualquer biblioteca não muda o resultado sem você perceber.
`requirements-dev.txt` acrescenta as ferramentas de teste e `requirements-logos.txt` o Pillow, usado só para baixar os logos.

Para atualizar, troque os números no arquivo, rode `pytest` e confira a execução do fluxo na aba Actions.
O arquivo `tzdata` fica sem versão porque é só a base de fusos horários.

O Dependabot abre um pedido por mês para atualizar as ferramentas do próprio fluxo (`.github/dependabot.yml`).
Os alertas de segurança do GitHub também podem abrir pedidos para as bibliotecas Python. Depois de aprovar um pedido,
confira se a execução na aba Actions ficou verde e rode `git pull` no seu computador antes de enviar novas alterações.

## Limitações conhecidas

- Os nomes das colunas de jogadores e de logos seguem o padrão do nflverse. Se o nflverse mudar algum nome, a estatística aparece zerada ou o logo vira distintivo.
- Os dados do nflverse costumam ser atualizados na manhã seguinte aos jogos. Se uma execução rodar antes disso, o site mostra dados parciais até a próxima.
- Nos playoffs, só a página de Confrontos avança para as novas rodadas. Painel, Evolução e Jogadores continuam mostrando a temporada regular, e as médias, os rankings e as projeções dos jogos de playoffs também vêm da temporada regular. Depois do Super Bowl, Confrontos mantém o resultado final.
- A página Playoffs não mostra resultados de playoffs: mantém os seeds e o chaveamento da temporada regular.
- As transmissões dependem de o administrador marcá-las; jogos sem marcação não mostram canal.
- O nome das divisões aparece em inglês (por exemplo "AFC East"), do jeito que o nflverse informa.
- O estilo usa a fonte Barlow Semi Condensed, carregada do Google Fonts. Sem internet, o navegador usa uma fonte do sistema.

## Aviso

As projeções e análises do projeto, em especial a página de **Confrontos**, são **apenas didáticas**.
Não devem ser usadas para apostas nem para fins lucrativos.

## Licença e dados

- **Código:** [licença MIT](LICENSE).
- **Dados:** [nflverse](https://nflverse.com). A maior parte dos dados do nflverse é licenciada sob
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), que exige **atribuição** ao nflverse
  (e ao provedor original, quando o conjunto indicar um). Os dados FTN usam CC BY-SA 4.0; este projeto **não** usa o conjunto FTN.
  O site traz a atribuição no rodapé e informa que os dados foram processados e agregados.
- Conjuntos específicos podem ter licença ou provedor próprio, indicados nas páginas de release do
  [nflverse-data](https://github.com/nflverse/nflverse-data/releases) e na documentação do nflreadpy.
  Ao incluir um conjunto novo, confira a licença dele. No caso do CC BY-SA, os trabalhos derivados precisam seguir os mesmos termos.
- O nflverse não dá garantia sobre os dados nem assume responsabilidade legal pelo uso comercial deles.
- **Logos e marcas:** pertencem aos respectivos titulares e não são cobertos pela licença do código nem pela dos dados.