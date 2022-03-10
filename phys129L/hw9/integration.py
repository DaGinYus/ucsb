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


def riemann_integrate(func, start, end, nints, *args, **kwargs):
    """Performs integration by left-sided Riemann approximation.

    Args:
        func: The function to integrate over.
        start (float): The left end of the bounds.
        end (float): The right end of the bounds.
        nints (int): The number of subdivisions.
        val (optional): The expected value of integration.

    Returns:
        result: The result of integration.
        rel_err: The fractional (relative) error in integration.
    """
    rel_err = None
    result = 0
    width = (end - start) / nints
    points = np.linspace(start, end, nints)
    for x in points:
        result += func(x, *args) * width
    if "val" in kwargs.keys():
        val = kwargs["val"]
        rel_err = np.abs(result - val) / val
    return result, rel_err


def mc_integrate(func, start, end, npts, *args, **kwargs):
    """Performs integration by Monte Carlo integration.

    Points are generated using numpy routines to avoid `for` loop overhead.

    Args:
        func: The function to integrate over.
        start (float): The left end of the bounds.
        end (float): The right end of the bounds.
        npts (int): The number of subdivisions.
        val (optional): The expected value of integration.

    Returns:
        result: The result of integration.
        rel_err: The fractional error compared to the known value of the
            integral.
    """
    rel_err = None
    interval = end - start
    points = np.random.uniform(start, end, npts)
    result = interval / npts * np.sum(func(points, *args))
    if "val" in kwargs.keys():
        val = kwargs["val"]
        rel_err = np.abs(result - val) / val
    return result, rel_err


def main():
    """Numerical integration by Riemannian and Monte Carlo methods."""
    start = -5000
    end = 5000
    numints = 1_000_000
    numpts = 100_000_000
    expected = np.sqrt(np.pi)

    riemann = riemann_integrate(f, start, end, numints, val=expected)
    print(f"Riemann Sum from {start} to {end} with {numints} subdivisions:")
    print(f"  Value: {riemann[0]}\n"
          f"  Error: {riemann[1]}")
    montecarlo = mc_integrate(f, start, end, numpts, val=expected)
    print(f"Monte Carlo Integration from {start} "
          f"to {end} with {numpts} points:")
    print(f"  Value: {montecarlo[0]}\n"
          f"  Error: {montecarlo[1]}")

    # relative error as a function of N, the number of points
    riemann_errs = []
    mc_errs = []
    nums = range(10, 10001, 10)
    for n in nums:
        riemann_errs.append(riemann_integrate(f, start, end, n,
                                              val=expected)[1])
        mc_errs.append(mc_integrate(f, start, end, n,
                                    val=expected)[1])
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
