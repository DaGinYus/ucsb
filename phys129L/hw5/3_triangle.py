"""
TKC!
3-4-5 Right Triangle
Matthew Wong
Phys 129L Hw5 Pb3
2022-02-10
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def main():
    """Draws a 3-4-5 right triangle by setting individual pixels.

    The thick lines are created by filling in the inside of the boundary
    with a certain width. The image excluding the area inside the
    boundary is then filled in with white pixel values to form the
    background. This will cut off any overlap made by the width of the
    lines.
    """
    X = 512 # width
    Y = 512 # height
    C = (0, 0, 255) # color
    W = 1 # line weight
    
    # pixel values: x, y, color (in RGB)
    pvals = np.zeros((X, Y, 3), dtype="uint8")
    print(np.shape(pvals))

    # divide up the triangle into 3 lines:
    # the adjacent (base), opposite (height), and hypotenuse
    # the hypotenuse is given by the equation y = (adj/opp)*x
    width = 512
    height = width*3//4
    pvals[:width, 0:20] = C

    # flip the image to conform to conventional image coordinates
    plotarr = np.flipud(pvals.transpose(1, 0, 2))
    
    plt.imshow(plotarr, interpolation="none")
    plt.show()
    

if __name__ == "__main__":
    main()
