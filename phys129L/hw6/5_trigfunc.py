"""
TKC!
Plot Trig Functions
Matthew Wong
Phys 129L Hw6 Pb5
2022-02-17
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    """Plots the sine and tangent functions."""
    # one period is 2pi so 2.5 periods is 5pi
    x = np.linspace(0, 5*np.pi, 100)

    plt.plot(x, np.sin(x), label=r"sin($\theta$)")
    plt.plot(x, np.tan(x), label=r"tan($\theta$)")
    plt.ylim(-5, 5) # since tan() blows up
    plt.xlabel(r"$\theta$ [rad]")
    plt.ylabel("Function Value in Units")
    plt.title("Sine and Tangent Functions")
    plt.legend()
    plt.savefig("trigfunc.pdf", format="pdf")
    plt.show()

    
if __name__ == "__main__":
    main()
