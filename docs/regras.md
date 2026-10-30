# Regras — NFL Dashboard

> Última atualização: 27/10/2026

## 1. Regras de cálculo

### 1.1 Base de dados
- Só jogos da **temporada regular** já disputados (agenda com placar, estatísticas semanais de times e play-by-play).
- Cada jogo gera uma linha por time, com os números do time e os do adversário no mesmo jogo.

### 1.2 Janelas de período
- **Último jogo:** o jogo mais recente do time. **Últimas 3 semanas:** os 3 últimos jogos do time. **Temporada:** todos os jogos.
- Contam os jogos do time, não as semanas do calendário: a semana de bye não entra.

### 1.3 Métricas
| Métrica | Regra |
|---|---|
| Médias por jogo | Pontos feitos e cedidos, saldo de pontos, jardas aéreas e corridas feitas e cedidas, saldo de jardas, turnovers cedidos e forçados, saldo de turnovers, sacks sofridos e aplicados. |
| Turnovers cedidos | Interceptações + fumbles perdidos (passe, corrida, recepção e sacks). |
| Turnovers forçados | Os turnovers cedidos pelo adversário no mesmo jogo. |
| Saldo de jardas | Jardas feitas (aéreas + corridas) menos as do adversário. |
| Sacks aplicados | Sacks sofridos pelo ataque adversário no mesmo jogo. |
| Jd/jogada | (jardas aéreas + corridas) ÷ (passes tentados + corridas + sacks sofridos); a defesa usa os números do adversário. |
| EPA/jogada | Soma do EPA ÷ número de jogadas de passe e corrida; só play-by-play da temporada regular. |
| Success rate | Jogadas bem-sucedidas ÷ jogadas de passe e corrida, em %. |
| Razões | Jd/jogada, EPA e success rate são razão entre somas, não média das médias. |
| Arredondamento | 2 casas nas médias, 3 no EPA e 1 no success rate. |

### 1.4 Campanha e aproveitamento
- Vitórias-derrotas em cada janela, com empates como terceiro número só quando existem.
- Aproveitamento = (vitórias + 0,5 × empates) ÷ jogos.

### 1.5 Ranking na liga
- Posição de 1 a 32, em que **1 é o melhor em todas as métricas, inclusive nas defensivas** (menos pontos cedidos = melhor).
- Empates dividem a posição (posição = 1 + quantos times são estritamente melhores). Valores ausentes ficam de fora.
- O ranking é recalculado para cada janela.
- **Maior é melhor:** pontos feitos, saldo de pontos, jardas feitas, saldo de jardas, turnovers forçados, saldo de turnovers, sacks aplicados, jd/jogada, EPA e success rate do ataque.
  **Menor é melhor:** pontos cedidos, jardas cedidas, turnovers cedidos, sacks sofridos, jd/jogada, EPA e success rate da defesa.

## 2. Regras da página de Confrontos

### 2.1 Quais jogos aparecem
1. Temporada regular: a **primeira semana que ainda tem jogo pendente** (mostra a semana inteira, com placares dos jogos já finalizados).
2. Temporada regular encerrada: a **primeira rodada dos playoffs com jogo pendente**; se todas foram disputadas, a **última rodada**.
3. Jogos de playoffs sem os dois times definidos são ignorados. Sem nada a mostrar, a página avisa "Sem jogos pendentes".
4. Os jogos aparecem em ordem de data e horário. A lista de folgas (bye) só existe na temporada regular.

### 2.2 Rodadas dos playoffs
| Código do nflverse | Nome exibido |
|---|---|
| `WC` | Wild Card |
| `DIV` | Rodada Divisional |
| `CON` | Final da Conferência |
| `SB` | Super Bowl |

### 2.3 Horários
- O nflverse informa data e hora no horário do Leste dos EUA (ET). O site converte para o fuso configurado (padrão: Brasília), com o horário de verão dos EUA.
- Formato: `dom, 18/10` e `14:00`. Se o horário não estiver definido: "horário a definir". Se a conversão falhar: o horário original com "ET".
- Se a data mudar na conversão, vale a data no fuso de exibição.

### 2.4 Marcações do card
- **Jogo de divisão:** os dois times têm a mesma divisão na tabela de times do nflverse; etiqueta amarela com o nome da divisão.
- **Playoffs:** etiqueta com a cor da rodada e faixa lateral nessa cor (vale mesmo se o jogo também for de divisão).
- **Campo neutro:** o separador entre os times é "x" (quando a localização do jogo é "Neutral"); caso contrário, "@" (visitante @ mandante).

