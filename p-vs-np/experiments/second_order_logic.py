#!/usr/bin/env python3
"""
FASE 3 EXPERIMENTO: Lógica de Segunda Ordem e P vs NP
Codificação de problemas em lógica de predicados e verificação com Z3
"""

# Tenta importar Z3, se não disponível usa implementação manual
try:
    from z3 import *
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False
    print("Z3 não disponível. Usando implementação manual.\n")

class PropositionalLogic:
    """Sistema de lógica proposicional para codificação de SAT"""
    
    def __init__(self, num_variables):
        self.num_variables = num_variables
        self.variables = {}
        self.clauses = []
        
        # Inicializa variáveis
        for i in range(1, num_variables + 1):
            self.variables[i] = f"x{i}"
    
    def add_clause(self, literals):
        """
        Adiciona uma cláusula
        Exemplo: (1, -2, 3) significa (x1 OR NOT x2 OR x3)
        """
        self.clauses.append(literals)
    
    def to_cnf(self):
        """Retorna a fórmula em CNF"""
        return self.clauses
    
    def evaluate(self, assignment):
        """Avalia a fórmula com uma atribuição"""
        for clause in self.clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                value = assignment.get(var, False)
                if lit < 0:
                    value = not value
                if value:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                return False
        return True
    
    def brute_force_solve(self):
        """Força bruta para encontrar satisfatibilidade"""
        from itertools import product
        
        for assignment_tuple in product([True, False], repeat=self.num_variables):
            assignment = {i+1: v for i, v in enumerate(assignment_tuple)}
            if self.evaluate(assignment):
                return True, assignment
        return False, None

def encode_sat_as_logic():
    """
    Codifica SAT como problema de lógica de predicados
    """
    print("=== CODIFICAÇÃO DE SAT EM LÓGICA DE PREDICADOS ===\n")
    
    # Fórmula: (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3)
    print("Fórmula: (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)")
    
    pl = PropositionalLogic(3)
    pl.add_clause([1, 2])      # (x1 OR x2)
    pl.add_clause([-1, 3])     # (NOT x1 OR x3)
    pl.add_clause([-2, -3])    # (NOT x2 OR NOT x3)
    
    print("\nCodificação em lógica de predicados:")
    print("∃x1, x2, x3 ∈ {0,1}:")
    print("  (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)")
    
    print("\nVerificação por força bruta:")
    sat, assignment = pl.brute_force_solve()
    
    if sat:
        print(f"SAT! Atribuição: {assignment}")
    else:
        print("UNSAT")
    
    return pl

def second_order_simulation():
    """
    Simula quantificadores de segunda ordem
    """
    print("\n=== SIMULAÇÃO DE QUANTIFICADORES DE SEGUNDA ORDEM ===\n")
    
    # Conceito: Em segunda ordem, podemos quantificar sobre CONJUNTOS
    # Exemplo: ∃S ⊆ {1,...,n} tal que ∀x ∈ S, P(x)
    
    n = 5
    print(f"Universo: {{1, 2, ..., {n}}}")
    
    # Predicado P(x): x é par
    def P(x):
        return x % 2 == 0
    
    # Simula ∃S ⊆ U tal que ∀x ∈ S: P(x)
    print("\nBuscando S tal que ∀x ∈ S: P(x) (onde P(x) = 'x é par')")
    
    # Em segunda ordem, quantificamos sobre TODOS os subconjuntos
    from itertools import combinations
    
    subsets_with_property = []
    for size in range(n + 1):
        for subset in combinations(range(1, n + 1), size):
            if all(P(x) for x in subset):
                subsets_with_property.append(subset)
    
    print(f"Subconjuntos onde todos os elementos são pares:")
    for s in subsets_with_property:
        print(f"  {s}")
    
    print(f"\nTotal: {len(subsets_with_property)} subconjuntos")
    print("\nEm primeira ordem, não poderíamos quantificar sobre conjuntos.")
    print("Em segunda ordem, podemos - isso aumenta a expressividade.")
    
    # Conexão com P vs NP
    print("\n=== CONEXÃO COM P VS NP ===")
    print("Para definir 'P', precisamos quantificar sobre:")
    print("  - Todas as máquinas de Turing (conjunto infinito)")
    print("  - Todas as funções de tempo (funções N → N)")
    print("Isso requer segunda ordem ou mais.")

