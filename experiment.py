# experiment.py
import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import gridspec
from utils import generate_connected_graph, path_weight
from greedy import greedy_max_edge_no_cycle, greedy_max_reachable
from local_search import search_with_restarts

def run_single_instance(n=30, density=0.2, start=0, end=None, seed=None, restarts=10):
    if end is None:
        end = n-1
    G = generate_connected_graph(n=n, density=density, seed=seed)
    # Greedy 1
    g1 = greedy_max_edge_no_cycle(G, start, end)
    if g1 is None:
        g1_path, g1_w = None, float('-inf')
    else:
        g1_path, g1_w = g1
    # Greedy 2
    g2 = greedy_max_reachable(G, start, end)
    if g2 is None:
        g2_path, g2_w = None, float('-inf')
    else:
        g2_path, g2_w = g2
    # Local search with restarts starting from Greedy1 (init method is greedy_max_edge_no_cycle)
    best1_path, best1_w, trace1 = search_with_restarts(G, greedy_max_edge_no_cycle, start, end, restarts=restarts)
    # Local search with restarts starting from Greedy2
    best2_path, best2_w, trace2 = search_with_restarts(G, greedy_max_reachable, start, end, restarts=restarts)

    return {
        'G': G,
        'g1_path': g1_path, 'g1_w': g1_w,
        'g2_path': g2_path, 'g2_w': g2_w,
        'g1_ls_path': best1_path, 'g1_ls_w': best1_w, 'trace1': trace1,
        'g2_ls_path': best2_path, 'g2_ls_w': best2_w, 'trace2': trace2
    }

def run_batch_experiments(num_instances=30, n=30, density=0.2, restarts=10, seed0=0):
    results = {'G1':[], 'G2':[], 'G1+LS':[], 'G2+LS':[]}
    random.seed(seed0)
    for i in range(num_instances):
        seed = None if seed0 is None else seed0 + i
        out = run_single_instance(n=n, density=density, start=0, end=n-1, seed=seed, restarts=restarts)
        results['G1'].append(out['g1_w'])
        results['G2'].append(out['g2_w'])
        results['G1+LS'].append(out['g1_ls_w'])
        results['G2+LS'].append(out['g2_ls_w'])
    return results

def plot_boxplot(results, title='Comparación de calidad (peso total del camino)'):
    labels = ['G1','G2','G1+LS','G2+LS']
    data = [results['G1'], results['G2'], results['G1+LS'], results['G2+LS']]
    plt.figure(figsize=(8,5))
    plt.boxplot(data, labels=labels, showmeans=True)
    plt.ylabel('Peso total (mayor mejor)')
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

