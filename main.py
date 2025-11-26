from experiment import run_experiment
from plots import plot_results

if __name__ == "__main__":
    results = run_experiment(reps=30)
    print(results)
    plot_results(results)
