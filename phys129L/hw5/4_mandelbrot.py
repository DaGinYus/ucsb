"""
TKC!
Mandelbrot Set
Matthew Wong
Phys 129L Hw5 Pb4
2022-02-10
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def mandelbrot(c):
    """Checks if c is in the Mandelbrot Set."""
    z = 0
    for i in range(250):
        z = z**2 + c
        if abs(z) > 2:
            return i
    return -1

def main():
    """Plots the Mandelbrot Set."""
    IMAGEW = 512
    IMAGEH = 384
    
    pvals = np.zeros((IMAGEW, IMAGEH))
    for j in range(IMAGEH):
        for i in range(IMAGEW):
            c = complex((i-IMAGEW//2-50)/150, (j-IMAGEH//2)/150)
            pvals[i,j] = mandelbrot(c)

    plt.imshow(pvals.T, interpolation="none", cmap="gist_earth")
    plt.show()

    # save image to TIFF mandelbrot.tif
    im = Image.fromarray(pvals, "RGB")
    im.save("mandelbrot.tif")


if __name__ == "__main__":
    main()
