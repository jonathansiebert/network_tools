# -*- coding: utf-8 -*-

"""
Tests for a simple http server/client pair
Connection parameters are by convention
"""

import pytest
from http_server import http_server, http_ok, http_error
from http_client import http_client


@pytest.fixture(scope="session")
def init_server(request):
    """
    Launch the http server, but don't start blocking until
    the testing session is over!
    """
    request.addfinalizer(http_server().join)


def test_http_ok(init_server):
    assert http_ok("/some/uri") == """HTTP/1.1 200 OK
Content-Type: text/plain
\r\n
/some/uri"""


def test_http_error():
    assert http_error(505, "Server accepts only HTTP/1.1 requests") == \
        """HTTP/1.1 505 HTTP Version Not Supported
Content-Type: text/plain
\r\n
Error 505: Server accepts only HTTP/1.1 requests"""
    assert http_error(404, "No URI requested") == \
        """HTTP/1.1 404 Not Found
Content-Type: text/plain
\r\n
Error 404: No URI requested"""
    assert http_error(501, "Server supports only GET requests") == \
        """HTTP/1.1 501 Not Implemented
Content-Type: text/plain
\r\n
Error 501: Server supports only GET requests"""


def test_http_client_success():
    assert http_client("/some/uri") == """HTTP/1.1 200 OK
Content-Type: text/plain
\r\n
/some/uri"""


def test_http_client_error():
    assert http_client('') == \
        """HTTP/1.1 404 Not Found
Content-Type: text/plain
\r\n
Error 404: No URI requested"""
