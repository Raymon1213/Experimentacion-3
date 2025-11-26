import random

def greedy_1(G):
    """Greedy 1: siempre toma el vecino con mayor peso."""
    node = random.choice(list(G.nodes()))
    path = [node]
    visited = set(path)

    while True:
        neighbors = [(v, G[node][v]['weight']) for v in G.neighbors(node) if v not in visited]
        if not neighbors:
            break
        node = max(neighbors, key=lambda x: x[1])[0]
        visited.add(node)
        path.append(node)

    return path


def greedy_2(G):
    """Greedy 2: siempre toma el vecino con mejor ratio (peso/grado)."""
    node = random.choice(list(G.nodes()))
    path = [node]
    visited = set(path)

    while True:
        neighbors = []
        for v in G.neighbors(node):
            if v not in visited:
                weight = G[node][v]['weight']
                ratio = weight / (1 + G.degree[v])
                neighbors.append((v, ratio))

        if not neighbors:
            break

        node = max(neighbors, key=lambda x: x[1])[0]
        visited.add(node)
        path.append(node)

    return path
