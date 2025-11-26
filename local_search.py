import random

def path_cost(G, path):
    return sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))


def local_search_elim_reinsert(G, path):
    best_path = path[:]
    best_cost = path_cost(G, best_path)

    for _ in range(50): 
        if len(best_path) < 3:
            return best_path

        # eliminar un nodo aleatorio del medio
        i = random.randint(1, len(best_path)-2)
        removed = best_path[i]
        new_path = best_path[:i] + best_path[i+1:]

        # buscar reinserción válida
        candidates = []
        for j in range(1, len(new_path)):
            if G.has_edge(new_path[j-1], removed) and G.has_edge(removed, new_path[j]):
                temp = new_path[:j] + [removed] + new_path[j:]
                candidates.append(temp)

        if not candidates:
            continue

        new = random.choice(candidates)
        new_cost = path_cost(G, new)

        if new_cost > best_cost:
            best_cost = new_cost
            best_path = new

    return best_path
