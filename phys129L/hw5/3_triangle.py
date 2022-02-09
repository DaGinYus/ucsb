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


def draw_triangle(pvals, xcoord, ycoord, width, height, color):
    """Draws a filled in triangle in the following orientation:
    
          /|
         / |
        /  |
        ---

    Args:
        pvals: The pixel value array. The function sets values in the
            pixel value array to the color.
        xcoord: The x-coordinate offset for the bottom left point of 
            the triangle.
        ycoord: The y-coordinate offset.
        width: The width of the base of the triangle.
        height: The height of the triangle.
        color: The color in RGB format given as a tuple.
    """
    for x in range(width):
        y = height*x//width + ycoord
        pvals[x+xcoord, ycoord:y] = color


def main():
    """Draws a 3-4-5 right triangle by setting individual pixels.

    The image is recreated by drawing a blue triangle, then
    drawing a white triangle on top of it.
    """
    # define image parameters
    IMAGEX = 512 # width
    IMAGEY = 512 # height
    BGCOLOR = (255, 255, 255) # white
    FGCOLOR = (0, 0, 255) # color
    
    # pixel values: x, y, color (in RGB)
    pvals = np.full((IMAGEX, IMAGEY, 3), BGCOLOR, dtype="uint8")

    # parameters for the blue triangle
    fg_w = 400
    fg_h = fg_w*3//4
    fg_x = 51
    fg_y = 51
    # draw blue triangle
    draw_triangle(pvals, fg_x, fg_y, fg_w, fg_h, FGCOLOR)

    # parameters for the white triangle
    # scale it by 80%
    bg_w = int(0.8*fg_w)
    bg_h = int(0.8*fg_h)
    # offset it by 20 pixels compared to the other triangle
    # (as measured by bottom right corner)
    bg_x = fg_w - bg_w - 20 + fg_x
    bg_y = 20 + fg_y
    draw_triangle(pvals, bg_x, bg_y, bg_w, bg_h, BGCOLOR)
    
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
