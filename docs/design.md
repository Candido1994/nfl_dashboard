# Design — NFL Dashboard

> Última atualização: 27/10/2026

## 1. Princípios

1. **Mobile-first:** pensado para o celular, com a tabela rolando só dentro do próprio quadro.
2. **Dados primeiro:** números alinhados e legíveis; a cor serve para indicar posição, vantagem ou fase, não para enfeitar.
3. **Camadas de leitura:** o que importa vem primeiro (resumo, destaques); o detalhe fica expansível.
4. **Coerência:** os mesmos componentes e as mesmas cores em todas as páginas.
5. **Temas:** claro e escuro automáticos, com contraste de texto de pelo menos 4,5:1.

Identidade: verde de gramado como cor principal, amarelo (cor do flag de penalidade) para o que está ativo, e uma faixa discreta de
marcações de jardas sob o cabeçalho.

## 2. Tipografia

| Item | Valor |
|---|---|
| Família | Barlow Semi Condensed (Google Fonts), com fallback para Roboto Condensed, Arial Narrow e a fonte do sistema. |
| Pesos | 400 a 700. |
| Números | `font-variant-numeric: tabular-nums` em todo o site. |
| Corpo | 16 px, entrelinha 1,4. Tabela do painel: 15 px. Títulos de coluna: 13 px. |
| Título da página | 26 px, peso 700, espaçamento −0,01 em. |
| Seções | `h2` 18 px; `h3` dos cards 15 px; textos de apoio 13–14 px. |

Em telas de até 480 px os botões segmentados passam a 15 px, e em até 400 px as abas e os botões vão a 14 px.

## 3. Cores

### 3.1 Base
| Papel | Variável | Claro | Escuro |
|---|---|---|---|
| Fundo | `--bg` | `#F3F5F1` | `#0D130F` |
| Superfície (cards, tabelas) | `--surface` | `#FFFFFF` | `#141C17` |
| Texto | `--fg` | `#17211B` | `#E7EEE8` |
| Texto secundário | `--mut` | `#5A685F` | `#97A89D` |
| Linhas | `--line` | `#DCE2DA` | `#27322B` |
| Destaque (verde) | `--acc` | `#1B6B3A` | `#58BF7B` |
| Texto sobre o verde | `--acc-ink` | `#FFFFFF` | `#07130B` |
| Positivo | `--good` | `#1B7A41` | `#58BF7B` |
| Negativo | `--bad` | `#B3261E` | `#FF8A80` |
| Ativo / divisão (amarelo) | `--flag` | `#F2B705` | `#F5C518` |
| Linha alternada | `--zebra` | `#F8FAF7` | `#171F1A` |
| Passar o mouse | `--hover` | `#EAF2EA` | `#1F2B23` |
| Fundo suave / segmentado | `--seg` | `#E9EEE7` | `#1B241E` |
| Melhor valor (verde claro) | `--win` | `#E4F3E8` | `#1B3325` |
| Fundo do selo ruim | `--badbg` | `#FBE9E7` | `#3A1F1C` |
| Foco | `--focus` | `#1B6B3A` | `#58BF7B` |

### 3.2 Rodadas dos playoffs
| Rodada | Classe | Claro (fundo / texto) | Escuro (fundo / texto) | Contraste do texto |
|---|---|---|---|---|
| Wild Card | `po-wc` | `#1F5FBF` / `#FFFFFF` | `#7DB3FF` / `#0A1A33` | 6,1 e 8,1 |
| Rodada Divisional | `po-div` | `#6B3FA0` / `#FFFFFF` | `#B9A0F0` / `#1E1033` | 7,4 e 7,9 |
| Final da Conferência | `po-con` | `#C2410C` / `#FFFFFF` | `#FFA374` / `#2A1004` | 5,2 e 9,1 |
| Super Bowl | `po-sb` | `#BE185D` / `#FFFFFF` | `#F59AC4` / `#330A20` | 6,0 e 8,5 |

O amarelo fica reservado a "Jogo de divisão" (texto `#17211B`, contraste 9,1 no claro e 10,1 no escuro) e ao item ativo (aba atual, coluna ordenada).

## 4. Espaçamento, forma e largura

