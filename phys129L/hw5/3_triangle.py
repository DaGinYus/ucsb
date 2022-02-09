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


def validate_points(a, b, c):
    """Checks the validity of points using the triangle inequality.

    Args:
        a [int]: A coordinate in (x, y) format.
        b [int]: Another coordinate in (x, y) format.
        c [int]: The final coordinate.
    
    Returns:
        valid: A boolean value for whether or not it's valid.
    """
    # calculate the side lengths using Euclidian distance
    ax, ay = a
    bx, by = b
    cx, cy = c
    ab = np.sqrt((ax-bx)**2 + (ay-by)**2)
    bc = np.sqrt((bx-cx)**2 + (by-cy)**2)
    ca = np.sqrt((cx-ax)**2 + (cy-ay)**2)
    if 2*max(ab, bc, ca) < ab + bc + ca:
        return True
    return False

def draw_triangle(pvals, a, b, c, color, linew=10):
    """Draws a triangle, e.g.

           a
          /|
         / |
        /  |
       b---c

    This is done by starting at the leftmost coordinate and defining
    three equations. The triangle is filled in by setting pixel values
    that fall in the range defined by the three equations.

    Line thickness is done by creating a truth-value array that is
    filled in with the shape of the triangle, then overwriting an
    'inner triangle' with false values, indicating that the background
    should be left untouched there. Then the function overwrites pvals
    wherever the array is true. This means the function can handle
    a background that is nonuniform in color.

    The inner triangle is created by scaling the triangle by a certain
    ratio, keeping the centroids the same.

    Args:
        pvals: The pixel value array. The function sets values in the
            pixel value array to the color.
        a [int]: A coordinate in (x, y) for a vertex of the triangle
        b [int]: Another coordinate
        c [int]: A final coordinate
        color [int]: The color in RGB format.
        linew (int): The width of the line.
    """
    points = np.array([a,b,c])
    centroid = (np.sum(points[:0])//3, np.sum(points[:1]//3))

    # sort points from leftmost to rightmost x-coordinate
    p = points[np.argsort(points[:,0])]
    leftx, midx, rightx = p[:,0]

    # slopes
    m1, m2 = [(p[i,1]-p[0,1])/(p[i,0]-p[0,0]) for i in [1,2]]
    m = sorted([m1, m2], key=abs)
    # the third slope is the steeper one calculated from the rightmost point
    m3, m4 = [(p[i,1]-p[2,1])/(p[i,0]-p[2,0]) for i in [0,1]]
    m.append(max([m3, m4], key=abs))
    print(m)
    for x in range(rightx-leftx):
        # plot in 2 sections, the left and right sides based on the midpoint
        # (this is because the system of equations changes)
        # the steeper slope corresponds to the shorter triangle leg
        # the longer leg is plotted in one piece
        y1 = int(round(m[0]*(x-p[0,0]))) + p[0,1]
        if x < midx-leftx:
            y2 = int(round(m[1]*(x-p[0,0]))) + p[0,1]
        elif x >= midx:
            y2 = int(round(m[2]*(x-p[1,0]))) + p[1,1]
        y = np.sort([y1, y2])
        pvals[x+leftx, y[0]:y[1]] = color


def main():
    """Allows the user to specify a triangle to draw.

    Line thickness is created by blitting a copy of the background
    on top of a filled triangle. At the expense of speed, we get
    a programmatically simpler solution with uniform line thickness
    on all three sides (and nice looking corners).
    """
    # define image parameters
    IMAGEX = 512 # width
    IMAGEY = 512 # height
    BGCOLOR = (255,255,255) # white
    FGCOLOR = (0,0,255) # color
    
    # pixel values: x, y, color (in RGB)
    pvals = np.full((IMAGEX, IMAGEY, 3), BGCOLOR, dtype="uint8")

    # draw blue triangle
    draw_triangle(pvals, (0,0), (400,300), (500,200), FGCOLOR)

    # flip the image to conform to conventional image coordinates
    plotarr = np.flipud(pvals.transpose(1, 0, 2))
    
    plt.imshow(plotarr, interpolation="none")
    plt.axis("off")
    plt.show()

    # save image to TIFF img.tif
    im = Image.fromarray(plotarr, "RGB")
    im.save("img.tif")


if __name__ == "__main__":
    main()
