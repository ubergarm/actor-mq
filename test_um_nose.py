#!/usr/bin/env python

import timeit
import time
from functools import wraps
import ftpFiles
import gevent

def timeThis(func):
    """uses functools.wraps so nosetest will still sniff out test_ funcs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print timeit.timeit(func(*args, **kwargs), number=1)
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print (t2 - t1)
        # return func(*args, **kwargs)
        return result
    return wrapper

class TestUM:
    """run this test class with nosetest -s -v test_um_nose.py"""
    def __init__(self):
        self.servers = ['ftp.debian.org',
                        'debian.cs.binghamton.edu',
                        'debian.ec.as6453.net',
                        'debian.gtisc.gatech.edu',
                        'debian.uchicago.edu',
                        'lug.mtu.edu',
                        'mirror.cc.columbia.edu',
                        'mirror.fdcservers.net',
                        'ftp-nyc.osuosl.org']
        self.files = ['/debian/README']

    @timeThis
    def test_simple(self):
        results = dict()
        for server in self.servers:
            try:
                results[server] = ftpFiles.get(server,self.files)
            except:
                pass
        print results

    @timeThis
    def test_gevent(self):
        import gevent.monkey
        gevent.monkey.patch_socket()
        threads = []
        for server in self.servers:
            threads.append(gevent.spawn(ftpFiles.get,server,self.files))
        gevent.joinall(threads)

    @timeThis
    def test_actor(self):
        print 'TBD'

if __name__ == '__main__':
    run = TestUM()
    # print timeit.timeit(run.test_simple, number=1)
    run.test_simple()
    # print timeit.timeit(run.test_gevent, number=1)
    run.test_gevent()
    # print timeit.timeit(run.test_actor, number=1)
