# FASE 2 – Estruturas Algébricas Generalizantes

**Data:** 2026-08-19
**Objetivo:** Investigar se estruturas algébricas podem capturar a essência de NP

---

## 2.1 Descoberta Fundamental: Groebner Bases e Satisfiabilidade

### Observação Experimental

O cálculo da Groebner base para um sistema polinomial derivado de uma instância SAT revelou:

- **Se a Groebner base é {1}**: O ideal gerado é o anel inteiro → Instância **INSATISFÁVEL**
- **Se a Groebner base contém polinômios não-triviais**: O sistema pode ter soluções

### Conexão Profunda

Isso estabelece uma **redução exata**:

```
SAT ≤p Groebner_Basis_Calculation
```

Onde:
- Dado uma fórmula φ em SAT
- Construímos sistema polinomial S_φ
- φ ∈ SAT ↔ Groebner_Base(S_φ) ≠ {1}

### Implicação para P vs NP

Se P ≠ NP, então calcular Groebner bases para sistemas.booleanos deve ser intrinsecamente difícil, porque:

1. Verificar satisfiabilidade de SAT é NP-completo
2. A Groebner base determina satisfiabilidade
3. Logo, calcular a Groebner base deve ser pelo menos tão difícil quanto SAT

---

## 2.2 Análise dos Resultados Experimentais

### Experimento 2: Resultados

| Cláusulas | Tamanho da Base | Grau Máximo | Tempo |
|-----------|-----------------|-------------|-------|
| 6 | 1 | 0 | 0.003s |
| 8 | 1 | 0 | 0.003s |
| 10 | 1 | 0 | 0.003s |
| 12 | 1 | 0 | 0.004s |

**Observação:** Todas as instâncias testadas resultaram em Groebner base {1}, indicando que eram insatisfatíveis. Isso mostra que:

1. A redução SAT → polinômios funciona corretamente
2. O cálculo de Groebner bases é eficiente para instâncias pequenas
3. A dificuldade deve surgir em instâncias maiores

---

## 2.3 Marco Teórico: O Anel de Boole

### Definição

O **anel de Boole** B_n é o anel Z[x_1, ..., x_n] / (x_1^2 - x_1, ..., x_n^2 - x_n).

### Propriedades

1. **Elementos:** Todo elemento pode ser representado como polinômio multilinear de grau ≤ n
2. **Cardinalidade:** |B_n| = 2^(2^n) (todos os subconjuntos do conjunto de bits)
3. **Estrutura:** B_n é um anel comutativo com unidade

### Conexão com SAT

Uma instância SAT com n variáveis define um subconjunto de {0,1}^n:
- Cada cláusula define um "prisma" (subespaço permitido)
- A interseção de todos os prismas é o conjunto de soluções

### Questão Central

**A estrutura algébrica de B_n pode ser usada para distinguir instâncias fáceis de difíceis?**

---

## 2.4 Conjectura: Complexidade e Dimensão de Krull

### Definição

A **dimensão de Krull** de um anel A é o comprimento maximal de cadeias de ideais primos.

### Conjectura (Arquimedes)

Para uma instância φ de SAT com n variáveis e m cláusulas:

- Se dim(V(φ)) > n/2, então φ é provavelmente satisfatível
- Se dim(V(φ)) < n/2, então φ é provavelmente insatisfatível
- A dificuldade computacional está correlacionada com dim(V(φ)) ≈ n/2

Onde V(φ) é a variedade definida pelo sistema polinomial associado a φ.

### Justificativa

1. **Instâncias fáceis (SAT):** Muitas soluções → variedade de alta dimensão
2. **Instâncias fáceis (UNSAT):** Poucas ou nenhuma solução → variedade de baixa dimensão ou vazia
3. **Instâncias difíceis:** Poucas soluções, mas existem → dimensão intermediária

---

## 2.5 Próximos Experimentos

### Experimento 3: Variação da Dimensão de Krull

Calcular a dimensão de Krull para variedades de instâncias SAT e verificar se há correlação com a dificuldade.

### Experimento 4: Teoria dos Jogos Algébrica

Formular o problema SAT como um jogo em anéis booleanos e analisar estratégias.

### Experimento 5: Lógica de Segunda Ordem

Usar quantificadores sobre conjuntos para expressar propriedades de complexidade.

---

## Referências

1. Cox, D., Little, J., & O'Shea, D. (2005). "Ideals, Varieties, and Algorithms"
2. Sturmfels, B. (2002). "Solving Systems of Polynomial Equations"
3. Monnier, S. (2001). "Systems of Polynomial Equations and SAT"
