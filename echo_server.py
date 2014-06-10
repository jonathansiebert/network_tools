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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    server_socket.bind(('127.0.0.1', 50000))
    buff = 1024
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    complete_msg = ""
    completed = False
    while not completed:
        rcvd_msg = conn.recv(buff)
        if len(rcvd_msg) < 1024:
            completed = True
            complete_msg += rcvd_msg
    conn.sendall(complete_msg)
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
