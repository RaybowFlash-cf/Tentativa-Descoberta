# FASE 4: Formulações de Teoria dos Jogos para P vs. NP

## OBJETIVO
Explorar conexões entre P vs. NP e teoria dos jogos, particularmente jogos de verificação e equilíbrios.

## FUNDAMENTOS DE TEORIA DOS JOGOS

### Definições Básicas
- **Jogo:** Conjunto de jogadores, estratégias, e pagamentos
- **Equilíbrio de Nash:** Nenhum jogador pode melhorar unilateralmente
- **PPAD:** Classe de problemas com equilíbrios garantidos (mas não necessariamente encontráveis)

### Conexões com Complexidade
- Encontrar equilíbrios de Nash é PPAD-completo
- PPAD está contido em FP (funcional polinomial), mas não se sabe se é igual
- P vs NP implica questões sobre PPAD

## FORMULAÇÕES JOGO-TEÓRICAS DE P VS NP

### Formulação 4.1: Jogo de Verificação Prova-Certificador

**Conceito:** Transformar P vs NP em um jogo entre:
- **Prover (Prova):** Tenta convencer de que L ∈ NP
- **Verifier (Verificador):** Tenta refutar

**Estrutura:**
1. Prover envia um certificado y para entrada x
2. Verificador verifica se y é uma prova válida
3. Se Verificador sempre aceita provas válidas, L ∈ NP

**Conexão com P vs NP:**
- Se P = NP, então existe um algoritmo polinomial que encontra y
- Se P ≠ NP, então encontrar y é intrinsecamente difícil

### Formulação 4.2: Jogo de Busca em Grafos

**Problema do Caminho Hamiltoniano como Jogo:**
- **Jogador 1 (Construtor):** Tenta construir um caminho hamiltoniano
- **Jogador 2 (Sabotador):** Tenta bloquear arestas

**Estrutura:**
1. Construtor escolhe um vértice inicial
2. Sabotador remove k arestas do grafo
3. Construtor escolhe próxima aresta
4. Repete até visitar todos ou falhar

**Conexão:**
- Se P = NP, Construtor pode sempre vencer para k pequeno
- Se P ≠ NP, Sabotador pode forçar vitória para k suficientemente grande

### Formulação 4.3: Jogo de Adivinhação de SAT

**Jogo de Adivinhação:**
- **Adivinha (Solver):** Tenta adivinhar atribuição satisfatória
- **Pergunta (Instance):** Esconde uma fórmula SAT

**Estrutura:**
1. Pergunta escolhe fórmula φ
2. Adivinha escolhe atribuição α
3. Pergunta verifica se φ(α) = True

**Conexão:**
- Se P = NP, Adivinha pode vencer com estratégia polinomial
- Se P ≠ NP, Pergunta pode forçar vitória

## RESULTADOS CONHECIDOS

### PPAD e Equilíbrios
- **Teorema (Daskalakis-Goldberg-Papadimitriou, 2009):** Encontrar equilíbrios de Nash é PPAD-completo
- **Implicação:** Mesmo que P = NP, encontrar equilíbrios pode ser difícil

### Jogos de Soma Zero
- **Minimax Theorem:** Em jogos de soma zero finitos, existe valor do jogo
- **P vs NP:** Se P = NP, valores de jogo podem ser computados eficientemente

### Jogos Iterados
- **Folk Theorem:** Em jogos repetidos, muitos equilíbrios existem
- **Conexão:** Estratégias complexas podem emergir de interações simples

## HIPÓTESE JOGO-TEÓRICA

**Conjectura Archimedes (v0.2):**
P ≠ NP se e somente se existem jogos onde:
1. Verificar vitória é fácil (polinomial)
2. Encontrar estratégia vencedora é difícil (exponencial)
3. Não existe "atalho" que aproveite a estrutura do jogo

## EXPERIMENTOS JOGO-TEÓRICOS

### Experimento 4.1: SAT como Jogo de Verificação
- Implementar jogo Prover vs Verifier
- Analisar estratégias ótimas

### Experimento 4.2: Caminho Hamiltoniano como Jogo
- Implementar jogo Construtor vs Sabotador
- Medir complexidade para diferentes tamanhos

### Experimento 4.3: Algoritmos Genéticos para Jogos
- Usar algoritmos genéticos para encontrar equilíbrios
- Relacionar com complexidade computacional

## REFERÊNCIAS
- Nash, J. (1951). "Non-cooperative games"
- Daskalakis, C., et al. (2009). "The complexity of computing a Nash equilibrium"
- Papadimitriou, C. (1994). "On the complexity of the parity argument"
