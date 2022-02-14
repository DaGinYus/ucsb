"""
TKC!
Time Server
Matthew Wong
Phys 129L Hw6 Pb4
2022-02-17
"""

import logging
import socket
import time


def main():
    """Serves the current time and date in human-readable form.

    I use a `with` statement so that the socket is closed automatically.
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[logging.StreamHandler()])
    PORT = 55555
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        hostname = socket.gethostname()
        serversocket.bind(('', PORT))
        logging.info("Started server at %s on port %i", hostname, PORT)
        serversocket.listen(5)
        
        while True:
            clientsocket, address = serversocket.accept()
            logging.info("Connection from %s accepted", address[0])
            tfile = clientsocket.makefile("w")
            with tfile:
                tfile.write(time.asctime())
                tfile.flush()
                logging.info("Sent time to %s", address[0])
            clientsocket.close()
            logging.info("Closing connection to %s", address[0])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Shutting server down")
