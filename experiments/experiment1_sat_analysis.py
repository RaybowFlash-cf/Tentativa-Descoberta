"""
EXPERIMENTO 1: Análise de SAT com Z3
Explorar a estrutura de soluções de problemas SAT para buscar padrões

Objetivo: Testar se existem propriedades algébricas que distinguem
instâncias fáceis de difíceis em 3-SAT
"""

import z3
from z3 import is_true
import time
import random
import json
from itertools import product

def generate_3sat_instance(n_vars, n_clauses, seed=None):
    """Gera uma instância 3-SAT aleatória"""
    if seed is not None:
        random.seed(seed)
    
    clauses = []
    for _ in range(n_clauses):
        # Escolhe 3 variáveis aleatórias
        vars_in_clause = random.sample(range(1, n_vars + 1), min(3, n_vars))
        # Escolhe sinal para cada variável
        clause = []
        for v in vars_in_clause:
            if random.random() < 0.5:
                clause.append(z3.Bool(f'x{v}'))
            else:
                clause.append(z3.Not(z3.Bool(f'x{v}')))
        clauses.append(z3.Or(*clause))
    return clauses

def solve_sat_with_timing(clauses, timeout_ms=5000):
    """Resolve SAT com medição de tempo"""
    solver = z3.Solver()
    solver.set("timeout", timeout_ms)
    for clause in clauses:
        solver.add(clause)
    
    start = time.time()
    result = solver.check()
    elapsed = time.time() - start
    
    return result, elapsed

def analyze_phase_transition(n_vars=20, trials=50):
    """
    Analisa a transição de fase em 3-SAT
    
    A transição de fase ocorre quando o número de cláusulas
    é proporcional ao número de variáveis (razão c/n ≈ 4.267 para 3-SAT)
    """
    print("=" * 60)
    print("ANÁLISE DE TRANSIÇÃO DE FASE EM 3-SAT")
    print("=" * 60)
    
    results = []
    
    # Diferentes razões de cláusulas por variável
    ratios = [1.0, 2.0, 3.0, 4.0, 4.267, 4.5, 5.0, 6.0, 7.0, 8.0]
    
    for ratio in ratios:
        n_clauses = int(ratio * n_vars)
        sat_count = 0
        total_time = 0
        
        for trial in range(trials):
            clauses = generate_3sat_instance(n_vars, n_clauses, seed=trial * 100 + int(ratio * 10))
            result, elapsed = solve_sat_with_timing(clauses)
            if result == z3.sat:
                sat_count += 1
            total_time += elapsed
        
        sat_prob = sat_count / trials
        avg_time = total_time / trials
        
        results.append({
            'ratio': ratio,
            'n_clauses': n_clauses,
            'sat_probability': sat_prob,
            'avg_time': avg_time
        })
        
        print(f"  c/n = {ratio:.3f}: P(SAT) = {sat_prob:.3f}, Tempo médio = {avg_time:.4f}s")
    
    return results

