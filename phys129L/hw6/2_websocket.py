"""
TKC!
Web Page with socket
Matthew Wong
Phys 129L Hw6 Pb2
2022-02-17
"""

import socket
import ssl

def main():
    """Checks when the webpage announcements were last updated.

    I've used `with` statements so that the sockets and files are closed
    automatically. Instead of using `sendall()` or `recv()`, I've
    chosen to use Python's `makefile()`, which allows me to treat the
    socket like it is a file.

    Note that the webpage actually serves over HTTPS instead of HTTP
    so we need to configure SSL.
    """
    HOST = "web.physics.ucsb.edu"
    PORT = 443 # https

    context = ssl.create_default_context()
    
    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            f = ssock.makefile("rwb")
            with f:
                f.write(b"GET /~phys129/lipman HTTP/1.1\r\n"
                        b"Host: web.physics.ucsb.edu\r\n\r\n")
                f.flush()
                print(f.readlines())


if __name__ == "__main__":
    main()
