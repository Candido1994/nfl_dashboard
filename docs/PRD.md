# PRD — NFL Dashboard

> Última atualização: 27/10/2026 · Status: em produção (GitHub Pages)

## 1. Visão geral

Painel semanal da NFL em **páginas HTML estáticas**, gerado em Python a partir dos dados abertos do nflverse
(via `nflreadpy`) e publicado no GitHub Pages. Uma rotina do GitHub Actions atualiza o site sozinha durante a semana.

## 2. Problema e objetivo

**Problema:** acompanhar o desempenho dos 32 times semana a semana exige juntar várias fontes e planilhas, e os números
brutos sozinhos não deixam claro quem está bem, quem está em queda e como dois times se comparam.

**Objetivo:** reunir, em um só lugar acessível de qualquer aparelho, os números de ataque e defesa de cada time, a posição dele
na liga, a evolução ao longo da temporada e uma leitura organizada de cada confronto, para o usuário tirar as próprias conclusões.

## 3. Público e uso

- Uso principal: acompanhamento pessoal, com acesso pelo celular (mobile-first) e pelo desktop.
- Usuário-alvo: fã de NFL que quer dados, sem precisar saber de estatística avançada.
- Finalidade: **didática**. O conteúdo não se destina a apostas nem a fins lucrativos.

## 4. Escopo

**Dentro do escopo**
- Estatísticas dos 32 times na temporada regular, em três janelas: temporada, últimas 3 semanas e último jogo.
- Página de confrontos da semana e das rodadas dos playoffs.
- Evolução semana a semana e estatísticas de jogadores (QB, corrida, recepção, defesa e kickers).
- Atualização automática e publicação gratuita.

**Fora do escopo (decisão atual)**
- Previsões geradas por IA ou qualquer chamada à API do Claude.
- Pesquisa na internet, notícias, lesões, escalações, clima e linhas de apostas.
- Estatísticas dos jogos de playoffs nas páginas Painel, Evolução e Jogadores (só a temporada regular).
- Servidor, banco de dados, login ou conteúdo enviado por visitantes.

## 5. Requisitos funcionais

### Painel (`index.html`)
| ID | Requisito |
|---|---|
| RF-01 | Tabela dos 32 times com jogos, campanha (V-D) e 19 métricas, ordenável por qualquer coluna. |
| RF-02 | Métricas de ataque e defesa: pontos, jardas aéreas e corridas, turnovers, sacks, jardas por jogada, EPA/jogada e success rate, mais os saldos de pontos, jardas e turnovers. |
| RF-03 | Janelas de período: temporada, últimas 3 semanas e último jogo. |
| RF-04 | Filtro por todos os times, conferência ou divisão. |
| RF-05 | Ranking por métrica com barras. |
| RF-06 | Times identificados como "SIGLA - Apelido" (ex.: NE - Patriots). |

### Confrontos (`confrontos.html`)
| ID | Requisito |
|---|---|
| RF-10 | Mostrar os jogos da semana atual (a primeira com jogo pendente) ou da próxima. |
| RF-11 | Nos playoffs, mostrar a rodada em andamento, com etiqueta colorida por rodada. |
| RF-12 | Horários convertidos para Brasília; Super Bowl e jogos em campo neutro usam "x" no lugar de "@". |
| RF-13 | Cada jogo é um card expansível, com "expandir/recolher todos"; o estado dos cards é preservado ao trocar a janela. |
| RF-14 | Resumo com pontos projetados e placar de duelos ataque x defesa com vantagem clara. |
| RF-15 | Destaques automáticos: oportunidade e obstáculo de cada time. |
| RF-16 | Tabela de duelos ataque x defesa (pontos, jardas aéreas, jardas corridas, EPA, success rate) com a posição de cada time na liga. |
| RF-17 | Campanha (V-D) de cada time nas três janelas. |
| RF-18 | Comparativo completo agrupado, com a posição na liga e o melhor valor destacado. |
| RF-19 | Etiqueta e faixa amarelas para jogo entre times da mesma divisão. |
| RF-20 | Links no card para Jogadores e Evolução já filtrados pelos dois times. |
| RF-21 | Aviso de que projeções e análises são apenas didáticas (no topo da página e em cada card). |
| RF-22 | Lista de times em folga (bye) na temporada regular. |

### Evolução (`evolucao.html`)
| ID | Requisito |
|---|---|
| RF-30 | Gráfico semana a semana de qualquer métrica (mais o aproveitamento), em valor ou em posição no ranking. |
| RF-31 | Janela acumulada ou média móvel de 3 jogos. |
| RF-32 | Seleção de times por menu e chips; padrão: os 3 melhores da métrica; aceita filtros pela URL. |
| RF-33 | Tabela "Movimentação do ranking" com a variação (▲▼) em relação à semana anterior. |

