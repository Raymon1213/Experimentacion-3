import math
import random
from local_search import path_cost

def simulated_annealing(G, path, T=100, alpha=0.98, iterations=200):
    current = path[:]
    current_cost = path_cost(G, current)
    best = current
    best_cost = current_cost

    for _ in range(iterations):
        # vecino = eliminación + reinserción
        neighbor = current[:]
        i = random.randint(1, len(neighbor)-2)
        removed = neighbor[i]
        neighbor = neighbor[:i] + neighbor[i+1:]

        # reinserción válida
        valid_positions = [j for j in range(1, len(neighbor))
                           if G.has_edge(neighbor[j-1], removed) and G.has_edge(removed, neighbor[j])]

        if not valid_positions:
            continue

        j = random.choice(valid_positions)
        neighbor = neighbor[:j] + [removed] + neighbor[j:]
        neighbor_cost = path_cost(G, neighbor)

        # aceptación
        if neighbor_cost > current_cost:
            current = neighbor
            current_cost = neighbor_cost
        else:
            p = math.exp((neighbor_cost - current_cost)/T)
            if random.random() < p:
                current = neighbor
                current_cost = neighbor_cost

        if current_cost > best_cost:
            best = current
            best_cost = current_cost

        T *= alpha

    return best
