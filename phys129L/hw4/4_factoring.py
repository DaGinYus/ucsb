"""
TKC!
Factoring Numbers
Matthew Wong
Phys 129L Hw4 Pb4
2022-02-03
"""

import numpy as np


def main():
    """Gets the prime factorization of a number.

    Uses NumPy to perform array arithmetic, because it is much faster
    than looping.
    """
    while True:
        usrinput = input("Enter an integer: ")
        try:
            num = int(usrinput)
            break
        except ValueError:
            print("Please enter an integer.")

    if num < 0:
        print("Converting negative number to positive number...")
        num *= -1
    elif num == 0 or num == 1:
        print("Can't be prime factorized!")
        return
    
    midpoint = int(np.ceil(np.sqrt(num)))
    dividend = np.array([num]*midpoint)
    divisors = np.arange(midpoint)+2
    result = dividend % divisors
    lower_factors = divisors[np.where(result == 0)]
    upper_factors = dividend[:len(lower_factors)] / lower_factors
    output = np.append(lower_factors, upper_factors).astype(int)
    print(' '.join(str(n) for n in output))
    

if __name__ == "__main__":
    main()
