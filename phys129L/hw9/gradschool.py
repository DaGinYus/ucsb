"""
TKC!
Gradschool Admissions
Matthew Wong
Phys 129L Hw9 Pb2
2022-03-10
"""


import numpy as np
from scipy import integrate
from scipy.stats import norm


def gaussian(x, exp, std):
    """Gaussian distribution.

    Args:
        x: The value to evaluate the Gaussian at.
        exp: The expectation value.
        std: The standard deviation.
    """
    coeff = 1/std/np.sqrt(2*np.pi)
    arg = -((x-exp)/std)**2 / 2
    return coeff * np.exp(arg)


def est_prob(n, pop_size):
    """Estimates the probability of a binomial distribution.

    The estimated probability from a single trial is obtained by
    dividing n by the total population size. The standard deviation in
    the probability is extrapolated from the standard deviation of the
    binomial distribution.

    Args:
        n (int): The number of 'successes'.
        pop_size (int): The total sample population.

    Returns:
        p_est: The estimated probability.
        p_std: The 1-sigma standard deviation in this probability.
    """
    p_est = n / pop_size
    variance = pop_size*p_est*(1 - p_est)
    std = np.sqrt(variance)
    p_std = (n + std)/pop_size - p_est
    return p_est, p_std


def main():
    """Gradschool Admissions statistics."""
    # parameters defined from the problem
    N = 1209
    N_a = 143
    p_est, p_std = est_prob(N_a, N)
    print(f"Estimated Probability (p): {p_est}")
    # variance and stdev of this binomial distribution
    var = N*p_est*(1 - p_est)
    std_a = np.sqrt(var)
    print(f"a) Standard Deviation: {std_a}")
    # take (N_a +/- std_a) / N and subtract p to find the difference
    # this is done in est_prob()
    print(f"b) One Sigma Deviation in p: {p_std}")
    # Gaussian approximation
    # expectation (loc) is N_a, stdev (scale) is std_a
    gaussian = norm(loc=N_a, scale=std_a)
    # calculations with 42 admitted out of 143
    p_g_est, p_g_std = est_prob(42, 143)
    print(f"d) Estimated Probability (p_g): {p_g_est}\n"
          f"   One Sigma Deviation in p_g: {p_g_std}")
    # calculations not in the group are just (143-42) out of 143
    p_n_est, p_n_std = est_prob(101, 143)
    print(f"e) Estimated Probability (p_n): {p_n_est}\n"
          f"   One Sigma Deviation in p_n: {p_n_std}")


if __name__ == "__main__":
    main()
