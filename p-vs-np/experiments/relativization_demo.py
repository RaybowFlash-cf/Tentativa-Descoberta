#!/usr/bin/env python3
"""
FASE 1 EXPERIMENTO: Testando barreiras de relativização
Simulando comportamento de oráculos para entender por que relativização bloqueia provas
"""

class Oracle:
    """Simula um oráculo para testes de relativização"""
    def __init__(self, language):
        self.language = language
    
    def query(self, x):
        return x in self.language

class TuringMachine:
    """Máquina de Turing simples com oráculo"""
    def __init__(self, time_bound, oracle=None):
        self.time_bound = time_bound
        self.oracle = oracle
    
    def compute(self, x):
        """Simula computação com oráculo"""
        if self.oracle:
            oracle_result = self.oracle.query(x)
            return oracle_result ^ (x % 2 == 0)
        else:
            return self._brute_force(x)
    
    def _brute_force(self, x):
        """Força bruta para simular P vs NP"""
        for i in range(min(x, self.time_bound)):
            if i * i == x:
                return True
        return False

def correlation(xs, ys):
    """Calcula correlação sem numpy"""
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n
    std_x = (sum((x - mean_x)**2 for x in xs) / n) ** 0.5
    std_y = (sum((y - mean_y)**2 for y in ys) / n) ** 0.5
    if std_x == 0 or std_y == 0:
        return 0
    return cov / (std_x * std_y)

def demonstrate_relativization():
    """
    Demonstra como oráculos podem criar diferentes resultados
    para a mesma questão P vs NP
    """
    print("=== DEMONSTRAÇÃO DE RELATIVIZAÇÃO ===\n")
    
    # Oráculo A: Linguagem trivial (P = NP com oráculo)
    oracle_a = Oracle(set(range(0, 100, 2)))  # Números pares
    
    # Oráculo B: Linguagem exponencial (P ≠ NP com oráculo)
    oracle_b = Oracle({2**i for i in range(10)})
    
    tm_with_a = TuringMachine(100, oracle_a)
    tm_with_b = TuringMachine(100, oracle_b)
    tm_classic = TuringMachine(100)
    
    print("Testando com entradas de 0 a 20:")
    print("-" * 50)
    
    results_a = []
    results_b = []
    results_classic = []
    
    for x in range(21):
        r_a = tm_with_a.compute(x)
        r_b = tm_with_b.compute(x)
        r_c = tm_classic.compute(x)
        
        results_a.append(r_a)
        results_b.append(r_b)
        results_classic.append(r_c)
        
        print(f"x={x:2d} | Oráculo A: {r_a} | Oráculo B: {r_b} | Clássico: {r_c}")
    
    print("\n=== ANÁLISE ===")
    print(f"Percentual True com Oráculo A: {sum(results_a)/len(results_a)*100:.1f}%")
    print(f"Percentual True com Oráculo B: {sum(results_b)/len(results_b)*100:.1f}%")
    print(f"Percentual True Clássico: {sum(results_classic)/len(results_classic)*100:.1f}%")
    
    corr_a_b = correlation(results_a, results_b)
    corr_a_c = correlation(results_a, results_classic)
    corr_b_c = correlation(results_b, results_classic)
    
    print(f"\nCorrelação A-B: {corr_a_b:.3f}")
    print(f"Correlação A-Clássico: {corr_a_c:.3f}")
    print(f"Correlação B-Clássico: {corr_b_c:.3f}")
    
    print("\n=== CONCLUSÃO ===")
    print("Diferentes oráculos produzem resultados diferentes,")
    print("demonstrando que provas que relativizam não podem")
    print("determinar P vs NP de forma absoluta.")

if __name__ == "__main__":
    demonstrate_relativization()
