# -*- coding: utf-8 -*-

"""
Tests for a simple http server/client pair
Connection parameters are by convention
"""

import pytest
from http_server import http_server, http_ok, http_error
from http_client import http_client, http_client_send_unaltered


@pytest.fixture(scope="session")
def init_server(request):
    """
    Launch the http server, but don't start blocking until
    the testing session is over!
    """
    request.addfinalizer(http_server().join)


def test_http_ok(init_server):
    success_str = \
        "HTTP/1.1 200 OK\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        "/some/uri\r\n"
    assert http_ok("/some/uri") == success_str


def test_http_error():
    error_str = \
        "HTTP/1.1 404 Not Found\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        "Error 404: No URI requested\r\n"
    assert http_error(505, "No URI requested") == error_str

    error_str = \
        "HTTP/1.1 501 Not Implemented\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        "Error 501: Server supports only GET requests\r\n"
    assert http_error(501,
                      "Server supports only GET requests") == error_str

    error_str = \
        "HTTP/1.1 505 HTTP Version Not Supported\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        "Error 505: Server accepts only HTTP/1.1 requests\r\n"
    assert http_error(505, "Server accepts only HTTP/1.1 requests") == \
        error_str


def test_http_client_success():
    success_str = \
        "HTTP/1.1 200 OK\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        "/some/uri\r\n"
    assert http_client("/some/uri") == success_str


def test_http_client_error():
    """
    send a request with no Host head, which is illegal in HTTP/1.1
    """
    request_str = \
        "GET /some/uri HTTP/1.1\r\n" + \
        "\r\n"
    error_str = \
        "HTTP/1.1 400 Bad Request\r\n" + \
        "Content-Type: text/plain\r\n" + \
        "\r\n" + \
        "Error 400: No URI requested\r\n"
    assert http_client_send_unaltered(request_str) == error_str