### 2.5 Leitura do confronto
- **Pontos projetados:** (pontos feitos pelo ataque + pontos cedidos pela defesa adversária) ÷ 2, na janela selecionada. É uma estimativa simples.
- **Duelo ataque x defesa:** compara a posição do ataque com a posição da defesa adversária em pontos, jardas aéreas, jardas corridas, EPA e success rate.
  Diferença = posição da defesa − posição do ataque. A partir de **6 posições** (constante `TH` em `static/js/confrontos.js`) há **vantagem clara**; abaixo disso, "Equilíbrio".
- **Placar de duelos:** de 10 duelos (5 de cada lado), quantos cada time vence com vantagem clara. Um duelo vencido pela defesa conta para o time dono da defesa.
- **Destaques:** por time, a maior oportunidade (maior vantagem a favor do ataque) e o maior obstáculo (maior vantagem da defesa adversária), se passarem do limite.
- **Comparativo completo:** o melhor valor de cada linha fica em verde; o selo ao lado do valor é a posição na liga (verde no 1º quarto, vermelho no último).
- Sem estatísticas suficientes para a janela, o card avisa em vez de calcular.

## 3. Regras da página de Evolução

- Para cada semana, o acumulado considera os jogos até aquela semana; a média móvel considera os 3 últimos jogos até ela.
- No modo "Posição no ranking", a posição é recalculada semana a semana.
- Variação na tabela = posição da semana anterior − posição atual (▲ subiu, ▼ caiu, = igual).
- Sem times na URL, o gráfico começa com os 3 melhores da métrica na última semana.

## 4. Regras da página de Jogadores

- As janelas usam os jogos do **time atual** do jogador. Os valores são somados nas semanas da janela.
- **Quem entra em cada lista:** QBs com passes tentados; corredores com corridas; recebedores com alvos ou recepções; defesa com qualquer estatística defensiva; kickers com field goals ou extra points tentados.
- **Rating do QB:** fórmula oficial do passer rating (cada componente limitado a 0–2,375).
- **Tackles:** solos + assistidos. **FG 40+:** feitos de 40 jardas ou mais. **Mais longo:** o maior valor, não a soma.
- Colunas que não existirem nos dados contam como zero.
- **Líderes do time** (até 4 times): QB, corredor e recebedor por jardas; defensor por tackles; pass rush por sacks (só se houver sacks); kicker por tentativas de FG. Só aparece quem tem valor maior que zero.
- Sem time selecionado, cada tabela mostra os 60 primeiros; com time, mostra todos.

## 5. Regras de ordenação e filtros

- Clicar no título de uma coluna ordena; clicar de novo inverte. A coluna ordenada mostra seta e sublinhado.
- Padrão do Painel: saldo de pontos, do maior para o menor. Padrão de cada tabela de jogadores: a estatística principal da categoria.
- Filtro do Painel: todos, AFC, NFC ou uma das 8 divisões.

## 6. Regras de conteúdo e legais

- **Aviso didático:** projeções e análises são apenas didáticas e não devem ser usadas para apostas nem para fins lucrativos. Aparece no topo e em cada card de Confrontos, no README e na descrição do projeto.
- **Atribuição:** o rodapé informa que os dados são do nflverse (CC BY 4.0) e que foram processados e agregados.
- **Licenças:** código sob MIT; dados do nflverse sob CC BY 4.0; o conjunto FTN (CC BY-SA 4.0) não é usado. Ao incluir um conjunto novo, conferir a licença antes.
- **Marca:** o rodapé informa que o projeto é independente e sem vínculo com a NFL.
- **IA:** o projeto não usa IA nem a API do Claude; os textos de destaque são regras fixas sobre os números.
- **Contador de acessos:** só com `GOATCOUNTER_URL` preenchido; nesse caso o rodapé informa que a contagem é anônima e sem cookies.

## 7. Regras de desenvolvimento e entrega

- **Versões fixas:** `requirements.txt` com versões exatas; atualizar trocando o número, rodando `pytest` e conferindo a execução no GitHub.
- **Testes:** rodam a cada alteração enviada para a `main`; as execuções agendadas só atualizam os dados.
- **Publicação:** commit na `main` publica automaticamente; se o build falhar, o site continua na última versão.
- **Antes de colar arquivos novos:** rodar `git pull` (pedidos do Dependabot e outras alterações podem ter mudado o repositório).
- **Pedidos do Dependabot:** aprovar, conferir a execução na aba Actions e, se ficar vermelha, usar "Revert".
- **Entrega de alterações:** o código e os arquivos são enviados completos no chat, para copiar e colar; não são gerados arquivos para baixar.
- **Documentação:** sempre que uma alteração afetar produto, arquitetura, regras ou design, os documentos de `docs/` são atualizados, e a mudança é registrada no `memory.md` com a data.
- **Datas:** cada registro leva a data da solicitação, da modificação e da implementação.

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir do estado atual do projeto. |