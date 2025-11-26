import networkx as nx
import random
from algorithms import greedy_1, greedy_2
from local_search import local_search_elim_reinsert, path_cost
from simulated_annealing import simulated_annealing

def create_large_graph(n=80, density=0.15):
    G = nx.gnp_random_graph(n, density)
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(1, 20)
    return G


def run_experiment(reps=20):
    results = {
        "G1_LS": [],
        "G2_LS": [],
        "G1_SA": [],
        "G2_SA": [],
    }

    for _ in range(reps):
        G = create_large_graph()

        g1 = greedy_1(G)
        g2 = greedy_2(G)

        # local search
        res1 = local_search_elim_reinsert(G, g1)
        res2 = local_search_elim_reinsert(G, g2)

        # simulated annealing
        sa1 = simulated_annealing(G, g1)
        sa2 = simulated_annealing(G, g2)

        results["G1_LS"].append(path_cost(G, res1))
        results["G2_LS"].append(path_cost(G, res2))
        results["G1_SA"].append(path_cost(G, sa1))
        results["G2_SA"].append(path_cost(G, sa2))

    return results