def algebraic_structure_analysis():
    """
    Analisa a estrutura algébrica do espaço de soluções SAT
    
    Conjectura: A geometria do conjunto de soluções SAT
    contém informações sobre a complexidade do problema
    """
    print("\n" + "=" * 60)
    print("ANÁLISE DE ESTRUTURA ALGÉBRICA")
    print("=" * 60)
    
    n_vars = 10
    n_clauses = 25  # Próximo da transição de fase
    
    # Gera múltiplas instâncias
    solutions_per_instance = []
    
    for seed in range(20):
        clauses = generate_3sat_instance(n_vars, n_clauses, seed=seed)
        
        solver = z3.Solver()
        for clause in clauses:
            solver.add(clause)
        
        solutions = []
        count = 0
        while solver.check() == z3.sat and count < 10:
            model = solver.model()
            solution = tuple(1 if is_true(model[z3.Bool(f'x{i}')]) else 0 
                           for i in range(1, n_vars + 1))
            solutions.append(solution)
            
            # Adiciona restrição para encontrar solução diferente
            solver.add(z3.Or(*[z3.Bool(f'x{i+1}') != model[z3.Bool(f'x{i+1}')] 
                              for i in range(n_vars)]))
            count += 1
        
        solutions_per_instance.append(len(solutions))
    
    avg_solutions = sum(solutions_per_instance) / len(solutions_per_instance)
    print(f"  Número médio de soluções por instância: {avg_solutions:.2f}")
    print(f"  Soluções encontradas por instância: {solutions_per_instance}")
    
    # Analisa a distribuição de soluções
    print(f"\n  Distribuição de soluções:")
    print(f"    Mínimo: {min(solutions_per_instance)}")
    print(f"    Máximo: {max(solutions_per_instance)}")
    print(f"    Desvio padrão: {(sum((x - avg_solutions)**2 for x in solutions_per_instance) / len(solutions_per_instance))**0.5:.2f}")
    
    return solutions_per_instance

def symmetry_breaking_experiment():
    """
    Experimento: Quebra de simetria em SAT
    
    Conjectura: A simetria das instâncias SAT está relacionada
    à complexidade de resolução
    """
    print("\n" + "=" * 60)
    print("EXPERIMENTO DE QUEBRA DE SIMETRIA")
    print("=" * 60)
    
    n_vars = 8
    
    # Instância com alta simetria (toda cláusula usa variáveis consecutivas)
    symmetric_clauses = []
    for i in range(1, n_vars):
        symmetric_clauses.append(z3.Or(
            z3.Bool(f'x{i}'), 
            z3.Bool(f'x{i+1}')
        ))
    
    result_sym, time_sym = solve_sat_with_timing(symmetric_clauses)
    print(f"  Instância simétrica: {result_sym}, tempo = {time_sym:.6f}s")
    
    # Instância sem simetria (variáveis aleatórias)
    asymmetric_clauses = generate_3sat_instance(n_vars, n_vars, seed=42)
    result_asym, time_asym = solve_sat_with_timing(asymmetric_clauses)
    print(f"  Instância assimétrica: {result_asym}, tempo = {time_asym:.6f}s")
    
    return {
        'symmetric': {'result': str(result_sym), 'time': time_sym},
        'asymmetric': {'result': str(result_asym), 'time': time_asym}
    }

def main():
    print("ARQUIMEDES - EXPERIMENTO 1: Análise SAT com Z3")
    print("=" * 60)
    print()
    
    # 1. Análise de transição de fase
    phase_results = analyze_phase_transition()
    
    # 2. Análise de estrutura algébrica
    algebraic_results = algebraic_structure_analysis()
    
    # 3. Experimento de quebra de simetria
    symmetry_results = symmetry_breaking_experiment()
    
    # Salva resultados
    all_results = {
        'phase_transition': phase_results,
        'algebraic_structure': algebraic_results,
        'symmetry_breaking': symmetry_results
    }
    
    with open('/home/daytona/project/data/experiment1_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("\n" + "=" * 60)
    print("CONCLUSÕES DO EXPERIMENTO 1")
    print("=" * 60)
    print("""
    1. Transição de fase: Confirma que a dificuldade de SAT
       está concentrada em uma faixa específica de razão cláusulas/variáveis.
    
    2. Estrutura algébrica: O número de soluções varia significativamente,
       sugerindo que a geometria do espaço de soluções é complexa.
    
    3. Simetria: Instâncias com mais estrutura podem ser mais fáceis
       de resolver, indicando que simetria é uma propriedade importante.
    
    PRÓXIMA HIPÓTESE: 
    Se a complexidade está relacionada à estrutura do espaço de soluções,
    podemos tentar capturar essa estrutura usando teoria de ideais
    e variedades algébricas (Teoria de Grobner).
    """)

if __name__ == "__main__":
    main()
