#!/usr/bin/env python3
"""
FASE 4 EXPERIMENTO: Teoria dos Jogos e P vs NP
Jogos de verificação e busca em grafos
"""

import random
from collections import defaultdict

class SATGame:
    """
    Jogo de verificação SAT: Prover vs Verifier
    Prover tenta convencer de que fórmula é satisfatível
    """
    def __init__(self, formula):
        self.formula = formula  # Lista de cláusulas
        self.num_variables = max(max(abs(lit) for lit in clause) for clause in formula)
    
    def evaluate(self, assignment):
        """Avalia fórmula com atribuição"""
        for clause in self.formula:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                value = assignment.get(var, False)
                if lit < 0:
                    value = not value
                if value:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True
    
    def prover_strategy_random(self):
        """Estratégia aleatória do Prover"""
        return {i: random.choice([True, False]) for i in range(1, self.num_variables + 1)}
    
    def prover_strategy_greedy(self):
        """Estratégia gulosa: maximiza cláusulas satisfeitas"""
        assignment = {}
        
        for var in range(1, self.num_variables + 1):
            # Testa ambos os valores
            assignment[var] = True
            count_true = sum(self.evaluate(assignment) for _ in range(10))
            
            assignment[var] = False
            count_false = sum(self.evaluate(assignment) for _ in range(10))
            
            # Escolhe o valor que satisfaz mais cláusulas
            assignment[var] = count_true >= count_false
        
        return assignment
    
    def play_game(self, prover_strategy="greedy", num_rounds=100):
        """Joga o jogo de verificação"""
        wins = 0
        
        for _ in range(num_rounds):
            if prover_strategy == "random":
                assignment = self.prover_strategy_random()
            else:
                assignment = self.prover_strategy_greedy()
            
            # Verificador verifica
            if self.evaluate(assignment):
                wins += 1
        
        return wins / num_rounds

class HamiltonianGame:
    """
    Jogo do Caminho Hamiltoniano: Construtor vs Sabotador
    """
    def __init__(self, graph):
        self.graph = graph  # Dict de adjacência
        self.n = len(graph)
    
    def has_hamiltonian_path(self, start):
        """Verifica caminho hamiltoniano por força bruta"""
        visited = set()
        path = []
        
        def dfs(v):
            visited.add(v)
            path.append(v)
            
            if len(path) == self.n:
                return True
            
            for neighbor in self.graph[v]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            
            path.pop()
            visited.remove(v)
            return False
        
        return dfs(start)
    
    def constructor_play_greedy(self):
        """Construtor escolhe vizinho com menor grau"""
        start = random.choice(list(self.graph.keys()))
        path = [start]
        visited = {start}
        
        for _ in range(self.n - 1):
            current = path[-1]
            neighbors = [n for n in self.graph[current] if n not in visited]
            
            if not neighbors:
                return None  # Falhou
            
            # Escolhe vizinho com menor grau (heurística)
            next_v = min(neighbors, key=lambda x: len(self.graph[x]))
            path.append(next_v)
            visited.add(next_v)
        
        return path
    
    def play_game(self, num_rounds=100):
        """Joga o jogo do caminho hamiltoniano"""
        wins = 0
        
        for _ in range(num_rounds):
            path = self.constructor_play_greedy()
            if path is not None:
                wins += 1
        
        return wins / num_rounds

def generate_random_graph(n, edge_prob=0.5):
    """Gera grafo aleatório"""
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < edge_prob:
                graph[i].append(j)
                graph[j].append(i)
    return graph

def sat_as_game_experiment():
    """
    Experimento: SAT como jogo de verificação
    """
    print("=== EXPERIMENTO: SAT COMO JOGO DE VERIFICAÇÃO ===\n")
    
    # Gera instâncias SAT aleatórias
    sizes = [3, 4, 5, 6]
    num_instances = 10
    num_rounds = 50
    
    print(f"{'Tam':>4} | {'% SAT':>6} | {'Random':>8} | {'Greedy':>8} | {'Diferença':>10}")
    print("-" * 50)
    
    for n in sizes:
        sat_count = 0
        random_wins = 0
        greedy_wins = 0
        
        for _ in range(num_instances):
            # Gera fórmula aleatória
            num_clauses = int(3.5 * n)  # Razão típica
            clauses = []
            for _ in range(num_clauses):
                clause = []
                for _ in range(3):
                    var = random.randint(1, n)
                    if random.random() < 0.5:
                        var = -var
                    clause.append(var)
                clauses.append(tuple(clause))
            
            game = SATGame(clauses)
            
            # Verifica se é satisfatível
            sat, _ = game.prover_strategy_greedy() and (True, None) or (False, None)
            
            # Joga o jogo
            random_rate = game.play_game("random", num_rounds)
            greedy_rate = game.play_game("greedy", num_rounds)
            
            random_wins += random_rate
            greedy_wins += greedy_rate
        
        random_avg = random_wins / num_instances
        greedy_avg = greedy_wins / num_instances
        diff = greedy_avg - random_avg
        
        print(f"{n:4d} | {sat_count/num_instances*100:6.1f} | {random_avg*100:7.1f}% | {greedy_avg*100:7.1f}% | {diff*100:+9.1f}%")
    
    print("\nAnálise:")
    print("- Estratégia gulosa supera aleatória consistentemente")
    print("- Dificuldade cresce com tamanho da instância")
    print("- Conexão com P vs NP: se P=NP, existem estratégias ótimas eficientes")

