"""
TKC!
Sine Function
Matthew Wong
Phys 129L Hw4 Pb5
2022-02-03
"""

import math

def sind(deg, stop, total=0, previous=0, count=0):
    """The sine of a number in degrees.
    
    We can obtain it recursively by dividing the nth term of the Taylor
    Series by the (n-1)th to obtain a ratio of
        x^2/(2n)/(2n+1)
    So we just multiply the previous term by this term and add it to the
    running total.

    Args:
        deg: the degree measure to calculate the sine of.
        stop: the number of terms to calculate.
        total: the running total.
        previous: the last term in the series.
        count: the number of terms we've summed over.

    Returns:
        total: the result of summing the series.
    """
    # convert to radians
    deg %= 360
    x = deg*math.pi/180
    if count == 0:
        return sind(deg, stop, x, x, 1)
    elif count > 0 and count != stop:
        term = -1*x**2/(2*count)/(2*count+1)*previous
        total += term
        count += 1
        return sind(deg, stop, total, term, count)
    return total

def main():
    """Calculates the sine of a number in degrees."""
    while True:
        usrinput = input("Enter a number (degrees): ")
        try:
            num = float(usrinput)
            break
        except ValueError:
            print("Please enter a valid number")
    while True:
        usrinput = input("Enter the number of terms (<= 25): ")
        try:
            numterms = int(usrinput)
            if numterms <= 0:
                raise(ValueError)
            break
        except ValueError:
            print("Please enter a positive integer")

    if numterms > 25:
        numterms = 25
    print(sind(num, numterms))
    

if __name__ == "__main__":
    main()
