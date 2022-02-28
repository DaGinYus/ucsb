"""
TKC!
Monte Carlo Circle
Matthew Wong
Phys 129L Hw8 Pb1
2022-03-03
"""


import montecarlo
import numpy as np
import matplotlib.pyplot as plt


def main():
    """Plots the variance in Monte Carlo integration."""
    N = np.arange(20, 2000)
    var = np.array([montecarlo.integrate(n) for n in N])[:,1]
    plt.plot(var, label="Variance")
    plt.plot(0.1/N, label="0.1/N")
    plt.yscale("log")
    plt.legend()
    plt.title("Variance in Monte Carlo Integration")
    plt.xlabel("Number of Samples (N)")
    plt.ylabel("Variance")
    plt.savefig("montecarlo.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    main()