def show_example_paths(out):

    G = out['G']

    pos = nx.spring_layout(G, seed=42, k=2.2, iterations=400)

    def edge_list(path):
        return list(zip(path, path[1:])) if path else []

    def draw_path(path, original_path, title):
        fig = plt.figure(figsize=(10, 7), dpi=140)
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

        ax_graph = plt.subplot(gs[0])
        ax_table = plt.subplot(gs[1])
        ax_table.axis('off')

        # ========== NODOS BASE (más pequeños) ==========
        nx.draw_networkx_nodes(
            G, pos, ax=ax_graph,
            node_size=480, node_color="white",
            edgecolors="black", linewidths=1.4
        )
        nx.draw_networkx_labels(
            G, pos, ax=ax_graph,
            font_size=10, font_weight="bold"
        )

        # ========== ARISTAS BASE ==========
        nx.draw_networkx_edges(
            G, pos, ax=ax_graph,
            width=1.2, edge_color="gray", alpha=0.4
        )

        # ========== PESOS BASE ==========
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax_graph,
            edge_labels=nx.get_edge_attributes(G, 'weight'),
            font_size=7,
            font_color="gray",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.5, pad=0.1)
        )

        # ========== DIFERENCIA ENTRE GREEDY Y LS ==========
        greedy_edges = set(edge_list(original_path)) if original_path else set()
        final_edges = set(edge_list(path)) if path else set()

        added_edges = final_edges - greedy_edges
        removed_edges = greedy_edges - final_edges

        # VERDE = agregado
        nx.draw_networkx_edges(
            G, pos, ax=ax_graph,
            edgelist=list(added_edges),
            width=3.5, edge_color="green"
        )

        # NARANJO = quitado
        nx.draw_networkx_edges(
            G, pos, ax=ax_graph,
            edgelist=list(removed_edges),
            width=3.5, edge_color="orange", style='dashed'
        )

        # ========== CAMINO FINAL (NODOS Y ARISTAS DESTACADAS) ==========
        if path:
            final_edges_list = list(zip(path, path[1:]))

            # nodos
            nx.draw_networkx_nodes(
                G, pos, ax=ax_graph,
                nodelist=path,
                node_size=600,
                node_color="#B3D9FF",
                edgecolors="black",
                linewidths=2
            )

            # aristas
            nx.draw_networkx_edges(
                G, pos, ax=ax_graph,
                edgelist=final_edges_list,
                width=5, edge_color="red"
            )

            # PESOS DEL CAMINO FINAL (claros y grandes)
            big_labels = {e: G[e[0]][e[1]]['weight'] for e in final_edges_list}
            nx.draw_networkx_edge_labels(
                G, pos, ax=ax_graph,
                edge_labels=big_labels,
                font_size=12,
                font_color="red",
                font_weight="bold",
                bbox=dict(
                    facecolor="white",
                    edgecolor="red",
                    boxstyle="round,pad=0.2"
                )
            )

        ax_graph.set_title(title, fontsize=14, fontweight="bold")
        ax_graph.axis("off")

        # ========== TABLA DE PESOS ==========
        if path:
            rows = []
            total = 0
            for u, v in zip(path, path[1:]):
                w = G[u][v]['weight']
                rows.append([f"{u} → {v}", w])
                total += w

            rows.append(["TOTAL", total])

            ax_table.table(
                cellText=rows,
                colLabels=["Arista", "Peso"],
                loc="center",
                cellLoc="center"
            )

        plt.tight_layout()
        plt.show()

    # Dibujos
    draw_path(out['g1_path'], None, f"Greedy 1  (peso={out['g1_w']})")
    draw_path(out['g2_path'], None, f"Greedy 2  (peso={out['g2_w']})")
    draw_path(out['g1_ls_path'], out['g1_path'], f"Greedy 1 + LS  (peso={out['g1_ls_w']})")
    draw_path(out['g2_ls_path'], out['g2_path'], f"Greedy 2 + LS  (peso={out['g2_ls_w']})")


def run_experiment(reps=30, n_nodes=40, density=0.2, restarts=50, seed0=0):

    random.seed(seed0)

    # Ahora cada método es una heurística distinta para el gráfico
    results = {
        "G1":     {"costs": []},
        "G1+LS":  {"costs": []},
        "G1+ILS": {"costs": []},
        "G2":     {"costs": []},
        "G2+LS":  {"costs": []},
        "G2+ILS": {"costs": []},
    }

    for i in range(reps):
        seed = seed0 + i

        out = run_single_instance(
            n=n_nodes,
            density=density,
            start=0,
            end=n_nodes - 1,
            seed=seed,
            restarts=restarts
        )

        # ---------------------------------------
        # Heurística 1
        # ---------------------------------------
        results["G1"]["costs"].append(out["g1_w"])
        results["G1+ILS"]["costs"].append(out["g1_ls_w"])

        sls1_path, sls1_w, _ = search_with_restarts(
            out['G'], greedy_max_edge_no_cycle, 0, n_nodes - 1, restarts=1
        )
        results["G1+LS"]["costs"].append(sls1_w)

        # ---------------------------------------
        # Heurística 2
        # ---------------------------------------
        results["G2"]["costs"].append(out["g2_w"])
        results["G2+ILS"]["costs"].append(out["g2_ls_w"])

        sls2_path, sls2_w, _ = search_with_restarts(
            out['G'], greedy_max_reachable, 0, n_nodes - 1, restarts=1
        )
        results["G2+LS"]["costs"].append(sls2_w)

    return results


