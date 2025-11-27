# utils.py
import random
import networkx as nx

def generate_connected_graph(n=30, density=0.2, wmin=1, wmax=10, seed=None):
    """Genera un grafo no dirigido conexo con pesos enteros en [wmin,wmax]."""
    if seed is not None:
        random.seed(seed)
    while True:
        G = nx.gnp_random_graph(n, density, seed=seed)
        if nx.is_connected(G) and G.number_of_edges() > 0:
            break
        # si no es conexo, cambia seed aleatoriamente (para evitar bucle infinito con densidades muy bajas)
        if seed is None:
            seed = random.randint(0, 10**9)
        else:
            seed += 1

    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(wmin, wmax)
    return G

def path_weight(G, path):
    """Suma de pesos de aristas en un camino (lista de nodos)."""
    if path is None or len(path) < 2:
        return 0
    w = 0
    for u, v in zip(path, path[1:]):
        if not G.has_edge(u, v):
            # camino inválido
            return float('-inf')
        w += G[u][v]['weight']
    return w

def is_valid_simple_path(G, path, start=None, end=None):
    """Valida camino simple (no repeticiones), aristas existentes y endpoints si se dan."""
    if path is None: 
        return False
    if len(path) != len(set(path)):
        return False
    for u, v in zip(path, path[1:]):
        if not G.has_edge(u, v):
            return False
    if start is not None and path[0] != start:
        return False
    if end is not None and path[-1] != end:
        return False
    return True
