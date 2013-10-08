#!/usr/bin/env python

# This example uses gevent example:
# [gevent-zeromq](http://sdiehl.github.io/gevent-tutorial/#gevent-zeromq)
# and combines it with zmq example:
# [divide and conquer](http://zguide.zeromq.org/page:all#header-15)

import time
import gevent
import zmq.green as zmq

# Global Context
context = zmq.Context()

def ventilator():
    """ Task ventilator
    Binds PUSH socket to tcp://5557
    Sends batch of tasks to workers via that socket
    """
    # Socket on which to send messages
    tx = context.socket(zmq.PUSH)
    tx.bind("tcp://*:5557")

    # Socket with direct access to sink to synchronize start of batch
    sink_tx = context.socket(zmq.PUSH)
    sink_tx.connect("tcp://localhost:5558")

    # to ensure proper 'load balancing'
    # make sure all workers are spawned and listening before starting
    gevent.sleep(1)

    # The first message is '0' and signals start of batch
    sink_tx.send('0')

    for request in range(1,30):
        tx.send('Ventilator Task {0}'.format(request))
        print('Switched to ventilator for %s' % request)
        gevent.sleep(0)

    print 'Ventilator done... Shutting it down...'
    # Give 0mq time to deliver
    gevent.sleep(1)

def worker():
    """ Task worker
    connects PULL socket to tcp://localhost:5557
    Collects workloads from ventilator via that socket
    Connects PUSH socket to tcp://localhost:5558
    Sends results to sink via that socket
    """
    # Socket on which to receive messages
    rx = context.socket(zmq.PULL)
    rx.connect("tcp://localhost:5557")

    # Socket on which to send messages
    tx = context.socket(zmq.PUSH)
    tx.connect("tcp://localhost:5558")

    for request in range(1,10):
        s = rx.recv()
        print('Switched to worker for %s' % request)
        tx.send("Worker")
        gevent.sleep(0)

    print 'Worker done... Shutting it down...'

def sink():
    """ Task sink
    Binds PULL socket to tcp://localhost:5558
    Collects results from workers via that socket
    """
    rx = context.socket(zmq.PULL)
    rx.bind("tcp://*:5558")

    # wait for start of batch message from ventilator
    s = rx.recv()

    for request in range(1,30):
        s = rx.recv()
        print('Switched to sink for %s' % request)
        gevent.sleep(0)

    # it never finishes... only gets to 27...
    # so either i have some loop counts off a bit or it seems
    # like the workers don't process enough messages? something
    # is getting lost or dropped??  interesting... i gotta read more!
    print 'Sink done... Shutting it down...'

print 'Spawning ventilator'
ventilator = gevent.spawn(ventilator)
print 'Spawning worker'
worker1    = gevent.spawn(worker)
print 'Spawning worker'
worker2    = gevent.spawn(worker)
print 'Spawning worker'
worker3    = gevent.spawn(worker)
print 'Spawning sink'
sink       = gevent.spawn(sink)
print 'Spawning running'
gevent.joinall([ventilator, worker1, worker2, worker3, sink])