### Jogadores (`jogadores.html`)
| ID | Requisito |
|---|---|
| RF-40 | Tabelas ordenáveis de QBs, corredores, recebedores, defesa e kickers. |
| RF-41 | Filtro por times; com times selecionados, cartões de líderes (QB, corredor, recebedor, defensor, pass rush e kicker) para até 4 times. |
| RF-42 | As mesmas três janelas de período. |

### Transversais
| ID | Requisito |
|---|---|
| RF-50 | Navegação por abas nas quatro páginas. |
| RF-51 | Rodapé com atribuição ao nflverse (CC BY 4.0), licença MIT do código e link do código-fonte. |
| RF-52 | Atualização automática pelo GitHub Actions (segunda, terça e sábado) e por execução manual. |
| RF-53 | Contador de acessos opcional (GoatCounter, sem cookies). |
| RF-54 | Tema claro e escuro automáticos, conforme o aparelho. |

## 6. Requisitos não funcionais

- **Mobile-first:** sem rolagem lateral da página em 360, 390 e 414 px; alvos de toque de pelo menos 40–44 px.
- **Custo zero:** hospedagem gratuita; nenhuma chave de API ou segredo no projeto.
- **Sem servidor:** os números ficam embutidos em cada página; o navegador só monta tabelas e gráficos.
- **Resiliência:** se uma atualização falhar, o site continua com a última versão publicada.
- **Reprodutibilidade:** versões das bibliotecas fixas; testes automatizados (24 testes).
- **Privacidade:** sem cookies; contador de acessos anônimo e opcional.
- **Acessibilidade:** contraste mínimo de 4,5:1 no texto, foco visível, respeito a "reduzir movimento".

## 7. Dados e licenças

- **Fonte:** nflverse, via `nflreadpy` (agenda, estatísticas semanais de times e jogadores, play-by-play e tabela de times).
- **Licença dos dados:** CC BY 4.0, que exige atribuição. O conjunto FTN (CC BY-SA 4.0) **não** é usado.
- **Licença do código:** MIT.
- **Marca:** projeto independente, sem vínculo com a NFL.

## 8. Decisões de produto

| Decisão | Motivo |
|---|---|
| Site 100% estático gerado em Python | Hospedagem gratuita e simples; nada para manter no ar. |
| Não usar a API do Claude nem texto gerado por IA | O usuário não quer depender de limites de uso; o card organiza os dados para ele concluir. |
| Sem pesquisa na internet | Usar somente os dados da base. |
| Horários em Brasília | Usuário no Brasil; o nflverse informa em horário do Leste dos EUA. |
| Janelas por jogos do time, não por semanas do calendário | A semana de bye não distorce as médias. |
| Estatísticas só da temporada regular | Simplicidade; a página de Confrontos usa essa base também nos playoffs. |
| Página de jogadores separada, com link nos cards | Evita poluir o card; o filtro já chega pronto. |
| Atualizações em segunda, terça e sábado | Cobre domingo, o Monday Night Football e o Thursday Night Football. |

## 9. Riscos e limitações

- O GitHub pode atrasar as execuções agendadas (já ocorreu um atraso de mais de 4 horas) e desativa agendamentos de repositórios públicos sem atividade por 60 dias.
- O nflverse costuma atualizar os dados na manhã seguinte aos jogos; uma execução antes disso mostra dados parciais.
- Os nomes de colunas de jogadores seguem o nflverse; se mudarem, a estatística aparece zerada.
- O nome das divisões aparece em inglês (ex.: "AFC East").
- A fonte Barlow Semi Condensed vem do Google Fonts; sem internet, usa-se uma fonte do sistema.

## 10. Ideias avaliadas e ainda não implementadas

- Médias ajustadas pela qualidade dos adversários e dificuldade do calendário.
- Expectativa pitagórica (campanha x saldo de pontos).
- Indicador de tendência (↑↓) comparando últimas 3 semanas com a temporada.
- Eficiência na terceira descida e na red zone; splits de casa e fora; dias de descanso.
- Lesões, quarterback titular e outros dados fora da base atual.
- Estatísticas dos jogos de playoffs nas demais páginas.
- Testes automáticos em pull requests e Dependabot para as bibliotecas Python.
- Fixar as versões das actions por hash do commit.

## 11. Indicadores de acompanhamento

- Atualizações automáticas concluídas por semana (aba Actions).
- Acessos por página e origem (painel do GoatCounter).
- Tempo entre o fim dos jogos e a publicação dos dados.

## 12. Glossário

| Termo | Significado |
|---|---|
| EPA/jogada | Pontos esperados adicionados por jogada; mede a eficiência. |
| Success rate | Porcentagem de jogadas bem-sucedidas. |
| Turnover | Perda de posse (interceptação ou fumble perdido). |
| Bye | Semana de folga do time. |
| Janela | Período das médias: temporada, últimas 3 semanas ou último jogo. |
| Vantagem clara | Diferença de 6 ou mais posições no ranking da liga em um duelo ataque x defesa. |

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir do estado atual do projeto. |