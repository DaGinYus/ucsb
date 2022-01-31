"""
TKC!
Julian Day
Matthew Wong
Phys 129L Hw4 Pb6
2022-02-03
"""

import time

def usrprompt():
    """Prompts the user for a date in DDMmmYYYY format.
    
    I honestly don't think this should be a separate function but the
    homework asked for it.

    Returns:
        An input string.
    """
    return input("Enter a date in DDMmmYYYY format: ")

def parseinput(usrinput):
    """Parses a DDMmmYYYY string into a list.

    Args:
        usrinput: the string of user input.

    Returns:
        date: a list containing the year, month number, and day of the
            month.
        None: the list is in the incorrect format.
    """
    MONTHS = {"jan": 31, "feb": 29, "mar": 31, "apr": 30, "may": 31, "jun": 30,
              "jul": 31, "aug": 31, "sep": 30, "oct": 31, "nov": 30, "dec": 31}
    date = []
    try:
        year = int(usrinput[5:])
        monthname = usrinput[2:5].lower()
        month = list(MONTHS.keys()).index(monthname) + 1
        day = int(usrinput[:2])
        
        # make sure date is valid
        if (day > MONTHS[monthname]
            or (year%4 != 0 and (month == 2 and day > 28))
            or day < 0):
            print("Please enter a valid day")
            return None
        
        date = [year, month, day]
    except (ValueError, IndexError):
        print("Please enter the date in the correct format")
        return None
    return date

def date_to_JDN(date):
    """Computes the Julian day number from a date.

    Args:
        date: a list in [year, month, day] format

    Returns:
        jdn: the Julian day number.
    """

def main():
    """Does math with Julian days."""
    while True:
        date = parseinput(usrprompt())
        if date:
            print(date)
            break

if __name__ == "__main__":
    main()
