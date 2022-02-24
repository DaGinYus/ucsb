"""
TKC!
Fourier Analysis
Matthew Wong
Phys 129L Hw7 Pb3
2022-02-24
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import psd


def main():
    """Plotting data in the frequency domain.
    
    matplotlib.mlab.psd returns an array [Pxx, freqs] where Pxx is the
    power spectrum, and freqs is the frequency domain.

    Units aren't given in the data, but if the data is meant to describe
    light, then we expect frequencies on the order of 10^14 Hz
    """
    sundata = np.loadtxt("sunlight.txt", dtype=float)[:,1]
    LEDdata = np.loadtxt("LEDlight.txt", dtype=float)[:,1]
    FTIME = 2 # units aren't given
    npts = len(sundata)
    fs = npts/FTIME # samples per second

    plt.plot(*np.flip(psd(sundata, npts, fs), axis=0), lw=0.5, label="Sunlight")
    plt.plot(*np.flip(psd(LEDdata, npts, fs), axis=0), lw=0.5, label="LED")
    annotations = {
        "1": (2.5, 10.7),
        "2": (61.8, 6.8e-07),
        "3": (121, 0.002),
    }
    for label, loc in annotations.items():
        plt.annotate(label, loc)
    plt.yscale("log")
    plt.ylabel("Power")
    plt.xlabel("Frequency (10^14 Hz)")
    plt.title("Power Spectrum of Two Signals")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
