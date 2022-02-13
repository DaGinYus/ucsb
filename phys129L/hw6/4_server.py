"""
TKC!
Time Server
Matthew Wong
Phys 129L Hw6 Pb4
2022-02-17
"""

import logging
import socket
import threading
import time


def main():
    """Serves the current time and date in human-readable form.

    I use a `with` statement to handle the closing of the socket
    automatically. By default, the server is listening on port 55555.
    """
    PORT = 55555

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        hostname = socket.gethostname()
        serversocket.bind((hostname, PORT))
        logging.info("Started server at %s on port %i", hostname, PORT)
        serversocket.listen(5)
        
        while True:
            (clientsocket, address) = serversocket.accept()
            logging.info(address)


if __name__ == "__main__":
    main()