def z3_attempt():
    """
    Tenta usar Z3 para provar P ≠ NP em instâncias pequenas
    """
    if not Z3_AVAILABLE:
        print("\n=== Z3 NÃO DISPONÍVEL ===")
        print("Pulando experimento com Z3.")
        return
    
    print("\n=== EXPERIMENTO COM Z3: TENTATIVA DE PROVA ===\n")
    
    # Define o problema como satisfatibilidade
    x1, x2, x3 = Bools('x1 x2 x3')
    
    # Fórmula SAT
    formula = And(
        Or(x1, x2),
        Or(Not(x1), x3),
        Or(Not(x2), Not(x3))
    )
    
    print("Fórmula: (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)")
    
    s = Solver()
    s.add(formula)
    
    result = s.check()
    print(f"Resultado Z3: {result}")
    
    if result == sat:
        m = s.model()
        print(f"Modelo: x1={m[x1]}, x2={m[x2]}, x3={m[x3]}")
    
    # Agora tenta algo impossível: provar que NÃO existe solução
    print("\nTentando provar que a fórmula é UNSAT:")
    s2 = Solver()
    s2.add(Not(formula))  # Negação: "não existe solução"
    
    result2 = s2.check()
    print(f"Resultado: {result2}")
    
    if result2 == unsat:
        print("Z3 provou que a negação é insatisfatível")
        print("=> A fórmula original é satisfatível")
    else:
        print("Z3 encontrou modelo para a negação")
        print("=> A fórmula original é insatisfatível")

def hierarquia_quantificadores():
    """
    Demonstra a hierarquia de quantificadores
    """
    print("\n=== HIERARQUIA DE QUANTIFICADORES ===\n")
    
    n = 4
    
    print(f"Universo: {{1, 2, ..., {n}}}")
    print("\nNíveis de complexidade lógica:")
    
    # Σ0 = Δ0 = predicados decidíveis
    print("\nΣ0 (predicados decidíveis):")
    print("  P(x): 'x é par'")
    
    # Σ1 = ∃ (primeira ordem existencial)
    print("\nΣ1 (∃ primeira ordem):")
    print("  ∃x P(x): 'existe x par'")
    
    # Π1 = ∀ (primeira ordem universal)
    print("\nΠ1 (∀ primeira ordem):")
    print("  ∀x P(x): 'todo x é par'")
    
    # Σ2 = ∃∀
    print("\nΣ2 (∃∀ segunda ordem):")
    print("  ∃S ∀x ∈ S: P(x)")
    
    # Π2 = ∀∃
    print("\nΠ2 (∀∃ segunda ordem):")
    print("  ∀S ∃x ∈ S: P(x)")
    
    # Para P vs NP
    print("\n=== ONDE P VS NP SE ENCAIXA? ===")
    print("Definição de P envolve:")
    print("  ∃M (máquina) ∃c ∈ N: M decide em tempo n^c")
    print("Isso é Σ2 (existencial sobre máquinas e constantes)")
    
    print("\nDefinição de NP envolve:")
    print("  ∃R ⊆ Σ* × Σ*: verificação polinomial")
    print("Isso é Σ1 (existencial sobre relação)")
    
    print("\n'P ≠ NP' seria:")
    print("  ¬(∃M, c: M decide NP em tempo n^c)")
    print("  = ∀M, c: ¬(M decide NP em tempo n^c)")
    print("Isso é Π2 (universal sobre máquinas e constantes)")
    
    print("\nSe 'P ≠ NP' é Π2-completo, então:")
    print("1. É expressível em SOL")
    print("2. Não pode ser provado em sistemas de primeira ordem")
    print("3. Requer axiomas transcendentes")

if __name__ == "__main__":
    # Executa todos os experimentos
    encode_sat_as_logic()
    second_order_simulation()
    z3_attempt()
    hierarquia_quantificadores()
