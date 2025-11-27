# greedy.py
import random
import networkx as nx
from utils import path_weight, is_valid_simple_path

def greedy_max_edge_no_cycle(G, start, end):
    """Greedy 1: desde `start` elige la arista de mayor peso que no forme ciclo
       y que permita (con nodos no visitados) llegar a `end`."""
    cur = start
    visited = {cur}
    path = [cur]
    n = G.number_of_nodes()

    while cur != end:
        candidates = []
        for nbr in G.neighbors(cur):
            if nbr in visited:
                continue
            # comprobar que desde nbr aún existe camino a end sin usar visited
            allowed_nodes = set(G.nodes()) - visited | {nbr}
            subG = G.subgraph(allowed_nodes)
            if nx.has_path(subG, nbr, end):
                candidates.append((G[cur][nbr]['weight'], nbr))
        if not candidates:
            # no hay candidatos válidos: no se puede llegar a end desde aquí sin repetir
            return None
        # escoger el vecino con mayor peso (rompe empates aleatoriamente)
        candidates.sort(key=lambda x: (x[0], random.random()), reverse=True)
        nxt = candidates[0][1]
        path.append(nxt)
        visited.add(nxt)
        cur = nxt

    if is_valid_simple_path(G, path, start=start, end=end):
        return path, path_weight(G, path)
    return None

def greedy_max_reachable(G, start, end):
    """Greedy 2: escoger expansión que maximice número de vértices alcanzables (sin visitar),
       manteniendo posibilidad de llegar a `end`."""
    cur = start
    visited = {cur}
    path = [cur]

    while cur != end:
        cands = []
        for nbr in G.neighbors(cur):
            if nbr in visited:
                continue
            # contar cantidad de nodos alcanzables desde nbr sin usar visited
            allowed_nodes = set(G.nodes()) - visited | {nbr}
            subG = G.subgraph(allowed_nodes)
            try:
                comp = nx.node_connected_component(subG, nbr)
                score = len(comp)
            except Exception:
                score = 0
            # solo si end es alcanzable desde nbr
            if end in comp:
                cands.append((score, nbr))
        if not cands:
            return None
        # escoger el candidato que maximiza score (tie-breaker aleatorio)
        cands.sort(key=lambda x: (x[0], random.random()), reverse=True)
        nxt = cands[0][1]
        path.append(nxt)
        visited.add(nxt)
        cur = nxt

    if is_valid_simple_path(G, path, start=start, end=end):
        return path, path_weight(G, path)
    return None