- **Raios:** cards e tabelas 14 px; campos e botões 10 px; controle segmentado 12 px (botões internos 9 px); etiquetas e selos 999 px.
- **Espaçamentos comuns:** conteúdo 16 px; cards 12–16 px; separação entre blocos 12–18 px.
- **Largura máxima:** Painel e Jogadores 1100 px; Evolução 880 px; Confrontos 760 px. O rodapé acompanha a largura da página.
- **Pontos de quebra:** 599 px (abas ocupam a largura toda), 480 px (ranking e botões compactos) e 400 px (fontes menores nas abas).

## 5. Componentes

| Componente | Descrição |
|---|---|
| Cabeçalho | Título, subtítulo com data de atualização, abas (Painel, Confrontos, Evolução, Jogadores) e faixa de marcações de jardas. A aba atual leva sublinhado amarelo. |
| Controle segmentado | Botões lado a lado para a janela, a posição e o modo; o selecionado fica verde. Altura de 40 px. |
| Menus e botões | Altura mínima de 44 px; menus com rótulo visível acima. |
| Tabela | Cabeçalho fixo, primeira coluna fixa, linhas alternadas, destaque ao passar o mouse, divisórias entre grupos de colunas e seta + sublinhado amarelo na coluna ordenada. A rolagem fica dentro do quadro (altura máxima de 75% da tela). |
| Ranking | Linhas com posição, nome, barra e valor; no celular a barra vai para uma segunda linha. |
| Card de confronto | `details` expansível: times e campanhas, horário e placar, etiquetas, seta que gira ao abrir. Conteúdo: links, resumo, destaques, duelos, campanha e comparativo. |
| Etiquetas | "Jogo de divisão" (amarela) e "Playoffs · rodada" (cor da rodada), em uma linha própria sob o horário; quebram de linha em telas estreitas. |
| Faixa lateral do card | Amarela para jogo de divisão; na cor da rodada nos playoffs (a rodada tem prioridade). |
| Placar projetado | Dois números grandes (32 px) em um bloco suave, com o texto "pontos projetados" no meio. |
| Selo de posição | Pequeno selo ao lado do valor ("12º"): verde no 1º quarto da liga, vermelho no último, neutro no meio. |
| Destaques | Lista de barras com borda verde (oportunidade) ou vermelha (obstáculo). |
| Vantagem | Texto "Ataque" (verde), "Defesa" (vermelho) ou "Equilíbrio" (neutro). |
| Aviso | Bloco com borda amarela, no topo de Confrontos; versão em texto simples nos cards. |
| Chips de times | Botões arredondados com a cor da linha no gráfico e "✕" para remover. |
| Gráfico de evolução | SVG com grade tracejada, linhas dos times selecionados em cores distintas (8 cores) e as demais em cinza claro. |
| Cartão de líderes | Um cartão por time com QB, corredor, recebedor, defensor, pass rush e kicker. |
| Rodapé | Texto centralizado com atribuição, licença e link do código. |

## 6. Interação

- Cards: tocar no cabeçalho abre ou fecha; "Expandir todos" e "Recolher todos" no topo; ao trocar a janela, os cards abertos continuam abertos.
- Tabelas: tocar no título ordena; tocar de novo inverte.
- Links entre páginas já levam os filtros (times, posição, janela, métrica e modo).
- Movimento: só a seta do card gira (0,2 s); com "reduzir movimento" ativo, não há animação.

## 7. Acessibilidade

- Contraste de texto de pelo menos 4,5:1 nos dois temas (calculado para as cores das rodadas e do amarelo).
- Foco visível com contorno de 3 px; alvos de toque de 40 a 44 px.
- A aba atual é marcada com `aria-current="page"`; o gráfico tem `role="img"` e texto alternativo; os menus têm rótulo.
- Os temas seguem a preferência do aparelho (`prefers-color-scheme`).

## 8. Como evoluir o design

- Mudar cores: editar as variáveis no início de `static/css/style.css` (e conferir o contraste nos dois temas).
- Nova rodada ou nova cor de rodada: acrescentar o par de variáveis, a classe `po-*` e o mapa `RC` em `static/js/confrontos.js`; o teste de consistência falha se algo ficar de fora.
- Novas métricas aparecem sozinhas no painel e nos rankings (ver `regras.md` e `arquitetura.md`).

## Histórico de alterações

| Data | Alteração |
|---|---|
| 27/10/2026 | Criação do documento a partir do estado atual do projeto. |