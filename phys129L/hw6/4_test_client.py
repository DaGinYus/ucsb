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

    host = input("Enter address: ")
    port = input("Enter port: ")

    # use loopback address
    with socket.create_connection((host, port)) as sock:
        f = sock.makefile("r")
        with f:
            print(f.readlines())

if __name__ == "__main__":
    main()
        
