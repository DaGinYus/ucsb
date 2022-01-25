"""
TKC!
Dictionaries and Databases
Matthew Wong
Phys 129L Hw4 Pb2
2022-02-03
"""

import csv
import sys


def read_csv(keys):
    """Reads in a .csv file.

    Checks for command-line arguments and uses that first. If there are
    no command-line arguments passed, then ask the user for a file.

    Args: 
        keys: A list of keys to initialize the dictionary with.

    Returns:
        csvdata: A list of dictionaries with values corresponding to the
            keys passed into the function.
    """
    csvdata = []

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the name of a file: ")

    try:
        with open (filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != len(keys):
                    print("Unexpected number of columns! Exiting.")
                    return []
                data = {keys[i]: value for i,value in enumerate(row)}
                csvdata.append(data)
    except FileNotFoundError:
        print("File not found! Exiting.")
        
    return csvdata

def browse_data(csvdata, keys):
    """The main user interaction part.

    Prints out the list of available keys for the user to select. When
    a key is selected, prints out the corresponding info. Continues
    asking for keys until quit.

    Args:
       csvdata: The .csv data in a list of dictionaries
       keys: The keys of the dictionaries
    """
    while True:
        print(f"\nAvailable keys:")
        for key in keys:
            print(f"  {key}")
        usrinput = input("\nEnter a key (type 'quit' to quit): ")
        usrinput = usrinput.strip().lower()
        
        if usrinput == "quit":
            return
        elif usrinput in keys:
            print_data(csvdata, usrinput)
        else:
            print("Please type in one of the keys\n")

def print_data(csvdata, key):
    """Prints the data for a particular key.

    If the key is either `first` or `last`, it prints out the sorted
    names. If another key is passed, then sort by last name. The values
    are printed with the names.

    Args:
        csvdata: The .csv data in a list of dictionaries
        key: The key to print out
    """
    output = []
    for row in csvdata:
        first = row["first"].capitalize()
        last = row["last"].capitalize()
        if key == "first":
            output.append(f"{first} {last}")
        elif key == "last":
            output.append(f"{last}, {first}")
        else:
            output.append(f"{last}, {first}: {row[key]}")
    print()
    print('\n'.join(sorted(output)))

    
def main():
    """An exercise in reading and formatting .csv data."""

    KEYS = ["first", "last", "color", "food", "field", "physicist"]

    csvdata = read_csv(KEYS)
    if len(csvdata) != 0:
        browse_data(csvdata, KEYS)
    else:
        print("Bad .csv format! Exiting.")
        

if __name__ == "__main__":
    main()
