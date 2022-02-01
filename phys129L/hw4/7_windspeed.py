"""
TKC!
Wind Speed
Matthew Wong
Phys 129L Hw4 Pb7
2022-02-03
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    """Plots average wind speed with errorbars."""

    data = np.loadtxt("wind.dat")
    t = data[:,0]
    windspeed = data[:,1]
    error = data[:,2]
    
    fig, ax = plt.subplots()
    ax.errorbar(t, windspeed, error, marker='.', ls='', capsize=4)
    ax.set_title("Average Wind Speed")
    ax.minorticks_on()
    ax.set_xlim([-1, 24])
    ax.set_xticks(np.arange(0, 25, 4))
    ax.set_ylim([0, 12])
    ax.set_xlabel("Time [h]")
    ax.set_ylabel("Wind Speed [kt]")
    fig.savefig("plot.pdf")

if __name__ == "__main__":
    main()
