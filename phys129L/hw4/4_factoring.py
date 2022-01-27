"""
TKC!
Factoring Numbers
Matthew Wong
Phys 129L Hw4 Pb4
2022-02-03
"""

import random
import numpy as np


def isprime(num, k=40):
    """Implementation of Rabin-Miller primality test.
    See Wikipedia article for details.
    
    Args:
        num: a positive integer to test for primality.
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
    while d%2 == 0:
        d //= 2
        s += 1
    # check congruence of random number a^d with 1 or -1 mod n
    # (Fermat's little theorem)
    for _ in range(k):
        a = random.randint(2, num-2)
        x = pow(a, d, num)
        if x == 1 or x == num-1:
            continue
        for _ in range(s):
            x = pow(x, 2, num)
            if x == num-1:
                break
        else:
            return False
    # probably prime
    return True

def pollardrho(num, count=0):
    """Implementation of Pollard's rho algorithm.
    
    Args:
        num: an odd number greater than 3 to be factorized.
        count: a number used to count how many times we've retried.
            If it's greater than 0, then the polynomial is incremented
            and a starting value is randomly generated.

    Returns:
        d: a factor of num
    """
    if isprime(num):
        return num
    # starting values
    tort = 2
    if count:
        tort = random.randint(3, num)
    hare = tort
    d = 1 # this variable is checked if it is a factor
    while d == 1:
        # the polynomial g(x) = (x^2 + 1) mod n is applied
        # (twice for y)
        tort = (tort**2 + 1 + count)%num
        hare = (hare**2 + 1 + count)%num
        hare = (hare**2 + 1 + count)%num
        d = int(np.gcd(np.abs(tort-hare), num))

        if d == num:
            # the test failed, try with a different starting value
            return pollardrho(num, count+1)
        elif d != 1:
            # found a factor
            return d

def factorize(factors, reseed=False):
    """Prime factorizes a number using Pollard's rho algorithm.
    
    This algorithm is faster than trial by division for large numbers.
    Factors of 2 are repeatedly divided first, leaving an odd number to
    factorize. Then the function is repeatedly called over the running
    list of factors until they are all prime.

    Args:
        factors: a list of the current factors, which should only
            contain n, the number to factorize, the first time
            factorize() is called.

    Returns:
        factors: a list of prime integers.
    """
    # factorize powers of 2 first
    f0 = factors[0]
    if f0%2 == 0 and f0 != 2:
        count = 0
        while f0%2 == 0 and f0 != 2:
            f0 //= 2
            count += 1
        factors[0:0] = [2 for _ in range(count)]
        factors[-1] = f0
    # check if the factors are all prime, in which case return
    # otherwise set n to the first composite factor
    all_prime = True
    for f in factors:
        if not isprime(f):
            # set composite number
            composite = f
            all_prime = False
            break
    if all_prime:
        return factors

    factor = pollardrho(composite)
    # replace the composite with its factors
    replace = factors.index(composite)
    factors[replace:replace+1] = factor, composite//factor
    return factorize(factors)


def main():
    """Gets the prime factorization of a number."""
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

    result = factorize([num])
    print(' '.join([str(n) for n in result]))
    

if __name__ == "__main__":
    main()
