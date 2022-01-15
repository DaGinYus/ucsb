"""
TKC!
String Processing
Matthew Wong
Phys 129L Hw3 Pb3
2022-01-27
"""

def get_usrinput():
    """Checks if the string is at least 3 words, then returns the string
    as a list of words.
    """
    while True:
        usrinput = input("Enter a string with at least 3 words: ")
        words = usrinput.strip().split(' ')
        if len(words) >= 3:
            return words


def main():
    """Asks the user for a string that is at least 3 words, then:
        - prints the words in the string, one per line
        - prints the first 3 characters, not including leading whitespace
        - prints the last 3 characters, not including the newline character
        - prints the first half, inclusive
        - prints the second half, inclusive
        - prints the string with the words in reverse order
        - prints the string with the words alphabetized
        - prints each character, one per line
        - prints hexadecimal values for each char, one per line
    """
    # get the string as a list of words, and as a sentence
    # (for processing later)
    words = get_usrinput()
    sentence = ' '.join(words)

    # incoming print statements (yikes!)
    print("The words:")
    for word in words:
        print(word)

    print("First 3 characters:")
    print(sentence[:3])

    print("Last 3 characters:")
    print(sentence[-3:])

    print("First half (inclusive):")
    print(sentence[:round(len(sentence)/2)])

    print("Last half (inclusive):")
    print(sentence[-round(len(sentence)/2):])

    print("The words, in reverse:")
    revwords = words.copy()
    revwords.reverse()
    print(' '.join(revwords))

    print("Alphabetized string:")
    print(' '.join(sorted(words, key=str.lower)))

    print("Each character in its own line:")
    for char in sentence:
        print(char)

    print("Hex values for each character:")
    for char in sentence:
        print(hex(ord(char)))

if __name__ == "__main__":
    main()
