# FASE 5: Experimentos Computacionais em Instâncias Pequenas

## OBJETIVO
Testar conjecturas e padrões em instâncias pequenas de problemas NP-completos, buscando regularidades que possam levar a algoritmos polinomiais ou a evidência de dificuldade.

## ABORDAGEM GERAL

### 1. Geração de Instâncias
- Gerar instâncias aleatórias controladas
- Variar parâmetros sistematicamente
- Garantir reprodutibilidade

### 2. Medidas de Complexidade
- Tempo de execução
- Número de soluções
- Distribuição de soluções no espaço de busca
- Propriedades estruturais

### 3. Análise Estatística
- Ajuste de curvas
- Identificação de transições de fase
- Correlações entre propriedades

## PROBLEMAS INVESTIGADOS

### 5.1 SAT e 3-SAT
**Métricas:**
- Razão cláusulas/variáveis
- Distribuição de tamanhos de cláusulas
- Número de soluções

### 5.2 Clique Máximo
**Métricas:**
- Tamanho do clique máximo
- Distribuição de graus
- Coeficiente de clustering

### 5.3 Caminho Hamiltoniano
**Métricas:**
- Existência de caminho
- Densidade de arestas
- Componentes conexas

### 5.4 Vertex Cover
**Métricas:**
- Tamanho mínimo do cover
- Relação com matching máximo
- Estrutura do grafo

## EXPERIMENTOS DETALHADOS

### Experimento 5.1: Crescimento de Tempo em SAT
- Medir tempo para resolver 3-SAT
- Ajustar curva T(n) = a * 2^(bn)
- Estimar expoente b

### Experimento 5.2: Distribuição de Soluções
- Contar número de soluções para instâncias aleatórias
- Analisar distribuição (exponencial? polinomial?)

### Experimento 5.3: Estrutura do Espaço de Busca
- Mapear vizinhanças de soluções
- Analisar conectividade do espaço

### Experimento 5.4: Algoritmos Heurísticos
- Comparar: guloso, simulated annealing, algoritmos genéticos
- Medir qualidade da solução vs tempo

## CONJECTURAS A TESTAR

### Conjectura 5.1: Crescimento Exponencial
O tempo para resolver problemas NP-completos cresce exponencialmente com o tamanho da entrada.

### Conjectura 5.2: Transição de Fase
Existe um ponto crítico onde a dificuldade muda abruptamente.

### Conjectura 5.3: Estrutura de Lattice
O espaço de soluções tem estrutura de lattice que pode ser explorada.

## REFERÊNCIAS
- Schöning, T. (1999). "A probabilistic algorithm for k-SAT"
- Selman, B., et al. (1996). "Random walk planning"
- Achlioptas, D. (2009). "Random satisfiability"
