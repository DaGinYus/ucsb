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
    # define image parameters
    X = 512 # width
    Y = 512 # height
    BG = (255, 255, 255) # white
    FG = (0, 0, 255) # color
    LW = 15 # line weight
    
    # pixel values: x, y, color (in RGB)
    pvals = np.full((X, Y, 3), BG, dtype="uint8")
    print(np.shape(pvals))

    # divide up the triangle into 3 lines:
    # the adjacent (base), opposite (leg), and hypotenuse
    # the hypotenuse is given by the equation y = (adj/opp)*x
    width = 400
    height = width*3//4
    # offset is defined to be from the bottom left corner
    offset_x = 51
    offset_y = 51
    edge_r = offset_x + width
    # set the base
    pvals[offset_x:edge_r, offset_y:LW+offset_y] = FG
    # set leg (subtract LW since we are filling inside)
    pvals[edge_r-LW:edge_r, offset_y:offset_y+height+LW//2] = FG
    # set hypotenuse
    xvals = np.arange(offset_x, edge_r)
    yvals = height*xvals//width + LW
    for i in range(LW):
        pvals[xvals, yvals+i] = FG
    # flip the image to conform to conventional image coordinates
    plotarr = np.flipud(pvals.transpose(1, 0, 2))
    
    plt.imshow(plotarr, interpolation="none")
    plt.show()
    

if __name__ == "__main__":
    main()
