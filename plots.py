import matplotlib.pyplot as plt

def plot_results(results):
    data = [
        results["G1_LS"],
        results["G2_LS"],
        results["G1_SA"],
        results["G2_SA"]
    ]

    plt.boxplot(data, tick_labels=['G1+LS', 'G2+LS', 'G1+SA', 'G2+SA'])
    plt.title("Comparación de Resultados")
    plt.ylabel("Costo del Camino")
    plt.grid(True)
    plt.show()
