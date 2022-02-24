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

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.plot(*np.flip(psd(sundata, npts, fs), axis=0), lw=0.5, label="Sun")
    ax.plot(*np.flip(psd(LEDdata, npts, fs), axis=0), lw=0.5, label="LED")
    annotations = {
        "1": (61.8, 6.8e-07),
        "2": (121, 0.002),
        "3": (155.5, 5.08e-05),
    }
    for label, loc in annotations.items():
        ax.annotate(label, loc)
    ax.set_yscale("log")
    ax.set_ylabel("Power")
    ax.set_xlabel("Frequency (10^14 Hz)")
    foottext = ("Since the data describes light, I've assumed that the "
                "frequency matches the same order of magnitude of light "
                "waves.\nThe numbers highlight several peaks in the graph. "
                "Note that there are far more distinct peaks in the LED "
                "graph,\nsince those are the spectral lines emitted by "
                "the LED, whereas the sun emits a more continuous spectrum.")
    fig.text(0.5, 0.07, foottext, ha="center", fontsize=8)
    ax.set_title("Power Spectrum of Two Signals")
    ax.legend()
    plt.savefig("spectrum.pdf", format="pdf")
    plt.show()

if __name__ == "__main__":
    main()
