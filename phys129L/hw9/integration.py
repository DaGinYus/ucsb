"""
TKC!
Numerical Integration
Matthew Wong
Phys 129L Hw9 Pb4
2022-03-10
"""


import numpy as np
import matplotlib.pyplot as plt


def f(x):
    """The function to integrate over, given in homework problem."""
    return np.exp(-1*x**2)


def riemann_integrate(func, start, end, nints):
    """Performs integration by left-sided Riemann approximation.

    Args:
        func: The function to integrate over.
        start (float): The left end of the bounds.
        end (float): The right end of the bounds.
        nints (int): The number of subdivisions.

    Returns:
        result: The result of integration.
        rel_err: The fractional (relative) error in integration.
    """
    val = np.sqrt(np.pi) # known value of function
    result = 0
    width = (end - start) / nints
    points = np.linspace(start, end, nints)
    for x in points:
        result += func(x) * width
    rel_err = np.abs(result - val) / val
    return result, rel_err


def mc_integrate(func, start, end, npts):
    """Performs integration by Monte Carlo integration.

    Points are generated using numpy routines to avoid `for` loop overhead.

    Args:
        func: The function to integrate over.
        start (float): The left end of the bounds.
        end (float): The right end of the bounds.
        npts (int): The number of subdivisions.

    Returns:
        result: The result of integration.
        rel_err: The fractional error compared to the known value of the
            integral.
    """
    val = np.sqrt(np.pi) # known value of function
    interval = end - start
    points = np.random.uniform(start, end, npts)
    result = interval / npts * np.sum(func(points))
    rel_err = np.abs(result - val) / val
    return result, rel_err


def main():
    """Numerical integration by Riemannian and Monte Carlo methods."""
    start = -5000
    end = 5000
    numints = 1_000_000
    numpts = 100_000_000

    riemann = riemann_integrate(f, start, end, numints)
    print(f"Riemann Sum from {start} to {end} with {numints} subdivisions:")
    print(f"  Value: {riemann[0]}\n"
          f"  Error: {riemann[1]}")
    montecarlo = mc_integrate(f, start, end, numpts)
    print(f"Monte Carlo Integration from {start} to {end} with {numpts} points:")
    print(f"  Value: {montecarlo[0]}\n"
          f"  Error: {montecarlo[1]}")

    # relative error as a function of N, the number of points
    riemann_errs = []
    mc_errs = []
    nums = range(10, 10001, 10)
    for n in nums:
        riemann_errs.append(riemann_integrate(f, start, end, n)[1])
        mc_errs.append(mc_integrate(f, start, end, n)[1])
    fig, axs = plt.subplots(2, figsize=(6, 8))
    fig.subplots_adjust(hspace=0.3, top=0.9)
    ax1, ax2 = axs
    ax1.plot(nums, riemann_errs)
    ax2.plot(nums, mc_errs)
    ax1.set_title("Riemann Sum")
    ax1.set_xlabel("Number of Rectangles")
    ax1.set_ylabel("Relative Error")
    ax2.set_title("Monte Carlo Integration")
    ax2.set_xlabel("Number of Points")
    ax2.set_ylabel("Relative Error")
    fig.savefig("integration.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    main()
