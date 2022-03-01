"""
TKC!
fork() and execv()
Matthew Wong
Phys 129L Hw8 Pb3
2022-03-03
"""


import sys
import os
import time


def main():
    """An exercise in forking and running files using execv()."""
    TICK_INTERVAL = 0.5 # seconds
    counter = 0
    while True:
        counter += 1
        print(counter)
        if counter%10 == 0:
            print("Forking!")
            time.sleep(TICK_INTERVAL)
            retval = os.fork()
            if retval == 0: # is child process
                print("Running `ls -l` command")
                time.sleep(TICK_INTERVAL)
                os.execv("/bin/ls", ("/bin/ls", "-l"))
        time.sleep(TICK_INTERVAL)


if __name__ == "__main__":
    main()
