"""
TKC!
Write File
Matthew Wong
Phys 129L Hw3 Pb2
2022-01-27
"""

_WRITE_FNAME = "out.txt"

def overwrite_confirm():
    """Ask the user if they want to overwrite the file."""
    usr_overwrite = input("File already exists, overwrite? (y/n): ")
    if usr_overwrite.lower() == 'y' or usr_overwrite.lower() == 'yes':
        return True
    elif usr_overwrite.lower() == 'n' or usr_overwrite.lower() == 'no':
        return False
    else:
        print("Please enter 'yes' or 'no'.")
        overwrite_confirm()

def main():
    """Asks the user for two strings, then writes these two separate 
    lines to a file. If the file already exists, ask the user if it
    is ok to overwrite.
    """
    input1 = input("Enter first string: ")
    input2 = input("Enter second string: ")

    try:
        with open(_WRITE_FNAME, mode='x') as f:
            f.write(f"{input1}\n")
            f.write(f"{input1}\n")
    except FileExistsError:
        if overwrite_confirm():
            with open(_WRITE_FNAME, mode='w') as f:
                f.write(f"{input1}\n")
                f.write(f"{input2}\n")

if __name__ == "__main__":
    main()
