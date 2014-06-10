"""
A basic echo client
Opens a specific socket and tries to send a message
Returns whatever the server sends back
"""

import sys
import socket


def echo_client(message):
    """
    Do everything here!
    Open the socket, send the message passed in,
    store the servers response, shutdown and close the socket,
    and return the servers response
    """
    client_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  socket.IPPROTO_IP)
    client_socket.connect(('127.0.0.1', 50000))
    client_socket.sendall(message)
    client_socket.shutdown(socket.SHUT_WR)
    retval = client_socket.recv(128)
    client_socket.close()
    return retval


if __name__ == "__main__":
    """
    Simply pass along the first command line argument as
    the message to the server
    """
    print echo_client(sys.argv[1])
