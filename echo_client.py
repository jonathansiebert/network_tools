# -*- coding: utf-8 -*-

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
    client_socket.sendall(message.encode('utf-8'))
    client_socket.shutdown(socket.SHUT_WR)
    echo_msg = ''
    msg_comp = False
    while not msg_comp:
        msg_part = client_socket.recv(128)
        echo_msg += msg_part
        if len(msg_part) < 128:
            msg_comp = True
    client_socket.close()
    return unicode(echo_msg, 'utf-8')


if __name__ == "__main__":
    """
    Simply pass along the first command line argument as
    the message to the server
    """
    print echo_client(sys.argv[1])
