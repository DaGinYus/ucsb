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
        self.calc_lengths()
        self.calc_slopes()
        self.validate()
        self.centroid = np.sum(self.points, axis=0)/3

    def validate(self):
        """Checks if the triangle is valid."""
        self.valid = 2*max(self.lengths) < sum(self.lengths)

    def calc_lengths(self):
        """Calculates the side lengths of a triangle.
        
        Appends to the list the distance between the current point
        and the next point in the list (mod 3)
        """
        self.lengths = []
        for i, point in enumerate(self.points):
            next_index = (i+1)%len(self.points)
            self.lengths.append(np.sqrt(
                (point[0]-self.points[next_index,0])**2 +
                (point[1]-self.points[next_index,1])**2))

    def calc_slopes(self):
        """Calculates the slopes."""
        np.seterr(divide="ignore") # handle the division by zero separately
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
        # check for vertical lines
        if self.a[0] == self.b[0]:
            return (((y-self.a[1])/(x-self.a[0]) >= self.mca) &
                    ((y-self.c[1])/(x-self.c[0]) >= self.mbc))
        elif self.b[0] == self.c[0]:
            return (((y-self.a[1])/(x-self.a[0]) >= self.mca) &
                    ((y-self.a[1])/(x-self.a[0]) <= self.mab))
        else:
            return (((y-self.a[1])/(x-self.a[0]) >= self.mca) &
                    ((y-self.a[1])/(x-self.a[0]) <= self.mab) &
                    ((y-self.c[1])/(x-self.c[0]) >= self.mbc))
        
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


def input_coords(msg_string, imgsize):
    """Validates and parses coordinates.

    Args:
        msg_string: The string to ask the user something.
        imgsize (int, int): The maximum dimensions of the image.

    Returns:
        coords: A tuple of coordinates.
    """
    usrinput = input(msg_string)
    try:
        x, y = usrinput.split(',')
        x = int(x)
        y = int(y)
        if (0 <= x <= imgsize[0]) and (0 <= y <= imgsize[1]):
            return (x, y)
        else:
            print("Image coordinates do not fit the image size!")
            return input_coords(msg_string, imgsize)
    except ValueError as e:
        print(f"{e}, please try again")
        return input_coords(msg_string, imgsize)

def input_rgb():
    """Validates and parses RGB value.

    Returns:
        color: A tuple of RGB values
    """
    usrinput = input("Enter RGB value (default (0,0,255)): ")
    
    try:
        if not usrinput:
            r = 0
            g = 0
            b = 255
        else:
            r, g, b = usrinput.split(',')
            r = int(r)
            g = int(g)
            b = int(b)
            
        if (0 <= r <= 255) & (0 <= g <= 255) & (0 <= b <= 255):
            return (r, g, b)
        else:
            print("Invalid RGB value")
            return input_rgb
    except ValueError as e:
        print(f"{e}, please try again")
        return input_rgb

def params_from_input(bounds):
    """Asks the user to determine the triangle parameters.
    
    Args:
        bounds: A tuple of the max image dimensions.

    Returns:
        options: A tuple of options in the following format:
            ([(ax,ay), (bx,by), (cx,cy)], color)
    """
    print("Enter comma-separated coordinates for: ")
    a = input_coords("a: ", bounds)
    b = input_coords("b: ", bounds)
    c = input_coords("c: ", bounds)
    color = input_rgb()
    return ((a, b, c), color)
    
def main():
    """Allows the user to specify a triangle to draw.

    Line thickness is created by drawing a copy of the background
    on top of a filled triangle. At the expense of speed, we get
    a programmatically simpler solution with uniform line thickness
    on all three sides (and nice looking corners).
    """
    # define image parameters
    IMAGEX = 512 # width
    IMAGEY = 512 # height
    SCALEFACTOR = 0.8 # scale factor for filling
    BGCOLOR = (255,255,255) # white
    
    # pixel values: x, y, color (in RGB)
    pvals = np.full((IMAGEX, IMAGEY, 3), BGCOLOR, dtype="uint8")

    # draw blue triangle
    params = params_from_input((IMAGEX, IMAGEY))
    triangle = Triangle(*params[0])
    if not triangle.valid:
        print("The points entered don't constitute a triangle. Exiting!")
        return
    triangle.draw(pvals, params[1])

    # scale the triangle around a
    # basically shorten sides ab and ca, recalculate the endpoints,
    # then translate the triangle so the centroid is the same    
    scaled = (triangle.points
              + (triangle.centroid - triangle.points)*(1-SCALEFACTOR))
    scaled = np.rint(scaled).astype(int)
    fill = Triangle(*scaled)
    fill.draw(pvals, BGCOLOR)
    
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
