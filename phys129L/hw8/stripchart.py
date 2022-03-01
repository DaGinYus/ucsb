#!/usr/bin/env python3
#
# stripchart.py
#
# 28Feb22  Implementation of threading
# 15Feb22  Modification by Matthew Wong for homework purposes
# 11May16  Many improvements by Ben LaRoque
# 10May16  Adapted from 
#             http://matplotlib.org/examples/animation/strip_chart_demo.html
#          by Everett Lipman
#
"""
Emulate an oscilloscope.  Requires the animation API introduced in
matplotlib 1.0 SVN.
"""


import time
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D


user_val = 0


def set_user_val():
    """Sets the global variable."""
    while True:
        usrinput = input("Enter a value: ")
        try:
            global user_val
            user_val = float(usrinput)
        except ValueError:
            print("Invalid input, please try again")


class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = np.array([])
        self.ydata = np.array([])
        self.ymin = -10
        self.ymax = 10
        self.t0 = time.perf_counter()
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_xlim(0, self.maxt)

    def update(self, data):
        t,y = data
        # update scaling to fit larger numbers as they are inputted
        if y <= self.ymin:
            self.ymin = 1.1*y
        if y >= self.ymax:
            self.ymax = 1.1*y
        self.tdata = np.append(self.tdata, t)
        self.ydata = np.append(self.ydata, y)
        self.ydata = self.ydata[self.tdata > (t-self.maxt)]
        self.tdata = self.tdata[self.tdata > (t-self.maxt)]
        self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.legend([self.line], [f"Current Value: {y}"])
        self.ax.figure.canvas.draw()
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

    def emitter(self, p=0.1):
        while True:
            t = time.perf_counter() - self.t0
            yield t, user_val


if __name__ == '__main__':
    inputthread = threading.Thread(target=set_user_val)
    inputthread.start()
    dt = 0.01
    fig, ax = plt.subplots()
    scope = Scope(ax, maxt=10, dt=dt)
    ani = animation.FuncAnimation(fig, scope.update, scope.emitter, interval=dt*1000., blit=True)
    plt.show()
