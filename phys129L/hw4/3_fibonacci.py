"""
TKC!
Fibonacci Numbers
Matthew Wong
Phys 129L Hw4 Pb3
2022-02-03
"""

import sys


def main():
    """Prints out the first n Fibonacci numbers.
    
    Takes input by command-line arguments. If none are passed, exit the
    program. Output is restricted to 
    """
    errmsg = (f"Usage: {sys.argv[0]} n\n"
              f"    n (int) is the number of Fibonacci numbers to print out")
    if len(sys.argv) != 2:
        print(errmsg)
        return
    try:
        n = int(sys.argv[1])
    except ValueError:
        print(errmsg)
        return

    a = 1
    b = 1
    output = [str(a)]
    if n >= 1:
        for _ in range(n-1):
            # line length logic here
            out = str(a)
            digits = len(out)
            if digits > 75:
                break
            lastline = output[-1]
            # reserve one extra character for space
            if len(lastline)+digits <= 74:
                # join() is used instead of += to prevent trailing whitespace
                output[-1] = ' '.join([lastline, out])
            else:
                output.append(out)
                
            temp = a + b
            b = a
            a = temp
            
        for line in output:
            print(line)

    else:
        print(errmsg)    
    

if __name__ == "__main__":
    main()
