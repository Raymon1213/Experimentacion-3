# local_search.py
import random
import networkx as nx
from utils import path_weight, is_valid_simple_path

def reconnect_with_subgraph(G, prefix, suffix_start, end):
    forbidden = set(prefix)
    allowed = set(G.nodes()) - forbidden | {suffix_start}
    subG = G.subgraph(allowed).copy()

    for u, v, data in subG.edges(data=True):
        w = data.get('weight', 1)
        data['cost_inv'] = 1.0 / w if w > 0 else 1.0

    try:
        path = nx.shortest_path(subG, suffix_start, end, weight='cost_inv')
        return path
    except:
        return None


def eliminate_and_reinsert_move(G, path):
    if path is None or len(path) <= 3:
        return None, None

    idx = random.randint(1, len(path)-2)
    removed = path[idx]
    prefix = path[:idx]
    suffix_start = prefix[-1]

    new_suffix = reconnect_with_subgraph(G, prefix, suffix_start, path[-1])
    if new_suffix is None:
        return None, removed

    new_path = prefix + new_suffix[1:]
    if not is_valid_simple_path(G, new_path, start=path[0], end=path[-1]):
        return None, removed

    return new_path, removed


def local_search_elim_reinsert(G, init_path, max_no_improve=100):
    """
    Devuelve:
      best_path
      best_weight
      trace_steps = lista con movimientos registrados
    """
    if init_path is None:
        return None, float('-inf'), []

    best = init_path[:]
    best_w = path_weight(G, best)

    trace_steps = [] 
    no_improve = 0

    while no_improve < max_no_improve:
        cand, removed_node = eliminate_and_reinsert_move(G, best)

        if cand is None:
            trace_steps.append({
                "old_path": best,
                "new_path": best,
                "removed": removed_node,
                "delta": 0,
                "color": "gray",
                "msg": f"No se pudo reinsertar nodo {removed_node}"
            })
            no_improve += 1
            continue

        w = path_weight(G, cand)
        delta = w - best_w

        if w > best_w:
            trace_steps.append({
                "old_path": best,
                "new_path": cand,
                "removed": removed_node,
                "delta": delta,
                "color": "green",
                "msg": f"Mejora: +{delta:.2f} al eliminar {removed_node}"
            })
            best = cand
            best_w = w
            no_improve = 0
        else:
            trace_steps.append({
                "old_path": best,
                "new_path": cand,
                "removed": removed_node,
                "delta": delta,
                "color": "red",  # no se acepta, pero queda registrado
                "msg": f"No mejora (Δ={delta:.2f}). Eliminado {removed_node}"
            })
            no_improve += 1

    return best, best_w, trace_steps


def search_with_restarts(G, init_method, start, end, restarts=10, max_no_improve=100):

    best_overall = None
    best_w = float('-inf')
    best_trace = []

    for r in range(restarts):
        res = init_method(G, start, end)
        if res is None:
            continue

        init_path, init_w = res
        ls_path, ls_w, trace_steps = local_search_elim_reinsert(
            G, init_path, max_no_improve
        )

        if ls_w > best_w:
            best_w = ls_w
            best_overall = ls_path
            best_trace = trace_steps

    return best_overall, best_w, best_trace