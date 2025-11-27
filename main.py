# main.py
from experiment import run_batch_experiments, plot_boxplot, run_single_instance, show_example_paths, run_experiment, plot_comparison, run_experiments_only_heuristics, plot_only_heuristics

if __name__ == '__main__':
    # parámetros experimentales
    num_instances = 30
    n_nodes = 30
    density = 0.2
    restarts = 10
    results = run_batch_experiments(num_instances=num_instances, n=n_nodes, density=density, restarts=restarts, seed0=42)

    # plot comparativo (boxplot)
    plot_boxplot(results, title=f'Comparación Greedy vs LS (n={n_nodes}, instances={num_instances})')

    # mostrar ejemplo en detalle (una instancia) para la presentación
    example = run_single_instance(n=n_nodes, density=density, start=0, end=n_nodes-1, seed=123, restarts=restarts)
    show_example_paths(example)

    comp_results = run_experiment(reps=30,n_nodes=40)
    plot_comparison(comp_results)
    heuristic_results = run_experiments_only_heuristics(reps=30, n_nodes=40)
    plot_only_heuristics(heuristic_results)