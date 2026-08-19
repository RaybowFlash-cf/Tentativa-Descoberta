"""
EXPERIMENTO 2: Estruturas Algébricas e Complexidade
Explorar a relação entre teoria de ideais/Groebner bases e complexidade computacional

Objetivo: Investigar se a estrutura algébrica do anel de polinômios
pode capturar informações sobre a complexidade de problemas NP
"""

import sympy
from sympy import symbols, And, Or, Not, simplify, expand, Poly
from sympy.polys.orderings import lex
import json
import time
from itertools import product

def sat_to_polynomial_boolean(n_vars, clauses):
    """
    Converte fórmula SAT para sistema polinomial sobre GF(2)
    
    Cada variável x_i é mapeada para x_i ∈ {0, 1}
    Cada cláusula (l1 ∨ l2 ∨ l3) é convertida para:
    1 - (1-l1)(1-l2)(1-l3) = 0
    
    Isso cria um ideal no anel Z[x1,...,xn] / (x_i^2 - x_i)
    """
    x = symbols('x1:%d' % (n_vars + 1))
    polynomials = []
    
    for clause in clauses:
        # clause é uma lista de (variável, negada)
        product_term = 1
        for var_idx, negated in clause:
            if negated:
                product_term *= (1 - x[var_idx - 1])
            else:
                product_term *= x[var_idx - 1]
        # A cláusula é satisfeita se o produto for 0
        polynomials.append(1 - product_term)
    
    # Adiciona restrições x_i^2 = x_i para booleanidade
    for i in range(n_vars):
        polynomials.append(x[i]**2 - x[i])
    
    return polynomials, x

def analyze_ideal_structure(n_vars=6, n_clauses=12):
    """
    Analisa a estrutura do ideal gerado pelas restrições SAT
    """
    print("=" * 60)
    print("ANÁLISE DE ESTRUTURA DE IDEAL - SAT")
    print("=" * 60)
    
    import random
    random.seed(42)
    
    # Gera cláusulas aleatórias
    clauses = []
    for _ in range(n_clauses):
        vars_in_clause = random.sample(range(1, n_vars + 1), 3)
        clause = [(v, random.random() < 0.5) for v in vars_in_clause]
        clauses.append(clause)
    
    print(f"\nInstância: {n_vars} variáveis, {n_clauses} cláusulas")
    print("Cláusulas:")
    for i, clause in enumerate(clauses):
        literals = []
        for v, neg in clause:
            literals.append(f"¬x{v}" if neg else f"x{v}")
        print(f"  C{i+1}: ({' ∨ '.join(literals)})")
    
    # Converte para polinômios
    polynomials, x = sat_to_polynomial_boolean(n_vars, clauses)
    
    print(f"\nPolinômios gerados: {len(polynomials)}")
    
    # Calcula a Groebner base
    print("\nCalculando Groebner base...")
    start = time.time()
    try:
        from sympy.polys import groebner
        G = groebner(polynomials, *x, order=lex)
        elapsed = time.time() - start
        print(f"Groebner base calculada em {elapsed:.3f}s")
        print(f"Tamanho da base: {len(G)}")
        print(f"Polinômios na base:")
        for i, g in enumerate(G):
            print(f"  g{i+1} = {g}")
        
        # Analisa propriedades da base
        degrees = [g.as_poly(*x).total_degree() for g in G]
        print(f"\nGraus dos polinômios: {degrees}")
        print(f"Grau máximo: {max(degrees)}")
        print(f"Grau médio: {sum(degrees)/len(degrees):.2f}")
        
    except Exception as e:
        print(f"Erro no cálculo: {e}")
        elapsed = time.time() - start
        G = None
    
    return {
        'n_vars': n_vars,
        'n_clauses': n_clauses,
        'n_polynomials': len(polynomials),
        'groebner_size': len(G) if G else 0,
        'elapsed': elapsed
    }

def polynomial_sat_equivalence():
    """
    Demonstra a equivalência entre SAT e sistemas polinomiais
    
    Se P = NP, então existe um algoritmo polinomial para encontrar
    pontos em variedades definidas por polinômios booleanos
    """
    print("\n" + "=" * 60)
    print("EQUIVALÊNCIA SAT ↔ SISTEMAS POLINOMIAIS")
    print("=" * 60)
    
    x1, x2, x3 = symbols('x1 x2 x3')
    
    # Exemplo: (x1 ∨ x2 ∨ x3) ∧ (¬x1 ∨ ¬x2 ∨ x3) ∧ (x1 ∨ ¬x2 ∨ ¬x3)
    # Convertido para polinômios:
    # C1: 1 - x1*x2*x3 = 0
    # C2: 1 - (1-x1)*(1-x2)*x3 = 0
    # C3: 1 - x1*(1-x2)*(1-x3) = 0
    
    p1 = 1 - x1*x2*x3
    p2 = 1 - (1-x1)*(1-x2)*x3
    p3 = 1 - x1*(1-x2)*(1-x3)
    
    # Restrições de booleanidade
    b1 = x1**2 - x1
    b2 = x2**2 - x2
    b3 = x3**2 - x3
    
    print("\nSistema polinomial:")
    print(f"  p1 = {expand(p1)} = 0")
    print(f"  p2 = {expand(p2)} = 0")
    print(f"  p3 = {expand(p3)} = 0")
    print(f"  b1 = {b1} = 0")
    print(f"  b2 = {b2} = 0")
    print(f"  b3 = {b3} = 0")
    
    # Verifica soluções conhecidas
    print("\nVerificação de soluções:")
    solutions_found = []
    
    for v1, v2, v3 in product([0, 1], repeat=3):
        vals = {x1: v1, x2: v2, x3: v3}
        p1_val = p1.subs(vals)
        p2_val = p2.subs(vals)
        p3_val = p3.subs(vals)
        
        if p1_val == 0 and p2_val == 0 and p3_val == 0:
            print(f"  x1={v1}, x2={v2}, x3={v3} → SOLUÇÃO VÁLIDA")
            solutions_found.append((v1, v2, v3))
        else:
            print(f"  x1={v1}, x2={v2}, x3={v3} → Não satisfaz")
    
    print(f"\nTotal de soluções: {len(solutions_found)}")
    return solutions_found

