network_tools
=============

##echo_server / echo_client

a basic socket server that sends back copies of what is sent to it,
and a client that can send messages to it.

##http_server / http_client

a simple http server that can only respond to http/1.1 GET requests, and
only by sending back a response containing the uri requested in the
response body. The client can only send GET requets

##sources

Reviewed: http://pymotw.com/2/socket/tcp.html