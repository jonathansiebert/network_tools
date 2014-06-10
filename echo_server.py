# -*- coding: utf-8 -*-

"""
A basic echo server
Listens on a specific port and echos messages
Shuts down when it recieves and End of Transmission message
"""

import socket
from multiprocessing import Process


def server_process():
    """
    Open a specific socket to match the client module,
    and echo any messages recieved up to and including
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
        echo_msg = ''

        msg_comp = False
        while not msg_comp:
            msg_part = conn.recv(128)
            echo_msg += msg_part
            if len(msg_part) < 128:
                msg_comp = True

        if echo_msg == bytes(u"End of Transmission"):
            done = True

        conn.sendall(echo_msg)
        conn.close()

    server_socket.close()


def echo_server():
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
    echo_server().join()
