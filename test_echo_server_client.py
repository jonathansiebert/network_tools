"""
Tests for a simple echo server/client pair
Connection parameters are by convention
"""

import pytest
import socket
from echo_server import echo_server
from echo_client import echo_client


@pytest.fixture(scope="session")
def init_server(request):
    """
    Launch the echo server, but don't start blocking until
    the testing session is over!
    """
    request.addfinalizer(echo_server().join)


def test_success(init_server):
    assert echo_client("Testing 1 2 3") == "Testing 1 2 3"


def test_unicode():
    assert echo_client(u"Testing 1 2 3") == u"Testing 1 2 3"
    assert echo_client("End of Transmission") == "End of Transmission"


def test_eot():
    """
    Server should already have closed up shop, so the
    client should no longer be able to connect
    """
    with pytest.raises(socket.error):
        echo_client("Testing 1 2 3")