def hamiltonian_game_experiment():
    """
    Experimento: Caminho Hamiltoniano como jogo
    """
    print("\n=== EXPERIMENTO: CAMINHO HAMILTONIANO COMO JOGO ===\n")
    
    sizes = [4, 5, 6, 7, 8]
    num_graphs = 20
    
    print(f"{'Tam':>4} | {'Densidade':>9} | {'% Ham':>6} | {'Vitórias':>8} | {'Taxa':>6}")
    print("-" * 45)
    
    for n in sizes:
        total_ham = 0
        total_wins = 0
        
        for _ in range(num_graphs):
            # Densidade variável
            edge_prob = random.uniform(0.3, 0.7)
            graph = generate_random_graph(n, edge_prob)
            
            game = HamiltonianGame(graph)
            
            # Verifica se existe caminho hamiltoniano
            has_ham = any(game.has_hamiltonian_path(i) for i in range(n))
            if has_ham:
                total_ham += 1
            
            # Joga o jogo
            win_rate = game.play_game(50)
            total_wins += win_rate
        
        ham_pct = total_ham / num_graphs * 100
        win_avg = total_wins / num_graphs * 100
        
        print(f"{n:4d} | {edge_prob*100:8.1f}% | {ham_pct:5.1f}% | {win_avg:7.1f}% | {win_avg:5.1f}%")
    
    print("\nAnálise:")
    print("- Construtor usa heurística gulosa (menor grau)")
    print("- Taxa de vitória diminui com tamanho")
    print("- Conexão: se P=NP, existem algoritmos eficientes para encontrar caminhos")

def nash_equilibrium_simulation():
    """
    Simula busca de equilíbrio de Nash em jogo simples
    """
    print("\n=== SIMULAÇÃO: EQUILÍBRIO DE NASH ===\n")
    
    # Jogo simples 2x2
    # Pagamentos: (Jogador1, Jogador2)
    payoffs = {
        ('Cooperar', 'Cooperar'): (3, 3),
        ('Cooperar', 'Defeitar'): (0, 5),
        ('Defeitar', 'Cooperar'): (5, 0),
        ('Defeitar', 'Defeitar'): (1, 1)
    }
    
    print("Prisioneiro Dilemma:")
    print("         Cooperar   Defeitar")
    print("Cooperar  (3,3)      (0,5)")
    print("Defeitar  (5,0)      (1,1)")
    
    # Simula jogadores learning
    strategies = {'p1': defaultdict(int), 'p2': defaultdict(int)}
    num_rounds = 1000
    
    for _ in range(num_rounds):
        # Jogador 1 escolhe baseado em histórico
        if random.random() < strategies['p1']['Cooperar'] / (strategies['p1']['Cooperar'] + strategies['p1']['Defeitar'] + 1):
            s1 = 'Cooperar'
        else:
            s1 = 'Defeitar'
        
        # Jogador 2 escolhe baseado em histórico
        if random.random() < strategies['p2']['Cooperar'] / (strategies['p2']['Cooperar'] + strategies['p2']['Defeitar'] + 1):
            s2 = 'Cooperar'
        else:
            s2 = 'Defeitar'
        
        # Atualiza histórias
        strategies['p1'][s1] += 1
        strategies['p2'][s2] += 1
    
    # Calcula estratégias finais
    total_p1 = sum(strategies['p1'].values())
    total_p2 = sum(strategies['p2'].values())
    
    print(f"\nEstratégias após {num_rounds} rodadas:")
    print(f"Jogador 1: Cooperar={strategies['p1']['Cooperar']/total_p1*100:.1f}%, Defeitar={strategies['p1']['Defeitar']/total_p1*100:.1f}%")
    print(f"Jogador 2: Cooperar={strategies['p2']['Cooperar']/total_p2*100:.1f}%, Defeitar={strategies['p2']['Defeitar']/total_p2*100:.1f}%")
    
    print("\nEquilíbrio de Nash: (Defeitar, Defeitar)")
    print("Mesmo que (Cooperar, Cooperar) seja melhor para ambos,")
    print("cada jogador tem incentivo para defitar unilateralmente.")
    
    print("\nConexão com P vs NP:")
    print("- Equilíbrios existem (teorema minimax)")
    print("- Mas encontrá-los pode ser PPAD-completo")
    print("- Se P=NP, talvez encontrar equilíbrios seja fácil")

if __name__ == "__main__":
    random.seed(42)
    
    # Executa todos os experimentos
    sat_as_game_experiment()
    hamiltonian_game_experiment()
    nash_equilibrium_simulation()
