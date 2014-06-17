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

    buf_size = 4096

    done = False
    while not done:
        conn, addr = server_socket.accept()
        http_req = ''

        req_part = False
        while not req_part:
            msg_part = conn.recv(buf_size)
            http_req += msg_part
            # still not perfect but pretty good about catching the
            # end of http requests, looks for partial message or
            # double CLRF
            if len(msg_part) < buf_size or '\r\n\r\n' in msg_part:
                req_part = True

        if "secretstopmessage" in http_req:
            done = True

        conn.sendall(process_request(http_req))
        conn.close()

    server_socket.close()


def process_request(request):
    """
    parse a http GET request, returning appropriate error pages
    when necessary, and returning a 200 page with the uri that
    the user requested as the body otherwise
    """
    req = request.split()
    if req[0] != "GET":
        return http_error(501, "Server supports only GET requests")
    if req[2] != "HTTP/1.1":
        return http_error(505, "Server accepts only HTTP/1.1 requests")
    if len(req) < 4 or req[3] != "Host:" or len(req) < 5:
        return http_error(400, "No Host Specified")
    return http_ok(req[1])


def http_server():
    """
    Returns the process that the server is running in,
    it is left to the parent process to terminate this one
    (call process.join())
    """
    process = Process(target=server_process)
    process.start()
    return process


def http_ok(uri):
    """
    returns a valid HTTP/1.1 response containing plain text
    of the the uri requested as the body
    """
    return \
        "HTTP/1.1 200 OK\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        uri + "\r\n"


# for http_error function
http_errors = {
    404: "Not Found",
    501: "Not Implemented",
    505: "HTTP Version Not Supported",
    400: "Bad Request"
}


def http_error(code, message):
    """
    returns a http error response appropriate for the http error code
    with a human readable message in the response body
    """
    return "HTTP/1.1 " + str(code) + " " + http_errors[code] + "\r\n"\
           "Content-Type: text/plain\r\n" + \
           "\r\n" + \
           "Error " + str(code) + ": " + message + "\r\n"


if __name__ == "__main__":
    """
    We're already our own process, so go ahead and block
    """
    http_server().join()
