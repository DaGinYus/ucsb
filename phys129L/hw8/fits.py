"""
TKC!
Polynomial Fits
Matthew Wong
Phys 129L Hw8 Pb2
2022-03-03
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P


def input_npts():
    """Gets the number of points to use either from CLI or raw input.

    Returns:
        npts (int): The number of points.
    """
    if len(sys.argv) > 1:
        npts = sys.argv[1]
    else:
        npts = input("Enter the number of points (less than 10): ")
    try:
        npts = int(npts)
        if 200 <= npts <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
        return
    return npts


def main():
    """Fits functions using polynomials.

    numpy.polynomial.Polynomial.fit() is more numerically stable than
    numpy.polyfit().
    """
    npts = input_npts()
    if not npts:
        return
    rand_x = np.random.uniform(0., 1000., npts)
    rand_x = np.sort(rand_x)
    rand_y = np.random.uniform(0., 1000., npts)

    poly_deg = (1, npts-3, npts-1)
    plt.plot(rand_x, rand_y, label="Random Points")
    for poly_n in poly_deg:
        poly = P.fit(rand_x, rand_y, poly_n)
        plt.plot(*poly.linspace(1000), label=f"Fit deg. {poly_n}")
    plt.xlim([0,1000])
    plt.ylim([0,1000])
    plt.title("Curve Fitting")
    plt.legend()
    plt.savefig("fits.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    main()
