"""
TKC!
Discrete Fourier Transform
Matthew Wong
Phys 129L Hw7 Pb2
2022-02-24
"""


import time
import numpy as np


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
    print(f"Starting DFT on sequence of length {seq.size}")
    k = n[:, None]
    k = np.array_split(k, chunks)
    
    counter = 0
    for sub in k:
        values = np.sum(seq * np.exp(-2j*np.pi*n*sub/N), axis=1)
        begin = sub[0,0]
        end = sub[-1,0]
        output[begin:end+1] = values
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
    return np.random.random(length) + np.rnadom.random(length)*1j


def main():
    """Work on Fourier transforms."""
    SEQ_LENGTH = 1024
    

if __name__ == "__main__":
    main()
