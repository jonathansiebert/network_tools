# -*- coding: utf-8 -*-

"""
A basic http server
Listens on a specific port and returns http responses
Shuts down when it recieves and End of Transmission message
"""

import socket
from multiprocessing import Process


def server_process():
    """
    Open a specific socket to match the client module,
    and http any messages recieved up to and including
    an End of Transmission
    """
    server_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    server_socket.listen(1)

    done = False
    while not done:
        conn, addr = server_socket.accept()
        http_req = ''

        req_part = False
        while not req_part:
            msg_part = conn.recv(128)
            http_req += msg_part
            if len(msg_part) < 128:
                req_part = True

        if http_req == bytes(u"End of Transmission"):
            done = True

        conn.sendall(http_req)
        conn.close()

    server_socket.close()


def http_server():
    """
    Returns the process that the server is running in,
    it is left to the parent process to terminate this one
    (call process.join())
    """
    process = Process(target=server_process)
    process.start()
    return process


if __name__ == "__main__":
    """
    We're already our own process, so go ahead and block
    """
    http_server().join()
