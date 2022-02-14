"""
TKC!
Time Server
Matthew Wong
Phys 129L Hw6 Pb4
2022-02-17
"""

import socket


def main():
    """A simple client to test the time server."""
    PORT = 55555
    addr = input("Enter address: ")

    # use loopback address
    with socket.create_connection((addr, PORT)) as sock:
        f = sock.makefile("r")
        with f:
            print(f.readline())


if __name__ == "__main__":
    main()
