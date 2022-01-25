"""
TKC!
Read File and Average
Matthew Wong
Phys 129L Hw3 Pb4
2022-01-27
"""

import sys

def main():
    """Reads numbers (one per line) from a user-specified file and prints
    their average.
    """
    # either get filename from input or command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the name of the file: ")

    try:
        with open(filename) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found! Exiting.")
        return

    total = 0
    count = 0
    for line in lines:
        # check the first word (number)
        # skip if it's not a number
        # a try-except statement is used to handle floats as well
        first_word = line.split()[0]
        try:
            num = float(first_word)
            total += num
            count += 1
        except ValueError:
            continue
    print(f"Average is {total/count}")

if __name__ == "__main__":
    main()
