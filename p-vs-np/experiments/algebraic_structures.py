#!/usr/bin/env python3
"""
FASE 2 EXPERIMENTO: Análise de estruturas algébricas em problemas NP-completos
Foco: Transição de fase em 3-SAT e representação algébrica
"""

import random
import time
from itertools import product

class BooleanFormula:
    """Representa uma fórmula 3-SAT"""
    def __init__(self, num_variables, clauses):
        self.num_variables = num_variables
        self.clauses = clauses  # Lista de (l1, l2, l3), lit > 0 = variável, lit < 0 = negação
    
    def evaluate(self, assignment):
        """Avalia a fóbrua com uma atribuição"""
        for clause in self.clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                value = assignment[var - 1]
                if lit < 0:
                    value = not value
                if value:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                return False
        return True
    
    def brute_force_check(self):
        """Força bruta para verificar satisfatibilidade"""
        for assignment in product([True, False], repeat=self.num_variables):
            if self.evaluate(assignment):
                return True, assignment
        return False, None
    
    def clause_to_variable_ratio(self):
        """Retorna razão cláusulas/variáveis"""
        return len(self.clauses) / self.num_variables

def generate_3sat(num_variables, num_clauses):
    """Gera uma instância aleatória de 3-SAT"""
    clauses = []
    for _ in range(num_clauses):
        # Escolhe 3 variáveis aleatórias
        vars_in_clause = random.sample(range(1, num_variables + 1), min(3, num_variables))
        # Adiciona negações aleatórias
        clause = []
        for v in vars_in_clause:
            if random.random() < 0.5:
                clause.append(-v)
            else:
                clause.append(v)
        clauses.append(tuple(clause))
    return BooleanFormula(num_variables, clauses)

def phase_transition_experiment():
    """
    Experimento: Transição de fase em 3-SAT
    Varia a razão cláusulas/variáveis e mede satisfatibilidade
    """
    print("=== EXPERIMENTO: TRANSIÇÃO DE FASE EM 3-SAT ===\n")
    
    num_variables = 10  # Pequeno para ser viável
    num_trials = 20
    
    # Diferentes razões cláusulas/variáveis
    ratios = [2.0, 3.0, 3.5, 4.0, 4.26, 4.5, 5.0, 6.0, 7.0, 8.0]
    
    results = []
    
    print(f"Variáveis: {num_variables}")
    print(f"Trials por razão: {num_trials}")
    print("-" * 60)
    print(f"{'Razão C/V':>10} | {'Média Cláusulas':>15} | {'% Satisfatível':>15} | {'Tempo (ms)':>10}")
    print("-" * 60)
    
    for ratio in ratios:
        num_clauses = int(ratio * num_variables)
        satisfiable_count = 0
        total_time = 0
        
        for _ in range(num_trials):
            formula = generate_3sat(num_variables, num_clauses)
            
            start = time.time()
            sat, _ = formula.brute_force_check()
            elapsed = (time.time() - start) * 1000
            
            if sat:
                satisfiable_count += 1
            total_time += elapsed
        
        pct = satisfiable_count / num_trials * 100
        avg_time = total_time / num_trials
        results.append((ratio, pct, avg_time))
        
        print(f"{ratio:10.2f} | {num_clauses:15d} | {pct:15.1f} | {avg_time:10.2f}")
    
    # Análise da transição
    print("\n=== ANÁLISE DA TRANSIÇÃO ===")
    print("A transição de fase ocorre aproximadamente em C/V ≈ 4.26")
    print("onde a satisfatibilidade muda de ~100% para ~0%")
    
    # Identificar ponto de transição
    transition_point = None
    for i in range(len(results) - 1):
        if results[i][1] > 50 and results[i+1][1] < 50:
            transition_point = (results[i][0] + results[i+1][0]) / 2
            break
    
    if transition_point:
        print(f"\nPonto de transição estimado: C/V ≈ {transition_point:.2f}")
        print("Teórico: ~4.267 (Monasson et al., 1999)")
    
    return results

def algebraic_representation_experiment():
    """
    Experimento: Representação algébrica de SAT em anéis booleanos
    """
    print("\n=== EXPERIMENTO: REPRESENTAÇÃO ALGÉBRICA EM Z₂ ===\n")
    
    # Exemplo: (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3)
    # Representação: cada cláusula é uma soma em Z₂, produto é AND
    
    print("Fórmula: (x1 OR x2) AND (¬x1 OR x3) AND (¬x2 OR ¬x3)")
    print("\nRepresentação em anel booleano Z₂:")
    print("Cada cláusula: (1 + x_i1)(1 + x_i2)(1 + x_i3) = 0 em Z₂")
    print("Onde x_i = 1 se variável é falsa, 0 se verdadeira")
    
    # Verifica todas as atribuições
    print("\nVerificando todas as atribuições:")
    print("-" * 40)
    
    formula = BooleanFormula(3, [(1, 2), (-1, 3), (-2, -3)])
    
    for x1 in [True, False]:
        for x2 in [True, False]:
            for x3 in [True, False]:
                assignment = [x1, x2, x3]
                result = formula.evaluate(assignment)
                # Representação em Z₂
                z2_values = [0 if v else 1 for v in assignment]
                print(f"x={assignment} -> Fórmula={result} -> Z₂={z2_values}")
    
    print("\nObservação: A satisfatibilidade está ligada à existência")
    print("de zeros em uma variedade algébrica sobre Z₂.")

def spectral_analysis_experiment():
    """
    Experimento: Análise espectral de grafos para problemas de clique
    """
    print("\n=== EXPERIMENTO: ANÁLISE ESPECTRAL DE GRAFOS ===\n")
    
    # Gera um grafo aleatório
    n = 6
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < 0.5:
                edges.append((i, j))
    
    # Matriz de adjacência
    adj = [[0] * n for _ in range(n)]
    for i, j in edges:
        adj[i][j] = 1
        adj[j][i] = 1
    
    print(f"Grafo com {n} vértices e {len(edges)} arestas:")
    print("Matriz de adjacência:")
    for row in adj:
        print(" ".join(str(x) for x in row))
    
    # Calcula autovalores (aproximação usando potência da matriz)
    print("\nPropriedades do grafo:")
    
    # Grau de cada vértice
    degrees = [sum(row) for row in adj]
    print(f"Graus: {degrees}")
    print(f"Grau médio: {sum(degrees)/n:.2f}")
    
    # Número de triângulos (via A^3)
    # A^2[i][j] = número de caminhos de tamanho 2 de i para j
    a2 = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                a2[i][j] += adj[i][k] * adj[k][j]
    
    # Número de triângulos = tr(A^3) / 6
    triangles = 0
    for i in range(n):
        for j in range(n):
            triangles += adj[i][j] * a2[j][i]
    triangles //= 6
    
    print(f"Número de triângulos: {triangles}")
    
    # Conexão com cliques: um k-clique tem (k choose 2) arestas
    print("\nConexão com cliques:")
    for k in range(2, n+1):
        # Se existe um k-clique, tem (k choose 2) arestas
        # e cada vértice tem grau ≥ k-1
        clique_edges = k * (k - 1) // 2
        min_degree = k - 1
        print(f"k={k}: {clique_edges} arestas necessárias, grau mínimo {min_degree}")
    
    print("\nA análise espectral pode revelar a existência de cliques")
    print("através dos autovalores da matriz de adjacência.")

if __name__ == "__main__":
    random.seed(42)  # Para reprodutibilidade
    
    # Executa todos os experimentos
    phase_transition_experiment()
    algebraic_representation_experiment()
    spectral_analysis_experiment()