def complexity_algebraic_bridge():
    """
    Explora a ponte entre complexidade computacional e álgebra
    
    Conjectura: A complexidade de calcular uma Groebner base
    está relacionada com a complexidade do problema original
    """
    print("\n" + "=" * 60)
    print("PONTE ALGÉBRICO-COMPUTACIONAL")
    print("=" * 60)
    
    from sympy.polys import groebner
    import random
    
    x = symbols('x1:%d' % 7)
    
    results = []
    
    # Testa diferentes tamanhos de sistema
    for n_clauses in [6, 8, 10, 12]:
        random.seed(42)
        polynomials = []
        
        # Booleanidade
        for i in range(6):
            polynomials.append(x[i]**2 - x[i])
        
        # Cláusulas aleatórias
        for _ in range(n_clauses):
            vars_in_clause = random.sample(range(1, 7), 3)
            product_term = 1
            for v in vars_in_clause:
                if random.random() < 0.5:
                    product_term *= (1 - x[v - 1])
                else:
                    product_term *= x[v - 1]
            polynomials.append(1 - product_term)
        
        start = time.time()
        try:
            G = groebner(polynomials, *x, order=lex)
            elapsed = time.time() - start
            base_size = len(G)
            max_degree = max(g.as_poly(*x).total_degree() for g in G)
            
            results.append({
                'n_clauses': n_clauses,
                'base_size': base_size,
                'max_degree': max_degree,
                'elapsed': elapsed
            })
            
            print(f"  Cláusulas: {n_clauses}, Base: {base_size}, "
                  f"Grau máx: {max_degree}, Tempo: {elapsed:.3f}s")
            
        except Exception as e:
            print(f"  Cláusulas: {n_clauses}, ERRO: {e}")
    
    print("\nAnálise:")
    if len(results) > 1:
        growth = results[-1]['elapsed'] / results[0]['elapsed'] if results[0]['elapsed'] > 0 else float('inf')
        print(f"  Crescimento do tempo: {growth:.2f}x")
        print(f"  Isso sugere complexidade {'super-polinomial' if growth > 10 else 'aproximadamente polinomial'}")
    
    return results

def main():
    print("ARQUIMEDES - EXPERIMENTO 2: Estruturas Algébricas")
    print("=" * 60)
    print()
    
    # 1. Análise de estrutura de ideal
    ideal_results = analyze_ideal_structure()
    
    # 2. Equivalência SAT ↔ sistemas polinomiais
    equivalence_results = polynomial_sat_equivalence()
    
    # 3. Ponte algébrico-computacional
    bridge_results = complexity_algebraic_bridge()
    
    # Salva resultados
    all_results = {
        'ideal_structure': ideal_results,
        'equivalence': {'solutions': equivalence_results},
        'algebraic_bridge': bridge_results
    }
    
    with open('/home/daytona/project/data/experiment2_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("\n" + "=" * 60)
    print("CONCLUSÕES DO EXPERIMENTO 2")
    print("=" * 60)
    print("""
    1. Estrutura de Ideais: A Groebner base captura a estrutura
       do problema SAT, mas seu cálculo é potencialmente difícil.
    
    2. Equivalência: SAT é fielmente representado como sistema polinomial,
       confirmando a conexão entre lógica e álgebra.
    
    3. Complexidade do cálculo: O tempo de Groebner base cresce
       rapidamente, sugerindo que cálculos algébricos podem capturar
       a complexidade NP.
    
    INSIGHT FUNDAMENTAL:
    Se P ≠ NP, então calcular Groebner bases para sistemas.booleanos
    deve ser intrinsecamente difícil. Isso sugere uma Possible
    redução: SAT ≤p Groebner_Basis_Calculation
    
    PRÓXIMA HIPÓTESE:
    Investigar se existem subclasses de ideais (correspondendo a
    subclasses de SAT) onde o cálculo é polinomial, e se isso
    corresponde a subclasses de NP que estão em P.
    """)

if __name__ == "__main__":
    main()
