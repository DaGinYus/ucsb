"""
TKC!
Factoring Numbers
Matthew Wong
Phys 129L Hw4 Pb4
2022-02-03
"""

import random
import numpy as np


def isprime(num, k=20):
    """Implementation of Rabin-Miller primality test.
    See Wikipedia article for details.
    
    Args:
        n: a positive integer to test for primality.
        k: the number of rounds of testing.    

    Returns:
        result (bool): true if n is prime, false if not.
    """
    # simple checks so randrange() doesn't fail
    if num == 2 or num == 3:
        return True
    elif num < 2 or num == 4:
        return False
    # rewrite n as (2^s)*d + 1 by repeated factoring
    d = num-1
    s = 0
    while s%2 == 0:
        d = d//2
        s += 1
    # check congruence of random number a^d with 1 or -1 mod n
    for _ in range(k):
        a = random.randrange(2, num-2)
        x = a**d % num
        if x == 1 or x == num-1:
            continue
        for _ in range(s-1):
            x = x**2 % num
            if x == num-1:
                continue
        return False
    return True

def factorize(factors, reseed=False):
    """Prime factorizes a number using Pollard's rho algorithm.
    
    This algorithm is faster than trial by division for large numbers.
    See Wikipedia article for details.

    Args:
        factors: a list of the current factors, which should only
            contain n, the number to factorize, the first time
            factorize() is called.

    Returns:
        factors: a list of prime integers.
    """
    # check if the factors are all prime, in which case return
    # otherwise set n to the first composite factor
    all_prime = True
    print(factors)
    for i, f in enumerate(factors):
        if not isprime(f):
            # set composite number
            composite = f
            all_prime = False
            break
    if all_prime:
        print("all prime")
        return factors

    # starting values
    tort = 2
    if reseed:
        tort = random.randrange(3, composite)
    hare = tort
    candidate = 1
    while candidate == 1:
        # the polynomial g(x) = (x^2 + 1) mod n is applied
        # (twice for y)
        tort = (tort**2 + 1)%composite
        hare = (hare**2 + 1)%composite
        hare = (hare**2 + 1)%composite
        candidate = np.gcd(np.abs(tort-hare), composite)

        if candidate == composite:
            # the test failed, try with a different starting value
            factorize(factors, True)
        else:
            # found a factor, replace f with d and f/d
            factors[i:i+1] = candidate, composite//candidate
            factorize(factors)


def main():
    """Gets the prime factorization of a number.

    Uses NumPy to perform array arithmetic, because it is much faster
    than looping.
    """
    while True:
        usrinput = input("Enter an integer: ")
        try:
            num = int(usrinput)
            if num != 0 and num != 1:
                break
            elif num < 0:
                print("Converting negative number to positive number...")
                num *= -1
                break
            print("The number you entered can't be prime factorized.")
        except ValueError:
            print("Please enter an integer.")

    print(isprime(41))
    print(factorize([num]))
    

if __name__ == "__main__":
    main()
