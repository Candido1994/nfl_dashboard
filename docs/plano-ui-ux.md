# Plano de Melhorias de UI/UX — NFL Dashboard

> Data: 19/11/2026 · Branch: `gemini` · Status: implementado (22/11/2026)

## Objetivo

Elevar a experiência visual e a legibilidade das telas do **NFL Dashboard** para o padrão dos principais portais esportivos (como ESPN, The Athletic e rbsdm/nflverse), reduzindo a densidade excessiva das tabelas, aproveitando as cores dos times com moderação e oferecendo controle manual de tema.

---

## 1. Controle de tema claro/escuro e cabeçalho

- **Arquivos:** `templates/layout.html`, `static/js/comum.js`, `static/css/style.css`
- **O que muda:**
  - Botão discreto de alternância de tema (claro / escuro) no cabeçalho (`.top`), acessível por teclado e com rótulo `aria-label`.
  - Preferência salva em `localStorage`; na ausência de escolha manual, o site continua seguindo `prefers-color-scheme` do sistema.
  - Aplicação via atributo `data-theme="light" | "dark"` em `<html>`, compatível com a CSP estrita da página `admin.html`.

---

## 2. Painel semanal (`index.html`)

- **Arquivos:** `templates/pages/painel.html`, `static/js/painel.js`, `static/css/style.css`
- **O que muda:**
  - **Abas de visão das métricas** na tabela principal para evitar scroll horizontal forçado na leitura padrão:
    - **Resumo:** principais métricas (`pf`, `pa`, `pd`, `yd_diff`, `to_diff`, `epa`, `epa_a`, `sr`, `sr_a`)
    - **Ataque:** produção e eficiência ofensiva (`pf`, `pass_yds`, `rush_yds`, `to_lost`, `sacks_taken`, `ypp`, `epa`, `sr`)
    - **Defesa:** números cedidos e pressão (`pa`, `pass_yds_a`, `rush_yds_a`, `to_gain`, `sacks_made`, `ypp_a`, `epa_a`, `sr_a`)
    - **Eficiência:** leitura avançada e saldos (`pd`, `yd_diff`, `to_diff`, `ypp`, `ypp_a`, `epa`, `epa_a`, `sr`, `sr_a`)
    - **Todas:** visão completa com todas as 19 métricas juntas
  - **Ranking por métrica:** barras horizontais passam a usar a cor oficial de cada time (`window.__DATA__.colors`), mantendo `--bad` para valores negativos quando aplicável.

---

## 3. Confrontos da semana (`confrontos.html`)

- **Arquivos:** `nfl_dashboard/render.py` (`body_class` de `confrontos`), `templates/pages/confrontos.html`, `static/js/confrontos.js`, `static/css/style.css`
- **O que muda:**
  - **Grade de 2 colunas no desktop** (`max-width: 1100px`): cards fechados ficam organizados em 2 colunas; ao expandir um card (`details[open]`), ele ocupa a **largura total** (`grid-column: 1 / -1`) para preservar a leitura confortável dos quadros internos. Em telas estreitas, mantém 1 coluna.
  - **Identidade dos times no cabeçalho do card:** faixa/acento sutil usando as cores dos dois times (`colors[away]` e `colors[home]`), preservando os indicadores de jogo de divisão (amarelo) e rodadas de playoffs.
  - **Barras comparativas duplas:** no comparativo completo dentro do card expandido, adicionar barras proporcionais lado a lado coloridas com as cores dos dois times, mantendo os valores numéricos, os selos de posição na liga e o destaque do melhor valor.

---

## 4. Verificação e documentação

- Rodar `.venv/bin/pytest -q` garantindo que todos os testes (inclusive `test_render.py` e `test_matchups.py`) continuem passando.
- Gerar o site localmente com `.venv/bin/python generate.py --out site` e validar visualmente nos temas claro e escuro, no desktop e no mobile.
- Atualizar `docs/design.md` e `docs/memory.md` após a implementação.
