"""
TKC!
Gradschool Admissions
Matthew Wong
Phys 129L Hw9 Pb2
2022-03-10
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.stats import norm
from scipy.special import erfc


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


def stdev(p, n):
    """The standard deviation.

    Args:
        p: The probability of the event occuring.
        n (int): The number of trials.
    
    Returns:
        std: The standard deviation.
    """
    return np.sqrt(n*p*(1-p))


def est_prob(s, pop_size):
    """Estimates the probability of a binomial distribution.

    The estimated probability from a single trial is obtained by
    dividing n by the total population size. Where n is the number of
    'successes' in the initial trial.  The standard deviation in the
    probability is extrapolated from the standard deviation of the
    binomial distribution.

    Args:
        s (int): The number of 'successes'.
        pop_size (int): The total sample population.

    Returns:
        p_est: The estimated probability.
        p_std: The 1-sigma standard deviation in this probability.
    """
    p_est = s / pop_size
    std = stdev(p_est, pop_size)
    p_std = (s + std)/pop_size - p_est
    return p_est, p_std


def main():
    """Gradschool Admissions statistics."""
    # parameters defined from the problem
    tot_pop = 1209
    tot_admit = 143
    p_est, p_std = est_prob(tot_admit, tot_pop)
    print(f"Estimated Probability (p): {p_est}")
    # variance and stdev of this binomial distribution
    std_admit = stdev(p_est, tot_pop)
    print(f"a) Standard Deviation: {std_admit}")
    # the calculation is done in est_prob()
    print(f"b) One Sigma Deviation in p: {p_std}")
    # statistics for sample size 143
    samp_pop = 143
    samp_admit = 42
    std = stdev(p_est, samp_pop)
    # number of sigmas away using CDF of distribution
    exp = samp_pop*p_est # expectation
    sig = (samp_admit - exp)/std
    p_samp = 0.5*erfc(sig/np.sqrt(2))
    print(f"c) Chances of at least 42 students admitted: {p_samp}")
    # statistics within the sample
    p_g_est, p_g_std = est_prob(samp_admit, samp_pop)
    std_samp = stdev(p_g_est, samp_pop)
    print(f"d) Estimated Probability (p_g): {p_g_est}\n"
          f"   One Sigma Deviation in p_g: {p_g_std}")
    # calculations not in the group are for N - group
    excl_pop = tot_pop - samp_pop
    excl_admit = tot_admit - samp_admit
    p_n_est, p_n_std = est_prob(excl_admit, excl_pop)
    std_excl = stdev(p_n_est, excl_pop)
    print(f"e) Estimated Probability (p_n): {p_n_est}\n"
          f"   One Sigma Deviation in p_n: {p_n_std}")
    # plot the Gaussian distributions
    norm_p = norm(loc=tot_admit, scale=std_admit)
    norm_pg = norm(loc=samp_admit, scale=std_samp)
    norm_pn = norm(loc=excl_admit, scale=std_excl)
    scale_pg = samp_pop/tot_pop
    scale_pn = excl_pop/tot_pop
    x = np.linspace(0, 200, 1000)
    plt.plot(x, norm_p.pdf(x), label="Total Applicant Pool")
    plt.plot(x, norm_pg.pdf(x)*scale_pg, label="Pool of 143 Students")
    plt.plot(x, norm_pn.pdf(x)*scale_pn, label="The Other Applicants")
    plt.legend()
    plt.title("Gaussian Distributions with Scaled Areas")
    plt.xlabel("Number of Students Admitted")
    plt.ylabel("Probability Density within Sample")
    plt.savefig("gradschool.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    main()
