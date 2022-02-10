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


class Triangle:
    def __init__(self, a, b, c):
        """Initializes based on vertex coordinates (sorted by x value).
        
        Args:
            a (int, int): A coordinate in (x,y) format.
            b (int, int): The second coordinate in (x,y) format.
            c (int, int): The third coordinate in (x,y) format.
        """
        points = np.array([a, b, c])
        self.points = points[np.argsort(points[:,0])]
        self.a, self.b, self.c = self.points
        self.set_lengths()
        self.set_slopes()

    def set_lengths(self):
        """Calculates the side lengths of a triangle.
        
        Appends to the list the distance between the current point
        and the next point in the list (mod 3)
        """
        lengths = []
        for i, point in enumerate(self.points):
            next_index = (i+1)%len(self.points)
            lengths.append(np.sqrt(
                (point[0]-self.points[next_index,0])**2 +
                (point[1]-self.points[next_index,1])**2))
        self.ab, self.bc, self.ca = lengths

    def set_slopes(self):
        """Calculates the slopes."""
        self.mab = (self.a[1]-self.b[1])/(self.a[0]-self.b[0])
        self.mbc = (self.b[1]-self.c[1])/(self.b[0]-self.c[0])
        self.mca = (self.c[1]-self.a[1])/(self.c[0]-self.a[0])

    def inside(self, x, y):
        """Checks if the point satisfies the three inequalities.

        For example, (y-Ay)/(x-Ax) > mAC
        (given points a, b, c defined in clockwise fashion)

        Args:
            x (int): the x-coordinate
            y (int): the y-coordinate

        Returns:
            True if the point is inside the triangle, False if not.
        """
        if (((y-self.a[1])/(x-self.a[0]) >= self.mca) & 
            ((y-self.a[1])/(x-self.a[0]) <= self.mab)):
            if self.mbc > 0:
                return ((y-self.c[1])/(x-self.c[0]) >= self.mbc)
            elif self.mbc < 0:
                return ((y-self.c[1])/(x-self.c[0]) <= self.mbc)
        return False
        
        
    def draw(self, pvals, color):
        """Draws a filled in triangle based on the endpoints.

        Args:
            pvals: A 3D array corresponding to X,Y pixel values,
                with the 3rd dimension being color.
            color: A tuple describing the color in RGB format.
        """
        # x values already sorted
        ymin = np.min(self.points, axis=0)[1]
        ymax = np.max(self.points, axis=0)[1]
        for i in range(self.a[0]+1, self.c[0]):
            for j in range(ymin, ymax):
                if self.inside(i, j):
                    pvals[i,j] = color
            

def draw_triangle(pvals, a, b, c, color):
    """Draws a filled triangle, e.g.

           a
          /|
         / |
        /  |
       b---c

    This is done by starting at the leftmost coordinate and defining
    three equations. The triangle is filled in by setting pixel values
    that fall in the range defined by the three equations.

    Args:
        pvals: The pixel value array. The function sets values in the
            pixel value array to the color.
        a [int]: A coordinate in (x, y) for a vertex of the triangle
        b [int]: Another coordinate
        c [int]: A final coordinate
        color [int]: The color in RGB format.
    """
    points = np.array([a,b,c])

    # sort points from leftmost to rightmost x-coordinate
    p = points[np.argsort(points[:,0])]
    leftx, midx, rightx = p[:,0]

    # slopes
    m1, m2 = [(p[i,1]-p[0,1])/(p[i,0]-p[0,0]) for i in [1,2]]
    m = sorted([m1, m2], key=abs)
    # the third slope is the steeper one calculated from the rightmost point
    m3, m4 = [(p[i,1]-p[2,1])/(p[i,0]-p[2,0]) for i in [0,1]]
    m.append(max([m3, m4], key=abs))
    for x in range(rightx-leftx):
        # plot in 2 sections, the left and right sides based on the midpoint
        # (this is because the system of equations changes)
        # the steeper slope corresponds to the shorter triangle leg
        # the longer leg is plotted in one piece
        y1 = round(m[0]*(x-p[0,0])) + p[0,1]
        if x < midx-leftx:
            y2 = round(m[1]*(x-p[0,0])) + p[0,1]
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
    triangle = Triangle((0,0), (400,300), (500,200))
    #draw_triangle(pvals, (0,0), (400,300), (500,200), FGCOLOR)
    triangle.draw(pvals, FGCOLOR)

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
