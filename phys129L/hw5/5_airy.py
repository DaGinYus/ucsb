"""
TKC!
3D Plots
Matthew Wong
Phys 129L Hw5 Pb5
2022-02-10
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from PIL import Image

def I(x, y):
    """The intensity of the pattern as a function of x and y.

    This is (2*J1(r)/r)^2 where J1 is the first Bessel function.

    Args:
        r (float): The distance from the center.
    
    Returns:
        intensity: The intensity of light (normalized to 1 at r=0)
    """
    numterms = 100 # number of terms to sum in the Bessel function
    r = np.sqrt(x**2 + y**2)
    jterms = [(-1)**m/math.factorial(m)/math.gamma(m+2) * (r/2)**(2*m+1)
              for m in range(numterms)]
    J1 = np.sum(jterms, axis=0)
    return (2*J1/r)**2


def main():
    """Plots a 3D surface plot Airy pattern."""
    N = 100 # subdivisions
    MIN = 0
    MAX = 1
    PLOTDIST = 10 # max x, y values
    
    x, y = np.full((2, N), np.linspace(-PLOTDIST, PLOTDIST, N))
    X, Y = np.meshgrid(x, y)
    Z = I(X, Y)

    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap="viridis", edgecolor="none",
                    norm=colors.LogNorm(vmin=1e-08, vmax=1))
    ax.set_title("Airy Disk with Logarithmic Colormap")
    ax.set_zlabel("Normalized Intensity")
    ax.set_ylabel("Distance [arcseconds]")
    ax.set_xlabel("Distance [arcseconds]")
    
    plt.show()
    plt.savefig("airy.pdf", format="pdf")


if __name__ == "__main__":
    main()
