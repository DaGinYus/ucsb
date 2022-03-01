"""
TKC!
Coin Toss Simulation
Matthew Wong
Phys 129L Hw8 Pb5
2022-03-03
"""


import random
import numpy as np
import matplotlib.pyplot as plt


def cointoss():
    """Tosses a 'coin' 100 times, counting the number of heads.

    Returns:
        heads (int): A count of the number of heads.
    """
    tosses = random.choices(["heads", "tails"], k=100)
    return tosses.count("heads")


def gaussian(x, stdev, mean):
    """The Gaussian distribution of a dataset.
    
    Args:
        x: The variable.
        stdev: The standard deviation of the distribution.
        mean: The mean of the distribution.

    Returns:
        gaussian: The Gaussian distribution.
    """
    frac = 1/stdev/np.sqrt(2*np.pi)
    exponent = -0.5*((x - mean)/stdev)**2
    return frac * np.exp(exponent)


def main():
    """Simulates coin tossing."""
    outcomes = []
    for _ in range(1000):
        outcomes.append(cointoss())
    stdev = np.std(outcomes)
    mean = np.mean(outcomes)
    x = np.linspace(min(outcomes), max(outcomes), 1000)
    print(f"Stdev.: {stdev}\n"
          f"Mean: {mean}")
    plt.hist(outcomes, density=True, label="Binomial dist.")
    plt.plot(x, gaussian(x, stdev, mean), label="Gaussian dist.")
    plt.title("Coin Toss Simulation")
    plt.xlabel("Number of Heads")
    plt.ylabel("Probability Density (Normalized)")
    plt.legend()
    plt.savefig("coinchart.pdf", format="pdf")
    plt.show()

if __name__ == "__main__":
    main()
