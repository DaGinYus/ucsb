"""
TKC!
Julian Day
Matthew Wong
Phys 129L Hw4 Pb6
2022-02-03
"""

import math
from time import gmtime, strftime

def usrprompt():
    """Prompts the user for a date in DDMmmYYYY format.
    
    I honestly don't think this should be a separate function but the
    homework asked for it.

    Returns:
        An input string.
    """
    return input("Enter a date in DDMmmYYYY format: ")

def parsedate(usrinput):
    """Parses a DDMmmYYYY string into a list.

    time.strptime() could be useful here but it does not handle negative
    numbers. My implementation does, at the cost of generality, but we
    expect a certain input format anyways.

    Args:
        usrinput: the string of user input.

    Returns:
        date: a list containing the year, month number, and day of the
            month.
        None: the list is in the incorrect format.
    """
    MONTHS = {"jan": 31, "feb": 29,
              "mar": 31, "apr": 30,
              "may": 31, "jun": 30,
              "jul": 31, "aug": 31,
              "sep": 30, "oct": 31,
              "nov": 30, "dec": 31,}
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

def date_to_JD(date):
    """Computes the Julian day number from a date.

    Args:
        date: a list in [year, month, day] format.

    Returns:
        jdn: the Julian day number.
    """
    y, m, d = date
    if m == (1 or 2):
        y -= 1
        m += 12
    a = y//100
    b = 2 - a + a//4
    jdn = (math.floor(365.25*(y+4716)) + math.floor(30.6001*(m+1))
           + d + b - 1524.5)
    return jdn

def JD_to_weekday(jdn):
    """Finds the day of the week for a given Julian day.

    Args:
        jdn: a Julian date.
    
    Returns:
        weekday: a string containing the day name.
    """
    DAYS = ["Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",]
    return DAYS[math.floor((jdn+1.5)%7)]

def time_interval(jdn):
    """Calculates the days from today since (or until) the Julian day.

    Args:
        jdn: a Julian date.

    Returns:
        days: days since the event (negative if in the future).
    """
    today = strftime("%d%b%Y", gmtime())
    today_jdn = date_to_JD(parsedate(today))
    return math.floor(today_jdn - jdn)


def main():
    """Does math with Julian days."""
    while True:
        date = parsedate(usrprompt())
        if date:
            break
    
    jdn = date_to_JD(date)
    weekday = JD_to_weekday(jdn)
    delta_t = time_interval(jdn)
    print(f"Julian Day: {jdn}")
    if delta_t > 0:
        print(f"This day was a {weekday}")
        print(f"Days since this date: {delta_t}")
    elif delta_t == 0:
        print(f"This day is a {weekday}")
        print("That's today!")
    else:
        print(f"This day will be a {weekday}")
        print(f"Days until this date: {-delta_t}")

        
if __name__ == "__main__":
    main()
