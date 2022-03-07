"""
TKC!
Counting Simulation
Matthew Wong
Phys 129L Hw9 Pb3
2022-03-10
"""


import time
import random
import numpy as np
import matplotlib.pyplot as plt


def photon_count():
    """Simulates photon counting for 1000 one-millisecond intervals.

    The chance is specified to be 0.0045.

    Returns:
        count: The number of `detections`
    """
    count = 0
    for _ in range(1000):
        if random.random() < 0.0045:
            count += 1
    return count


def poisson(n, var):
    """The Poisson distribution.

    Args:
        n: The number of occurences.
        var: The expectation value, or the variance

    Returns:
        poisson: The value of the Poisson distribution evaluated at n.
    """
    return var**n * np.exp(-var) / np.math.factorial(n)


def main():
    """Simulates photon counting."""
    data = []
    for _ in range(1000):
        data.append(photon_count())

    x = range(int(min(data)), int(max(data)))
    var = np.std(data)**2
    pdist = [poisson(i, var) for i in x]
    plt.hist(data, density=True, label="Photon Counts")
    plt.plot(x, pdist, label="Poisson Distribution")
    plt.title("Photon Counting Simulation")
    plt.xlabel("Number of Photons Counted")
    plt.ylabel("Probability Density")
    plt.savefig("photon.pdf", format="pdf")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
