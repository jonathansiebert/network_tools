# -*- coding: utf-8 -*-

"""
A basic http client
"""

import sys
import socket


def http_client_send_unaltered(message):
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
    buf_size = 4096
    http_msg = ''
    msg_comp = False
    while not msg_comp:
        msg_part = client_socket.recv(buf_size)
        http_msg += msg_part
        if len(msg_part) < buf_size:
            msg_comp = True
    client_socket.close()
    return unicode(http_msg, 'utf-8')


def http_client(uri):
    """
    Build a valid request for a specific resource
    """
    request = \
        "GET " + uri + " HTTP/1.1\r\n" + \
        "Host: 127.0.0.1:50000\r\n" + \
        "\r\n"
    return http_client_send_unaltered(request)


if __name__ == "__main__":
    """
    Simply pass along the first command line argument as
    the message to the server
    """
    print http_client(sys.argv[1])
