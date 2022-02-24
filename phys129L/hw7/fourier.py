"""
TKC!
Discrete Fourier Transform
Matthew Wong
Phys 129L Hw7 Pb2
2022-02-24
"""


import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import (ScalarFormatter,
                               NullFormatter,
                               NullLocator)


def timer(func):
    """A timing decorator.

    Args:
        func: The function to time.

    Returns:
        wrapper: A wrapper function.
    """
    ITERATIONS = 10
    
    def wrapper(*args, **kwargs):
        start_t = time.perf_counter()
        for _ in range(ITERATIONS):
            result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_t
        perloop = elapsed / ITERATIONS
        print(f"{ITERATIONS} loops completed in {elapsed:6g}"
              f" s, {perloop:6g} s per loop")
        return perloop
    return wrapper


def dft(seq, n=None, memlimit=1024):
    """The discrete Fourier transform of a sequence of complex numbers.

    Implements the following formula:
        X_k = sum(x_n * exp(-2Pi*i*k*n/N))
    where X_k is the transformed number, x_n is the input number,
    k is the current index, and n is the number of terms. k is
    broadcasted and multiplied so we can take advantage of vectorized
    operations.

    For large n, we use chunking to reduce looping overhead without
    blowing up memory usage. Since we are using broadcasting for speed,
    we wind up with an nxn matrix, which can get out of hand for 
    large n. If the memory needed exceeds memlimit, then we chunk the
    data into subdivisions that don't exceed memlimit. However, the main
    bottleneck is in the np.exp() function, so there isn't much
    optimization we can do.

    Args:
        seq [cmpl]: A numpy array of complex numbers.
        n: Optional length of the transformed axis. If n is smaller than
            the length of the input, the input is cropped. If it is
            larger, the input is padded with zeros. If n is not given,
            the length of the sequence is used. This is made so the
            function call is similar to the numpy.fft.fft() function
            call.
        memlimit: The size in MiB to limit the arrays to.
    
    Returns:
        output [cmpl]: A numpy array of the transformed numbers.
    """
    N = n
    if not N:
        N = len(seq)
    else:
        temp = np.zeros(N, dtype=np.complex128)
        temp[:len(seq)] = seq[:N]
        seq = temp
    n = np.arange(N)
    output = np.zeros(N, dtype=np.complex128)

    arrsize = seq.itemsize * seq.size**2 # bytes
    chunks = int(np.ceil(arrsize/(memlimit*1024**2)))
    k = n[:, None]
    k = np.array_split(k, chunks)
    
    counter = 0
    for sub in k:
        values = np.sum(seq * np.exp(-2j*np.pi*n*sub/N), axis=1)
        begin = sub[0,0]
        end = sub[-1,0]
        output[begin:end+1] = values
        if chunks > 1:
            counter += 1
            print(f"Processed {counter}/{chunks} chunks")

    return output


def seq_gen(length):
    """Generates a sequence of random complex numbers.

    Args:
        length: The length of the sequence.
    
    Returns:
        seq: A sequence of random complex numbers.
    """
    return np.random.random(length) + np.random.random(length)*1j


def plot_data(seq_lengths, dft_times, fft_times, dft_fit, fft_fit):
    """Plots the comparison between the DFT and FFT functions.

    Args:
        seq_lengths: The sequence lengths tested (x-axis).
        dft_times: The DFT times for each length (y-axis).
        fft_times: The FFT times for each length.
        dft_fit: A tuple containing the fit function and the
            fit coefficients. The coefficients are a list satisfying
            log(y) = log(A)*x + log(B), which plots as a straight line
            on a log-log scale.
        fft_fit: The same thing as dft_fit, but for FFT values.
    """
    _, ax = plt.subplots()
    ax.loglog(seq_lengths, dft_times, ls='', marker='.', label="DFT")
    ax.loglog(seq_lengths, fft_times, ls='', marker='.', label="NumPy FFT")
    ax.loglog(seq_lengths, dft_fit[0], ls="--", color="tab:blue",
              label=f"Fit Slope: {dft_fit[1][0]:.4f}")
    ax.loglog(seq_lengths, fft_fit[0], ls="--", color="tab:orange",
              label=f"Fit Slope: {fft_fit[1][0]:.4f}")
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticks(seq_lengths, seq_lengths)
    ax.set_ylabel("Execution Time [s]")
    ax.set_xlabel("Sequence Length")
    ax.set_title("DFT and NumPy FFT Comparison")
    ax.legend()
    plt.savefig("fourier.pdf", format="pdf")
    plt.show()


def main():
    """Work on Fourier transforms.

    Timing is done through a decorator.
    """
    SEQ_LENGTHS = (256, 512, 1024, 2048, 4096, 8192)
    dft_times = []
    fft_times = []
    for seq_length in SEQ_LENGTHS:
        print(f"\nStarting DFT test on sequence of length {seq_length}")
        dft_times.append(dft(seq_gen(seq_length)))
        print(f"\nStarting NumPy FFT test on sequence of length {seq_length}")
        fft_times.append(np.fft.fft(seq_gen(seq_length)))

    fit_x = np.log(SEQ_LENGTHS)
    coeffs = [np.polyfit(fit_x, np.log(times), deg=1)
              for times in (dft_times, fft_times)]
    poly = [np.poly1d(coeff) for coeff in coeffs]
    fits = [(np.exp(f(fit_x)), coeffs[i]) for i,f in enumerate(poly)]
    plot_data(SEQ_LENGTHS, dft_times, fft_times, *fits)

        
if __name__ == "__main__":
    # wrap the functions with the timer
    dft = timer(dft)
    np.fft.fft = timer(np.fft.fft)
    main()
