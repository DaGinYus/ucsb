"""
TKC!
User Input
Matthew Wong
Phys 129L Hw3 Pb1
2022-01-27
"""

# default variables
_ITERATIONS = 10

def main():
    """Asks the user to enter a string, then prints it 10 times."""
    usrinput = input("Enter a string: ")
    for _ in range(_ITERATIONS):
        print(usrinput)

if __name__ == "__main__":
    main()