def plot_comparison(results):

    heuristics = list(results.keys())

    means = [np.mean(results[h]["costs"]) for h in heuristics]
    stds  = [np.std(results[h]["costs"]) for h in heuristics]

    x = np.arange(len(heuristics))

    plt.figure(figsize=(14, 7))

    plt.bar(x, means, yerr=stds, capsize=7)

    plt.xticks(x, heuristics, rotation=25)
    plt.ylabel("Costo promedio", fontsize=14)
    plt.title("Comparación entre Greedy, LS y ILS", fontsize=16)

    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()



def plot_heuristics_only(results):
    import matplotlib.pyplot as plt

    # Detectar automáticamente las heurísticas
    heuristics = {}
    for key, val in results.items():
        if "heuristic" in key.lower() and "ls" not in key.lower():
            heuristics[key] = val["value"] if "value" in val else val["greedy"]

    if len(heuristics) == 0:
        raise ValueError("⚠️ No se detectaron heurísticas base (Greedy). Revisa las claves del diccionario.")

    # Construir el boxplot
    plt.figure(figsize=(8,5))
    plt.boxplot(heuristics.values(), labels=heuristics.keys())
    plt.title("Comparación Solo Heurísticas (sin LS)")
    plt.ylabel("Costo / Longitud del camino")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


def run_experiments_only_heuristics(reps=30, n_nodes=40, density=0.2, seed0=0):
    """
    Ejecuta solo Greedy 1 y Greedy 2 usando el mismo generador de grafos
    que usan los otros experimentos.
    """
    results = {
        "Greedy1": [],
        "Greedy2": []
    }

    for i in range(reps):
        seed = seed0 + i
        G = generate_connected_graph(n_nodes, density, 1, 10, seed)

        start, end = 0, n_nodes - 1

        # Greedy 1
        g1_path, g1_cost = greedy_max_edge_no_cycle(G, start, end)
        results["Greedy1"].append(g1_cost)

        # Greedy 2
        g2_path, g2_cost = greedy_max_reachable(G, start, end)
        results["Greedy2"].append(g2_cost)

    return results



def plot_only_heuristics(results):
    """
    Boxplot comparando solo heurísticas greedy 1 y greedy 2.
    Estilo similar al gráfico de ejemplo del enunciado.
    """

    import matplotlib.pyplot as plt

    labels = ["Greedy 1", "Greedy 2"]
    data = [
        results["Greedy1"],
        results["Greedy2"]
    ]

    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=labels, patch_artist=True)

    plt.title("Comparación entre Heurística 1 y Heurística 2")
    plt.ylabel("Costo (longitud del camino)")

    # Colores suaves estilo ejemplo
    colors = ["#82B1FF", "#FFCC80"]
    for patch, color in zip(plt.gca().artists, colors):
        patch.set_facecolor(color)

    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.show()




def show_local_search_progress(G, trace_steps):
    """
    Muestra todos los cambios aceptados durante la búsqueda local.
    Cada paso muestra:
    - camino anterior
    - camino nuevo
    - edges agregadas (verde)
    - edges eliminadas (naranjo)
    """

    def edges(path):
        return set(zip(path, path[1:]))

    pos = nx.spring_layout(G, seed=42)

    step = 1
    for old_path, new_path in trace_steps:

        old_edges = edges(old_path)
        new_edges = edges(new_path)

        added = list(new_edges - old_edges)
        removed = list(old_edges - new_edges)

        plt.figure(figsize=(10,7))
        nx.draw(G, pos, node_color="white", edge_color="lightgray", 
                with_labels=True, node_size=600)

        nx.draw_networkx_edges(G, pos, edgelist=added, width=4, edge_color="green")
        nx.draw_networkx_edges(G, pos, edgelist=removed, width=4, edge_color="orange", style="dashed")

        plt.title(f"Paso {step}: cambio en búsqueda local")
        plt.show()
        step += 1