#!/usr/bin/env python

# This example taken straight from:
# [gevent-zeromq](http://sdiehl.github.io/gevent-tutorial/#gevent-zeromq)
# Minor updated to use new pyzmq support instead of depricated:
#     gevent-zeromq

from multiprocessing import Process
import gevent
import zmq.green as zmq

# Global Context
context = zmq.Context()

def server():
    server_socket = context.socket(zmq.REQ)
    server_socket.bind("tcp://127.0.0.1:5000")

    for request in range(1,10):
        server_socket.send("Hello")
        print('Switched to Server for %s' % request)
        # Implicit context switch occurs here
        server_socket.recv()

def client():
    client_socket = context.socket(zmq.REP)
    client_socket.connect("tcp://127.0.0.1:5000")

    for request in range(1,10):

        client_socket.recv()
        print('Switched to Client for %s' % request)
        # Implicit context switch occurs here
        client_socket.send("World")

def ownGuy(msg = None):
    print msg

p = Process(target=ownGuy, args=('hello',))
p.start()

publisher = gevent.spawn(server)
client    = gevent.spawn(client)

gevent.joinall([publisher, client])
p.join()

